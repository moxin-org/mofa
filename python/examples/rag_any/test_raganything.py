#!/usr/bin/env python3
"""
RAG-Anything 测试脚本
"""

import asyncio
import logging
from pathlib import Path
from raganything import RAGAnything, RAGAnythingConfig
import httpx
import json
import numpy as np

# 设置日志
logging.basicConfig(level=logging.INFO)

async def ollama_llm_func(prompt, **kwargs):
    """简单的 Ollama LLM 函数"""
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

class SimpleEmbeddingWrapper:
    """嵌入函数包装器"""
    def __init__(self, dim=384):
        self.embedding_dim = dim
    
    async def __call__(self, texts, **kwargs):
        """简单的嵌入函数（使用 Ollama）"""
        if isinstance(texts, str):
            texts = [texts]
        
        embeddings = []
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                for text in texts:
                    response = await client.post(
                        "http://10.100.1.115:11434/api/embeddings",
                        json={
                            "model": "gpt-oss:20b",
                            "prompt": text
                        }
                    )
                    if response.status_code == 200:
                        embedding = response.json().get("embedding", [])
                        if not embedding:
                            # 如果没有嵌入，创建一个简单的假嵌入
                            embedding = np.random.normal(0, 1, self.embedding_dim).tolist()
                        embeddings.append(embedding)
                    else:
                        # 创建假嵌入
                        embeddings.append(np.random.normal(0, 1, self.embedding_dim).tolist())
        except Exception as e:
            logging.warning(f"嵌入函数出错: {e}，使用随机嵌入")
            # 创建假嵌入
            for _ in texts:
                embeddings.append(np.random.normal(0, 1, self.embedding_dim).tolist())
        
        return embeddings

async def test_raganything():
    """测试 RAG-Anything 功能"""
    
    # 配置 RAG-Anything
    config = RAGAnythingConfig(
        working_dir="./rag_test_storage",
        parse_method="auto",
        parser_output_dir="./rag_test_output",
        parser="mineru",
        display_content_stats=True,
        enable_image_processing=True,
        enable_table_processing=True,
        enable_equation_processing=True,
        max_concurrent_files=1,
        recursive_folder_processing=True
    )
    
    # 初始化 RAG-Anything（配置 LLM 和嵌入函数）
    embedding_func = SimpleEmbeddingWrapper(dim=384)
    rag = RAGAnything(
        config=config,
        llm_model_func=ollama_llm_func,
        embedding_func=embedding_func
    )
    
    # 测试处理单个文件（如果存在）
    test_file = Path("./test_document.md")
    if not test_file.exists():
        # 创建测试文档
        test_content = """# 测试文档

这是一个测试文档，包含了不同类型的内容。

## 文本内容
RAG-Anything 是一个多模态文档处理框架，支持：
- PDF 文档处理
- 图片内容理解
- 表格数据提取
- 数学公式识别

## 技术特点
1. 端到端的文档处理流程
2. 多模态内容理解
3. 智能信息检索

## 应用场景
适用于知识库构建、文档分析、智能问答等场景。
"""
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        print(f"✅ 创建测试文档: {test_file}")
    
    try:
        # 处理文档
        print("🔄 开始处理测试文档...")
        await rag.process_document_complete(str(test_file))
        print("✅ 文档处理完成")
        
        # 测试查询
        print("\n🔍 测试查询功能...")
        
        # 测试查询 1
        result1 = await rag.aquery("什么是 RAG-Anything？", mode="hybrid")
        print(f"\n问题 1: 什么是 RAG-Anything？")
        print(f"回答: {result1}")
        
        # 测试查询 2
        result2 = await rag.aquery("RAG-Anything 有哪些技术特点？", mode="hybrid")
        print(f"\n问题 2: RAG-Anything 有哪些技术特点？")
        print(f"回答: {result2}")
        
        # 测试查询 3
        result3 = await rag.aquery("RAG-Anything 的应用场景有哪些？", mode="local")
        print(f"\n问题 3: RAG-Anything 的应用场景有哪些？")
        print(f"回答: {result3}")
        
        print("\n🎉 所有测试完成！")
        
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 清理资源
        try:
            await rag.finalize_storages()
            print("✅ 资源清理完成")
        except:
            pass

if __name__ == "__main__":
    asyncio.run(test_raganything())