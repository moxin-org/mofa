#!/usr/bin/env python3
"""
LightRAG 交互式问答系统
基于 LightRAG 框架构建的高效知识检索和问答系统
支持多种查询模式：hybrid、local、global、naive
"""

import os
import asyncio
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import httpx

# 导入环境变量加载器
from dotenv import load_dotenv

# 导入 LightRAG 核心组件
from lightrag import LightRAG, QueryParam
from lightrag.utils import EmbeddingFunc
from lightrag.kg.shared_storage import initialize_pipeline_status

# 加载环境变量
load_dotenv()

# 从环境变量读取配置
OLLAMA_LLM_HOST = os.getenv('OLLAMA_LLM_HOST', '10.100.1.115:11434')
LLM_MODEL = os.getenv('LLM_MODEL', 'gpt-oss:20b')

# OpenAI Embedding 配置
LLM_API_KEY = os.getenv('LLM_API_KEY')
LLM_BASE_URL = os.getenv('LLM_BASE_URL', 'https://api.openai.com/v1')
EMBED_MODEL = os.getenv('EMBED_MODEL', 'text-embedding-3-large')

KNOWLEDGE_BASE_PATH = os.getenv('KNOWLEDGE_BASE_PATH',
                                '/Users/chenzi/project/chenzi-knowledge/chenzi-knowledge-library')
LIGHTRAG_WORKING_DIR = os.getenv('LIGHTRAG_WORKING_DIR', './lightrag_storage')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'lightrag_system.log')

# Qdrant 配置
USE_QDRANT = os.getenv('USE_QDRANT', 'false').lower() == 'true'
QDRANT_URL = os.getenv('QDRANT_URL', 'http://localhost:6333')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
QDRANT_COLLECTION_NAME = os.getenv('QDRANT_COLLECTION_NAME', 'lightrag_vectors')


async def ollama_llm_func(prompt, system_prompt=None, history_messages=None, **kwargs):
    """LightRAG 兼容的 Ollama LLM 函数"""
    try:
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        if history_messages:
            messages.extend(history_messages)

        messages.append({"role": "user", "content": prompt})

        async with httpx.AsyncClient(timeout=180.0) as client:
            response = await client.post(
                f"http://{OLLAMA_LLM_HOST}/v1",
                json={
                    "model": LLM_MODEL,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "num_predict": 2000,
                        "temperature": 0.3,
                        "top_p": 0.9,
                        "top_k": 40
                    }
                }
            )

            if response.status_code == 200:
                result = response.json()
                message_content = result.get("message", {}).get("content", "")

                if not message_content or message_content.strip() == "":
                    return "Based on the provided context, I can provide information on this topic."

                return message_content
            else:
                logging.error(f"Ollama API 错误: {response.status_code}")
                return "I apologize, but I cannot process this request at the moment due to a service error."

    except Exception as e:
        logging.error(f"LLM 请求失败: {e}")
        return "I apologize, but I'm experiencing technical difficulties and cannot provide a response right now."


async def openai_embed_func(texts, **kwargs):
    """符合 LightRAG 标准的 OpenAI 嵌入函数"""
    if isinstance(texts, str):
        texts = [texts]

    results = []
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                f"{LLM_BASE_URL}/embeddings",
                headers=headers,
                json={
                    "model": EMBED_MODEL,
                    "input": texts
                }
            )
            if response.status_code == 200:
                data = response.json()
                embeddings = data.get("data", [])
                for item in embeddings:
                    results.append(item["embedding"])

                return results
            else:
                logging.error(f"OpenAI Embedding API 错误: {response.status_code}")
                return None

        except Exception as e:
            logging.error(f"OpenAI 嵌入请求失败: {e}")
            return None


class LightRAGSystem:
    """LightRAG 系统主类"""

    def __init__(self, working_dir: str = None, knowledge_base_path: str = None):
        self.working_dir = Path(working_dir or LIGHTRAG_WORKING_DIR)
        self.knowledge_base_path = Path(
            knowledge_base_path or KNOWLEDGE_BASE_PATH) if knowledge_base_path or KNOWLEDGE_BASE_PATH else None
        self.rag = None

        # 确保工作目录存在
        self.working_dir.mkdir(exist_ok=True)

        logging.info(f"LightRAG 系统初始化: {self.working_dir}")

    def check_services(self):
        """检查服务连通性"""
        try:
            import requests

            # 检查 LLM 服务
            llm_response = requests.get(f"http://{OLLAMA_LLM_HOST}/api/tags", timeout=5)
            if llm_response.status_code != 200:
                logging.error(f"LLM 服务异常: {llm_response.status_code}")
                return False

            # 检查 OpenAI Embedding 服务
            embed_response = requests.get(
                "https://api.openai.com/v1/models",
                headers={"Authorization": f"Bearer {LLM_API_KEY}"},
                timeout=5
            )
            if embed_response.status_code != 200:
                logging.error(f"OpenAI Embedding 服务异常: {embed_response.status_code}")
                return False

            # 检查 Qdrant 服务
            if USE_QDRANT:
                qdrant_headers = {}
                if QDRANT_API_KEY:
                    qdrant_headers["api-key"] = QDRANT_API_KEY

                qdrant_response = requests.get(
                    f"{QDRANT_URL}/collections",
                    headers=qdrant_headers,
                    timeout=5
                )
                if qdrant_response.status_code != 200:
                    logging.error(f"Qdrant 服务异常: {qdrant_response.status_code}")
                    return False

            logging.info("服务检查通过")
            return True

        except Exception as e:
            logging.error(f"服务检查失败: {e}")
            return False

    async def initialize(self):
        """初始化 LightRAG 系统"""
        try:
            # 创建嵌入函数
            embedding_func = EmbeddingFunc(
                embedding_dim=3072,
                max_token_size=8191,
                func=openai_embed_func
            )

            # 根据配置决定是否使用 Qdrant
            if USE_QDRANT:
                qdrant_config = {
                    "cosine_better_than_threshold": 0.2
                }

                self.rag = LightRAG(
                    working_dir=str(self.working_dir),
                    llm_model_func=ollama_llm_func,
                    embedding_func=embedding_func,
                    vector_storage="QdrantVectorDBStorage",
                    vector_db_storage_cls_kwargs=qdrant_config,
                    enable_llm_cache=True,
                    max_parallel_insert=os.cpu_count(),
                )
            else:
                self.rag = LightRAG(
                    working_dir=str(self.working_dir),
                    llm_model_func=ollama_llm_func,
                    embedding_func=embedding_func,
                    enable_llm_cache=True
                )

            # 初始化存储和管道
            await self.rag.initialize_storages()
            await initialize_pipeline_status()

            logging.info("LightRAG 系统初始化完成")
            return True

        except Exception as e:
            logging.error(f"LightRAG 初始化失败: {e}")
            return False

    async def process_files_batch(self, files: List[Path], batch_size: int = 10) -> Dict[str, Any]:
        """批量处理文件"""
        if not files:
            return {'success': False, 'error': '没有文件需要处理'}

        total_success = 0
        total_failed = 0

        logging.info(f"开始批量处理 {len(files)} 个文件")

        for i in range(0, len(files), batch_size):
            batch_files = files[i:i + batch_size]

            # 批量读取文件内容
            documents = []
            file_paths = []

            for file_path in batch_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    if content.strip():
                        documents.append(content)
                        file_paths.append(str(file_path))
                except Exception as e:
                    logging.error(f"读取文件失败 {file_path.name}: {e}")
                    total_failed += 1

            # 批量插入RAG - 使用同步方法进行批量插入
            if documents:
                try:
                    # LightRAG 支持批量插入 - 使用同步方法避免事件循环冲突
                    self.rag.insert(documents, file_paths=file_paths)
                    total_success += len(documents)
                    logging.info(f"批次 {i // batch_size + 1} 插入成功: {len(documents)} 个文件")
                except Exception as e:
                    logging.error(f"批量插入失败: {e}")
                    total_failed += len(documents)

        logging.info(f"批量处理完成: 成功 {total_success}, 失败 {total_failed}")

        return {
            'success': True,
            'total_files': len(files),
            'success_count': total_success,
            'failed_count': total_failed
        }

    async def process_knowledge_base(self) -> Dict[str, Any]:
        """处理知识库中的所有文档"""
        if not self.knowledge_base_path or not self.knowledge_base_path.exists():
            return {'success': False, 'error': f'知识库路径不存在: {self.knowledge_base_path}'}

        try:
            # 查找所有支持的文件
            supported_extensions = ['.md', '.txt', '.rtf', '.py', '.json']
            files = []

            for ext in supported_extensions:
                files.extend(list(self.knowledge_base_path.rglob(f"*{ext}")))

            if not files:
                return {'success': False, 'error': '未找到支持的文档文件'}

            # 使用批量处理
            return await self.process_files_batch(files, batch_size=15)

        except Exception as e:
            logging.error(f"处理知识库失败: {e}")
            return {'success': False, 'error': str(e)}

    async def query(self, question: str, mode: str = "hybrid") -> Dict[str, Any]:
        """LightRAG 查询"""
        try:
            if not self.rag:
                return {
                    'question': question,
                    'answer': 'LightRAG 系统未初始化',
                    'mode': mode,
                    'status': 'error'
                }

            # 执行查询
            response = await self.rag.aquery(question, param=QueryParam(mode=mode))

            return {
                'question': question,
                'answer': response,
                'mode': mode,
                'status': 'success'
            }

        except Exception as e:
            logging.error(f"查询失败: {e}")
            return {
                'question': question,
                'answer': f'查询处理失败: {str(e)}',
                'mode': mode,
                'status': 'error'
            }

    def print_query_result(self, result: Dict[str, Any]):
        """打印查询结果"""
        print("=" * 80)
        print(f"问题: {result['question']}")
        print(f"模式: {result['mode']}")
        print(f"\n回答:\n{result['answer']}")
        print("=" * 80)

    async def interactive_session(self):
        """交互式会话"""
        print("\n🎉 LightRAG 交互式问答系统")
        print("支持模式: hybrid, local, global, naive")
        print("输入 'mode:模式 问题' 指定查询模式")
        print("输入 'quit' 退出, 'reindex' 重新索引\n")

        while True:
            try:
                user_input = input("请输入问题: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("再见！")
                    break

                if user_input.lower() == 'reindex':
                    print("重新索引中...")
                    result = await self.process_knowledge_base()
                    if result['success']:
                        print(f"重新索引完成: {result['success_count']}/{result['total_files']} 个文档")
                    else:
                        print(f"重新索引失败: {result.get('error', '未知错误')}")
                    continue

                # 解析查询模式
                mode = "hybrid"
                question = user_input

                if user_input.startswith("mode:"):
                    parts = user_input.split(" ", 1)
                    if len(parts) == 2:
                        mode_part = parts[0].replace("mode:", "")
                        if mode_part in ["hybrid", "local", "global", "naive"]:
                            mode = mode_part
                            question = parts[1]

                # 执行查询
                result = await self.query(question, mode=mode)
                self.print_query_result(result)

            except KeyboardInterrupt:
                print("\n程序被中断，再见！")
                break
            except Exception as e:
                logging.error(f"处理出错: {e}")
                print(f"处理出错: {e}")


async def main():
    """主函数"""
    # 设置日志
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper()),
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(LOG_FILE, encoding='utf-8')
        ]
    )

    print("LightRAG 知识检索问答系统")

    try:
        # 初始化系统
        rag_system = LightRAGSystem(
            working_dir=LIGHTRAG_WORKING_DIR,
            knowledge_base_path=KNOWLEDGE_BASE_PATH
        )

        # 检查服务并初始化
        if not rag_system.check_services():
            print("服务检查失败，请确保相关服务正常运行")
            return

        if not await rag_system.initialize():
            print("系统初始化失败")
            return

        # 处理知识库文档
        result = await rag_system.process_knowledge_base()
        if result['success']:
            print(f"知识库处理完成: {result['success_count']}/{result['total_files']} 个文档")
        else:
            print(f"知识库处理失败: {result.get('error', '未知错误')}")

        # 开始交互式会话
        await rag_system.interactive_session()

    except Exception as e:
        logging.error(f"系统启动失败: {e}")
        print(f"系统启动失败: {e}")
    finally:
        # 清理存储
        if rag_system and rag_system.rag:
            try:
                await rag_system.rag.finalize_storages()
                logging.info("存储已清理")
            except Exception as e:
                logging.warning(f"存储清理失败: {e}")


if __name__ == "__main__":
    asyncio.run(main())