

from openai import OpenAI
import json
if __name__ == "__main__":
    client = OpenAI(base_url="http://127.0.0.1:8025/v1", api_key="sk-jsha-1234567890")

    # user_input = """"endpoint": "https://api.ipify.org?format=json","description": "Get the public IP address in IPv4 format.","documentation_url": "https://www.ipify.org/?ref=freepublicapis.com","request_type": "GET","request_parameter": "None","error": false    """
    user_input = """I want to create an agent to query the meaning of a certain word def define_word(word): response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}") if response.ok: definition = response.json()[0]["meanings"][0]["definitions"][0]["definition"] return f"{word}: {definition}" return "未找到释义" print(define_word("serendipity"))"""
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content":str(user_input)},
    ],
    )
    print(response)