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
import numpy as np

# 导入 LightRAG 核心组件
from lightrag import LightRAG, QueryParam
from lightrag.utils import EmbeddingFunc
from lightrag.kg.shared_storage import initialize_pipeline_status

# 导入 Qdrant 客户端
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# 避免代理问题
os.environ['NO_PROXY'] = 'localhost,127.0.0.1,::1'
os.environ['no_proxy'] = 'localhost,127.0.0.1,::1'

# 配置 - 使用你的 Ollama 服务器和 Qdrant 数据库
OLLAMA_LLM_HOST = "10.100.1.115:11434"
OLLAMA_EMBED_HOST = "10.100.1.115:11435"
LLM_MODEL = "gpt-oss:20b"
EMBED_MODEL = "dengcao/Qwen3-Embedding-8B:Q5_K_M"

# Qdrant 配置
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
QDRANT_COLLECTION_NAME = "lightrag_8192"  # 8192维向量专用集合


async def ollama_llm_func(prompt, system_prompt=None, history_messages=None, **kwargs):
    """LightRAG 兼容的 Ollama LLM 函数"""
    try:
        # 构建完整的提示
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"System: {system_prompt}\n\nUser: {prompt}"

        # 添加历史消息
        if history_messages:
            history_text = "\n".join(
                [f"{msg.get('role', 'user')}: {msg.get('content', '')}" for msg in history_messages])
            full_prompt = f"{history_text}\n\nUser: {prompt}"

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"http://{OLLAMA_LLM_HOST}/api/generate",
                json={
                    "model": LLM_MODEL,
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {
                        "num_predict": 1000,
                        "temperature": 0.7,
                        "top_p": 0.9
                    }
                }
            )
            if response.status_code == 200:
                return response.json().get("response", "No response")
            else:
                return f"Error: {response.status_code}"
    except Exception as e:
        logging.error(f"LLM 请求失败: {e}")
        return f"LLM Error: {str(e)}"


async def ollama_embed_func(texts, **kwargs):
    """修复的 Ollama 嵌入函数"""
    if isinstance(texts, str):
        texts = [texts]

    results = []

    # 使用正确的 API 端点
    async with httpx.AsyncClient(timeout=60.0) as client:
        for text in texts:
            try:
                response = await client.post(
                    f"http://{OLLAMA_EMBED_HOST}/api/embed",  # ← 修复：使用正确的端点
                    json={
                        "model": EMBED_MODEL,
                        "input": text  # ← 修复：使用 input 而不是 prompt
                    }
                )
                if response.status_code == 200:
                    embedding = response.json().get("embeddings", [])
                    if embedding and len(embedding) > 0:
                        results.append(embedding[0])
                    else:
                        logging.error(f"❌ 空的 embedding 响应")
                        return None  # 不使用随机向量
                else:
                    logging.error(f"❌ Embedding API 错误: {response.status_code}")
                    return None

            except Exception as e:
                logging.error(f"❌ 嵌入请求失败: {e}")
                return None

    return results


class LightRAGSystem:
    """LightRAG 系统主类 - 集成 Qdrant 向量数据库"""

    def __init__(self, working_dir: str = "./lightrag_storage", knowledge_base_path: str = None):
        self.working_dir = Path(working_dir)
        self.knowledge_base_path = Path(knowledge_base_path) if knowledge_base_path else None
        self.rag = None
        self.qdrant_client = None

        # 确保工作目录存在
        self.working_dir.mkdir(exist_ok=True)

        logging.info(f"🚀 LightRAG 系统初始化")
        logging.info(f"   - 工作目录: {self.working_dir}")
        logging.info(f"   - 知识库路径: {self.knowledge_base_path}")
        logging.info(f"   - LLM: {LLM_MODEL} @ {OLLAMA_LLM_HOST}")
        logging.info(f"   - 嵌入: {EMBED_MODEL} @ {OLLAMA_EMBED_HOST}")
        logging.info(f"   - Qdrant: {QDRANT_HOST}:{QDRANT_PORT}/{QDRANT_COLLECTION_NAME}")
    
    def setup_qdrant(self) -> bool:
        """设置 Qdrant 向量数据库"""
        try:
            # 创建 Qdrant 客户端
            self.qdrant_client = QdrantClient(
                host=QDRANT_HOST,
                port=QDRANT_PORT,
                timeout=60
            )
            
            # 首先测试连接
            logging.info("🔌 测试 Qdrant 连接...")
            collections = self.qdrant_client.get_collections()
            logging.info(f"📦 当前 Qdrant 中有 {len(collections.collections)} 个集合")
            
            # 检查集合是否存在
            collection_exists = any(c.name == QDRANT_COLLECTION_NAME for c in collections.collections)
            
            if collection_exists:
                info = self.qdrant_client.get_collection(QDRANT_COLLECTION_NAME)
                logging.info(f"✅ 使用现有 Qdrant 集合: {QDRANT_COLLECTION_NAME} ({info.points_count} 个向量)")
            else:
                # 创建新集合
                logging.info(f"📝 创建新集合: {QDRANT_COLLECTION_NAME}")
                try:
                    self.qdrant_client.create_collection(
                        collection_name=QDRANT_COLLECTION_NAME,
                        vectors_config=VectorParams(
                            size=8192,  # Qwen3-Embedding-8B 的向量维度
                            distance=Distance.COSINE
                        )
                    )
                    logging.info(f"✅ 创建新 Qdrant 集合: {QDRANT_COLLECTION_NAME}")
                except Exception as create_error:
                    logging.error(f"❌ 创建集合失败: {create_error}")
                    # 如果创建失败，直接返回错误而不修改全局变量
                    return False
            
            return True
            
        except Exception as e:
            logging.error(f"❌ Qdrant 设置失败: {e}")
            return False

    async def initialize(self):
        """初始化 LightRAG 系统"""
        try:
            # 尝试设置 Qdrant 向量数据库
            qdrant_ok = self.setup_qdrant()
            if not qdrant_ok:
                logging.warning("⚠️ Qdrant 设置失败，系统将仅使用 LightRAG 内置存储")
                self.qdrant_client = None
            
            # 创建嵌入函数
            embedding_func = EmbeddingFunc(
                embedding_dim=8192,  # Qwen3-Embedding-8B 的正确维度
                max_token_size=8192,
                func=ollama_embed_func
            )

            # 创建 LightRAG 实例
            # 注意：LightRAG 可能不直接支持外部 Qdrant，我们先用默认存储
            self.rag = LightRAG(
                working_dir=str(self.working_dir),
                llm_model_func=ollama_llm_func,
                embedding_func=embedding_func,
                enable_llm_cache=True
            )
            
            # 初始化存储
            await self.rag.initialize_storages()
            await initialize_pipeline_status()

            logging.info("✅ LightRAG 系统初始化完成")
            return True

        except Exception as e:
            logging.error(f"❌ LightRAG 初始化失败: {e}")
            return False

    def check_services(self):
        """检查服务连通性"""
        print("🔍 检查服务状态...")

        try:
            import requests

            # 检查 LLM 服务
            llm_response = requests.get(f"http://{OLLAMA_LLM_HOST}/api/tags", timeout=5)
            if llm_response.status_code == 200:
                print("✅ LLM 服务正常")
            else:
                print(f"❌ LLM 服务异常: {llm_response.status_code}")
                return False

            # 检查 Embedding 服务
            embed_response = requests.get(f"http://{OLLAMA_EMBED_HOST}/api/tags", timeout=5)
            if embed_response.status_code == 200:
                print("✅ Embedding 服务正常")
            else:
                print(f"❌ Embedding 服务异常: {embed_response.status_code}")
                return False
            
            # 检查 Qdrant 服务
            qdrant_response = requests.get(f"http://{QDRANT_HOST}:{QDRANT_PORT}/collections", timeout=5)
            if qdrant_response.status_code == 200:
                print("✅ Qdrant 向量数据库正常")
            else:
                print(f"❌ Qdrant 服务异常: {qdrant_response.status_code}")
                return False

            return True

        except Exception as e:
            print(f"❌ 服务检查失败: {e}")
            return False

    async def insert_document(self, file_path: Path) -> bool:
        """插入单个文档 - 同时存储到 LightRAG 和 Qdrant"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if content.strip():
                # 使用 LightRAG 处理文档（包含知识图谱构建）
                await self.rag.ainsert(content)
                
                # 额外存储到 Qdrant（用于快速向量检索）
                await self._store_to_qdrant(content, str(file_path))
                
                logging.info(f"✅ 已插入文档: {file_path.name} (LightRAG + Qdrant)")
                return True
            else:
                logging.warning(f"⚠️ 文档为空，跳过: {file_path.name}")
                return False

        except Exception as e:
            logging.error(f"❌ 插入文档失败 {file_path.name}: {e}")
            return False
    
    async def _store_to_qdrant(self, content: str, file_path: str):
        """将文档向量存储到 Qdrant"""
        try:
            if not self.qdrant_client:
                return
            
            # 生成内容的嵌入向量
            embeddings = await ollama_embed_func([content])
            if not embeddings or not embeddings[0]:
                logging.warning(f"⚠️ 无法生成嵌入向量: {file_path}")
                return
            
            # 创建点ID（基于文件路径的哈希）
            import hashlib
            point_id = int(hashlib.md5(file_path.encode()).hexdigest()[:8], 16)
            
            # 插入到 Qdrant
            point = PointStruct(
                id=point_id,
                vector=embeddings[0],
                payload={
                    "content": content[:1000],  # 存储前1000字符作为预览
                    "file_path": file_path,
                    "timestamp": str(datetime.now())
                }
            )
            
            self.qdrant_client.upsert(
                collection_name=QDRANT_COLLECTION_NAME,
                points=[point]
            )
            
            logging.debug(f"✅ 向量已存储到 Qdrant: {file_path}")
            
        except Exception as e:
            logging.warning(f"⚠️ Qdrant 存储失败: {e}")
            # 不影响主流程，继续执行

    async def process_knowledge_base(self) -> Dict[str, Any]:
        """处理知识库中的所有文档"""
        if not self.knowledge_base_path or not self.knowledge_base_path.exists():
            return {'success': False, 'error': '知识库路径不存在'}

        try:
            # 查找所有支持的文件（专注于简单文本文件，避免复杂解析）
            supported_extensions = ['.md', '.txt', '.rtf']
            files = []

            for ext in supported_extensions:
                files.extend(list(self.knowledge_base_path.rglob(f"*{ext}")))

            if not files:
                return {'success': False, 'error': '未找到支持的文档文件'}

            logging.info(f"📚 开始处理 {len(files)} 个文档...")

            success_count = 0
            for i, file_path in enumerate(files, 1):
                print(f"📄 处理文档 {i}/{len(files)}: {file_path.name}")
                if await self.insert_document(file_path):
                    success_count += 1

                # 每处理5个文档显示进度
                if i % 5 == 0:
                    print(f"📊 进度: {i}/{len(files)} ({success_count} 个成功)")

            logging.info(f"🎉 文档处理完成: {success_count}/{len(files)} 个成功")

            return {
                'success': True,
                'total_files': len(files),
                'success_count': success_count,
                'failed_count': len(files) - success_count
            }

        except Exception as e:
            logging.error(f"❌ 处理知识库失败: {e}")
            return {'success': False, 'error': str(e)}

    async def query(self, question: str, mode: str = "hybrid") -> Dict[str, Any]:
        """增强查询 - 结合 LightRAG 和 Qdrant"""
        try:
            if not self.rag:
                return {
                    'question': question,
                    'answer': '❌ LightRAG 系统未初始化',
                    'mode': mode,
                    'status': 'error'
                }

            logging.info(f"🔍 查询: {question} (模式: {mode})")

            # 使用 LightRAG 查询（主要方法）
            try:
                # 尝试使用 mode 参数
                response = await self.rag.aquery(question, param=QueryParam())
            except TypeError:
                # 如果不支持 QueryParam，使用简单查询
                logging.warning(f"⚠️ 不支持查询模式 {mode}，使用默认查询")
                response = await self.rag.aquery(question)
            
            # 可选：使用 Qdrant 进行额外的向量检索验证
            qdrant_results = await self._query_qdrant(question, limit=3)

            return {
                'question': question,
                'answer': response,
                'mode': mode,
                'qdrant_results_count': len(qdrant_results) if qdrant_results else 0,
                'status': 'success'
            }

        except Exception as e:
            logging.error(f"❌ 查询失败: {e}")
            return {
                'question': question,
                'answer': f'查询处理失败: {str(e)}',
                'mode': mode,
                'status': 'error'
            }
    
    async def _query_qdrant(self, question: str, limit: int = 5) -> List[Dict[str, Any]]:
        """使用 Qdrant 进行向量检索"""
        try:
            if not self.qdrant_client:
                return []
            
            # 生成问题的嵌入向量
            embeddings = await ollama_embed_func([question])
            if not embeddings or not embeddings[0]:
                return []
            
            # 在 Qdrant 中搜索相似向量
            search_result = self.qdrant_client.search(
                collection_name=QDRANT_COLLECTION_NAME,
                query_vector=embeddings[0],
                limit=limit,
                with_payload=True,
                score_threshold=0.3  # 相似度阈值
            )
            
            results = []
            for result in search_result:
                results.append({
                    'score': result.score,
                    'content': result.payload['content'],
                    'file_path': result.payload['file_path'],
                    'timestamp': result.payload.get('timestamp', '')
                })
            
            logging.debug(f"🔍 Qdrant 找到 {len(results)} 个相似结果")
            return results
            
        except Exception as e:
            logging.warning(f"⚠️ Qdrant 查询失败: {e}")
            return []

    def print_query_result(self, result: Dict[str, Any]):
        """打印查询结果"""
        print("=" * 80)
        print("🎯 LightRAG + Qdrant 查询结果")
        print("=" * 80)

        print(f"❓ 问题: {result['question']}")
        print(f"🔍 查询模式: {result['mode']}")
        print(f"📊 状态: {result['status']}")
        
        if result.get('qdrant_results_count', 0) > 0:
            print(f"🗄️ Qdrant 辅助检索: {result['qdrant_results_count']} 个相关结果")
        
        print(f"\n🤖 回答:\n{result['answer']}")
        print("=" * 80)

    async def interactive_session(self):
        """交互式会话"""
        print("\n🎉 欢迎使用 LightRAG 交互式问答系统！")
        print("💡 提示:")
        print("   - 直接输入问题进行查询")
        print("   - 输入 'mode:模式 问题' 指定查询模式")
        print("   - 支持模式: hybrid (混合), local (局部), global (全局), naive (朴素)")
        print("   - 输入 'quit' 或 'exit' 退出")
        print("   - 输入 'stats' 查看系统状态")
        print("   - 输入 'help' 查看帮助")
        print("   - 输入 'reindex' 重新索引文档")

        while True:
            try:
                user_input = input("\n🗣️  请输入问题: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 再见！感谢使用 LightRAG 问答系统！")
                    break

                if user_input.lower() == 'stats':
                    print("📊 LightRAG + Qdrant 系统状态:")
                    print(f"   - 工作目录: {self.working_dir}")
                    print(f"   - 知识库路径: {self.knowledge_base_path}")
                    print(f"   - LLM 模型: {LLM_MODEL}")
                    print(f"   - 嵌入模型: {EMBED_MODEL}")
                    print(f"   - Qdrant 数据库: {QDRANT_HOST}:{QDRANT_PORT}/{QDRANT_COLLECTION_NAME}")
                    print(f"   - 支持查询模式: hybrid, local, global, naive")
                    
                    # 显示 Qdrant 集合信息
                    if self.qdrant_client:
                        try:
                            info = self.qdrant_client.get_collection(QDRANT_COLLECTION_NAME)
                            print(f"   - Qdrant 向量数: {info.points_count}")
                        except:
                            print(f"   - Qdrant 状态: 连接异常")
                    continue

                if user_input.lower() == 'help':
                    print("📖 LightRAG 系统帮助:")
                    print("   - 🎯 基于图增强的高效 RAG 系统")
                    print("   - 📄 支持文档: MD, TXT, RTF")
                    print("   - 🔍 查询模式:")
                    print("     • hybrid: 混合模式，结合向量和图检索 (推荐)")
                    print("     • local: 局部搜索，基于实体关系")
                    print("     • global: 全局搜索，基于社区总结")
                    print("     • naive: 朴素搜索，纯向量检索")
                    print("   - 💡 示例查询:")
                    print("     • 什么是机器学习?")
                    print("     • mode:local 深度学习的核心概念")
                    print("     • mode:global 总结所有文档的主要观点")
                    continue

                if user_input.lower() == 'reindex':
                    print("🔄 开始重新索引文档...")
                    result = await self.process_knowledge_base()
                    if result['success']:
                        print(f"✅ 重新索引完成: {result['success_count']}/{result['total_files']} 个文档")
                    else:
                        print(f"❌ 重新索引失败: {result.get('error', '未知错误')}")
                    continue

                # 解析查询模式
                mode = "hybrid"  # 默认模式
                question = user_input

                if user_input.startswith("mode:"):
                    parts = user_input.split(" ", 1)
                    if len(parts) == 2:
                        mode_part = parts[0].replace("mode:", "")
                        if mode_part in ["hybrid", "local", "global", "naive"]:
                            mode = mode_part
                            question = parts[1]
                        else:
                            print(f"⚠️ 未知查询模式: {mode_part}，使用默认模式 hybrid")
                            question = user_input

                # 执行查询
                result = await self.query(question, mode=mode)
                self.print_query_result(result)

            except KeyboardInterrupt:
                print("\n👋 程序被中断，再见！")
                break
            except Exception as e:
                logging.error(f"❌ 处理出错: {e}")
                print(f"❌ 处理出错: {e}")


async def main():
    """主函数"""
    # 设置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('lightrag_system.log', encoding='utf-8')
        ]
    )

    print("🚀 LightRAG 高效知识检索问答系统")
    print("基于图增强的先进 RAG 技术")
    print("=" * 60)

    # 配置
    KNOWLEDGE_BASE_PATH = "/Users/chenzi/chenzi/project/github/chenzi-knowledge-library"

    try:
        # 初始化 LightRAG 系统
        rag_system = LightRAGSystem(
            working_dir="./lightrag_storage",
            knowledge_base_path=KNOWLEDGE_BASE_PATH
        )

        # 检查服务连通性
        if not rag_system.check_services():
            print("❌ 请确保 Ollama 服务正常运行")
            return

        # 初始化系统
        if not await rag_system.initialize():
            logging.error("❌ 系统初始化失败")
            return

        # 处理知识库文档
        logging.info("📚 开始处理知识库文档...")
        result = await rag_system.process_knowledge_base()
        if result['success']:
            logging.info(f"✅ 知识库处理完成: {result['success_count']}/{result['total_files']} 个文档")
        else:
            logging.warning(f"⚠️ 知识库处理失败: {result.get('error', '未知错误')}")

        # 开始交互式会话
        await rag_system.interactive_session()

    except Exception as e:
        logging.error(f"❌ 系统启动失败: {e}")
        print(f"❌ 系统启动失败: {e}")


if __name__ == "__main__":
    asyncio.run(main())
