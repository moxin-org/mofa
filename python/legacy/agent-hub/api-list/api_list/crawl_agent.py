import os
import asyncio
import pandas as pd
from langchain_openai import ChatOpenAI
from browser_use import Agent
from pydantic import SecretStr
from dotenv import load_dotenv
# Initialize the model
api_key = os.getenv("API_KEY",'9d30dda4-67df-48b0-b86f-26184e674722')

llm=ChatOpenAI(base_url='https://ark.cn-beijing.volces.com/api/v3/', model='deepseek-r1-250120', api_key=SecretStr(api_key))


async def run_agent(url:str):
    task = """
                ### **Optimized CoSTAR Prompt (English Version)**
                **Context**  
                I'm developing an automation toolkit that extracts data from various REST APIs and encapsulates them into Python functions. While I have examples like `wiki_summary()`, I need to expand this to more domains (e.g., dictionary, finance, education) while maintaining consistent code style.
                **Objective**  
                Generate a strictly standardized prompt that enables the AI to:  
                1. Create structurally consistent Python functions based on user-provided API descriptions and example templates  
                2. Automatically identify key API elements (URL construction, parameters, error handling)  
                3. Ensure output code meets these requirements:  
                   - Uses `requests` library with `response.ok` validation  
                   - Includes clear docstrings and type annotations (e.g., `-> str`)  
                   - Covers error handling for network requests, JSON parsing, and missing data  

                **Style**  
                - **Code Style**: Exactly matches provided examples (e.g., f-strings, slicing operations)  
                - **Domain Adaptability**: Handles APIs across categories (Finance/Education/Reference)  
                - **Conciseness**: Prioritizes direct data access (e.g., `[0]["meanings"][0]`)  

                **Task**  
                1. Input: User provides:  
                   - API function description (e.g., "fetch cryptocurrency price")  
                   - Target API documentation/URL  
                2. Processing: AI must:  
                   - Parse API docs to extract endpoint URL and parameter rules (path params like `{word}` or query params like `?country=China`)  
                   - Generate functions matching the example structure  
                3. Output: Ready-to-use Python function containing:  
                   - Function signature (e.g., `def get_weather(city: str) -> dict:`)  
                   - Dynamic URL construction (using f-strings or params dict)  
                   - Precise data extraction (e.g., `response.json()[0]["capital"]`)  

                **Action**  
                AI must prioritize:  
                1. **URL Construction**:  
                   - Path params: `f"https://api.example.com/{word}"`  
                   - Query params: `params={"country": country}`  
                2. **Data Extraction**:  
                   - Direct access: `response.json()[0]["meanings"][0]["definition"]`  
                   - Batch processing: `[uni["name"] for uni in response.json()[:3]]`  
                3. **Error Handling**:  
                   - Basic: `if response.ok: ... else return "error message"`  
                   - Advanced: `try/except` for timeouts/JSON parsing  

                **Response**  
                Output must include:  
                1. **Core Function** (strict example format):  
                import requests
                def get_crypto_price(coin: str = "bitcoin") -> str:
                    Fetch real-time cryptocurrency price (default: bitcoin).

                    Args:
                        coin: Cryptocurrency ID (e.g., ethereum, dogecoin).

                    Returns:
                        str: Formatted string (e.g., "BTC price: $43000") or error message.

                    response = requests.get(
                        f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd",
                        timeout=5
                    )
                    if response.ok:
                        return f"{coin.upper()} price: ${response.json()[coin]['usd']}"
                    return "Failed to fetch price"

                2. **Extensions** (optional):  
                   - How to modify for multi-coin queries (`?ids=bitcoin,ethereum`)  
                   - Code snippets for caching/retry mechanisms  

                ### **Enhanced Features (From Examples)**  
                1. **Default Parameters**: E.g., `country="China"` (Education example)  
                2. **Data Cleaning**: E.g., `.split('T')[1][:5]` for time extraction (Timezone example)  
                3. **Compact Output**: E.g., direct `f"{word}: {definition}"` return (Dictionary example)  
                4. **Domain Coverage**: Proven support for Finance/Education/Reference categories  

                Simply provide **function description + API docs**, and the AI will generate code perfectly matching the examples!

                The webpage that needs to be summarized is : 
            """ + url
    # Create agent with the model
    agent = Agent(
        task=task,
        llm=llm
    )
    return await agent.run()

df = pd.read_csv('extracted_apis.csv')
api_list = df['url'].tolist()
for url in api_list:
    if isinstance(url,float):
        continue
    else:
        url = 'https://bitwarden.com/help/api/'
        print('url : ',url)
        result = asyncio.run(run_agent(url))
        print(result)
        break