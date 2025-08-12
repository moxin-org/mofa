#!/usr/bin/env python3
"""
快速测试 RAG-Anything 查询功能
"""

import asyncio
import sys
import os
sys.path.append('.')

from qdrant_rag_interactive import RAGAnythingSystem

async def test_query():
    """测试查询功能"""
    
    # 配置路径
    KNOWLEDGE_BASE_PATH = "/Users/chenzi/chenzi/project/github/chenzi-knowledge-library"
    
    print("🚀 初始化 RAG-Anything 系统...")
    
    # 初始化系统
    rag = RAGAnythingSystem(
        knowledge_base_path=KNOWLEDGE_BASE_PATH,
        collection_name="rag_anything_kb_v1",
        vector_size=384
    )
    
    # 设置集合
    if not rag.setup():
        print("❌ 无法设置 Qdrant 集合")
        return
    
    print("✅ 系统初始化完成")
    print("🔍 开始测试查询...")
    
    # 测试查询
    test_questions = [
        "什么是 MoFA？",
        "介绍一下人工智能",
        "Python 编程相关的内容",
        "机器学习的基本概念"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n📝 测试查询 {i}: {question}")
        
        try:
            result = await rag.answer_question(question)
            
            print(f"✅ 查询状态: {result.get('status', 'unknown')}")
            print(f"📖 回答长度: {len(result.get('answer', ''))} 字符")
            print(f"📚 相关源数量: {len(result.get('sources', []))}")
            
            if result.get('answer'):
                # 显示回答的前200字符
                answer_preview = result['answer'][:200]
                if len(result['answer']) > 200:
                    answer_preview += "..."
                print(f"💬 回答预览: {answer_preview}")
            
        except Exception as e:
            print(f"❌ 查询失败: {e}")
    
    print("\n🎉 查询测试完成！")

if __name__ == "__main__":
    asyncio.run(test_query())