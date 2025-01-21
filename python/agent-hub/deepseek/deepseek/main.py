import json
from mofa.agent_build.base.base_agent import MofaAgent
import os
from dotenv import load_dotenv
from openai import OpenAI
from deepseek import agent_config_dir_path
from mofa.utils.files.read import read_yaml


def main():
    agent = MofaAgent(agent_name='deepseek')
    while True:
        load_dotenv(agent_config_dir_path + '/.env.secret')
        client = OpenAI(api_key=os.getenv('LLM_API_KEY'), base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": json.dumps(read_yaml(file_path = agent_config_dir_path + '/configs/agent.yml').get('agent').get('prompt'))},
                {"role": "user", "content":  f"user query: {agent.receive_parameter(parameter_name='query')}  serper search data : {json.dumps(agent.receive_parameter(parameter_name='serper_result'))}"},
            ],
            stream=False
        )
        agent.send_output(agent_output_name='deepseek_result', agent_result=response.choices[0].message.content)
if __name__ == "__main__":
    main()
