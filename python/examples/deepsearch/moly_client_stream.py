from openai import OpenAI
import os

# Configure environment to bypass proxy for local connections
# This ensures direct connection to localhost without going through any proxy

if __name__ == "__main__":
    client = OpenAI(base_url="http://127.0.0.1:8000/v3", api_key="sk-jsha-1234567890")

    user_input = 'vllm 和 sglang的分析'
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input},
        ], stream=True
    )
    for chunk in response:
        print(chunk.choices[0].delta.id)
        # print("****************")
