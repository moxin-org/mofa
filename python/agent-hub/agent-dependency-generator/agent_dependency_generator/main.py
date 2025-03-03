import json
import os
from mofa.agent_build.base.base_agent import MofaAgent, run_agent
from mofa.utils.ai.conn import generate_json_from_llm, structor_llm
from mofa.utils.files.dir import make_dir
from mofa.utils.files.read import read_yaml
from agent_dependency_generator import agent_config_dir_path
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from mofa.utils.files.write import write_file
import toml

class LLMGeneratedRequire(BaseModel):
    """
    Schema for structured LLM output containing technical documentation and configuration
    """
    readme: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "GitHub-standard README content with installation, usage, and contribution guidelines",
            "example": """# Project\n\n## Installation\n```bash\npip install ...\n```"""
        }
    )

    toml: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "PEP 621-compliant pyproject.toml configuration content",
            "example": """[tool.poetry]\nname = "..."\n"""
        }
    )

    generation_time: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        json_schema_extra={
            "description": "ISO 8601 timestamp of generation",
            "example": "2023-10-01T12:00:00Z"
        }
    )
def generate_agent_config(user_query:str,agent_config_path:str,env_file_path:str,response_model:object,prompt_selection:str='prompt',add_prompt:str=None):
    agent_config = read_yaml(
        file_path=agent_config_path
    )
    sys_prompt = agent_config.get('agent', {}).get(prompt_selection, '')
    messages = [
        {
            "role": "system",
            "content": sys_prompt
        },
        {
            "role": "user",
            "content": user_query
        },
        {
            "role": "system",
            "content": add_prompt
        }
    ]
    print('----------- : ',messages)
    response = structor_llm(env_file=env_file_path, messages=messages, prompt=user_query,response_model=response_model)
    return response

def add_toml_info(file_path:str):
    data = toml.loads(file_path)
    data['tool']['poetry']['homepage'] = "https://github.com/moxin-org/mofa"
    data['tool']['poetry']['documentation'] = "https://github.com/moxin-org/mofa/blob/main/README.md"
    data['tool']['poetry']['readme'] = "README.md"
    write_file(data=data, file_path=file_path)


@run_agent
def run(agent: MofaAgent):
    env_file_path = os.path.join(agent_config_dir_path, '.env.secret')
    agent_config_path = os.path.join(agent_config_dir_path, 'configs', 'agent.yml')
    receive_data = agent.receive_parameters(['query','agent_config'])
    print('receive_data   : ',receive_data)
    agent_name = json.loads(receive_data.get('agent_config')).get('agent_name',None)
    module_name = json.loads(receive_data.get('agent_config')).get('module_name',None)
    result = generate_agent_config(response_model=LLMGeneratedRequire, user_query=receive_data.get('query'), agent_config_path=agent_config_path, env_file_path=env_file_path,add_prompt=f"agent_name: {agent_name} module_name: {module_name}")
    if agent_name is not  None:
        make_dir(f"{agent_name}/{module_name}")
        if result.readme in [' ','',None,'null']:
            write_file(data=f'# This Ai {agent_name}', file_path=f"{agent_name}/README.md")
        write_file(data=result.readme,file_path=f"{agent_name}/README.md")
        write_file(data=result.toml,file_path=f"{agent_name}/pyproject.toml")
        print('agent_name : ',agent_name,'    - --- module_name : ',module_name)
        data = toml.loads(f"{agent_name}/pyproject.toml")
        data['tool']['poetry']['name'] = agent_name
        data['tool']['poetry']['packages'][0]['include'] = module_name
        data['tool']['poetry']['scripts'] = {agent_name: f"{module_name}.main:main"}
        write_file(data=data,file_path=f"{agent_name}/pyproject.toml")
        add_toml_info(file_path=f"{agent_name}/pyproject.toml")
        add_toml_info(file_path=f"{agent_name}/pyproject.toml")

    agent.send_output(agent_output_name='dependency_generator_result', agent_result=result.json())

def main():
    agent = MofaAgent(agent_name='agent_dependency_generator')
    run(agent=agent)

if __name__ == "__main__":
    main()

