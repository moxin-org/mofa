from openai import OpenAI
import os

# Configure environment to bypass proxy for local connections
# This ensures direct connection to localhost without going through any proxy
os.environ['no_proxy'] = 'localhost,127.0.0.1'

if __name__ == "__main__":
    client = OpenAI(base_url="http://127.0.0.1:8000/v3", api_key="***REMOVED***jsha-1234567890")

    user_input = 'openai'
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input},
        ], stream=True
    )
    for chunk in response:
        print(chunk)
        print("****************")
