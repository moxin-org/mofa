from typing import List

from bs4 import BeautifulSoup
from pydantic import BaseModel

from mofa.utils.ai.conn import generate_json_from_llm


def load_prompt(prompt_type: str,html_code:str,keyword:str=None):
    prompt = ''
    if prompt_type == "search_box":
        prompt = f"""
        Please parse the following HTML web page code:
        HTML web page code:
        {html_code}

        1. C - Context
        "You will search for search box elements in the provided HTML web page code. The page may contain multiple `input` elements used for different functions, including search, form filling, etc."

        2. O - Objective
        "The objective is to find all `input` elements in the HTML web page code where the `id` or `class` attribute contains the keyword `'search'`, to help identify the search boxes on the page."

        3. S - Style
        "The output should be technical and concise to facilitate subsequent programming and data processing."

        4. T - Tone
        "The tone should be professional and direct, providing clear and task-related results."

        5. A - Audience
        "The target audience is developers or data engineers who want to automatically locate and use the search box on the page."

        6. R - Response
        "The output should be a JSON object containing a list of strings (`list[str]`), where each string is the CSS selector path of the matching `input` element. If no matching elements are found, return an empty JSON object."
        """

    if prompt_type == "search_text":
        prompt = f'''
        Backstory:
        "You are developing an automated system to extract information related to a specific keyword from web pages. The keyword for this task is '{keyword}'. The goal is to filter out all links, content summaries, and key media content related or similar to '{keyword}' from the provided HTML web page code. Since the web content may not directly contain the exact keyword, you need to look for content associated with or similar in meaning to the keyword."

        Objective:
        "Based on the provided HTML web page code, extract all information related or similar to the keyword '{keyword}' and output it in a structured JSON format. This information includes related or similar links (URLs), content summaries for each link, and related media content such as image and video links."

        Specifics:
        "- Extract content directly related to or similar in meaning to the keyword '{keyword}'.
        - Allow matching of keyword variants, synonyms, or related topics.
        - Related links should include the full URL.
        - Content summaries should be concise and accurately describe the link content.
        - Related media content includes image URLs and video links.
        - The output JSON structure should be clear and without redundant information, facilitating subsequent programming and data processing. The corresponding content should have clear descriptions and explanations."

        Tasks:
        "1. Parse the provided HTML web page code.
        2. Find all elements directly related or similar to the keyword '{keyword}', including links, headings, paragraphs, etc.
        3. Extract the URLs, content summaries, and related media content of these elements.
        4. Ensure the extracted information is accurate and comprehensive, including content related or similar to the keyword.
        5. Organize the extracted information into a structured JSON format."

        Actions:
        "1. Parse the HTML web page code.
        2. Use the keyword '{keyword}' along with its synonyms and related terms to search for matching content.
        3. Find elements containing related keywords such as links (<a> tags), headings (e.g., <h1> to <h6> tags), paragraphs (<p> tags), etc.
        4. For each found element, extract its content, related links, and media resources (e.g., src attributes of <img> and <video> tags).
        5. Organize all extracted information into a JSON object as required."

        Results:
        "Generate a JSON object containing all information related or similar to '{keyword}'. This object should include a field 'results', which is a list where each item contains the following subfields:
        - 'url': The full URL of the related link. If it does not exist, it should be an empty string.
        - 'description': A summary or abstract related to the content. If it does not exist, it should be an empty string.
        - 'media': A sub-object containing related media content, including:
            - 'images': A list of image URLs. If there are no images, it should be an empty list.
            - 'videos': A list of video links. If there are no videos, it should be an empty list.

        Ensure that the output JSON object is clean, without unnecessary HTML tags or script code, and contains only plain text information and valid media links."

        HTML web page code:
        {html_code}
        '''
    return prompt



def extract_search_related_elements(html_content: str) -> List[BeautifulSoup]:
    """
    提取 HTML 内容中可能与搜索功能相关的所有元素。

    参数：
        html_content (str): 要解析的 HTML 文本内容。

    返回：
        List[BeautifulSoup]: 一个包含所有可能与搜索相关的元素的列表。
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    search_elements = []

    # 定义要检查的标签
    tags_to_search = ['input', 'button', 'svg', 'div', 'span', 'form', 'textarea']

    # 搜索所有指定标签的元素
    for tag in tags_to_search:
        elements = soup.find_all(tag)
        for elem in elements:
            if is_search_related(elem):
                search_elements.append(elem)

    return search_elements

def is_search_related(element: BeautifulSoup) -> bool:
    """
    判断给定的元素是否可能与搜索功能相关。

    参数：
        element (BeautifulSoup): 要判断的元素。

    返回：
        bool: 如果元素可能与搜索功能相关，返回 True；否则返回 False。
    """
    SEARCH_KEYWORDS = ['search', '搜索', 'query', '查找', '查询', 'icon-search', 'icon_search','検索','Search']

    # 检查元素的属性
    for attr in ['name', 'id', 'class', 'placeholder', 'aria-label', 'title']:
        attr_value = element.get(attr)
        if attr_value:
            if isinstance(attr_value, list):
                attr_values = ' '.join(attr_value).lower()
            else:
                attr_values = str(attr_value).lower()
            for keyword in SEARCH_KEYWORDS:
                if keyword in attr_values:
                    return True

    # 特殊处理 <input> 标签的 type 属性
    if element.name == 'input':
        input_type = element.get('type', '').lower()
        if input_type in ['search', 'text']:
            return True

    return False
def get_css_selector_with_google(tag):
    """
    获取 BeautifulSoup 标签的唯一 CSS 选择器
    """
    selector = []
    while tag is not None and tag.name != '[document]':
        sibling = tag.previous_sibling
        nth = 1
        while sibling:
            if sibling.name == tag.name:
                nth += 1
            sibling = sibling.previous_sibling
        if tag.get('id'):
            selector_part = f"{tag.name}#{tag['id']}"
            selector.insert(0, selector_part)
            break  # ID 是唯一的，后续的选择器可以省略
        else:
            if tag.get('class'):
                classes = ".".join(tag.get('class'))
                selector_part = f"{tag.name}.{classes}"
            else:
                selector_part = tag.name
            # 添加 :nth-of-type(n) 以确保选择器的唯一性
            selector_part += f":nth-of-type({nth})"
            selector.insert(0, selector_part)
        tag = tag.parent
    return " > ".join(selector)
def get_css_selector(element: BeautifulSoup) -> str:
    """
    获取元素的 CSS 选择器路径。

    参数：
        element (BeautifulSoup): 目标元素。

    返回：
        str: 元素的 CSS 选择器路径。
    """
    path = []
    while element and element.name != '[document]':
        selector = element.name
        if element.get('id'):
            selector += f"#{element.get('id')}"
        elif element.get('class'):
            classes = '.'.join(element.get('class'))
            selector += f".{classes}"
        else:
            siblings = element.find_previous_siblings(element.name)
            index = len(siblings) + 1
            selector += f":nth-of-type({index})"
        path.insert(0, selector)
        element = element.parent
    return ' > '.join(path)

def find_search_elements_in_html(html_content: str,is_google_url:bool=False) -> List[str]:

    search_elements = extract_search_related_elements(html_content)
    if is_google_url:
        selectors = [get_css_selector_with_google(elem) for elem in search_elements]
    else:
        selectors = [get_css_selector(elem) for elem in search_elements]
    return selectors
class FindSearchBoxSelector(BaseModel):
    selector: List[str] = None
def find_search_box(html_content:str, llm_max_token:int=128000, llm_client=None,is_google_url:bool=False):
    search_box_html_result = []
    if len(html_content) <= llm_max_token:
        search_box_prompt = load_prompt(prompt_type='search_box', html_code=html_content)
        search_box_html = generate_json_from_llm(prompt=search_box_prompt, format_class=FindSearchBoxSelector, client=llm_client)
        search_box_html_result = search_box_html.selector
    else:
        selectors = find_search_elements_in_html(html_content=html_content,is_google_url=is_google_url)
        if selectors:
            search_box_html_result = list(set(selectors))
    return search_box_html_result