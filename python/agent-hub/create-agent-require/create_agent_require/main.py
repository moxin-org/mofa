
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from mofa.agent_build.base.base_agent import MofaAgent, run_agent
from mofa.utils.ai.conn import generate_json_from_llm, structor_llm
from mofa.utils.files.read import read_yaml
from create_agent_require import agent_config_dir_path

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
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
def generate_agent_config(user_query:str,agent_config_path:str,env_file_path:str,response_model:object) -> LLMGeneratedRequire:
    agent_config = read_yaml(
        file_path=agent_config_path
    )
    sys_prompt = agent_config.get('agent', {}).get('prompt', '')
    messages = [
        {
            "role": "system",
            "content": sys_prompt
        },
        {
            "role": "user",
            "content": user_query
        }
    ]
    response = structor_llm(env_file=env_file_path, messages=messages, prompt=user_query,response_model=response_model)
    return response

@run_agent
def run(agent: MofaAgent):
    env_file_path = os.path.join(agent_config_dir_path, '.env.secret')
    agent_config_path = os.path.join(agent_config_dir_path, 'configs', 'agent.yml')
    user_query = agent.receive_parameter('query')
    result = generate_agent_config(response_model=LLMGeneratedRequire, user_query=user_query, agent_config_path=agent_config_path, env_file_path=env_file_path)
    agent.send_output(agent_output_name='create_agent_require_result', agent_result=result.json())

def main():
    agent = MofaAgent(agent_name='create_agent_require')
    run(agent=agent)

if __name__ == "__main__":
    main()
