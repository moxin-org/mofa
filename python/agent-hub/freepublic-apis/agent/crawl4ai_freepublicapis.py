
import os
import json
import asyncio
from crawl4ai import BrowserConfig, CrawlerRunConfig, AsyncWebCrawler, CacheMode,LLMConfig
from itertools import batched

from crawl4ai.extraction_strategy import LLMExtractionStrategy
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Dict

def load_file_lines(path):
    try:
        with open(path, 'r', encoding='utf‑8') as f:
            return f.read().splitlines()
    except FileNotFoundError:
        return None  # 文件不存在
def append_ndjson(file_path:str, data:dict):
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")
class ApiEndpoint(BaseModel):
    endpoint: str = Field(..., description="The full path of the api is not a relative path")
    description: str = Field(..., description="A brief explanation of what the API does")
    documentation_url: str = Field(..., description="URL pointing to the API documentation or code sample")
    request_type: str = Field(..., description="HTTP request method, e.g., GET or POST")
    request_parameter: str = Field(..., description="Request parameters expected by the API in key-value format or schema")


async def crawl_one(crawler: AsyncWebCrawler, url: str, strategy: LLMExtractionStrategy) -> Dict:
    config = CrawlerRunConfig(extraction_strategy=strategy, cache_mode=CacheMode.BYPASS)
    result = await crawler.arun(url=url, config=config)
    data = {
        "url": url,
        "success": result.success,
        "data": json.loads(result.extracted_content) if result.success else None,
        "error": result.error if not result.success else None
    }

    append_ndjson(file_path='freepublic-apis.json',data=data)

    return data

async def main(urls: List[str]):

    llm_strategy = LLMExtractionStrategy(
        llmConfig=LLMConfig(provider=os.getenv('LLM_MODEL_NAME'), api_token=os.getenv('LLM_API_KEY')),
        schema=ApiEndpoint.model_json_schema(),
        extraction_type="schema",
        instruction="""
Context
You are an AI assistant working with structured API knowledge.
You will be given information about an API endpoint.
Your task is to understand and utilize this API by interpreting the provided metadata.

Each API object includes the following fields:
- endpoint (The full path of the api is not a relative path)
- description
- documentation_url (link to doc s or example code)
- request_type (GET, POST, etc.)
- request_parameter (parameters/schema)

Please find all API endpoints on the page and return a JSON array.
"""
    )

    async with AsyncWebCrawler() as crawler:
        tasks = [crawl_one(crawler, url, llm_strategy) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=False)

    # 打印所有抓取结果
    for res in results:
        print(f"\nURL: {res['url']}")
        if res["success"]:
            print("Extracted Data:", json.dumps(res["data"], indent=2))
        else:
            print("Error extracting:", res["error"])


if __name__ == "__main__":
    # 示例：批量抓取
    load_dotenv('.env.secret')
    urls_to_crawl = load_file_lines('urls.txt')
    for idx, batch in enumerate(batched(urls_to_crawl, 10), start=1):
    #     print(f'批次 {idx}，大小 {len(batch)}')
    # urls_to_crawl = urls_to_crawl[400]
        os.environ['OPENAI_API_KEY'] = os.getenv('LLM_API_KEY')
        asyncio.run(main(list(batch)))
