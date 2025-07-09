#!/usr/bin/env python3
import argparse
from openai import OpenAI
import os
import json

def main():
    parser = argparse.ArgumentParser(
        description="Run a chat completion with user-provided input"
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="User prompt to send to the assistant"
    )
    args = parser.parse_args()
    user_input = args.input

    client = OpenAI(
        base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:8025/v1"),
        api_key=os.getenv("OPENAI_API_KEY", "sk-your-default-key")
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input},
        ],
    )

    # 打印完整响应内容
    print(response)

if __name__ == "__main__":
    main()
