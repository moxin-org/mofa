# import os
#
# from openai import OpenAI
# from mem0 import Memory
#
# from mofa.utils.files.read import read_yaml
#
# os.environ["OPENAI_API_KEY"] = " "
#
# openai_client = OpenAI()
# data = read_yaml('/Users/chenzi/project/zcbc/mofa/python/agent-hub/memory-record/memory_record/configs/config.yml')
# memory = Memory.from_config(data.get('agent'))
#
# def chat_with_memories(message: str, user_id: str = "default_user") -> str:
#     # Retrieve relevant memories
#     relevant_memories = memory.search(query=message, user_id=user_id, limit=3)
#
#     memories_str = "\n".join(f"- {entry['memory']}" for entry in relevant_memories["results"])
#
#     # Generate Assistant response
#     system_prompt = f"You are a helpful AI. Answer the question based on query and memories.\nUser Memories:\n{memories_str}"
#     messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": message}]
#     response = openai_client.chat.completions.create(model="gpt-4o-mini", messages=messages)
#     assistant_response = response.choices[0].message.content
#
#     # Create new memories from the conversation
#     messages.append({"role": "assistant", "content": assistant_response})
#     memory.add(messages, user_id=user_id)
#
#     return assistant_response
#
# def main():
#     print("Chat with AI (type 'exit' to quit)")
#     while True:
#         # user_input = "Wu like Dog, Chenzi Like Car"
#         user_input = "Wu like Dog, Chenzi Like Car"
#         if user_input.lower() == 'exit':
#             print("Goodbye!")
#             break
#         print(f"AI: {chat_with_memories(user_input)}")
#
# if __name__ == "__main__":
#     main()


# class MemoryRetrievalAgent(BaseMofaAgent):
#     def load_config(self, config_path: str = None) -> Dict[str, Any]:
#         if config_path is None:
#             config_path = self.config_path
#         return read_yaml(file_path=config_path)['agent']['llm']
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
#         return results