import os

import requests
from mem0 import Memory

from mofa.kernel.memory.util import load_user_id, load_mem0_client, get_mem0_search_text

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
# task = "you name is ？ "
# yaml_file_path = "/Users/chenzi/project/zcbc/mofa/python/examples/memory/configs/memory_retrieval.yml"
# m = load_mem0_client(yaml_file_path)
# user_id = load_user_id(yaml_file_path)
# memory_result = m.search(task, user_id=user_id)
# results = get_mem0_search_text(memory_result)