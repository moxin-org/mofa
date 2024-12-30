import argparse
import json
import os
from pathlib import Path

from attrs import define, field
from typing import Any, Dict, Union
from dora import Node
from mofa.agent_build.base.base_agent import BaseMofaAgent
from mofa.kernel.utils.util import create_agent_output, load_node_result
from mofa.utils.files.read import read_yaml
import pyarrow as pa
import json
from letta import create_client, LLMConfig, EmbeddingConfig
from letta.schemas.memory import ChatMemory
from mofa.utils.files.write import copy_file

RUNNER_CI = True if os.getenv("CI") == "true" else False

class LettaAgent(BaseMofaAgent):
    agent_state_id:Union[str,None] =  field(default=None)
    agent_state:Any =  field(factory=dict)
    def __attrs_post_init__(self) -> None:
        copy_file(input_file=self.llm_config_path,output_file=str(Path(self.llm_config_path).parent / '.env'),overwrite=True)
        copy_file(input_file=self.llm_config_path,output_file=str(Path(self.llm_config_path).parent.parent / '.env'),overwrite=True)
        self.create_llm_client()
        self.agent_state_id = self.agent_state.id
    @property
    def search_memory(self):
        memory_data = self.llm_client.get_archival_memory(self.agent_state_id)
        if len(memory_data) >0:
            memory_data  = [i.text for i in memory_data]
        return memory_data
    def add_memory(self, data:str):
        self.llm_client.insert_archival_memory(self.agent_state_id, data)

    def create_llm_client(self,config:dict=None,*args,**kwargs):
        self.init_llm_config()
        llm_config = self.load_config()
        os.environ["OPENAI_API_KEY"] = os.environ.get('LLM_API_KEY')
        self.llm_client = create_client()
        self.agent_state =  self.llm_client.create_agent(
        memory=ChatMemory(
            persona=llm_config.get('agent').get('memory').get('persona','You are a helpful assistant that remembers past interactions'),
            human=llm_config.get('agent').get('memory').get('persona','My name is mofa')
        ),
        llm_config=LLMConfig.default_config(model_name=os.environ.get('LLM_MODEL_NAME')),
        embedding_config=EmbeddingConfig.default_config(model_name=os.environ.get('LLM_EMBEDDER_MODEL_NAME'))
    )
    def send_message_to_agent(self,prompt:str):
        response = self.llm_client.send_message(
            agent_id=self.agent_state_id,
            role="user",
            message=prompt
        )
        for message in response.messages:
            if message.message_type == 'tool_call_message':

                tool_call_args = json.loads(message.tool_call.arguments)
                user_response = tool_call_args.get('message')
                return user_response
    def record_memory(self,data:str):
        self.llm_client.insert_archival_memory(self.agent_state_id, data)
    def run(self,task:str=None,*args,**kwargs):
        memory_data = self.search_memory
        if len(memory_data) >0:
            memory_data = 'These are the context memories. : ' + '\n'.join(memory_data)
        else: memory_data = ''
        user_message = f"User task: {task}.  memory data :{memory_data}"
        agent_result = self.send_message_to_agent(prompt=user_message)
        self.record_memory(data='task: '+task + ' agent result: ' + agent_result)
        return agent_result

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
    task,agent_result  = None,None
    node = Node(
        args.name
    )  # provide the name to connect to the dataflow if dynamic node

    # assert_data = ast.literal_eval(data)
    agent = agent = LettaAgent(config_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/configs/config.yml',
                       llm_config_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/.env.secret')
    for event in node:

        if event["type"] == "INPUT" and event['id'] in ['task','data']:
            task = event["value"][0].as_py()

            result = agent.run(task=task)
            output_name = 'letta_agent_result'
            node.send_output(output_name, pa.array([create_agent_output(step_name=output_name, output_data=result,dataflow_status=os.getenv('IS_DATAFLOW_END',True))]), event['metadata'])

if __name__ == "__main__":
    # agent = LettaAgent(config_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/configs/config.yml',
    #                    llm_config_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/.env.secret')
    # result = agent.run(task='Paris Olympics')
    # print(result)
    main()
