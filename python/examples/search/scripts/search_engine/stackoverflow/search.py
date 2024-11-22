import json
import tiktoken
import undetected_chromedriver as uc
import time
from bs4 import BeautifulSoup, NavigableString, Tag
from selenium.webdriver.common.by import By
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

class Media(BaseModel):
    images:List[str] = None
    videos:List[str] = None


class HtmlSearchTextChunk(BaseModel):
    url:str = None
    description:str = None
    media:List[Media] = None
    price:str

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


def process_large_html_content(llm_client,html_content:str,search_text:str='',max_total_tokens=128000, model='gpt-4'):
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
def calculate_slide_distance_debug(background_path: str, slide_path: str, debug_output_path: str = "debug_result.png") -> int:
    """
    通过优化滑块匹配算法找到滑块的缺口并计算需要滑动的距离，并保存调试图片。
    :param background_path: 背景图片路径
    :param slide_path: 滑块图片路径
    :param debug_output_path: 保存调试图片的路径
    :return: 滑块需要滑动的距离
    """
    # 读取背景图和滑块图
    background = cv2.imread(background_path, cv2.IMREAD_GRAYSCALE)
    slide = cv2.imread(slide_path, cv2.IMREAD_GRAYSCALE)

    # 边缘检测
    background_edges = cv2.Canny(background, 50, 150)
    slide_edges = cv2.Canny(slide, 50, 150)

    # 对背景图取反色
    inverted_background = cv2.bitwise_not(background_edges)

    # 模板匹配
    result = cv2.matchTemplate(inverted_background, slide_edges, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    # 保存匹配结果到调试图片
    debug_image = cv2.cvtColor(inverted_background, cv2.COLOR_GRAY2BGR)
    h, w = slide_edges.shape[:2]
    cv2.rectangle(debug_image, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 255, 0), 2)
    cv2.imwrite(debug_output_path, debug_image)

    print(f"匹配结果保存到: {debug_output_path}")
    print(f"最大匹配置信度: {max_val}")


    # 滑块需要移动的 x 坐标
    distance = max_loc[0]
    return distance


def preprocess_image(image):
    """
    对图像进行预处理，减少噪声和干扰
    :param image: 输入灰度图
    :return: 处理后的图像
    """
    # 高斯模糊减少噪声
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    # 应用边缘检测
    edges = cv2.Canny(blurred, 50, 150)
    return edges

def save_base64_as_image(base64_str: str, output_path: str) -> None:
    """
    将 Base64 编码的字符串保存为图片
    :param base64_str: str - Base64 编码的字符串
    :param output_path: str - 保存图片的路径
    """
    try:
        # 移除可能存在的 `data:image/` 前缀和 `base64,` 标记
        if "," in base64_str:
            base64_str = base64_str.split(",")[1]

        # 解码 Base64 字符串
        image_data = base64.b64decode(base64_str)

        # 保存到文件
        with open(output_path, "wb") as f:
            f.write(image_data)

        print(f"图片已保存到: {output_path}")
    except Exception as e:
        print(f"保存图片失败: {e}")


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
def read_cookie_request_url(url:str,cookie_file_path:str=None,search_text:str='mac mini4 '):


    # 2. 启动 undetected_chromedriver 浏览器实例
    options = uc.ChromeOptions()
    options.add_argument(
        "--user-data-dir=/Users/chenzi/Library/Application Support/Google/Chrome/Default")  # 替换为你的用户数据目录
    options.add_argument("--profile-directory=Default")  # 使用默认配置文件

    driver = uc.Chrome(headless=False, use_subprocess=False, options=options)
    driver.get(url)
    time.sleep(5)
    if cookie_file_path is not None:
        with open(cookie_file_path, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        for cookie in cookies:
            # 删除可能导致问题的字段
            cookie.pop('sameSite', None)
            cookie.pop('httpOnly', None)
            cookie.pop('secure', None)
            # 添加 cookie
            driver.add_cookie(cookie)
        driver.refresh()
    time.sleep(10)
    input_search_selector = '#key'
    input_search_button_selector = '#search > div > div.form.hotWords > button'

    driver.find_element(by='css selector', value=input_search_selector).send_keys(search_text)
    driver.find_element(by='css selector', value=input_search_button_selector).click()
    time.sleep(5)
    html_context = driver.page_source
    driver.close()
    return html_context
def login_stackoverflow(url:str='https://stackoverflow.com/',selector_data:dict=None):
    if selector_data is None:
        selector_data = {'user_element_selector': '#loginname', 'pwd_element_selector': '#nloginpwd',
                         'login_button': '#loginsubmit',
                         'user_element_data': '18583383212', 'pwd_element_data': 'Tt66668888.'}
    options = uc.ChromeOptions()
    options.add_argument("--user-data-dir=/Users/chenzi/Library/Application Support/Google/Chrome/Default")  # 替换为你的用户数据目录
    options.add_argument("--profile-directory=Default")  # 使用默认配置文件
    options.add_argument("--auto-open-devtools-for-tabs")

    driver = uc.Chrome(headless=False,use_subprocess=False,options=options)
    driver.get(url)

    wait = WebDriverWait(driver, 20)

    # iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
    # driver.switch_to.frame(iframe)
    # checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="checkbox"]')))
    # checkbox.click()
    print('start skip Cloudflare')
    try:
        location = pyautogui.locateOnScreen('cloudflare_checkbox.png', confidence=0.8)  #
        if location:
            center = pyautogui.center(location)
            pyautogui.click(center)
            time.sleep(15)
        else:
            print("Can't find location")
        print('end skip Cloudflare')
    except Exception as e:
        pass
    search_box_element_selector = '# search > div > input'
    driver.find_element(by='css selector', value=search_box_element_selector).send_keys()
    driver.close()
    # user_element_selector, pwd_element_selector = selector_data['user_element_selector'], selector_data[
    #     'pwd_element_selector']
    # driver.find_element(by='css selector', value=user_element_selector).send_keys(selector_data['user_element_data'])
    # driver.find_element(by='css selector', value=pwd_element_selector).send_keys(selector_data['pwd_element_data'])
    # driver.find_element(by='css selector', value=selector_data['login_button']).click()
    # print('run login ')
    # time.sleep(3)
    #
    # bigimg_image = extract_and_download_images(driver.page_source, "JDJRV-bigimg", "JDJRV-bigimg.png")
    # small_image = extract_and_download_images(driver.page_source, "JDJRV-smallimg", "JDJRV-smallimg.png")
    # save_base64_as_image(bigimg_image[0], "JDJRV_bigimg.png")
    # save_base64_as_image(small_image[0], "JDJRV_smallimg.png")
    # move_pixel = calculate_slide_distance_debug("JDJRV_bigimg.png","JDJRV_smallimg.png")
    # validate_element = driver.find_element(by='css selector',value='#JDJRV-wrap-loginsubmit > div > div > div > div.JDJRV-slide-bg > div.JDJRV-slide-inner.JDJRV-slide-btn')
    # # slide_distance = round(validate_element.location['x'], -1) + int(move_pixel)
    # slide_distance = int(move_pixel)-2
    # human_like_drag_and_drop(driver, validate_element, slide_distance)
    # print('Wait User  login ')
    # time.sleep(20)
    # print('User  login Success ')
    # file_path = 'jd_cookies.json'
    # with open(file_path, 'w') as file:
    #     json.dump(driver.get_cookies(), file, indent=4)
    # driver.close()


if __name__ == '__main__':
    login_stackoverflow()
    # home_page_url = 'https://www.jd.com/'
    # search_text = "mac mini 4 "
    # html_source = read_cookie_request_url(url=home_page_url,cookie_file_path='jd_cookies.json',search_text=search_text)
    # clena_html_source = clean_html_js_and_style(html_source)
    # api_key = "sk"
    # client = OpenAI(api_key=api_key)
    # result = process_large_html_content(html_content=clena_html_source,llm_client=client,search_text=search_text)
    # print(result)




