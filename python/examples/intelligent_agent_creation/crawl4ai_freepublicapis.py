
import os
import json
import asyncio
from crawl4ai import BrowserConfig, CrawlerRunConfig, AsyncWebCrawler, CacheMode
from crawl4ai.async_configs import LlmConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Dict


class ApiEndpoint(BaseModel):
    endpoint: str = Field(..., description="The full path of the api is not a relative path")
    description: str = Field(..., description="A brief explanation of what the API does")
    documentation_url: str = Field(..., description="URL pointing to the API documentation or code sample")
    request_type: str = Field(..., description="HTTP request method, e.g., GET or POST")
    request_parameter: str = Field(..., description="Request parameters expected by the API in key-value format or schema")


async def crawl_one(crawler: AsyncWebCrawler, url: str, strategy: LLMExtractionStrategy) -> Dict:
    config = CrawlerRunConfig(extraction_strategy=strategy, cache_mode=CacheMode.BYPASS)
    result = await crawler.arun(url=url, config=config)
    return {
        "url": url,
        "success": result.success,
        "data": json.loads(result.extracted_content) if result.success else None,
        "error": result.error if not result.success else None
    }


async def main(urls: List[str]):

    llm_strategy = LLMExtractionStrategy(
        llmConfig=LlmConfig(provider="openai/gpt-4o", api_token=os.getenv('LLM_API_KEY')),
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
- documentation_url (link to docs or example code)
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
    urls_to_crawl = ['https://www.freepublicapis.com/404-error-handler',
 'https://www.freepublicapis.com/4chan-api',
 'https://www.freepublicapis.com/api-error-handler',
 'https://www.freepublicapis.com/api-tools',
 'https://www.freepublicapis.com/api2news-endpoint',
 'https://www.freepublicapis.com/apic-agent',
 'https://www.freepublicapis.com/aareguru-api',
 'https://www.freepublicapis.com/acousticbrainz-api',
 'https://www.freepublicapis.com/address-lookup-service',
 'https://www.freepublicapis.com/advice-slip-api-2',
 'https://www.freepublicapis.com/advice-slip-api',
 'https://www.freepublicapis.com/affirmation-generator-api',
 'https://www.freepublicapis.com/agifyio',
 'https://www.freepublicapis.com/air-quality-api',
 'https://www.freepublicapis.com/alan-perlis-quotes',
 'https://www.freepublicapis.com/amiiboapi',
 'https://www.freepublicapis.com/anapioficeandfire',
 'https://www.freepublicapis.com/answerbook-api',
 'https://www.freepublicapis.com/anti-phishing-detection',
 'https://www.freepublicapis.com/app-store-metadata-api']
    asyncio.run(main(urls_to_crawl))
