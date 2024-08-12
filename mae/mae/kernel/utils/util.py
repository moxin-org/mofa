import json

from crewai_tools import tool
import yaml

from mae.utils.files.read import read_yaml


def make_crewai_tool(func):
    tool.name = func.__name__
    return tool(func)

def load_agent_config(yaml_file:str):
    params = read_yaml(yaml_file)
    if 'AGENT' in params:
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