
import json
import os

from dotenv import load_dotenv
from mofa.agent_build.base.base_agent import run_agent, MofaAgent
from mem0 import Memory

from mofa.utils.files.read import read_yaml
load_dotenv('.env.secret')
config_path = 'config.yml'
config_data = read_yaml(str(config_path))
os.environ['OPENAI_API_KEY'] = os.getenv('LLM_API_KEY')

memory = Memory.from_config(config_data.get('agent'))
messages = []

user_id = os.getenv('MEMORY_ID', 'mofa-memory-user')

relevant_memories = memory.get_all(user_id=user_id)

memories_str = "\n".join(f"- {entry['memory']}" for entry in relevant_memories["results"])
print(memories_str)