
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from mofa.agent_build.base.base_agent import MofaAgent, run_agent
from mofa.utils.ai.conn import generate_json_from_llm, structor_llm
from mofa.utils.files.read import read_yaml


@run_agent
def run(agent: MofaAgent):

    receive_data = agent.receive_parameters(['query','create_agent_config_result','create_agent_main_result','create_agent_require_result'])
    print(receive_data)
    # Load environment variables




    agent.send_output(agent_output_name='create_agent_folder_result', agent_result=receive_data)

def main():
    agent = MofaAgent(agent_name='create_agent_folder')
    run(agent=agent)

if __name__ == "__main__":
    main()
