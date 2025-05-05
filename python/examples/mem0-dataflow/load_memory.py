# import argparse
# import json
# import os
#
# from dotenv import load_dotenv
# from mem0 import Memory
#
# from typing import Any, Dict
# from dora import Node
# from mofa.agent_build.base.base_agent import BaseMofaAgent
# from mofa.kernel.utils.util import create_agent_output, load_node_result
# from mofa.utils.files.read import read_yaml
# import pyarrow as pa
# RUNNER_CI = True if os.getenv("CI") == "true" else False
#
# class MemoryRecordAgent(BaseMofaAgent):
#     def load_config(self, config_path: str = None) -> Dict[str, Any]:
#         if config_path is None:
#             config_path = self.config_path
#         # return read_yaml(file_path=config_path)['agent']['llm']
#         return read_yaml(file_path=config_path)['agent']
#     def load_user_id(self,config_path:str=None):
#         if config_path is None:
#             config_path = self.config_path
#         return read_yaml(file_path=config_path)['agent']['user_id']
#     def create_llm_client(self,config:dict=None,*args,**kwargs):
#         self.init_llm_config()
#         os.environ["OPENAI_API_KEY"] = os.environ.get('LLM_API_KEY')
#         if os.environ.get('LLM_API_URL',None) is not None:
#             os.environ["OPENAI_API_BASE"] = os.environ.get('LLM_API_URL')
#         mem0_config = self.load_config()
#         m = Memory.from_config(mem0_config)
#         self.llm_client = m
#         return self
#     def run(self,agent_result:str, task:str=None,*args, **kwargs):
#         mem0_config = self.load_config()
#         self.create_llm_client(mem0_config)
#         user_id = self.load_user_id()
#         messages = [
#             {"role": "user", "content": task},
#             {"role": "assistant", "content": agent_result},
#         ]
#         self.llm_client.add(messages,user_id=user_id,metadata={"task":task})
#         return True
# import argparse
# import json
# import os
#
# from dotenv import load_dotenv
# from mem0 import Memory
#
# from typing import Any, Dict
# from dora import Node
# from mofa.agent_build.base.base_agent import BaseMofaAgent
# from mofa.kernel.utils.util import create_agent_output
# from mofa.utils.files.read import read_yaml
# import pyarrow as pa
# RUNNER_CI = True if os.getenv("CI") == "true" else False
#
# class MemoryRetrievalAgent(BaseMofaAgent):
#     def load_config(self, config_path: str = None) -> Dict[str, Any]:
#         if config_path is None:
#             config_path = self.config_path
#         return read_yaml(file_path=config_path)['agent']
#     def load_user_id(self,config_path:str=None):
#         if config_path is None:
#             config_path = self.config_path
#         return read_yaml(file_path=config_path)['agent']['user_id']
#     def create_llm_client(self,config:dict=None,*args,**kwargs):
#         self.init_llm_config()
#         os.environ["OPENAI_API_KEY"] = os.environ.get('LLM_API_KEY')
#         if os.environ.get('LLM_API_URL',None) is not None:
#             os.environ["OPENAI_API_BASE"] = os.environ.get('LLM_API_URL')
#         mem0_config = self.load_config()
#         m = Memory.from_config(mem0_config)
#         self.llm_client = m
#         return self
#     def get_mem0_search_text(self,memory_datas):
#         try:
#             results = list(set([memory_data.get("memory") for memory_data in memory_datas]))
#         except Exception as e :
#             results = memory_datas.get("results")
#         return results
#     def run(self, task:str=None,*args, **kwargs):
#         mem0_config = self.load_config()
#         self.create_llm_client(mem0_config)
#         user_id = self.load_user_id()
#         memory_result = self.llm_client.search(task, user_id=user_id)
#         results = self.get_mem0_search_text(memory_datas=memory_result)
#         self.llm_client.get_all(user_id='mofa')
#
#         return results
# task = 'chenzi like dog'
# config_path = '/Users/chenzi/project/zcbc/mofa/python/agent-hub/memory-record/memory_record/configs/config.yml'
# agent_result = """Answer: Dogs are often likened to humans in various ways due to their social nature, loyalty, and ability to form strong bonds with people. They exhibit emotions similar to humans, such as joy, fear, and affection. Additionally, dogs communicate through body language and vocalizations, much like humans use speech and gestures. Their capacity for learning and understanding commands also parallels human cognitive abilities. Overall, the comparison highlights the deep connection and companionship that can exist between dogs and humans. """
# memmory = MemoryRecordAgent(config_path=config_path,
#                                 llm_config_path='.env.secret')
# result = memmory.run(task=task,agent_result=agent_result)
#
# memmory = MemoryRetrievalAgent(config_path=config_path,
#                                 llm_config_path='.env.secret')
# resulta = memmory.run(task=task)