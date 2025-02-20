
import json
import os
from os import mkdir
from typing import Any
from mofa.agent_build.base.base_agent import MofaAgent, run_agent
from mofa.utils.files.dir import make_dir

def write_file(file_path:str,data:Any):
    try:
        if data is not None and data != '' and data !=' ' and data != 'null':
            if os.path.exists(file_path):
                os.remove(file_path)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(data)
    except Exception as e :
        print(e)
        print(f'data: {data} ----- {file_path}')


@run_agent
def run(agent: MofaAgent):
    receive_data = agent.receive_parameters(['create_agent_config_result','create_agent_main_result','create_agent_require_result'])
    # receive_data = agent.receive_parameters(['create_agent_config_result','create_agent_main_result'])
    print('-------  :',receive_data)

    agent_name = json.loads(receive_data.get('create_agent_config_result')).get('agent_name',None)
    if agent_name is not None:
        make_dir(agent_name)
        pyproject_toml_data = json.loads(receive_data.get('create_agent_require_result')).get('toml',None)
        write_file(data=pyproject_toml_data,file_path=f"{agent_name}/pyproject.toml")
        readme_data = json.loads(receive_data.get('create_agent_require_result')).get('readme',None)
        write_file(data=readme_data,file_path=f"{agent_name}/README.md")
        mkdir(f"{agent_name}/{agent_name}")
        with open(f"{agent_name}/{agent_name}/__init__.py", 'w', encoding='utf-8') as f:
            pass
        main_data = json.loads(receive_data.get('create_agent_main_result')).get('llm_generated_code',None)
        write_file(data=main_data,file_path=f"{agent_name}/{agent_name}/main.py")
        env_data = json.loads(receive_data.get('create_agent_config_result')).get('env_config',None)
        write_file(data=env_data,file_path=f"{agent_name}/{agent_name}/.env.secret")

        agent_config = json.loads(receive_data.get('create_agent_config_result')).get('yml_config',None)
        mkdir(f"{agent_name}/{agent_name}/configs")
        
        write_file(data=agent_config,file_path=f"{agent_name}/{agent_name}/configs/agent.yml")

    agent.send_output(agent_output_name='create_agent_folder_result', agent_result="Ok Create Agent ")

def main():
    agent = MofaAgent(agent_name='create_agent_folder')
    run(agent=agent)

if __name__ == "__main__":
    main()
