#!/usr/bin/env python3
"""
交互式 Qdrant RAG 问答系统
索引知识库后提供持续的问答服务
"""

import os
import asyncio
import json
import re
from pathlib import Path
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import httpx
from datetime import datetime

# 避免代理问题
os.environ['NO_PROXY'] = 'localhost,127.0.0.1,::1'
os.environ['no_proxy'] = 'localhost,127.0.0.1,::1'

class InteractiveRAG:
    """交互式 RAG 系统"""
    
    def __init__(
        self,
        knowledge_base_path: str,
        collection_name: str = "knowledge_base",
        ollama_host: str = "10.100.1.115:11434",
        ollama_model: str = "gpt-oss:20b"
    ):
        self.knowledge_base_path = Path(knowledge_base_path)
        self.collection_name = collection_name
        self.ollama_host = ollama_host
        self.ollama_model = ollama_model
        self.ollama_url = f"http://{ollama_host}/api/generate"
        
        # 初始化 Qdrant
        self.client = QdrantClient(
            host="localhost", 
            port=6333,
            timeout=60,
            prefer_grpc=False
        )
        
        # 词汇表和向量化
        self.vocabulary = {}
        self.vocab_size = 1000
        
        # 工作目录
        self.working_dir = Path("./rag_storage")
        self.working_dir.mkdir(exist_ok=True)
        
        print("🚀 交互式 RAG 系统初始化完成")
    
    def setup_collection(self):
        """设置 Qdrant 集合"""
        try:
            collections = self.client.get_collections()
            collection_exists = any(c.name == self.collection_name for c in collections.collections)
            
            if collection_exists:
                info = self.client.get_collection(self.collection_name)
                print(f"✅ 使用现有集合 '{self.collection_name}' ({info.points_count} 个文档)")
                return True
            
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.vocab_size, distance=Distance.COSINE)
            )
            print(f"✅ 创建新集合 '{self.collection_name}'")
            return True
            
        except Exception as e:
            print(f"❌ 集合设置失败: {e}")
            return False
    
    def get_supported_files(self) -> List[Path]:
        """获取支持的文件"""
        files = []
        for file_path in self.knowledge_base_path.rglob("*.md"):
            if (file_path.is_file() and 
                not file_path.name.startswith('.') and
                file_path.stat().st_size > 50):
                files.append(file_path)
        return sorted(files)[:100]  # 限制数量
    
    def build_vocabulary(self, texts: List[str]) -> Dict[str, int]:
        """构建词汇表"""
        word_freq = {}
        for text in texts:
            words = re.findall(r'\w+', text.lower())
            for word in words:
                if len(word) > 2:
                    word_freq[word] = word_freq.get(word, 0) + 1
        
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        vocabulary = {word: i for i, (word, _) in enumerate(sorted_words[:self.vocab_size])}
        return vocabulary
    
    def text_to_vector(self, text: str) -> List[float]:
        """文本向量化"""
        vector = [0.0] * len(self.vocabulary)
        words = re.findall(r'\w+', text.lower())
        
        for word in words:
            if word in self.vocabulary:
                vector[self.vocabulary[word]] += 1.0
        
        total = sum(vector)
        if total > 0:
            vector = [v / total for v in vector]
        
        while len(vector) < self.vocab_size:
            vector.append(0.0)
        
        return vector[:self.vocab_size]
    
    def chunk_text(self, text: str, chunk_size: int = 300) -> List[str]:
        """文本分块"""
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            if len(current_chunk) + len(para) > chunk_size and current_chunk:
                chunks.append(current_chunk)
                current_chunk = para
            else:
                current_chunk += "\n" + para if current_chunk else para
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return [chunk for chunk in chunks if len(chunk.strip()) > 20]
    
    async def index_documents(self):
        """索引文档"""
        print("📚 开始索引文档...")
        
        # 获取文件
        files = self.get_supported_files()
        print(f"📝 发现 {len(files)} 个文件")
        
        # 处理文档
        all_texts = []
        file_chunks = []
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                chunks = self.chunk_text(content)
                for i, chunk in enumerate(chunks):
                    all_texts.append(chunk)
                    file_chunks.append({
                        'file_path': str(file_path.relative_to(self.knowledge_base_path)),
                        'file_name': file_path.name,
                        'chunk_index': i,
                        'content': chunk
                    })
            except Exception as e:
                print(f"⚠️ 跳过文件 {file_path.name}: {e}")
        
        if not all_texts:
            print("❌ 没有找到可处理的文档")
            return False
        
        print(f"✅ 处理了 {len(all_texts)} 个文档块")
        
        # 构建词汇表
        print("🔤 构建词汇表...")
        self.vocabulary = self.build_vocabulary(all_texts)
        print(f"✅ 词汇表完成 ({len(self.vocabulary)} 个词)")
        
        # 向量化并插入
        print("🔢 生成向量并插入数据库...")
        points = []
        
        for i, (text, meta) in enumerate(zip(all_texts, file_chunks)):
            vector = self.text_to_vector(text)
            points.append(PointStruct(
                id=i,
                vector=vector,
                payload={**meta, 'indexed_at': datetime.now().isoformat()}
            ))
        
        # 批量插入
        batch_size = 20
        total_inserted = 0
        
        for i in range(0, len(points), batch_size):
            batch = points[i:i+batch_size]
            self.client.upsert(collection_name=self.collection_name, points=batch)
            total_inserted += len(batch)
            print(f"📥 已插入 {total_inserted}/{len(points)} 个文档块")
            await asyncio.sleep(0.1)
        
        # 保存词汇表
        vocab_file = self.working_dir / "vocabulary.json"
        with open(vocab_file, 'w', encoding='utf-8') as f:
            json.dump(self.vocabulary, f, ensure_ascii=False, indent=2)
        
        print(f"🎉 索引完成！共 {total_inserted} 个文档块")
        return True
    
    def load_vocabulary(self):
        """加载词汇表"""
        vocab_file = self.working_dir / "vocabulary.json"
        if vocab_file.exists():
            with open(vocab_file, 'r', encoding='utf-8') as f:
                self.vocabulary = json.load(f)
            print(f"📖 加载词汇表 ({len(self.vocabulary)} 个词)")
        else:
            print("⚠️ 未找到词汇表，需要重新索引")
    
    def search_documents(self, query: str, limit: int = 5) -> List[Dict]:
        """搜索文档"""
        try:
            query_vector = self.text_to_vector(query)
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
                "chunk_index": result.payload.get("chunk_index", 0)
            } for result in results]
            
        except Exception as e:
            print(f"❌ 搜索失败: {e}")
            return []
    
    async def query_ollama(self, prompt: str) -> str:
        """查询 Ollama"""
        payload = {
            "model": self.ollama_model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 800,
                "temperature": 0.7
            }
        }
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(self.ollama_url, json=payload)
                if response.status_code == 200:
                    return response.json().get("response", "未获取到响应")
                else:
                    return f"❌ Ollama 错误 ({response.status_code})"
        except Exception as e:
            return f"❌ 连接 Ollama 失败: {e}"
    
    async def answer_question(self, question: str) -> Dict[str, Any]:
        """回答问题"""
        print(f"\n🤔 问题: {question}")
        print("🔍 搜索相关文档...")
        
        # 搜索文档
        search_results = self.search_documents(question, limit=5)
        
        if not search_results:
            return {
                "question": question,
                "answer": "抱歉，我在知识库中没有找到相关信息。",
                "sources": [],
                "rag_context": "无相关文档"
            }
        
        # 过滤结果
        filtered_results = [r for r in search_results if r['score'] > 0.05]
        if not filtered_results:
            filtered_results = search_results[:3]
        
        print(f"📋 找到 {len(filtered_results)} 个相关文档")
        
        # 构建上下文
        context_parts = []
        sources = []
        
        for i, result in enumerate(filtered_results, 1):
            context_parts.append(f"【参考文档{i}】")
            context_parts.append(f"文件: {result['file_name']}")
            context_parts.append(f"内容: {result['content']}")
            context_parts.append("---")
            
            sources.append({
                "file": result['file_path'],
                "file_name": result['file_name'],
                "score": result['score'],
                "preview": result['content'][:80] + "..."
            })
        
        context = '\n'.join(context_parts)
        
        # RAG 提示
        rag_prompt = f"""你是一个专业的技术助手，请基于提供的知识库文档回答用户问题。

回答要求:
1. 仅基于提供的参考文档内容回答
2. 回答要准确、详细、易懂
3. 可以引用具体文档内容
4. 如果文档信息不足，请说明
5. 用中文回答

参考文档:
{context}

用户问题: {question}

请回答:"""
        
        print("🤖 AI 正在思考...")
        answer = await self.query_ollama(rag_prompt)
        
        return {
            "question": question,
            "answer": answer,
            "sources": sources,
            "rag_context": context,
            "filtered_results_count": len(filtered_results)
        }
    
    def print_rag_result(self, result: Dict[str, Any]):
        """打印 RAG 结果"""
        print("=" * 80)
        print("🎯 RAG 问答结果")
        print("=" * 80)
        
        print(f"❓ 问题: {result['question']}")
        print(f"\n🤖 回答:\n{result['answer']}")
        
        if result['sources']:
            print(f"\n📚 参考文档 ({result['filtered_results_count']} 个结果):")
            for i, source in enumerate(result['sources'], 1):
                print(f"   {i}. {source['file_name']} (相似度: {source['score']:.3f})")
                print(f"      预览: {source['preview']}")
        
        print(f"\n📝 RAG 上下文 (前200字符):")
        context_preview = result['rag_context'][:200] + "..." if len(result['rag_context']) > 200 else result['rag_context']
        print(f"   {context_preview}")
        
        print("=" * 80)
    
    async def interactive_session(self):
        """交互式问答会话"""
        print("\n🎉 欢迎使用交互式 RAG 问答系统！")
        print("💡 提示:")
        print("   - 直接输入问题进行查询")
        print("   - 输入 'quit' 或 'exit' 退出")
        print("   - 输入 'stats' 查看系统状态")
        print("   - 输入 'help' 查看帮助")
        
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
                        info = self.client.get_collection(self.collection_name)
                        print(f"📊 系统状态:")
                        print(f"   - 文档块数量: {info.points_count}")
                        print(f"   - 词汇表大小: {len(self.vocabulary)}")
                        print(f"   - 集合名称: {self.collection_name}")
                    except Exception as e:
                        print(f"❌ 获取状态失败: {e}")
                    continue
                
                if user_input.lower() == 'help':
                    print("📖 帮助信息:")
                    print("   - 这是基于你的知识库的 RAG 问答系统")
                    print("   - 系统会搜索相关文档，然后用 AI 生成回答")
                    print("   - 尝试问技术相关问题，如 'Python编程'、'Docker使用' 等")
                    print("   - 系统会显示完整的 RAG 处理过程")
                    continue
                
                # 处理问题
                result = await self.answer_question(user_input)
                self.print_rag_result(result)
                
            except KeyboardInterrupt:
                print("\n👋 程序被中断，再见！")
                break
            except Exception as e:
                print(f"❌ 处理出错: {e}")

async def main():
    print("🚀 交互式 Qdrant RAG 知识库问答系统")
    print("=" * 50)
    
    # 配置
    KNOWLEDGE_BASE_PATH = "/Users/chenzi/project/chenzi-knowledge/chenzi-knowledge-library"
    
    # 初始化系统
    rag = InteractiveRAG(KNOWLEDGE_BASE_PATH)
    
    # 设置集合
    if not rag.setup_collection():
        print("❌ 无法设置 Qdrant 集合")
        return
    
    # 检查是否需要索引
    try:
        info = rag.client.get_collection(rag.collection_name)
        if info.points_count == 0:
            print("📚 集合为空，开始索引文档...")
            success = await rag.index_documents()
            if not success:
                print("❌ 索引失败")
                return
        else:
            print(f"📖 使用现有索引 ({info.points_count} 个文档)")
            rag.load_vocabulary()
    except:
        print("📚 开始索引文档...")
        success = await rag.index_documents()
        if not success:
            print("❌ 索引失败")
            return
    
    # 开始交互式会话
    await rag.interactive_session()

if __name__ == "__main__":
    asyncio.run(main())