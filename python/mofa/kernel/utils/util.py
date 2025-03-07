import json
import os
from typing import Union

from crewai_tools import tool
from mofa.utils.files.read import read_yaml


def make_crewai_tool(func):
    tool.name = func.__name__
    return tool(func)

def load_agent_config(yaml_file:str,is_expand:bool=False):
    params = read_yaml(yaml_file)
    if 'AGENT' in params or is_expand == True:
        config = {}
        for key in params.keys():
            if params.get(key,None) is not None:
                config.update(params.get(key,None))
        config = {k.lower(): v for k, v in config.items()}
    else:
        config = params
    return config


def load_dora_inputs_and_task(dora_event):
    task_inputs = json.loads(dora_event["value"][0].as_py())
    dora_result = json.loads(dora_event["value"][0].as_py())
    if isinstance(task_inputs, dict):
        task = task_inputs.get('task', None)
    else:
        task = task_inputs
    return task_inputs,dora_result,task

def create_agent_output(agent_name:str, agent_result:Union[str,dict,list], dataflow_status:bool=os.getenv(
                                                                                    "IS_DATAFLOW_END",                                                              True)):
    if isinstance(agent_result, dict) or isinstance(agent_result, list):
        agent_result = json.dumps(agent_result, ensure_ascii=False)
    return json.dumps({'step_name':agent_name, 'node_results':agent_result, 'dataflow_status':dataflow_status}, ensure_ascii=False)

def load_node_result(node_data):
    return json.loads(node_data).get('node_results')