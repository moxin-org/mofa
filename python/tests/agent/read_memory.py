import os

import requests
from mem0 import Memory
config = {
    "llm": {
        "provider": "openai",
        "config": {
            "model": "Qwen/Qwen2.5-32B-Instruct",  # 替换为你的模型名称
            "max_tokens": 1500,
        }
    },
    "vector_store": {
            "provider": "chroma",
            "config": {
                "collection_name": "test",
                "path": "./db",
            }
        },
    "embedder": {
        "provider": "openai",
        "config": {
            "model": "BAAI/bge-large-zh-v1.5"
        }
    }

}
# os.environ["OPENAI_API_BASE"] = "https://api.siliconflow.cn/v1/"
# os.environ["OPENAI_API_KEY"] = "sk"
#
# m = Memory.from_config(config)
# related_memories = m.search(query="黑神话悟空", user_id="mofa")
# print(related_memories)