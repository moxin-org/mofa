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

