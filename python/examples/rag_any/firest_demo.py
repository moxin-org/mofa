import asyncio
import os
import inspect
import logging
import logging.config
import time
from pathlib import Path
from typing import List, Any, Dict

from lightrag import LightRAG, QueryParam
from lightrag.llm.ollama import ollama_model_complete, ollama_embed
from lightrag.llm.openai import openai_embed, gpt_4o_mini_complete
from lightrag.utils import EmbeddingFunc, logger, set_verbose_debug
from lightrag.kg.shared_storage import initialize_pipeline_status

from dotenv import load_dotenv

from mofa.utils.files.util import get_all_files

load_dotenv(dotenv_path=".env", override=False)

WORKING_DIR = os.getenv('LIGHTRAG_WORKING_DIR',
                                '.')

USE_QDRANT = os.getenv('USE_QDRANT', 'false').lower() == 'true'
QDRANT_URL = os.getenv('QDRANT_URL', 'http://localhost:6333')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
QDRANT_COLLECTION_NAME = os.getenv('QDRANT_COLLECTION_NAME', 'lightrag_vectors')
os.environ['OPENAI_API_KEY'] = os.getenv('LLM_API_KEY', 'sk-')


async def process_files_batch(rag, files: List[Path], batch_size: int = 10) -> Dict[str, Any]:
    """批量处理文件"""
    if not files:
        return {'success': False, 'error': '没有文件需要处理'}

    total_success = 0
    total_failed = 0

    logging.info(f"开始批量处理 {len(files)} 个文件")

    for i in range(0, len(files), batch_size):
        batch_files = files[i:i + batch_size]

        for file_path in batch_files:
            try:
                t1 = time.time()
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    await rag.ainsert(content)
                    logging.info(f"成功处理文件 {file_path.name}  ,耗时 {time.time() - t1:.2f} 秒")
            except Exception as e:
                logging.error(f"读取文件失败 {file_path.name}: {e}")
                total_failed += 1

        # 批量插入RAG - 使用同步方法进行批量插入


    logging.info(f"批量处理完成: 成功 {total_success}, 失败 {total_failed}")

    return {
        'success': True,
        'total_files': len(files),
        'success_count': total_success,
        'failed_count': total_failed
    }
def configure_logging():
    """Configure logging for the application"""

    # Reset any existing handlers to ensure clean configuration
    for logger_name in ["uvicorn", "uvicorn.access", "uvicorn.error", "lightrag"]:
        logger_instance = logging.getLogger(logger_name)
        logger_instance.handlers = []
        logger_instance.filters = []

    # Get log directory path from environment variable or use current directory
    log_dir = os.getenv("LOG_DIR", os.getcwd())
    log_file_path = os.path.abspath(os.path.join(log_dir, "lightrag_ollama_demo.log"))

    print(f"\nLightRAG compatible demo log file: {log_file_path}\n")
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    # Get log file max size and backup count from environment variables
    log_max_bytes = int(os.getenv("LOG_MAX_BYTES", 10485760))  # Default 10MB
    log_backup_count = int(os.getenv("LOG_BACKUP_COUNT", 5))  # Default 5 backups

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(levelname)s: %(message)s",
                },
                "detailed": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stderr",
                },
                "file": {
                    "formatter": "detailed",
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": log_file_path,
                    "maxBytes": log_max_bytes,
                    "backupCount": log_backup_count,
                    "encoding": "utf-8",
                },
            },
            "loggers": {
                "lightrag": {
                    "handlers": ["console", "file"],
                    "level": "INFO",
                    "propagate": False,
                },
            },
        }
    )

    # Set the logger level to INFO
    logger.setLevel(logging.INFO)
    # Enable verbose debug if needed
    set_verbose_debug(os.getenv("VERBOSE_DEBUG", "false").lower() == "true")


if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)


async def initialize_rag():
    qdrant_config = {
        "cosine_better_than_threshold": 0.2
    }
    # rag = LightRAG(
    #     working_dir=WORKING_DIR,
    #     llm_model_func=ollama_model_complete,
    #     llm_model_name=os.getenv('LLM_MODEL', 'gpt-oss:20b'),
    #     summary_max_tokens=10248,
    #     # vector_storage="QdrantVectorDBStorage",
    #     # vector_db_storage_cls_kwargs=qdrant_config,
    #     llm_model_kwargs={
    #         "host": os.getenv("OLLAMA_LLM_HOST", "http://10.100.1.115:11434"),
    #         "options": {"num_ctx": 8192},
    #         "timeout": int(os.getenv("TIMEOUT", "300")),
    #     },
    #     embedding_func=openai_embed,
    #     max_parallel_insert=os.cpu_count()*2
    # )
    rag = LightRAG(
        working_dir=WORKING_DIR,
        embedding_func=EmbeddingFunc(func=openai_embed,embedding_dim=1024),
        llm_model_func=gpt_4o_mini_complete,
        vector_storage="QdrantVectorDBStorage",
        vector_db_storage_cls_kwargs=qdrant_config,
        max_parallel_insert=os.cpu_count() * 2

    )
    await rag.initialize_storages()
    await initialize_pipeline_status()

    return rag


async def print_stream(stream):
    async for chunk in stream:
        print(chunk, end="", flush=True)


async def main():
    try:
        # Clear old data files
        files_to_delete = [
            "graph_chunk_entity_relation.graphml",
            "kv_store_doc_status.json",
            "kv_store_full_docs.json",
            "kv_store_text_chunks.json",
            "vdb_chunks.json",
            "vdb_entities.json",
            "vdb_relationships.json",
        ]

        for file in files_to_delete:
            file_path = os.path.join(WORKING_DIR, file)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleting old file:: {file_path}")

        # Initialize RAG instance
        rag = await initialize_rag()

        # Test embedding function
        test_text = ["This is a test string for embedding."]
        embedding = await rag.embedding_func(test_text)
        embedding_dim = embedding.shape[1]
        print(f"Detected embedding dimension: {embedding_dim}\n\n")
        with open("README.md", "r", encoding="utf-8") as f:
            await rag.ainsert(f.read())

        # Perform naive search
        print("\n=====================")
        print("Query mode: naive")
        print("=====================")
        resp = await rag.aquery(
            "如何启动 Qdrant 数据库",
            param=QueryParam(mode="hybrid"),
        )
        if inspect.isasyncgen(resp):
            await print_stream(resp)
        else:
            print(resp)



        # Perform hybrid search
        print("\n=====================")
        print("Query mode: hybrid")
        print("=====================")
        resp = await rag.aquery(
            "What are the top themes in this story?",
            param=QueryParam(mode="hybrid", stream=True),
        )
        if inspect.isasyncgen(resp):
            await print_stream(resp)
        else:
            print(resp)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if rag:
            await rag.llm_response_cache.index_done_callback()
            await rag.finalize_storages()


if __name__ == "__main__":
    # Configure logging before running the main function
    configure_logging()
    asyncio.run(main())
    print("\nDone!")
