#!/usr/bin/env python3
"""
简化的 LightRAG 交互式问答系统
专注于查询功能，避免复杂的批量文档处理
"""

import os
import asyncio
import logging
from pathlib import Path

# 导入 LightRAG 核心组件
from lightrag import LightRAG, QueryParam
from lightrag.utils import EmbeddingFunc
from lightrag.kg.shared_storage import initialize_pipeline_status

# 避免代理问题
os.environ['NO_PROXY'] = 'localhost,127.0.0.1,::1'
os.environ['no_proxy'] = 'localhost,127.0.0.1,::1'

# 配置
OLLAMA_HOST = "10.100.1.115:11434"
LLM_MODEL = "gpt-oss:20b"
EMBED_MODEL = "dengcao/Qwen3-Embedding-8B:Q5_K_M"


async def ollama_llm_func(prompt, system_prompt=None, history_messages=None, **kwargs):
    """Ollama LLM 函数"""
    import httpx
    
    try:
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"System: {system_prompt}\n\nUser: {prompt}"
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"http://{OLLAMA_HOST}/api/generate",
                json={
                    "model": LLM_MODEL,
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {
                        "num_predict": 1000,
                        "temperature": 0.7
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
    """Ollama 嵌入函数"""
    import httpx
    import numpy as np
    
    if isinstance(texts, str):
        texts = [texts]
    
    results = []
    
    # 需要使用不同的主机端口用于嵌入服务
    embed_host = "10.100.1.115:11434"  # 使用专门的嵌入服务端口
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        for text in texts:
            try:
                response = await client.post(
                    f"http://{embed_host}/api/embed",  # 正确的embed端点
                    json={
                        "model": EMBED_MODEL,
                        "input": text  # 正确的input参数
                    }
                )
                if response.status_code == 200:
                    embedding = response.json().get("embedding", [])
                    if embedding and len(embedding) > 0:
                        results.append(embedding)
                    else:
                        logging.error(f"❌ 空的 embedding 响应")
                        return None
                else:
                    logging.error(f"❌ Embedding API 错误: {response.status_code}")
                    return None
            except Exception as e:
                logging.error(f"❌ 嵌入请求失败: {e}")
                return None
    
    return results


async def main():
    """主函数"""
    # 设置日志
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    print("🚀 简化的 LightRAG 问答系统")
    print("=" * 50)
    
    try:
        # 创建嵌入函数
        embedding_func = EmbeddingFunc(
            embedding_dim=8192,  # Qwen3-Embedding-8B 的维度
            max_token_size=8192,
            func=ollama_embed_func
        )
        
        # 创建 LightRAG 实例
        rag = LightRAG(
            working_dir="./lightrag_simple_storage",
            llm_model_func=ollama_llm_func,
            embedding_func=embedding_func,
            enable_llm_cache=True
        )
        
        # 初始化存储
        await rag.initialize_storages()
        await initialize_pipeline_status()
        
        print("✅ LightRAG 系统初始化完成")
        
        # 插入一些测试数据
        test_docs = [
            "个人服务器驱动安装：NVIDIA驱动安装步骤包括下载最新驱动、卸载旧驱动、安装新驱动并重启系统。",
            "MoFA是一个基于DORA-RS的模块化AI代理框架，支持通过dataflow配置连接不同的节点和代理。",
            "Python虚拟环境管理可以使用conda、venv或poetry等工具，推荐使用conda进行环境隔离。"
        ]
        
        print("📝 插入测试文档...")
        for i, doc in enumerate(test_docs, 1):
            try:
                await rag.ainsert(doc)
                print(f"✅ 插入文档 {i}: {doc[:50]}...")
            except Exception as e:
                print(f"❌ 插入文档 {i} 失败: {e}")
        
        # 交互式查询
        print("\n🎉 系统就绪！开始交互式问答")
        print("💡 输入问题进行查询，输入 'quit' 退出")
        
        while True:
            try:
                question = input("\n🗣️  请输入问题: ").strip()
                
                if not question:
                    continue
                    
                if question.lower() in ['quit', 'exit', 'q']:
                    print("👋 再见！")
                    break
                
                print(f"🔍 查询中...")
                
                # 执行查询
                try:
                    response = await rag.aquery(question)
                    print("=" * 60)
                    print("🎯 查询结果")
                    print("=" * 60)
                    print(f"❓ 问题: {question}")
                    print(f"🤖 回答: {response}")
                    print("=" * 60)
                except Exception as e:
                    print(f"❌ 查询失败: {e}")
                
            except KeyboardInterrupt:
                print("\n👋 程序被中断，再见！")
                break
            except Exception as e:
                print(f"❌ 处理出错: {e}")
    
    except Exception as e:
        print(f"❌ 系统启动失败: {e}")
        logging.error(f"系统启动失败: {e}")


if __name__ == "__main__":
    asyncio.run(main())