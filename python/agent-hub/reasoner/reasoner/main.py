import argparse
import json
import os
from pathlib import Path
from mem0 import Memory
from typing import Any, Dict
from dora import Node
from mofa.agent_build.base.base_agent import BaseMofaAgent, MofaAgent
from mofa.kernel.utils.util import create_agent_output, load_node_result
from mofa.run.run_agent import run_dspy_agent
from mofa.utils.files.read import flatten_dict_simple, read_yaml
import pyarrow as pa
RUNNER_CI = True if os.getenv("CI") == "true" else False

class ReasonerAgent(BaseMofaAgent):
    
    def load_config(self, config_path: str = None) -> Dict[str, Any]:
        if config_path is None:
            config_path = self.config_path
        self.init_llm_config()
        config = flatten_dict_simple(nested_dict=read_yaml(file_path=config_path))
        config['model_api_key'] = os.environ.get('LLM_API_KEY')
        config['model_name'] = os.environ.get('LLM_MODEL_NAME','gpt-4o-mini')
        if os.environ.get('LLM_API_URL',None) is not None:
            config['model_api_url'] = os.environ.get('LLM_API_URL')
        return config
    

    def run(self, task:str=None,*args, **kwargs):
        if task is None:
            task = kwargs.get('task')
        config = self.load_config()
        config['task'] = task
        print('-------- : ',config )
        agent_result = run_dspy_agent(agent_config=config)
        return agent_result

def main():

    # Handle dynamic nodes, ask for the name of the node in the dataflow, and the same values as the ENV variables.
    agent = MofaAgent(description_file_path = Path(os.path.join(os.path.abspath(os.path.dirname(__file__)), )).parent / 'description.json')
    while True:
        agent.recevice_parameters()
        print('agent_inputs : ',agent.agent_inputs)
        reasoner = ReasonerAgent(config_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/configs/config.yml',
                            llm_config_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/.env.secret')
        result = reasoner.run(**agent.agent_inputs)
        print('reasoner_result : ',result)
        output_name = 'reasoner_result'
        agent.send_output(agent_output_name=output_name,agent_result=result)
        agent.init_agent_inputs
if __name__ == "__main__":
    main()
    # reasoner = ReasonerAgent(config_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/configs/config.yml',
    #                             llm_config_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/.env.secret')
    # result = reasoner.run(task="Hello Agent")
    # print(result)
