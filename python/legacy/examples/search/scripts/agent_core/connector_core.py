import time
import ray
from bs4 import BeautifulSoup
from crawl4ai import AsyncWebCrawler
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from .discovery_search_box_core import find_search_box

def click_chrome_selector(url: str, selector: str, second_selector:str=None,search_text: str='',is_send_text:bool=True,page_load_strategy:str='eager',time_out:int=10) -> str:
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 无头模式
    options.add_argument('--disable-gpu')  # 禁用GPU
    options.add_argument('--start-maximized')  # 最大化窗口
    options.page_load_strategy = page_load_strategy
    service = Service()

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    wait = WebDriverWait(driver, time_out)
    search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
    search_box.click()
    if is_send_text and second_selector is  None:
        search_box.send_keys(search_text)
        search_box.send_keys(Keys.RETURN)
    if second_selector is not None:
        search_input = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, second_selector))
        )
        search_input.send_keys(search_text)
        search_input.send_keys(Keys.RETURN)
        time.sleep(2)

    # 等待页面加载完成
    wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

    # 获取当前页面的HTML内容
    html = driver.page_source

    # 关闭浏览器
    driver.quit()

    return html


async def load_url_with_crawl4ai(url:str):
    async with AsyncWebCrawler(verbose=True) as crawler:
        wait_for = """() => {
                    return new Promise(resolve => setTimeout(resolve, 3000));
                }"""
        result = await crawler.arun(url=url, magic=True, simulate_user=True, override_navigator=True,wait_fo=wait_for)
        if result.status_code == 200:
            # 如果您需要进一步处理HTML内容，可以在这里进行
            # 例如，使用LLM或其他解析方法
            return result.html
        else:
            raise Exception(f"Error loading URL: {url}")

def load_url_with_selenium(url: str, time_out: int = 3, args=None, **kwargs):
    options = webdriver.ChromeOptions()
    if args is None:
        args = ['--headless', '--disable-gpu', '--start-maximized']
    for arg in args:
        options.add_argument(arg)
    service = Service()

    # 初始化Chrome浏览器
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    wait = WebDriverWait(driver, time_out)
    wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

    # 获取当前页面的HTML内容
    html = driver.page_source

    # 关闭浏览器
    driver.quit()

    return html


def clean_html(html_content: str) -> str:
    soup = BeautifulSoup(html_content, 'html.parser')
    for tag in soup(['script', 'style']):
        tag.decompose()
    clean_html = str(soup)
    return clean_html
@ray.remote
def multi_request_search_box(url:str,search_box_selector:str,search_text:str,is_clean_html:bool=True):
    try:
        if 'svg' in search_box_selector.split('>')[-1]:
            html_doc = click_chrome_selector(url=url, selector=search_box_selector, search_text=search_text,
                                             is_send_text=False)
            svg_search_box = find_search_box(html_doc)
            svg_search_box_data = []
            for i in svg_search_box:
                try:
                    html_doc = click_chrome_selector(url=url, selector=search_box_selector,
                                                     second_selector=i,
                                                     search_text=search_text)
                    if is_clean_html:
                        html_doc = clean_html(html_content=html_doc)
                    svg_search_box_data.append(html_doc)
                except Exception as e :
                    print(e)
                    continue
            return svg_search_box_data
        else:
            html_doc = click_chrome_selector(url=url, selector=search_box_selector, search_text=search_text)
            if is_clean_html:
                html_doc = clean_html(html_content=html_doc)
            return html_doc
    except Exception as e :
        print(e)
        return None
def load_search_box(url:str,search_box_html_result:list,search_text:str,is_clean_html:bool=True):
    new_search_box = []
    data = []

    if len(search_box_html_result) > 0:
        use_search_box = []
        for search_box_selector in search_box_html_result:
            try:
                if 'svg' in search_box_selector.split('>')[-1]:
                    html_doc = click_chrome_selector(url=url, selector=search_box_selector, search_text=search_text,
                                                     is_send_text=False)
                    svg_search_box = find_search_box(html_doc)
                    new_search_box = [search_box_selector + '|' + i for i in list(set(svg_search_box + new_search_box)) if
                                      i not in use_search_box + search_box_html_result]
                    continue
                use_search_box.append(search_box_selector)
                html_doc = click_chrome_selector(url=url, selector=search_box_selector, search_text=search_text)
                if is_clean_html:
                    html_doc = clean_html(html_content=html_doc)

                data.append(html_doc)
            except Exception as e:
                print(search_box_selector, '---------------  \n')
                continue
    if len(new_search_box) > 0:
        for search_box_selector in new_search_box:
            try:
                html_doc = click_chrome_selector(url=url, selector=search_box_selector.split('|')[0],
                                                 second_selector=search_box_selector.split('|')[1],
                                                 search_text=search_text)
                if is_clean_html:
                    html_doc = clean_html(html_content=html_doc)


                data.append(html_doc)
            except Exception as e:
                print(search_box_selector, '---------------  \n')
                continue
    return data

# def load_search_box(url:str,search_box_html_result:list,search_text:str,is_clean_html:bool=True):
#     task_ids = [multi_request_search_box.remote(url=url,search_box_selector=i,search_text=search_text,is_clean_html=is_clean_html) for i in search_box_html_result]
#     # task_ids = [multi_request_search_box(url=url,search_box_selector=i,search_text=search_text,is_clean_html=is_clean_html) for i in search_box_html_result]
#     results = ray.get(task_ids)
#     data = []
#     for i in results:
#         if i is not None:
#             if isinstance(i,list):
#                 data+=i
#             else:
#                 data.append(i)
#     return data
