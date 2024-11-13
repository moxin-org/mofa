from typing import List

import trafilatura

from .discovery_search_box_core import load_prompt, generate_json_from_llm,find_search_box

from pydantic import BaseModel

class Media(BaseModel):
    images:List[str] = None
    videos:List[str] = None

class HtmlSearchTextChunk(BaseModel):
    url:str = None
    description:str = None
    media:List[Media] = None

class HtmlSearchText(BaseModel):
    chunks:List[HtmlSearchTextChunk] = None


def extractor_search_box(llm_client,datas:list,search_text:str,is_load_homepage:bool=False,home_page_html:str=None):
    results = []
    for data in datas:
        html_prompt = load_prompt(prompt_type='search_text', html_code=data, keyword=search_text)
        llm_html_result = generate_json_from_llm(prompt=html_prompt, format_class=HtmlSearchText,
                                              supplement_prompt=trafilatura.extract(data),client=llm_client)
        results+=llm_html_result.chunks
    if is_load_homepage and home_page_html is not None:

        html_prompt = load_prompt(prompt_type='search_text', html_code=home_page_html, keyword=search_text)
        llm_html_result = generate_json_from_llm(prompt=html_prompt, format_class=HtmlSearchText,
                                                  supplement_prompt=trafilatura.extract(home_page_html),client=llm_client)
        results+=llm_html_result.chunks
    search_box_result = []
    if len(results) >0:
        search_box_result = [i.dict() for i in results]
    return search_box_result