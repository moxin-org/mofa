
import json
import os

from dotenv import load_dotenv
from mofa.agent_build.base.base_agent import run_agent, MofaAgent
from mem0 import Memory

from mofa.utils.files.read import read_yaml

config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/configs/config.yml'
config_data = read_yaml(str(config_path))
os.environ['OPENAI_API_KEY'] = 'sk-66'
messages = []
memory = Memory.from_config(config_data.get('agent'))
user_id = 'mofa'
query = 'my name is chenzi, i like to play games, i am a software engineer, i am 30 years old, i live in shanghai, i like to play basketball, i like to play football, i like to play tennis, i like to play badminton, i like to play table tennis, i like to play volleyball, i like to play baseball, i like to play golf, i like to play hockey, i like to play rugby, i like to play cricket, i like to play american football, i like to play soccer'
relevant_memories = memory.search(query=query, user_id=user_id, limit=os.getenv('MEMORY_LIMIT', 5))
print('----relevant_memories------  : ',relevant_memories)
llm_result = """Got it, Chenzi! 🎮⚽🏀 You're quite the sports enthusiast and a software engineer based in Shanghai. Let me know if you want help with anything—from code to game recommendations to sports discussions!"""

memories_str = "\n".join(f"- {entry['memory']}" for entry in relevant_memories["results"])
messages.append({'role': 'user', 'content': query})
messages.append({'role': 'assistant', 'content': llm_result})
print('------',messages)
memory.add(messages, user_id=user_id)
print('stop')