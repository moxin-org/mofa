#!/usr/bin/env python3
"""
RAG 系统演示版本
展示完整的 RAG 问答流程
"""

import asyncio
import os
import json
import re
from pathlib import Path
from typing import List, Dict, Any
from qdrant_client import QdrantClient
import httpx
from datetime import datetime

# 避免代理问题
os.environ['NO_PROXY'] = 'localhost,127.0.0.1,::1'
os.environ['no_proxy'] = 'localhost,127.0.0.1,::1'

class RAGDemo:
    """RAG 演示系统"""
    
    def __init__(
        self,
        collection_name: str = "knowledge_base",
        ollama_host: str = "10.100.1.115:11434",
        ollama_model: str = "gpt-oss:20b"
    ):
        self.collection_name = collection_name
        self.ollama_host = ollama_host
        self.ollama_model = ollama_model
        self.ollama_url = f"http://{ollama_host}/api/generate"
        
        # Qdrant 客户端
        self.client = QdrantClient(
            host="localhost", 
            port=6333,
            timeout=60,
            prefer_grpc=False
        )
        
        # 加载词汇表
        self.vocabulary = self.load_vocabulary()
        self.vocab_size = 1000
        
        print("🎯 RAG 演示系统初始化完成")
    
    def load_vocabulary(self) -> Dict[str, int]:
        """加载词汇表"""
        vocab_file = Path("./rag_storage/vocabulary.json")
        if vocab_file.exists():
            with open(vocab_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def text_to_vector(self, text: str) -> List[float]:
        """文本转向量"""
        if not self.vocabulary:
            return [0.0] * self.vocab_size
        
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
                "file_name": result.payload["file_name"]
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
                "num_predict": 600,
                "temperature": 0.7
            }
        }
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(self.ollama_url, json=payload)
                if response.status_code == 200:
                    return response.json().get("response", "未获取到响应")
                else:
                    return f"❌ Ollama 错误 ({response.status_code})"
        except Exception as e:
            return f"❌ 连接 Ollama 失败: {e}"
    
    async def demo_rag_process(self, question: str):
        """演示完整的 RAG 处理流程"""
        print("=" * 80)
        print("🎯 RAG 问答演示")
        print("=" * 80)
        print(f"❓ 问题: {question}")
        print()
        
        # 步骤 1: 文档搜索
        print("🔍 步骤 1: 文档向量搜索")
        print("-" * 40)
        search_results = self.search_documents(question, limit=5)
        
        if not search_results:
            print("   ❌ 未找到相关文档")
            return
        
        # 过滤结果
        filtered_results = [r for r in search_results if r['score'] > 0.05]
        if not filtered_results:
            filtered_results = search_results[:3]
        
        print(f"   ✅ 找到 {len(filtered_results)} 个相关文档:")
        for i, result in enumerate(filtered_results, 1):
            print(f"   {i}. {result['file_name']} (相似度: {result['score']:.3f})")
            print(f"      预览: {result['content'][:60]}...")
        
        # 步骤 2: 构建上下文
        print(f"\n🔧 步骤 2: 构建 RAG 上下文")
        print("-" * 40)
        
        context_parts = []
        for i, result in enumerate(filtered_results, 1):
            context_parts.append(f"【参考文档{i}】")
            context_parts.append(f"文件: {result['file_name']}")
            context_parts.append(f"内容: {result['content']}")
            context_parts.append("---")
        
        context = '\n'.join(context_parts)
        print(f"   📝 上下文长度: {len(context)} 字符")
        print(f"   📋 包含 {len(filtered_results)} 个文档片段")
        
        # 显示上下文预览
        context_preview = context[:300] + "..." if len(context) > 300 else context
        print(f"   🔍 上下文预览:\n{context_preview}")
        
        # 步骤 3: 构建提示词
        print(f"\n📝 步骤 3: 构建 AI 提示词")
        print("-" * 40)
        
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
        
        print(f"   💬 提示词长度: {len(rag_prompt)} 字符")
        print(f"   🎯 包含完整的上下文和指令")
        
        # 步骤 4: AI 生成回答
        print(f"\n🤖 步骤 4: AI 模型生成回答")
        print("-" * 40)
        
        print("   🔄 正在调用 Ollama 模型...")
        answer = await self.query_ollama(rag_prompt)
        
        print(f"   ✅ 回答生成完成")
        print(f"   📝 回答长度: {len(answer)} 字符")
        
        # 步骤 5: 展示最终结果
        print(f"\n🎉 步骤 5: 最终 RAG 结果")
        print("-" * 40)
        
        print(f"🤖 AI 回答:")
        print(f"{answer}")
        
        print(f"\n📚 参考来源:")
        for i, result in enumerate(filtered_results, 1):
            print(f"   {i}. {result['file_path']} (相似度: {result['score']:.3f})")
        
        print("=" * 80)
        print("✅ RAG 演示完成")
        print("=" * 80)
        
        return {
            "question": question,
            "answer": answer,
            "sources": filtered_results,
            "context_length": len(context),
            "prompt_length": len(rag_prompt)
        }

async def main():
    print("🚀 RAG-Anything 知识库问答系统演示")
    print("=" * 50)
    
    # 初始化系统
    rag = RAGDemo()
    
    # 检查系统状态
    try:
        info = rag.client.get_collection(rag.collection_name)
        print(f"✅ 知识库状态: {info.points_count} 个文档块")
        print(f"📖 词汇表大小: {len(rag.vocabulary)} 个词")
    except Exception as e:
        print(f"❌ 系统检查失败: {e}")
        return
    
    # 演示问题列表
    demo_questions = [
        "Python 编程有什么优势和特点？",
        "Docker 容器技术如何使用？",
        "AI Agent 的主要实现方式有哪些？",
        "如何进行数据科学项目开发？"
    ]
    
    print(f"\n🎯 开始 RAG 演示 (共 {len(demo_questions)} 个问题)")
    print()
    
    results = []
    
    for i, question in enumerate(demo_questions, 1):
        print(f"🔥 演示 {i}/{len(demo_questions)}")
        
        try:
            result = await rag.demo_rag_process(question)
            if result:
                results.append(result)
            
            # 演示间隔
            if i < len(demo_questions):
                print("\n⏱️  等待 3 秒后继续下一个演示...")
                await asyncio.sleep(3)
                
        except Exception as e:
            print(f"❌ 演示 {i} 失败: {e}")
    
    # 总结报告
    print("\n" + "=" * 80)
    print("📊 RAG 演示总结报告")
    print("=" * 80)
    
    if results:
        avg_context_len = sum(r['context_length'] for r in results) / len(results)
        avg_prompt_len = sum(r['prompt_length'] for r in results) / len(results)
        
        print(f"✅ 成功演示: {len(results)} 个问题")
        print(f"📝 平均上下文长度: {avg_context_len:.0f} 字符")
        print(f"💬 平均提示词长度: {avg_prompt_len:.0f} 字符")
        print(f"🎯 知识库覆盖: {info.points_count} 个文档块")
        
        print(f"\n📋 演示问题列表:")
        for i, result in enumerate(results, 1):
            print(f"   {i}. {result['question']}")
            print(f"      回答长度: {len(result['answer'])} 字符")
            print(f"      参考文档: {len(result['sources'])} 个")
    else:
        print("❌ 所有演示都失败了")
    
    print("\n🎉 RAG 演示完成！这就是完整的检索增强生成流程。")

if __name__ == "__main__":
    asyncio.run(main())