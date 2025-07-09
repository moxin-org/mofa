# xx.py
import argparse
from openai import OpenAI

def main():
    parser = argparse.ArgumentParser(
        description="Run a chat completion with user-provided input"
    )
    parser.add_argument(
        "-input", "--input_text",
        required=True,
        help="User prompt for the assistant"
    )
    args = parser.parse_args()
    user_input = args.input_text

    client = OpenAI(
        base_url="http://127.0.0.1:8025/v1",
        api_key="sk-jsha-1234567890"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input},
        ],
    )
    print(response)

if __name__ == "__main__":
    main()
