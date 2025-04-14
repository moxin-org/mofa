import os
import json
from mofa.utils.ai.conn import create_openai_client

client = create_openai_client(env_file='.env.secret')
file_path = 'crawl_results_20250411_142417.json'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"错误: 文件 '{file_path}' 未找到。")
except json.JSONDecodeError:
    print(f"错误: 文件 '{file_path}' 包含无效的 JSON 格式。")
except Exception as e:
    print(f"发生了一个错误: {e}")

prompt = """
COSTAR Prompt
Context: You will be provided with the content of an HTML document. This HTML might contain information about web services, integrations, or data sources accessible through APIs.
Objective: Your goal is to identify up to three potentially valuable APIs referenced or implied within the provided HTML content. For each identified API, you should demonstrate a possible use case by generating a concise Python code snippet. By default, assume the use of the requests library for interacting with these APIs. The code should illustrate how to retrieve data or perform an action using the identified API. It's crucial that your understanding of the API's presence and potential use is derived from the content of the HTML itself. However, if after carefully analyzing the HTML, you find no indications or suggestions of any external API usage, you MUST explicitly return None as your final response.
Steps:
Thoroughly examine the provided HTML content to understand its structure and purpose.
Identify elements, attributes, scripts, or text that suggest the interaction with external APIs. Look for:
Explicit mentions of API names (e.g., "YouTube Data API", "OpenWeatherMap API").
Patterns in URLs that resemble API endpoints (e.g., URLs containing terms like "api", "rest", "v1", followed by data identifiers or parameters).
JavaScript code that uses functions or methods commonly associated with making web requests (like fetch() or libraries like axios, which imply API calls).
Data structures (like JSON or XML) embedded in the HTML that might originate from an API.
References to API keys or authorization methods.
Crucially, if you cannot find any of the indicators mentioned in step 2 within the HTML content, immediately stop and return None. Do not proceed to step 4.
For each potential API you have identified (up to three):
Infer the API's base URL or a specific endpoint based on the clues in the HTML.
Determine a likely function or data point that the API could provide.
Construct a basic Python code snippet using the requests library to interact with this inferred endpoint. The code should include:
Importing the requests library (import requests).
Setting a variable for the inferred API endpoint URL.
Making a GET request to this URL.
Checking if the response was successful (status code 200).
If successful, provide a placeholder comment indicating how to process the response (e.g., # Process the JSON response here). If you can infer a likely data structure (like a list of dictionaries), include a comment suggesting how to access a specific piece of information.
If the request fails, print an error message including the status code.
Provide a brief description of what you believe this API does, based on your analysis of the HTML.
Answer Format:
If you identify one or more APIs, present your findings for each using the following structure:
API Description: [Your understanding of the API's purpose based on the HTML content]
Code Snippet:
Python
import requests
url = "[Inferred API Endpoint URL]"
response = requests.get(url)

if response.status_code == 200:
    # [Comment on how to process the response, e.g., "Process the JSON response here to extract data."]
    # Example: data = response.json()
    #          print(data.get('some_key'))
    pass
else:
    print(f"Request to {url} failed with status code: {response.status_code}")
If, after your analysis, you find no evidence of API usage within the HTML, your sole response should be:

None
Resources: The content of the HTML document.

By adding this explicit check and emphasizing it in the prompt, you ensure that the agent will return None when no APIs are detected in the HTML content. Remember to provide the HTML document to the agent when using this prompt.
"""
for example_data in data:
    if len(str(example_data['markdown'])) > 350 and example_data['status']=='success' and example_data.get('llm_result',None) is None:
        try:
            response = client.chat.completions.create(
                model=os.getenv('LLM_MODEL_NAME', 'gpt-4o'),
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": example_data['markdown']},
                    {"role": "system", "content": example_data['url']},
                ],
            )
            result = response.choices[0].message.content
            example_data['llm_result'] = result
        except Exception as e :
            continue
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                print(f"数据已成功写回文件: {file_path}")

        except Exception as e:
            print(f"写入文件时发生错误: {e}")
        print(f"完成 -> ", example_data['url'])

