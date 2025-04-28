

from openai import OpenAI
if __name__ == "__main__":
    client = OpenAI(base_url="http://127.0.0.1:8000/v1", api_key="***REMOVED***jsha-1234567890")
    user_input = """
    I want to create an agent to query the summary information corresponding to a certain wiki . def wiki_summary(topic): response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}") if response.ok: return response.json() return "未找到相关信息" print(wiki_summary("Python"))
    """
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content":user_input},
    ],
    )
    print(response)