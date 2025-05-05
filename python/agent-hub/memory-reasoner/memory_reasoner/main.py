import argparse
import json
import os

from flask.cli import load_dotenv
from mem0 import Memory
from typing import Any, Dict
from dora import Node
from mofa.agent_build.base.base_agent import BaseMofaAgent
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
    

    def run(self, memory_context:str,task:str=None,*args, **kwargs):
        config = self.load_config()
        config['task'] = task
        if len(memory_context)>0:
            config['input_fields'] = {"memory_data":memory_context}
            print(config['input_fields'])
        agent_result = run_dspy_agent(agent_config=config)
        return agent_result

def main():

    # Handle dynamic nodes, ask for the name of the node in the dataflow, and the same values as the ENV variables.
    parser = argparse.ArgumentParser(description="Reasoner Agent")

    parser.add_argument(
        "--name",
        type=str,
        required=False,
        help="The name of the node in the dataflow.",
        default="arrow-assert",
    )
    parser.add_argument(
        "--task",
        type=str,
        required=False,
        help="Tasks required for the memmory agent.",
        default="Paris Olympics",
    )
    parser.add_argument(
        "--memory_context",
        type=str,
        required=False,
        help="Contextual memory data retrieved from memory agent for reasoning tasks.",
        default="",
    )
    args = parser.parse_args()
    task = os.getenv("TASK", args.task)

    node = Node(
        args.name
    )  # provide the name to connect to the dataflow if dynamic node
    task = None
    memory_context = None
    load_dotenv('.env.secret')
    for event in node:
        if event["type"] == "INPUT" and event['id'] in ['task','data']:
            task = event["value"][0].as_py()
            print('task  : ',task)
        if event["type"] == "INPUT" and event['id'] in ["memory_context"]:
            memory_context = load_node_result(event["value"][0].as_py())
            print('memory_context : ',memory_context)
        if task is not None and memory_context is not None:
            
            reasoner = ReasonerAgent(config_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/configs/config.yml',
                                llm_config_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/.env.secret')
            result = reasoner.run(task=task,memory_context=memory_context)
            print('reasoner_result : ',result)
            output_name = 'reasoner_result'
            node.send_output(output_name, pa.array([create_agent_output(agent_name=output_name, agent_result=result, dataflow_status=os.getenv('IS_DATAFLOW_END', False))]), event['metadata'])
            task,memory_context = None,None
if __name__ == "__main__":
    main()
    # reasoner = ReasonerAgent(config_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/configs/config.yml',
    #                             llm_config_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/.env.secret')
    # result = reasoner.run(task="Hello Agent",memory_context='jksahjdsakd')
    # print(result)
