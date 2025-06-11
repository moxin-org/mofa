from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import asyncio
import os
import random

import pandas as pd
from crawl4ai import BrowserConfig, CrawlerRunConfig, AsyncWebCrawler, CacheMode, DefaultMarkdownGenerator, \
    PruningContentFilter,JsonCssExtractionStrategy
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

# 设置 Chrome 选项
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式


# 自动下载并安装 ChromeDriver
service = Service(ChromeDriverManager().install())

# 初始化 WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# 访问目标网站
driver.get("https://www.freepublicapis.com/tags/all")
time.sleep(5)

# 获取页面内容
print("页面标题:", driver.title)
print("页面URL:", driver.current_url)

page_content = driver.page_source
driver.close()


soup = BeautifulSoup(page_content, 'html.parser')
all_api_tags = soup.find_all('a', attrs={'data-v-f3996aef': True})
free_base_url = "https://www.freepublicapis.com"
for api_url in all_api_tags:
    api_url =  free_base_url  + api_url.get('href')
    print(api_url)
    break

