from openai import OpenAI
from typing import List
from typing import Optional
from mofa.utils.ai.conn import structor_llm
from pydantic import BaseModel, Field
output_num = 40
class APIDescription(BaseModel):
    """API Description Model"""
    api_name: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "The name of the API",
            "example": "Query English Word Definition"
        }
    )
    endpoint: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "The endpoint URL or path of the API",
            "example": "https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        }
    )
    method: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "The HTTP method (e.g., GET, POST)",
            "example": "GET"
        }
    )
    parameters: Optional[dict] = Field(
        default=None,
        json_schema_extra={
            "description": "Parameters for the API. Use {} if there are no parameters.",
            "example": {
                "word": {
                    "type": "string",
                    "required": True,
                    "description": "The English word to be defined"
                }
            }
        }
    )
    description: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "A brief description of the API's functionality",
            "example": "Fetches the definition of an English word using a public dictionary API."
        }
    )

class APIDescriptions(APIDescription):
    """API接口描述列表模型"""
    apis: List[APIDescription]

env_file_path = '.env.secret'
messages = [
    {
        "role": "system",
        "content": (
            "You are a professional API documentation expert who is highly knowledgeable about publicly available open source API documentation. "
            "You can accurately extract real-world API usage examples from existing documentation."
        )
    },
    {
        "role": "user",
        "content": (
            "Based on publicly available API documentation, please provide real examples of public API usage. Requirements:\n\n"
            "1. Use only real, publicly available APIs—do not fabricate any API details.\n"
            "2. Provide examples for n different APIs, each serving a unique purpose. For each API example, include:\n"
            "   - A title for the API example\n"
            "   - An English description of its functionality\n"
            "   - The API endpoint URL\n"
            "   - A complete Python code example demonstrating its usage, including a requests call and basic error handling\n\n"
            "For example:\n\n"
            "---- Query English Word Definition\n"
            "I want to create an agent to query the meaning of a specific word.\n"
            "API Endpoint: https://api.dictionaryapi.dev/api/v2/entries/en/{word}\n"
            "Code example:\n"
            "-------------------------------------------------\n"
            "def define_word(word):\n"
            "    import requests\n"
            "    response = requests.get(f\"https://api.dictionaryapi.dev/api/v2/entries/en/{word}\")\n"
            "    if response.ok:\n"
            "        definition = response.json()[0]['meanings'][0]['definitions'][0]['definition']\n"
            "        return f\"{word}: {definition}\"\n"
            "    return \"Definition not found\"\n\n"
            "print(define_word(\"serendipity\"))\n\n"
            "---- Time Zone Converter\n"
            "I want to create an agent that converts time zones.\n"
            "API Endpoint: http://worldtimeapi.org/api/timezone/{area}\n"
            "Code example:\n"
            "-------------------------------------------------\n"
            "def get_time_in(area=\"Asia/Shanghai\"):\n"
            "    import requests\n"
            "    response = requests.get(f\"http://worldtimeapi.org/api/timezone/{area}\")\n"
            "    if response.ok:\n"
            "        return response.json()['datetime'].split('T')[1][:5]\n"
            "    return \"Failed to retrieve time\"\n\n"
            "print(f\"Current time in Shanghai: {get_time_in()}\")\n\n"
            "Please strictly follow the format above for each example. Ensure that each example is based on a real, publicly available API "
            "and that no extra explanations are added."

        )
    },{"role": "user","content":f"Output at least {output_num} examples"}
]
if __name__ =="__main__":
    response = structor_llm(env_file=env_file_path, messages=messages, response_model=APIDescriptions)
    if len(response.apis)>0:
        client = OpenAI(base_url="http://127.0.0.1:8000/v1", api_key="sk-jsha-1234567890")
        for api in response.apis:
            api_input = api.json().replace("{",'').replace("}",'')
            print("inputs -> : ", api_input)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": api_input},
                ],
            )
            print(f"output -> ",response.choices[0].message.content)



# "api_name":"OpenWeather Current Weather Data","endpoint":"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}","method":"GET","parameters":null,"description":"Retrieve current weather data for any city using OpenWeather API."