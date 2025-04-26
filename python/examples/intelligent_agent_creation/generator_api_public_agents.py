import json
import time

from openai import OpenAI
from typing import List
client = OpenAI(base_url="http://127.0.0.1:8000/v1", api_key="***REMOVED***jsha-1234567890")

file_path = '/Users/chenzi/project/zcbc/mofa/python/agent-hub/api-list/api_list/crawl_results_20250411_142417.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

if __name__ == "__main__":
    new_agent_apis = []
    error_url_apis =  []
    for api_data  in data:
        # if i.get('llm_result',None) is not None and i.get('url') not in xx:
        t1 = time.time()
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": api_data.get('llm_result')},
                ],
            )
            print(f"完成 -> ", api_data.get('url'))
            new_agent_apis.append(api_data.get('url'))
            print('消耗时间 -> ',time.time()-t1)
            print('------------')
        except Exception as e :
            print(e )
            print('Error data', api_data)
            error_url_apis.append(api_data.get('url'))
    print('正确的是 ->',new_agent_apis)
    print('错误的是 ->',error_url_apis)