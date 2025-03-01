import copy
import json
import os
from functools import wraps
import traceback
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
class MofaAgent:
    agent_name:str = field(default='mofa-agent')
    node:Any = field(default=None)
    agent_inputs:dict = field(factory=dict)
    event:Any = field(factory=dict)
    event_time_out:int = field(default=20)
    def __attrs_post_init__(self):
        self.node = Node(self.agent_name)

    def _parse_event_value(self, event):
        try:
            return load_node_result(event["value"][0].as_py())
        except Exception:
            return event["value"][0].as_py()

    def _receive_event_input(self, event, parameter_names:Union[str,dict]):
        if event["type"] == "INPUT":
            if isinstance(parameter_names,str):

                if event['id'] == parameter_names :
                    input_data = self._parse_event_value(event=event)
                    return input_data
            elif isinstance(parameter_names,dict):
                data = copy.deepcopy(parameter_names)
                if event['id'] in list(data.keys()) :
                    data[event['id']] = self._parse_event_value(event=event)
                    return data
                else:
                    return data
    def receive_parameter(self,parameter_name:str):
        for event in self.node:
            input_data = self._receive_event_input(event=event, parameter_names=parameter_name)
            if input_data is not None:
                self.event = event
                return input_data
            else:
                continue
            # self.node.next(self.event_time_out)

    def receive_parameters(self,parameter_names:list)->dict:
        parameter_data = {}
        if len(parameter_names) > 0:
            parameter_data = {key: None for key in parameter_names}
        for event in self.node:

            parameter_data = self._receive_event_input(event=event,parameter_names=parameter_data)
            self.event = event
            # self.node.next(self.event_time_out)
            is_parameter_data_status = all(value is not None for value in parameter_data.values())
            if is_parameter_data_status :
                break
        return parameter_data
            
    def send_output(self, agent_output_name: str, agent_result: Any, is_end_status=os.getenv('IS_DATAFLOW_END', True)):
        if is_end_status == 'true' or is_end_status == 'True':
            is_end_status = True
        self.node.send_output(
            agent_output_name,
            pa.array([create_agent_output(
                agent_name=agent_output_name,
                agent_result=agent_result,
                dataflow_status=is_end_status
            )]),
            self.event['metadata']
        )


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


def run_agent(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        while True:
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(f"Error occurred: {e}")
                traceback.print_exc()
    return wrapper
