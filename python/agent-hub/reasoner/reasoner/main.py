import argparse
import json
import os
from mem0 import Memory

from typing import Any, Dict
from dora import Node
from mofa.agent_build.base.base_agent import BaseMofaAgent
from mofa.kernel.utils.util import create_agent_output
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
        config = self.load_config()
        config['task'] = task
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

    args = parser.parse_args()
    task = os.getenv("TASK", args.task)

    node = Node(
        args.name
    )  # provide the name to connect to the dataflow if dynamic node

    # assert_data = ast.literal_eval(data)
    for event in node:
 
        if event["type"] == "INPUT" and event['id'] in ['task','data']:
            task = event["value"][0].as_py()
            reasoner = ReasonerAgent(config_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/configs/config.yml',
                                llm_config_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/.env.secret')
            result = reasoner.run(task=task)
            # memmory.send_output(node=node,output_name='memeory_retrieval_result',output_data=result,is_end_dataflow=os.getenv('IS_DATAFLOW_END',True),
            #                     event=event,)
            print('reasoner_result : ',result)
            output_name = 'reasoner_result'
            node.send_output(output_name, pa.array([create_agent_output(step_name=output_name, output_data=result,dataflow_status=os.getenv('IS_DATAFLOW_END',True))]), event['metadata'])
        event = node.next(timeout=200)
if __name__ == "__main__":
    main()
    # reasoner = ReasonerAgent(config_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/configs/config.yml',
    #                             llm_config_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/.env.secret')
    # result = reasoner.run(task="Hello Agent")
    # print(result)
