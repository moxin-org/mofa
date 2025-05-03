from typing import List

from bs4 import BeautifulSoup


def remove_htm_label(html_content: str,labels:List[str]=None) -> str:
    if labels is None:
        labels = ['script', 'style']
    soup = BeautifulSoup(html_content, 'html.parser')
    for tag in soup(labels):
        tag.decompose()
    clean_html = str(soup)
    return clean_html