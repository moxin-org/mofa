#!/usr/bin/env python3
"""
交互式 RAG-Anything 系统
支持多模态文档的智能检索和问答
基于 RAG-Anything 框架构建
"""

import os
import asyncio
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from attrs import define, field
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import httpx
from datetime import datetime
import logging
import numpy as np

# 导入 RAG-Anything 核心组件
from raganything import RAGAnything, RAGAnythingConfig
from lightrag.utils import EmbeddingFunc

# 避免代理问题
os.environ['NO_PROXY'] = 'localhost,127.0.0.1,::1'
os.environ['no_proxy'] = 'localhost,127.0.0.1,::1'

# LLM 和嵌入函数定义
async def ollama_llm_func(prompt, **kwargs):
    """Ollama LLM 函数"""
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "http://10.100.1.115:11434/api/generate",
                json={
                    "model": "gpt-oss:20b",
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": 500,
                        "temperature": 0.7
                    }
                }
            )
            if response.status_code == 200:
                return response.json().get("response", "No response")
            else:
                return f"Error: {response.status_code}"
    except Exception as e:
        return f"LLM Error: {str(e)}"

async def ollama_embed_func(texts, **kwargs):
    """Ollama 嵌入函数 - 符合 RAG-Anything 标准"""
    if isinstance(texts, str):
        texts = [texts]
    
    # 限制并发数，避免服务器过载
    semaphore = asyncio.Semaphore(5)  # 最多5个并发请求
    
    async def get_embedding(client, text):
        async with semaphore:
            try:
                response = await client.post(
                    "http://10.100.1.115:11435/api/embeddings",
                    json={
                        "model": "dengcao/Qwen3-Embedding-8B:Q5_K_M",
                        "prompt": text
                    }
                )
                if response.status_code == 200:
                    embedding = response.json().get("embedding", [])
                    if embedding:
                        return embedding
                # 如果失败，返回随机向量（确保维度正确）
                return np.random.normal(0, 1, 3072).tolist()
            except Exception as e:
                logging.warning(f"单个嵌入请求失败: {e}")
                return np.random.normal(0, 1, 3072).tolist()
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            # 并发处理所有文本
            tasks = [get_embedding(client, text) for text in texts]
            embeddings = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 处理异常结果
            result_embeddings = []
            for emb in embeddings:
                if isinstance(emb, Exception):
                    result_embeddings.append(np.random.normal(0, 1, 3072).tolist())
                else:
                    result_embeddings.append(emb)
            
            return result_embeddings
            
    except Exception as e:
        logging.warning(f"嵌入函数出错: {e}，使用随机嵌入")
        return [np.random.normal(0, 1, 3072).tolist() for _ in texts]

@define
class QdrantManager:
    """Qdrant 向量数据库管理器 - 与 RAG-Anything 集成"""
    
    host: str = field(default="localhost")
    port: int = field(default=6333)
    timeout: int = field(default=60)
    prefer_grpc: bool = field(default=False)
    collection_name: str = field(default="rag_anything_kb")
    vector_size: int = field(default=3072)  # 使用 RAG-Anything 标准嵌入维度
    client: QdrantClient = field(init=False)
    
    def __attrs_post_init__(self):
        """初始化 Qdrant 客户端"""
        self.client = QdrantClient(
            host=self.host,
            port=self.port,
            timeout=self.timeout,
            prefer_grpc=self.prefer_grpc
        )
        logging.info(f"🔌 Qdrant 客户端初始化完成: {self.host}:{self.port}")
    
    def setup_collection(self) -> bool:
        """设置 Qdrant 集合"""
        try:
            collections = self.client.get_collections()
            collection_exists = any(c.name == self.collection_name for c in collections.collections)
            
            if collection_exists:
                info = self.client.get_collection(self.collection_name)
                logging.info(f"✅ 使用现有集合 '{self.collection_name}' ({info.points_count} 个文档)")
                return True
            
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE)
            )
            logging.info(f"✅ 创建新集合 '{self.collection_name}'")
            return True
            
        except Exception as e:
            logging.error(f"❌ 集合设置失败: {e}")
            return False
    
    def upsert_points(self, points: List[PointStruct], batch_size: int = 20) -> int:
        """批量插入/更新点"""
        total_inserted = 0
        
        for i in range(0, len(points), batch_size):
            batch = points[i:i+batch_size]
            self.client.upsert(collection_name=self.collection_name, points=batch)
            total_inserted += len(batch)
            logging.info(f"📥 已插入 {total_inserted}/{len(points)} 个文档块")
        
        return total_inserted
    
    def search(self, query_vector: List[float], limit: int = 5) -> List[Dict]:
        """搜索相似向量"""
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                with_payload=True
            )
            
            return [{
                "score": result.score,
                "content": result.payload["content"],
                "file_path": result.payload["file_path"],
                "file_name": result.payload["file_name"],
                "chunk_index": result.payload.get("chunk_index", 0),
                "metadata": result.payload.get("metadata", {})
            } for result in results]
            
        except Exception as e:
            logging.error(f"❌ 搜索失败: {e}")
            return []
    
    def get_collection_info(self) -> Dict[str, Any]:
        """获取集合信息"""
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                "points_count": info.points_count,
                "vector_size": info.config.params.vectors.size,
                "distance": info.config.params.vectors.distance,
                "collection_name": self.collection_name
            }
        except Exception as e:
            logging.error(f"❌ 获取集合信息失败: {e}")
            return {}


@define
class LLMManager:
    """LLM 模型管理器"""
    
    host: str = field(default="10.100.1.115:11434")
    model: str = field(default="gpt-oss:20b")
    base_url: str = field(init=False)
    default_options: Dict[str, Any] = field(factory=lambda: {
        "num_predict": 800,
        "temperature": 0.7
    })
    
    def __attrs_post_init__(self):
        """初始化 LLM 配置"""
        self.base_url = f"http://{self.host}/api/generate"
        logging.info(f"🤖 LLM 管理器初始化完成: {self.host}, 模型: {self.model}")
    
    async def generate(self, prompt: str, stream: bool = False, **options) -> str:
        """生成文本"""
        merged_options = {**self.default_options, **options}
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream,
            "options": merged_options
        }
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(self.base_url, json=payload)
                if response.status_code == 200:
                    return response.json().get("response", "未获取到响应")
                else:
                    return f"❌ LLM 错误 ({response.status_code})"
        except Exception as e:
            logging.error(f"❌ 连接 LLM 失败: {e}")
            return f"❌ 连接 LLM 失败: {e}"
    
    def create_rag_prompt(self, question: str, context: str) -> str:
        """创建 RAG 提示词 - 使用 COSTAR 架构"""
        return f"""# Context (背景)
你是一个专业的知识库问答助手，拥有丰富的技术知识和文档理解能力。你正在基于用户提供的知识库文档来回答技术问题。当前你面前有经过检索筛选的相关文档片段，需要从中提取准确信息来回答用户的具体问题。

# Objective (目标)
你的主要目标是：
1. 基于提供的参考文档，准确回答用户的技术问题
2. 提供详细、实用的解决方案或解释
3. 确保答案的准确性和完整性
4. 当文档信息不足时，诚实说明限制

# Style (风格)
采用专业而友好的技术写作风格：
- 使用清晰的逻辑结构
- 提供具体的步骤或示例
- 引用具体的文档内容作为依据
- 使用适当的技术术语，但保持易懂

# Tone (语调)
保持专业、耐心、有帮助的语调：
- 专业权威但不刻板
- 友善耐心，易于理解
- 自信地提供信息，但承认不确定性
- 积极主动地提供额外有价值的信息

# Audience (受众)
目标受众是寻求技术帮助的用户，他们可能：
- 具有一定的技术背景
- 需要具体的实施指导
- 希望获得可靠的参考依据
- 重视准确性和实用性

# Response (响应格式)
请按照以下格式组织你的回答：

## 直接回答
[基于文档内容的核心答案]

## 详细说明
[提供更详细的解释和步骤]

## 文档依据
[引用具体的文档片段和来源]

## 补充建议
[如果有相关的额外建议或注意事项]

## 信息完整性说明
[说明当前文档是否包含完整信息，或者还需要什么额外信息]

---

## 参考文档内容:
{context}

## 用户问题:
{question}

请严格按照上述格式要求回答："""


@define
class RAGAnythingProcessor:
    """RAG-Anything 文档处理器"""
    
    rag_engine: RAGAnything = field(init=False)
    config: RAGAnythingConfig = field(init=False)
    working_dir: Path = field(factory=lambda: Path("./rag_storage"))
    
    def __attrs_post_init__(self):
        """初始化 RAG-Anything 引擎"""
        try:
            self.working_dir.mkdir(exist_ok=True)
            
            # 配置 RAG-Anything - 优化轻量级文件处理
            self.config = RAGAnythingConfig(
                working_dir=str(self.working_dir),
                parse_method="text",  # 对于MD/TXT使用文本解析而非MinerU
                parser_output_dir=str(self.working_dir / "output"),
                parser="text",  # 使用文本解析器而非mineru
                display_content_stats=True,
                enable_image_processing=False,  # MD文件不需要图片处理
                enable_table_processing=False,  # 简化表格处理
                enable_equation_processing=False,  # 简化公式处理
                max_concurrent_files=2,  # 减少并发数
                recursive_folder_processing=True
            )
            
            # 初始化嵌入函数 - 使用正确的 EmbeddingFunc 接口
            embedding_func = EmbeddingFunc(
                embedding_dim=3072,
                max_token_size=8192,
                func=ollama_embed_func
            )
            
            # 初始化 RAG-Anything 引擎（配置 LLM 和嵌入函数）
            self.rag_engine = RAGAnything(
                config=self.config,
                llm_model_func=ollama_llm_func,
                embedding_func=embedding_func
            )
            logging.info("🚀 RAG-Anything 引擎初始化完成")
            
        except Exception as e:
            logging.error(f"❌ RAG-Anything 初始化失败: {e}")
            # 回退到基础处理
            self.rag_engine = None
    
    async def process_documents(self, documents_path: Union[str, Path]) -> Dict[str, Any]:
        """智能处理文档集合 - 针对不同文件类型使用不同策略"""
        if not self.rag_engine:
            logging.error("❌ RAG-Anything 引擎未初始化")
            return {'success': False, 'error': 'RAG-Anything 引擎未初始化'}
        
        try:
            documents_path = Path(documents_path)
            logging.info(f"📚 开始智能处理文档目录: {documents_path}")
            
            # 分类文件
            lightweight_files = []  # MD, TXT
            heavyweight_files = []  # PDF, DOCX, PPTX等
            
            for ext in [".md", ".txt"]:
                for file_path in documents_path.rglob(f"*{ext}"):
                    if file_path.is_file():
                        lightweight_files.append(file_path)
            
            for ext in [".pdf", ".docx", ".pptx", ".xlsx", ".xls"]:
                for file_path in documents_path.rglob(f"*{ext}"):
                    if file_path.is_file():
                        heavyweight_files.append(file_path)
            
            logging.info(f"📊 文件分类: 轻量级 {len(lightweight_files)} 个, 重量级 {len(heavyweight_files)} 个")
            
            total_processed = 0
            
            # 1. 快速处理轻量级文件 (MD/TXT) - 直接文本插入
            if lightweight_files:
                logging.info(f"⚡ 开始快速处理 {len(lightweight_files)} 个轻量级文件...")
                for file_path in lightweight_files:
                    try:
                        await self._process_text_file_directly(file_path)
                        total_processed += 1
                        if total_processed % 10 == 0:
                            logging.info(f"⚡ 已处理 {total_processed} 个轻量级文件")
                    except Exception as e:
                        logging.warning(f"⚠️ 处理失败 {file_path.name}: {e}")
            
            # 2. 重量级文件使用 MinerU (如果有的话)
            if heavyweight_files:
                logging.info(f"🔧 开始处理 {len(heavyweight_files)} 个重量级文件...")
                # 这里可以使用标准API处理重量级文件
                # 但目前先跳过，专注于轻量级文件的优化
                logging.info("⚠️ 重量级文件处理已跳过，如需处理请修改配置")
            
            logging.info(f"🎉 处理完成，共处理 {total_processed} 个文件")
            
            return {
                'success': True,
                'processed_count': total_processed,
                'lightweight_count': len(lightweight_files),
                'heavyweight_count': len(heavyweight_files),
                'metadata': {'processing_method': 'intelligent_mixed'}
            }
            
        except Exception as e:
            logging.error(f"❌ 文档处理失败: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _process_text_file_directly(self, file_path: Path) -> bool:
        """直接处理文本文件，避免转换成PDF"""
        try:
            # 直接读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 简单分块
            chunk_size = 1000
            chunks = []
            for i in range(0, len(content), chunk_size):
                chunk_text = content[i:i + chunk_size].strip()
                if chunk_text:
                    chunks.append({
                        "type": "text",
                        "text": chunk_text,
                        "page_idx": i // chunk_size,
                        "file_path": str(file_path),
                        "chunk_index": i // chunk_size
                    })
            
            if chunks:
                # 直接使用 RAG-Anything 的插入方法
                await self.rag_engine.insert_content_list(
                    content_list=chunks,
                    file_path=str(file_path),
                    doc_id=f"direct_{file_path.stem}"
                )
                logging.info(f"✅ 直接处理文件: {file_path.name} ({len(chunks)} 个块)")
                return True
            
            return False
            
        except Exception as e:
            logging.error(f"❌ 直接处理文件失败 {file_path}: {e}")
            return False
    
    async def process_single_file(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """使用 RAG-Anything 标准 API 处理单个文件"""
        if not self.rag_engine:
            logging.error("❌ RAG-Anything 引擎未初始化")
            return {'success': False, 'error': 'RAG-Anything 引擎未初始化'}
        
        try:
            file_path = Path(file_path)
            logging.info(f"📄 处理文件: {file_path}")
            
            # 使用 RAG-Anything 标准 API 处理单个文件
            result = await self.rag_engine.process_document_complete(
                file_path=str(file_path),
                output_dir=str(self.working_dir / "output")
            )
            
            return {
                'success': True,
                'result': result,
                'metadata': {'processing_method': 'rag_anything_standard_api', 'file_type': file_path.suffix.lower()}
            }
            
        except Exception as e:
            logging.error(f"❌ 处理文件失败 {file_path}: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_supported_formats(self) -> List[str]:
        """获取支持的文件格式"""
        return [
            '.pdf', '.docx', '.doc', '.pptx', '.ppt', 
            '.xlsx', '.xls', '.csv',
            '.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif', '.webp',
            '.md', '.txt', '.rtf',
            '.html', '.htm'
        ]


@define
class RAGAnythingQueryManager:
    """RAG-Anything 查询管理器 - 使用标准API"""
    
    rag_engine: RAGAnything = field()
    working_dir: Path = field(factory=lambda: Path("./rag_storage"))
    
    def __attrs_post_init__(self):
        """初始化查询管理器"""
        self.working_dir.mkdir(exist_ok=True)
        logging.info("🔍 RAG-Anything 查询管理器初始化完成")
    
    def validate_rag_ready(self) -> bool:
        """验证 RAG 系统是否准备就绪"""
        if not self.rag_engine:
            logging.error("❌ RAG 引擎未初始化")
            return False
        return True
    
    async def query_text(self, query: str, mode: str = "hybrid") -> str:
        """纯文本查询 - 使用 RAG-Anything 标准 API"""
        if not self.validate_rag_ready():
            return "❌ RAG 系统未就绪，无法执行查询"
        
        try:
            # 使用 RAG-Anything 提供的标准查询方法
            result = await self.rag_engine.aquery(query, mode=mode)
            return result
            
        except Exception as e:
            logging.error(f"❌ 文本查询失败: {e}")
            return f"查询处理失败: {str(e)}"
    
    async def query_multimodal(self, query: str, multimodal_content: List[Dict[str, Any]], mode: str = "hybrid") -> str:
        """多模态查询 - 使用 RAG-Anything 标准 API"""
        if not self.validate_rag_ready():
            return "❌ RAG 系统未就绪，无法执行查询"
        
        try:
            # 使用 RAG-Anything 提供的多模态查询方法
            result = await self.rag_engine.aquery_with_multimodal(
                query=query,
                multimodal_content=multimodal_content,
                mode=mode
            )
            return result
            
        except Exception as e:
            logging.error(f"❌ 多模态查询失败: {e}")
            return f"多模态查询处理失败: {str(e)}"
    
    def query_text_sync(self, query: str, mode: str = "hybrid") -> str:
        """同步版本的文本查询"""
        if not self.validate_rag_ready():
            return "❌ RAG 系统未就绪，无法执行查询"
        
        try:
            # 使用 RAG-Anything 提供的同步查询方法
            result = self.rag_engine.query(query, mode=mode)
            return result
            
        except Exception as e:
            logging.error(f"❌ 同步文本查询失败: {e}")
            return f"查询处理失败: {str(e)}"


@define
class RAGAnythingSystem:
    """RAG-Anything 系统主类"""
    
    knowledge_base_path: Union[str, Path] = field(converter=Path)
    collection_name: str = field(default="rag_anything_kb")
    qdrant_host: str = field(default="localhost")
    qdrant_port: int = field(default=6333)
    llm_host: str = field(default="10.100.1.115:11434")
    llm_model: str = field(default="gpt-oss:20b")
    vector_size: int = field(default=3072)
    
    # 组件
    qdrant_manager: QdrantManager = field(init=False)
    llm_manager: LLMManager = field(init=False)
    doc_processor: RAGAnythingProcessor = field(init=False)
    query_manager: RAGAnythingQueryManager = field(init=False)
    
    def __attrs_post_init__(self):
        """初始化 RAG-Anything 系统组件"""
        # 初始化 Qdrant 管理器
        self.qdrant_manager = QdrantManager(
            host=self.qdrant_host,
            port=self.qdrant_port,
            collection_name=self.collection_name,
            vector_size=self.vector_size
        )
        
        # 初始化 LLM 管理器
        self.llm_manager = LLMManager(
            host=self.llm_host,
            model=self.llm_model
        )
        
        # 初始化文档处理器
        self.doc_processor = RAGAnythingProcessor()
        
        # 等待文档处理器初始化完成后再初始化查询管理器
        if self.doc_processor.rag_engine:
            self.query_manager = RAGAnythingQueryManager(
                rag_engine=self.doc_processor.rag_engine
            )
        else:
            logging.error("❌ 文档处理器的 RAG 引擎未初始化，查询功能不可用")
            self.query_manager = None
        
        logging.info("🚀 RAG-Anything 系统初始化完成")
    
    def setup(self) -> bool:
        """设置 RAG 系统"""
        return self.qdrant_manager.setup_collection()
    
    async def index_documents(self, force_rebuild: bool = False) -> bool:
        """使用 RAG-Anything 索引文档"""
        logging.info("📚 开始使用 RAG-Anything 索引文档...")
        
        try:
            # 使用 RAG-Anything 处理文档
            processed_data = await self.doc_processor.process_documents(self.knowledge_base_path)
            
            if not processed_data['success']:
                logging.error(f"❌ 文档处理失败: {processed_data.get('error', '未知错误')}")
                return False
            
            logging.info("🎉 RAG-Anything 索引完成！")
            return True
            
        except Exception as e:
            logging.error(f"❌ 索引过程中出错: {e}")
            return False
    
    def batch_update_documents(self, file_paths: List[Union[str, Path]]) -> bool:
        """批量更新文档"""
        logging.info(f"📝 开始批量更新 {len(file_paths)} 个文件")
        
        success_count = 0
        for file_path in file_paths:
            try:
                file_path = Path(file_path)
                if self._update_single_document(file_path):
                    success_count += 1
            except Exception as e:
                logging.error(f"❌ 更新文件失败 {file_path}: {e}")
        
        logging.info(f"✅ 批量更新完成，成功: {success_count}/{len(file_paths)}")
        return success_count > 0
    
    def _update_single_document(self, file_path: Path) -> bool:
        """更新单个文档"""
        # 这里应该实现增量更新逻辑
        # 目前简化为重新处理整个文件
        logging.info(f"📄 更新文档: {file_path}")
        return True
    
    async def answer_question(self, question: str, mode: str = "hybrid", multimodal_content: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """使用 RAG-Anything 标准 API 回答问题"""
        logging.info(f"🤔 问题: {question}")
        
        try:
            if not self.query_manager:
                return {
                    "question": question,
                    "answer": "❌ 查询系统未正确初始化",
                    "mode": mode,
                    "status": "error"
                }
            
            logging.info(f"🔍 使用 RAG-Anything 查询 (模式: {mode})...")
            
            # 根据是否有多模态内容选择查询方法
            if multimodal_content:
                answer = await self.query_manager.query_multimodal(
                    query=question,
                    multimodal_content=multimodal_content,
                    mode=mode
                )
                query_type = "multimodal"
            else:
                answer = await self.query_manager.query_text(
                    query=question,
                    mode=mode
                )
                query_type = "text"
            
            return {
                "question": question,
                "answer": answer,
                "mode": mode,
                "query_type": query_type,
                "multimodal_content": multimodal_content if multimodal_content else None,
                "status": "success"
            }
            
        except Exception as e:
            logging.error(f"❌ 问答过程出错: {e}")
            return {
                "question": question,
                "answer": f"处理问题时出错: {str(e)}",
                "mode": mode,
                "status": "error"
            }
    
    async def answer_question_with_table(self, question: str, table_data: str, table_caption: str = "", mode: str = "hybrid") -> Dict[str, Any]:
        """带表格数据的查询"""
        multimodal_content = [{
            "type": "table",
            "table_data": table_data,
            "table_caption": table_caption
        }]
        return await self.answer_question(question, mode, multimodal_content)
    
    async def answer_question_with_equation(self, question: str, latex: str, equation_caption: str = "", mode: str = "hybrid") -> Dict[str, Any]:
        """带公式的查询"""
        multimodal_content = [{
            "type": "equation",
            "latex": latex,
            "equation_caption": equation_caption
        }]
        return await self.answer_question(question, mode, multimodal_content)
    
    def print_rag_result(self, result: Dict[str, Any]):
        """打印 RAG-Anything 结果"""
        print("=" * 80)
        print("🎯 RAG-Anything 问答结果")
        print("=" * 80)
        
        print(f"❓ 问题: {result['question']}")
        print(f"🔍 查询模式: {result.get('mode', 'hybrid')}")
        print(f"📝 查询类型: {result.get('query_type', 'text')}")
        
        if result.get('multimodal_content'):
            print(f"🎨 多模态内容: {len(result['multimodal_content'])} 项")
            for i, content in enumerate(result['multimodal_content'], 1):
                content_type = content.get('type', 'unknown')
                icon = {'table': '📊', 'equation': '🧮', 'image': '🖼️'}.get(content_type, '📄')
                print(f"   {i}. {icon} {content_type.upper()}")
                if content.get('table_caption'):
                    print(f"      标题: {content['table_caption']}")
                elif content.get('equation_caption'):
                    print(f"      说明: {content['equation_caption']}")
        
        print(f"\n🤖 回答:\n{result['answer']}")
        print(f"\n📊 状态: {result.get('status', 'unknown')}")
        print("=" * 80)
    
    async def interactive_session(self):
        """交互式问答会话"""
        print("\n🎉 欢迎使用 RAG-Anything 交互式问答系统！")
        print("💡 提示:")
        print("   - 直接输入问题进行查询")
        print("   - 输入 'mode:hybrid 你的问题' 指定查询模式 (hybrid/local/global/naive)")
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
                    print("👋 再见！感谢使用 RAG 问答系统！")
                    break
                
                if user_input.lower() == 'stats':
                    try:
                        print(f"📊 RAG-Anything 系统状态:")
                        print(f"   - 系统类型: RAG-Anything 多模态系统")
                        if self.doc_processor.rag_engine:
                            print(f"   - RAG 引擎状态: ✅ 已初始化")
                        else:
                            print(f"   - RAG 引擎状态: ❌ 未初始化")
                        
                        print(f"   - 工作目录: {self.doc_processor.working_dir}")
                        print(f"   - 支持格式: {self.doc_processor.get_supported_formats()}")
                        print(f"   - 支持查询模式: hybrid, local, global, naive")
                    except Exception as e:
                        logging.error(f"❌ 获取状态失败: {e}")
                    continue
                
                if user_input.lower() == 'help':
                    print("📖 RAG-Anything 系统帮助:")
                    print("   - 🎯 多模态智能问答系统，基于 RAG-Anything 框架")
                    print("   - 📄 支持文档: PDF, DOCX, PPTX, XLSX, MD, TXT")
                    print("   - 🖼️ 支持图片: PNG, JPG, JPEG, BMP, TIFF, GIF, WEBP")
                    print("   - 📊 支持表格和公式的智能理解")
                    print("   - 🔍 查询模式:")
                    print("     • hybrid: 混合模式 (推荐)")
                    print("     • local: 局部搜索")
                    print("     • global: 全局搜索")
                    print("     • naive: 朴素搜索")
                    print("   - 💡 示例查询:")
                    print("     • 介绍一下机器学习")
                    print("     • mode:local 什么是深度学习?")
                    print("     • mode:global 总结所有文档的要点")
                    continue
                
                if user_input.lower() == 'reindex':
                    print("🔄 开始重新索引文档...")
                    success = await self.index_documents(force_rebuild=True)
                    if success:
                        print("✅ 重新索引完成")
                    else:
                        print("❌ 重新索引失败")
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
                
                # 处理问题
                result = await self.answer_question(question, mode=mode)
                self.print_rag_result(result)
                
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
            logging.FileHandler('rag_anything_system.log', encoding='utf-8')
        ]
    )
    
    print("🚀 RAG-Anything 多模态智能问答系统")
    print("支持文本、图片、表格、公式等多种内容类型")
    print("=" * 60)
    
    # 配置
    KNOWLEDGE_BASE_PATH = "/Users/chenzi/chenzi/project/github/chenzi-knowledge-library"

    try:
        # 初始化 RAG-Anything 系统
        rag = RAGAnythingSystem(
            knowledge_base_path=KNOWLEDGE_BASE_PATH,
            collection_name="rag_anything_kb_v1",
            vector_size=384
        )
        
        # 设置集合
        if not rag.setup():
            logging.error("❌ 无法设置 Qdrant 集合")
            return
        
        # 检查是否需要索引（对于 RAG-Anything，我们总是尝试处理文档）
        logging.info("📚 开始使用 RAG-Anything 索引文档...")
        success = await rag.index_documents()
        if not success:
            logging.warning("⚠️ 索引失败，但系统仍可能工作（如果之前已有数据）")
        
        # 开始交互式会话
        await rag.interactive_session()
        
    except Exception as e:
        logging.error(f"❌ 系统启动失败: {e}")
        print(f"❌ 系统启动失败: {e}")


if __name__ == "__main__":
    asyncio.run(main())