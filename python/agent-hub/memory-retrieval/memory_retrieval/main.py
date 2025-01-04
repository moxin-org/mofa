import argparse
import json
import os
from mem0 import Memory

from typing import Any, Dict
from dora import Node
from mofa.agent_build.base.base_agent import BaseMofaAgent
from mofa.kernel.utils.util import create_agent_output
from mofa.utils.files.read import read_yaml
import pyarrow as pa
RUNNER_CI = True if os.getenv("CI") == "true" else False

class MemoryRetrievalAgent(BaseMofaAgent):
    def load_config(self, config_path: str = None) -> Dict[str, Any]:
        if config_path is None:
            config_path = self.config_path
        return read_yaml(file_path=config_path)['agent']['llm']
    def load_user_id(self,config_path:str=None):
        if config_path is None:
            config_path = self.config_path
        return read_yaml(file_path=config_path)['agent']['user_id']
    def create_llm_client(self,config:dict=None,*args,**kwargs):
        self.init_llm_config()
        os.environ["OPENAI_API_KEY"] = os.environ.get('LLM_API_KEY')
        if os.environ.get('LLM_API_URL',None) is not None:
            os.environ["OPENAI_API_BASE"] = os.environ.get('LLM_API_URL')
        mem0_config = self.load_config()
        m = Memory.from_config(mem0_config)
        self.llm_client = m
        return self
    def get_mem0_search_text(self,memory_datas):
        try:
            results = list(set([memory_data.get("memory") for memory_data in memory_datas]))
        except Exception as e :
            results = memory_datas.get("results")
        return results
    def run(self, task:str=None,*args, **kwargs):
        mem0_config = self.load_config()
        self.create_llm_client(mem0_config)
        user_id = self.load_user_id()
        memory_result = self.llm_client.search(task, user_id=user_id)
        results = self.get_mem0_search_text(memory_datas=memory_result)
        return results

def main():

    # Handle dynamic nodes, ask for the name of the node in the dataflow, and the same values as the ENV variables.
    parser = argparse.ArgumentParser(description="Mem0 Agent")

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
            memmory = MemoryRetrievalAgent(config_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/configs/config.yml',
                                llm_config_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/.env.secret')
            result = memmory.run(task=task)
            output_name = 'memory_retrieval_result'
            node.send_output(output_name, pa.array([create_agent_output(agent_name=output_name, agent_result=result, dataflow_status=os.getenv('IS_DATAFLOW_END', False))]), event['metadata'])
        # event = node.next(timeout=200)
if __name__ == "__main__":
    main()
    # mem0 = MemoryRetrievalAgent(config_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/configs/config.yml',
    #                             llm_config_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/.env.secret')
    # result = mem0.run(task='How to use the mem0-ai package in Python? ')
    # print(result)
