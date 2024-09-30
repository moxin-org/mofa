from dsp import LM
import requests
class SiliconFlowClient(LM):
    def __init__(self, model:str, api_key:str, base_url:str=None):
        self.model = model
        self.api_key = api_key
        if base_url is None:
            base_url = "https://api.siliconflow.cn/v1/chat/completions"
        self.base_url = base_url
        self.history = []
        self.kwargs = {"temperature":0.7}  # 初始化kwargs属性
    def basic_request(self, prompt: str, **kwargs):
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.api_key}"
        }
        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            "max_tokens": kwargs.get("max_tokens", 512),
            "temperature": kwargs.get("temperature", 0.7),
            "top_p": kwargs.get("top_p", 0.7),
            "top_k": kwargs.get("top_k", 50),
            "frequency_penalty": kwargs.get("frequency_penalty", 0.5),
            "n": kwargs.get("n", 1)
        }
        response = requests.post(self.base_url, headers=headers, json=data)
        response = response.json()
        self.history.append({
            "prompt": prompt,
            "response": response,
            "kwargs": kwargs,
        })
        return response
    def __call__(self, prompt, only_completed=True, return_sorted=False, **kwargs):
        response = self.basic_request(prompt, **kwargs)
        completions = [result.get('message').get("content") for result in response["choices"]]
        return completions