
import json
import os

from dotenv import load_dotenv
from mofa.agent_build.base.base_agent import run_agent, MofaAgent
from mem0 import Memory

from mofa.utils.files.read import read_yaml


@run_agent
def run(agent:MofaAgent,memory:Memory,user_id:str=None,messages:list=None):

    if user_id is None:
        user_id = os.getenv('MEMORY_ID','mofa-memory-user')
    user_location = agent.receive_parameter('user_location')
    messages = [
        {'role': 'user', 'content': f"I live in {user_location} since 2025."},
        {'role': 'assistant', 'content': f"Got it—you've been living in {user_location} since 2025."}
    ]
    messages.append({'role': 'user', 'content': user_location})
    messages.append({'role': 'assistant', 'content': user_location})
    if os.getenv('MEMORY_CLEAR',False):
        memory.delete_all(user_id=user_id)

    memory.add(messages, user_id=user_id,)
    print('获取所有的记忆: ',memory.get_all(user_id=user_id))
    agent.send_output('mem0_add_result', agent_result=json.dumps('Add Memory Success'),is_end_status=True)

def main():
    agent = MofaAgent(agent_name='mem0-add-agent')
    load_dotenv('.env.secret')
    config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/configs/config.yml'
    config_data = read_yaml(str(config_path))
    os.environ['OPENAI_API_KEY'] = os.getenv('LLM_API_KEY')

    memory = Memory.from_config(config_data.get('agent'))
    messages = []
    run(agent=agent,memory=memory,messages=messages)


if __name__ == "__main__":
    main()
