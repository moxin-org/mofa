
import json
import os

from dotenv import load_dotenv
from mofa.agent_build.base.base_agent import run_agent, MofaAgent
from mem0 import Memory

from mofa.utils.files.read import read_yaml

config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/configs/config.yml'
config_data = read_yaml(str(config_path))
os.environ['OPENAI_API_KEY'] = 'sk-'
messages = []
memory = Memory.from_config(config_data.get('agent'))
user_id = 'mofa'
query = 'Who lives in Shanghai? What is its name?'
relevant_memories = memory.search(query=query, user_id=user_id, limit=os.getenv('MEMORY_LIMIT', 5))
print(relevant_memories)