import os
from typing import List

from openai import OpenAI

def create_openai_client(api_key: str=os.getenv("OPENAI_API_KEY"),*args,**kwargs) -> OpenAI:
    client = OpenAI(api_key=api_key,**kwargs)
    return client
def generate_json_from_llm(client, prompt: str, format_class, messages: List[dict] = None, supplement_prompt: str = None, model_name: str = 'gpt-4o-mini') -> str:

    if messages is None:
        messages = [
            {"role": "system",
             "content": "You are a professional Ai assistant"},
            {"role": "user", "content": prompt},
        ]
    if supplement_prompt is not None:
        messages.append({"role": "user", "content": supplement_prompt})
    completion = client.beta.chat.completions.parse(
        model=model_name,
        messages=messages,
        response_format=format_class,
    )
    return completion.choices[0].message.parsed