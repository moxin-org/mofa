import json
import os
import attrs
import pyarrow as pa
from attrs import define, field
from typing import Any, Dict, Union
from mofa.kernel.utils.util import create_agent_output, load_node_result
from mofa.utils.files.read import read_yaml
import yaml
from dora import Node
from dotenv import load_dotenv
from pathlib import Path
@define
class MofaAgent():
    agent_name:str = field(default='mofa-agent')
    node:Any = field(default=None)
    agent_inputs:dict = field(factory=dict)
    description_file_path:Union[str,None] = field(default=Path(os.path.join(os.path.abspath(os.path.dirname(__file__)), )).parent / 'description.json')
    event:Any = field(factory=dict)
    def __attrs_post_init__(self):
        self.node = Node(self.agent_name)
        if not self.description_file_path.exists():
            raise FileNotFoundError(f"Description file not found at {self.description_file_path}")
        else:
             self.init_agent_inputs

    def _receive_event_input(self,event):
        if event["type"] == "INPUT":
            for agent_input in list(self.agent_inputs.keys()):
                if event['id'] == agent_input and self.agent_inputs[agent_input] is None:
                    try:
                        input_data = load_node_result(event["value"][0].as_py())
                    except Exception as e :
                        input_data = event["value"][0].as_py()
                    self.agent_inputs[agent_input] = input_data

    def recevice_parameters(self):
        for event in self.node:
            self._receive_event_input(event=event)
            self.event = event
            return self
    @property
    def init_agent_inputs(self):
        with open(self.description_file_path, 'r', encoding='utf-8') as f:
                description = json.load(f)
                self.agent_name = description['name']
                self.agent_inputs = {input_item["name"]: None for input_item in description["inputs"]}
    def send_output(self, agent_output_name: str, agent_result: Any, is_end_status=os.getenv('IS_DATAFLOW_END', True)):
        self.node.send_output(
            agent_output_name,
            pa.array([create_agent_output(
                agent_name=agent_output_name,
                agent_result=agent_result,
                dataflow_status=is_end_status
            )]),
            self.event['metadata']
        )
    @property
    def is_inputs_empty(self) -> bool:
        return all(value is None for value in self.agent_inputs.values())


@define
class BaseMofaAgent():
    """
    A base class for MOFA agents, providing configuration management,
    resource initialization, and a context manager interface.
    """

    config_path: Union[str, None] = field(default=None)
    config: Dict[str, Any] = field(init=False,factory=dict)
    llm_client: Any = field(init=False, default=None)
    llm_config_path: Union[str, None] = field(default='.env.secret')
    
    def __attrs_post_init__(self) -> None:
        """
        Automatically called by attrs after the object is instantiated.
        Loads the configuration, initializes the client, 
        and sets up additional resources.
        """
        if self.config_path is None:
            self.config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/configs/agent.yml'
        
    def init_llm_config(self,llm_config_path:str=None):
        if llm_config_path is None :
            llm_config_path = self.llm_config_path
        if Path(llm_config_path).exists():
            load_dotenv(llm_config_path)

    def load_config(self, config_path: str=None) -> Dict[str, Any]:
        """
        Load configuration from a YAML file.
        """
        if config_path is None:
            config_path = self.config_path
        return read_yaml(file_path = config_path)

    def send_output(self, node:Node,event,output_name: str, output_data: Any,output_step_name:str=None,is_end_dataflow:bool=True):
        if output_step_name is None:
            output_step_name = output_name
        node.send_output(output_name, pa.array([create_agent_output(agent_name=output_step_name, agent_result=output_data, dataflow_status=os.getenv('IS_DATAFLOW_END', is_end_dataflow))]), event['metadata'])
    
    def run(self,task:str=None,*args,**kwargs):
        pass
    
    def parse_agent_parameters(self,agent_input:Any):
        try:
            agent_input = load_node_result(agent_input)
        except:
            agent_input = agent_input
        return agent_input
    
    def create_llm_client(self,config:dict=None,*args,**kwargs):
        if config is None:
            config = self.config
        pass 
        
        