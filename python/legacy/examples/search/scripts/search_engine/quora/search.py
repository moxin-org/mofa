import json
import tiktoken
import undetected_chromedriver as uc
import time
from bs4 import BeautifulSoup, NavigableString, Tag
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
from PIL import Image
from typing import List
from bs4 import BeautifulSoup
import os
import requests
import base64
from openai import OpenAI
from pydantic import BaseModel
from selenium.webdriver.common.action_chains import ActionChains
import random

import cv2

from mofa.utils.search.util import add_driver_cookies


class Media(BaseModel):
    images:List[str] = None
    videos:List[str] = None


class HtmlSearchTextChunk(BaseModel):
    url:str = None
    description:str = None
    media:List[Media] = None
    topic:str = None
    model_name:str = None
    price:str = None
    model_size:str = None

class HtmlSearchText(BaseModel):
    chunks:List[HtmlSearchTextChunk] = None


def estimate_tokens(content, model='gpt-4'):
    """
    Estimate the number of tokens in the content using the specified model's tokenizer.
    """
    # Initialize the encoding for the given model
    encoding = tiktoken.encoding_for_model(model)
    # Encode the content and count the tokens
    return len(encoding.encode(content))


def split_html_content(html_content, max_tokens_per_chunk, model='gpt-4'):
    """
    将 HTML 内容拆分为多个块，确保不破坏 HTML 标签结构，每个块的 token 数不超过最大限制。
    """
    encoding = tiktoken.encoding_for_model(model)
    soup = BeautifulSoup(html_content, 'html.parser')

    chunks = []
    current_chunk = ''
    current_tokens = 0

    def process_node(node):
        nonlocal current_chunk, current_tokens, chunks

        if isinstance(node, NavigableString):
            text = str(node)
            tokens = len(encoding.encode(text))

            if current_tokens + tokens > max_tokens_per_chunk:
                if current_chunk.strip():
                    chunks.append(current_chunk)
                current_chunk = ''
                current_tokens = 0

            current_chunk += text
            current_tokens += tokens

        elif isinstance(node, Tag):
            # 获取开始标签和结束标签
            start_tag = f'<{node.name}'
            for attr, value in node.attrs.items():
                if isinstance(value, list):
                    value = ' '.join(value)
                start_tag += f' {attr}="{value}"'
            start_tag += '>'
            end_tag = f'</{node.name}>'

            start_tag_tokens = len(encoding.encode(start_tag))
            end_tag_tokens = len(encoding.encode(end_tag))

            # 保存当前块的状态
            prev_chunk = current_chunk
            prev_tokens = current_tokens

            # 尝试添加开始标签
            if current_tokens + start_tag_tokens > max_tokens_per_chunk:
                if current_chunk.strip():
                    chunks.append(current_chunk)
                current_chunk = ''
                current_tokens = 0

            current_chunk += start_tag
            current_tokens += start_tag_tokens

            # 递归处理子节点
            for child in node.contents:
                process_node(child)

            # 尝试添加结束标签
            if current_tokens + end_tag_tokens > max_tokens_per_chunk:
                if current_chunk.strip():
                    current_chunk += end_tag
                    chunks.append(current_chunk)
                else:
                    # 如果开始标签和结束标签本身就超过限制，强制添加
                    current_chunk = start_tag + end_tag
                    chunks.append(current_chunk)
                current_chunk = ''
                current_tokens = 0
            else:
                current_chunk += end_tag
                current_tokens += end_tag_tokens

    # 从 body 开始遍历，如果没有 body，则遍历整个文档
    root = soup.body if soup.body else soup
    for element in root.contents:
        process_node(element)

    if current_chunk.strip():
        chunks.append(current_chunk)

    return chunks


def process_large_html_content(llm_client,html_content:str,search_text:str='',max_total_tokens=128000, model='gpt-4o-mini'):
    """
    处理大型 HTML 内容，确保每个块的 token 数不超过最大限制。
    """
    total_tokens = estimate_tokens(html_content, model=model)

    if total_tokens <= max_total_tokens:
        prompt = f"""Backstory:
            You are interacting with an HTML webpage that displays content resulting from a keyword search. The webpage contains various pieces of main content that need to be extracted and utilized.

            Objective:

            To extract all the main content from the current HTML webpage in the exact order it appears, and display it accordingly.

            Specifics:

            The content originates from a search result for a specific keyword.
            All main content elements such as text, images, and links should be included.
            The original order of content on the webpage must be preserved.
            Exclude any irrelevant elements like advertisements or navigation menus.
            Tasks:

            Analyze the HTML structure of the webpage.
            Identify and extract all main content elements.
            Organize the extracted content in the sequence it appears on the page.
            Prepare the content for display or further processing.
            Actions:

            Parse the HTML document to access the DOM structure.
            Locate the containers or elements that hold the main content.
            Extract the text, images, and links from these elements.
            Maintain the sequence by organizing content as per their order in the HTML.
            Format the extracted content for clear presentation.
            Results:

            A compiled list of all main content from the webpage, organized sequentially.
            The content is ready for display or can be used for additional processing tasks.
            The extracted data accurately reflects the information presented on the webpage after the keyword search. 

            This is Html source {html_content}

            Search Keyword: {search_text}
            """
        response = use_llm_return_json(llm_client=llm_client, prompt=prompt, format_class=HtmlSearchText)
        print("处理内容未超出 token 限制。")
        # 在这里添加您的处理逻辑
        return response
    else:
        print("内容超出 token 限制，正在拆分为多个块。")
        # 预留一些 tokens 以防止意外超出限制
        max_tokens_per_chunk = max_total_tokens - 10000
        chunks = split_html_content(html_content, max_tokens_per_chunk, model=model)
        result = []
        for i in chunks:
            prompt = f"""Backstory:
                        You are interacting with an HTML webpage that displays content resulting from a keyword search. The webpage contains various pieces of main content that need to be extracted and utilized.

                        Objective:

                        To extract all the main content from the current HTML webpage in the exact order it appears, and display it accordingly.

                        Specifics:

                        The content originates from a search result for a specific keyword.
                        All main content elements such as text, images, and links should be included.
                        The original order of content on the webpage must be preserved.
                        Exclude any irrelevant elements like advertisements or navigation menus.
                        Tasks:

                        Analyze the HTML structure of the webpage.
                        Identify and extract all main content elements.
                        Organize the extracted content in the sequence it appears on the page.
                        Prepare the content for display or further processing.
                        Actions:

                        Parse the HTML document to access the DOM structure.
                        Locate the containers or elements that hold the main content.
                        Extract the text, images, and links from these elements.
                        Maintain the sequence by organizing content as per their order in the HTML.
                        Format the extracted content for clear presentation.
                        Results:

                        A compiled list of all main content from the webpage, organized sequentially.
                        The content is ready for display or can be used for additional processing tasks.
                        The extracted data accurately reflects the information presented on the webpage after the keyword search. 

                        This is Html source {i}

                        Search Keyword: {search_text}
                        """
            response = use_llm_return_json(llm_client=llm_client, prompt=prompt, format_class=HtmlSearchText)
            result.append(response)

        return result

def use_llm_return_json(llm_client, prompt: str, format_class, supplement_prompt: str = None,
                        model_name: str = 'gpt-4o-mini', image_data: str = None) -> str:
    """使用 LLM 进行Html文本解读"""
    prompt_data = [
        {
            "type": "text",
            "text": prompt
        },
    ]

    if image_data is not None:
        # 确保图像消息也包含content字段，即使它是一个空字符串
        prompt_data.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image_data}"
            }
        })

    response = llm_client.beta.chat.completions.parse(
        model=model_name,
        messages=[
                        {
                            "role": "user",
                            "content": prompt_data
                        }
                    ],
        response_format=format_class,

    )
    return response.choices[0].message.parsed

def extract_and_download_images(html: str, target_div_class: str, output_dir: str = "images") -> List[str]:
    """
    从 HTML 中提取指定 div class 下的图片 URL 并下载图片到本地
    :param html: str - HTML 内容（网页的 HTML 源代码）
    :param target_div_class: str - 目标 div 的 class 名称
    :param output_dir: str - 保存图片的本地目录
    :return: List[str] - 提取到的图片 URL 列表
    """
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 解析 HTML
    soup = BeautifulSoup(html, "html.parser")

    # 查找目标 div
    target_div = soup.find("div", class_=target_div_class)
    if not target_div:
        print(f"未找到 class 为 {target_div_class} 的 div")
        return []

    # 提取 div 内的所有 img 标签的 src 属性
    img_tags = target_div.find_all("img")
    image_urls = []

    for img in img_tags:
        src = img.get("src")
        if src:
            image_urls.append(src)

    # 下载所有图片
    for image_url in image_urls:
        try:
            # 如果图片 URL 是相对路径，抛出警告（需要上下文补充绝对路径）
            if not image_url.startswith("http"):
                print(f"相对路径未处理: {image_url}")
                continue

            # 生成保存文件名
            filename = os.path.join(output_dir, os.path.basename(image_url))

            # 下载图片
            response = requests.get(image_url, stream=True, timeout=10)
            response.raise_for_status()  # 检查 HTTP 请求是否成功

            # 保存图片
            with open(filename, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"图片已保存: {filename}")

        except Exception as e:
            print(f"无法下载图片 {image_url}: {e}")

    print(f"完成下载 {len(image_urls)} 张图片")
    return image_urls

def human_like_drag_and_drop(driver, slider_element, distance: int):
    """
    模拟人类拖动滑块完成验证
    :param driver: Selenium WebDriver 实例
    :param slider_element: 滑块的 WebElement 对象
    :param distance: 需要滑动的距离 (像素)
    """
    action = ActionChains(driver)

    # 点击并按住滑块
    action.click_and_hold(slider_element).perform()
    time.sleep(0.5)  # 短暂停留模拟人类

    # 拖动滑块，模拟不规则路径
    current = 0
    while current < distance:
        move = random.randint(5, 15)  # 随机移动步长
        if current + move > distance:
            move = distance - current  # 防止超出目标距离
        action.move_by_offset(move, random.randint(-2, 2)).perform()  # 随机上下抖动
        current += move
        time.sleep(random.uniform(0.01, 0.03))  # 随机停顿

    # 释放滑块
    action.release().perform()
    time.sleep(5)  # 等待验证完成

def clean_html_js_and_style(html_content: str) -> str:
    soup = BeautifulSoup(html_content, 'html.parser')
    for tag in soup(['script', 'style']):
        tag.decompose()
    clean_html = str(soup)
    return clean_html

def login_quora(search_text:str, url:str= 'https://www.quora.com/', cookie_file:str= 'www.quora.com.json', ):

    # options = uc.ChromeOptions()
    # options.add_argument("--user-data-dir=/Users/chenzi/Library/Application Support/Google/Chrome/Default")  # 替换为你的用户数据目录
    # options.add_argument("--profile-directory=Default")  # 使用默认配置文件
    # options.add_argument("--auto-open-devtools-for-tabs")

    driver = uc.Chrome(headless=False,use_subprocess=False,)

    driver.get(url)
    driver = add_driver_cookies(driver=driver,cookie_file_path=cookie_file)
    driver.refresh()
    print("Waiting for user to click")
    time.sleep(random.choice([1, 6]))

    driver.find_element(by='css selector', value='#root > div > div.q-box > div > div.q-fixed.qu-fullX.qu-zIndex--header.qu-bg--raised.qu-borderBottom.qu-boxShadow--medium.qu-borderColor--raised > div > div:nth-child(2) > div > div.q-box.qu-flex--auto.qu-mx--small.qu-alignItems--center > div > div > form > div > div > div > div > div > input').send_keys(search_text + Keys.RETURN)

    time.sleep(random.choice([1, 4]))
    html_source = driver.page_source
    driver.close()
    return html_source



if __name__ == '__main__':
    search_text = 'Ai Agent'
    html_source = login_quora(search_text=search_text)
    clena_html_source = clean_html_js_and_style(html_source)
    api_key = " "
    client = OpenAI(api_key=api_key)
    result = process_large_html_content(html_content=clena_html_source,llm_client=client,search_text=search_text)
    print(result)




