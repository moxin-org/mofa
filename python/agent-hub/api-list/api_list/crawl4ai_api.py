import asyncio
import os
import random

import pandas as pd
from crawl4ai import BrowserConfig, CrawlerRunConfig, AsyncWebCrawler, CacheMode, DefaultMarkdownGenerator, \
    PruningContentFilter
from typing import List, Dict
import json
from datetime import datetime


async def crawl_single_url(url: str, crawler: AsyncWebCrawler, run_config: CrawlerRunConfig) -> Dict:
    """爬取单个URL并返回结果字典"""
    try:
        result = await crawler.arun(url=url, config=run_config)
        return {
            "url": url,
            "status": "success",
            "markdown": result.markdown,
            "error": None
        }
    except Exception as e:
        return {
            "url": url,
            "status": "failed",
            "markdown": None,
            "error": str(e)
        }


async def crawl_multiple_urls(urls: List[str]) -> List[Dict]:
    """并发爬取多个URL"""
    browser_config = BrowserConfig(
        headless=True,
        verbose=False,  # 批量爬取时建议关闭详细日志
    )

    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.ENABLED,
        markdown_generator=DefaultMarkdownGenerator(
            content_filter=PruningContentFilter(threshold=0.48, threshold_type="fixed", min_word_threshold=0)
        ),
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        tasks = [crawl_single_url(url, crawler, run_config) for url in urls]
        results = await asyncio.gather(*tasks)
        return results


def save_results(results: List[Dict], filename: str = None):
    """保存结果到JSON文件"""
    if not filename:
        filename = f"crawl_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"结果已保存到 {filename}")


async def main(urls: List[str]):
    """主函数"""
    print(f"开始爬取 {len(urls)} 个URL...")
    start_time = datetime.now()

    results = await crawl_multiple_urls(urls)

    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()

    # 统计结果
    success_count = sum(1 for r in results if r['status'] == 'success')
    print(f"\n爬取完成! 耗时: {elapsed:.2f}秒")
    print(f"成功: {success_count}/{len(urls)}")
    print(f"失败: {len(urls) - success_count}/{len(urls)}")

    # 保存结果
    save_results(results)

    # 打印简要报告
    print("\n失败URL列表:")
    for r in results:
        if r['status'] != 'success':
            print(f"- {r['url']} (错误: {r['error']})")


if __name__ == "__main__":
    url_list = pd.read_csv('extracted_apis.csv')['url'].tolist()

    urls_to_crawl = random.sample(url_list, 20)

    # urls_to_crawl = [
    #     'https://db.ygoprodeck.com/api-guide/',
    #     'https://apiip.net/',
    #     'https://geocode.xyz/api',
    #     'https://api.techniknews.net/ipgeo/',
    #     # 添加更多URL...
    # ]

    # 设置并发限制 (可选)
    semaphore = asyncio.Semaphore(os.cpu_count())  # 限制最大并发数为10

    # 运行爬取
    asyncio.run(main(urls_to_crawl))

