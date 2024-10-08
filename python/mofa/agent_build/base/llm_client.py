from dsp import LM
import requests
import dspy

from mofa.utils.envs.util import init_proxy_env, init_env


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

def init_dspy_llm_client(agent_config:dict) :
    if agent_config.get('proxy_url', None) is not None:
        init_proxy_env(proxy_url=agent_config.get('proxy_url', 'http://127.0.0.1:10809'))
    if agent_config.get('envs', None) is not None: init_env(env=agent_config['envs'])
    if agent_config.get('model_api_key') != 'ollama' and agent_config.get('model_name',None) is None:
        turbo = dspy.OpenAI(model=agent_config.get('model_name'), max_tokens=agent_config.get('model_max_tokens'),
                            api_key=agent_config.get('model_api_key'), api_base=agent_config.get('model_api_url', None))
    elif agent_config.get('model_api_key') == 'ollama':
        turbo = dspy.OllamaLocal(model=agent_config.get('model_name', 'llama3'),
                                 base_url=agent_config.get('model_api_url', 'http://127.0.0.1:11434'), )
    else:
        turbo = SiliconFlowClient(
            model=agent_config.get('model_name'),
            api_key=agent_config.get('model_api_key'),
            base_url=agent_config.get('model_api_url', None),
        )

    dspy.settings.configure(lm=turbo)
