from mofa.run.run_agent import run_dspy_or_crewai_agent
from mofa.kernel.utils.util import load_agent_config
from mofa.run.run_agent import  run_dspy_or_crewai_agent
import dspy
#
# from dsp import LM
# import requests
#
# from mofa.agent_build.reasoner.reasoner import ReasonerModule
#
# from dsp import LM
# import requests
# class SiliconFlowClient(LM):
#     def __init__(self, model:str, api_key:str, base_url:str=None):
#         self.model = model
#         self.api_key = api_key
#         if base_url is None:
#             base_url = "https://api.siliconflow.cn/v1/chat/completions"
#         self.base_url = base_url
#         self.history = []
#         self.kwargs = {"temperature":0.7}  # 初始化kwargs属性
#     def basic_request(self, prompt: str, **kwargs):
#         headers = {
#             "accept": "application/json",
#             "content-type": "application/json",
#             "authorization": f"Bearer {self.api_key}"
#         }
#         data = {
#             "model": self.model,
#             "messages": [
#                 {"role": "user", "content": prompt}
#             ],
#             "stream": False,
#             "max_tokens": kwargs.get("max_tokens", 512),
#             "temperature": kwargs.get("temperature", 0.7),
#             "top_p": kwargs.get("top_p", 0.7),
#             "top_k": kwargs.get("top_k", 50),
#             "frequency_penalty": kwargs.get("frequency_penalty", 0.5),
#             "n": kwargs.get("n", 1)
#         }
#         response = requests.post(self.base_url, headers=headers, json=data)
#         response = response.json()
#         self.history.append({
#             "prompt": prompt,
#             "response": response,
#             "kwargs": kwargs,
#         })
#         return response
#     def __call__(self, prompt, only_completed=True, return_sorted=False, **kwargs):
#         response = self.basic_request(prompt, **kwargs)
#         completions = [result.get('message').get("content") for result in response["choices"]]
#         return completions
# # 使用示例
# import dspy
# # 初始化自定义客户端
# silicon_flow_client = SiliconFlowClient(
#     model="deepseek-ai/DeepSeek-V2-Chat",
#     api_key="sk-",
#     base_url="https://api.siliconflow.cn/v1/chat/completions"
# )
# # 配置DSPy
# dspy.configure(lm=silicon_flow_client)
# # 生成响应
# response = silicon_flow_client(prompt="你好 你是谁？ ")
#
# agent_config =  {'agents': [{'name': 'reasoner', 'role': 'Knowledgeable Assistant', 'goal': 'You are an AI-powered assistant with access to a vast database of knowledge across multiple domains, including history, science, literature, and geography. Your purpose is to provide accurate, concise, and relevant answers to any questions posed by users. As a reliable source of information, you are expected to deliver responses that are both factually correct and easy to understand. Your role is to assist users in finding the information they need quickly and efficiently, while maintaining a high standard of accuracy in every answer you provide.', 'backstory': "Answer questions based on user's questions\n", 'verbose': True, 'allow_delegation': False, 'tools': None}], 'tasks': [{'description': '你是谁? ', 'expected_output': 'details', 'agent': 'reasoner', 'max_inter': 1, 'human_input': False}], 'model': {'model_api_key': ' ', 'model_name': 'gpt-4o-mini', 'model_max_tokens': 2048, 'module_api_url': None}, 'other': {'proxy_url': None}, 'env': {'SERPER_API_KEY': None, 'AGENTOPS_API_KEY': None}, 'crewai_config': {'memory': False}}
# reasoner = ReasonerModule(role=agent_config.get('role', ''), backstory=agent_config.get('backstory', ''),
#                                       context=agent_config.get('context', None), objective=agent_config.get('objective', None), specifics=agent_config.get('specifics', None),
#                                       actions=agent_config.get('actions', None), results=agent_config.get('results', None), example=agent_config.get('example', None), answer=agent_config.get('answer', None),
#                                       temperature=agent_config.get('temperature', 0.7), input_fields=agent_config.get('input_fields', None))
#
# agent_result = run_dspy_or_crewai_agent(agent_config)
# print(agent_result)
# answer = reasoner.forward(question="你是谁?", kwargs=agent_config.get('input_fields', {}))
# print(answer)
# from taskweaver.app.app import TaskWeaverApp
# config = {'proxy_url': None, 'agent_type': 'reasoner', 'role': 'Knowledgeable Assistant', 'backstory': 'You are an AI-powered assistant with access to a vast database of knowledge across multiple domains, including history, science, literature, and geography. Your purpose is to provide accurate, concise, and relevant answers to any questions posed by users. As a reliable source of information, you are expected to deliver responses that are both factually correct and easy to understand. Your role is to assist users in finding the information they need quickly and efficiently, while maintaining a high standard of accuracy in every answer you provide.', 'task': None, 'model_api_key': ' ', 'model_name': 'gpt-4o-mini'}
