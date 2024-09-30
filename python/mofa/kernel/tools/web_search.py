import json
import requests
from fastapi import HTTPException
from loguru import logger
def search_web_with_serper(query: str, subscription_key: str,search_num:int=10,search_engine_timeout:int=5):
    """
    Search with serper and return the contexts.
    """
    payload = json.dumps({
        "q": query,
        "num": (
            search_num
            if search_num % 10 == 0
            else (search_num // 10 + 1) * 10
        ),
    })
    headers = {"X-API-KEY": subscription_key, "Content-Type": "application/json"}

    response = requests.post(
        "https://google.serper.dev/search",
        headers=headers,
        data=payload,
        timeout=search_engine_timeout,
    )
    if not response.ok:
        logger.error(f"{response.status_code} {response.text}")
        raise HTTPException(response.status_code, "Search engine error.")
    json_content = response.json()
    try:
        # convert to the same format as bing/google
        contexts = []
        if json_content.get("knowledgeGraph"):
            url = json_content["knowledgeGraph"].get("descriptionUrl") or json_content["knowledgeGraph"].get("website")
            snippet = json_content["knowledgeGraph"].get("description")
            description = json_content['knowledgeGraph'].get('description','')
            if url and snippet:
                contexts.append({
                    "name": json_content["knowledgeGraph"].get("title",""),
                    "url": url,
                    "snippet": snippet,
                    'description':description,
                })
        if json_content.get("answerBox"):
            url = json_content["answerBox"].get("url")
            snippet = json_content["answerBox"].get("snippet") or json_content["answerBox"].get("answer")
            title = json_content["answerBox"].get("title",'')
            if url and snippet:
                contexts.append({
                    "name": json_content["answerBox"].get("title",""),
                    "url": url,
                    "snippet": snippet,
                    'title':title,
                    'description':''
                })
        contexts += [
            {"name": c["title"], "url": c["link"], "snippet": c.get("snippet",""),}
            for c in json_content["organic"]
        ]
        return contexts
    except KeyError:
        logger.error(f"Error encountered: {json_content}")
        return []
