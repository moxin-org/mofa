from crewai_tools import tool
import yaml

from mae.utils.files.read import read_yaml


def make_crewai_tool(func):
    tool.name = func.__name__
    return tool(func)

def load_agent_config(yaml_file:str):
    params = read_yaml(yaml_file)
    if 'AGENT' in params:
        model_config, agent_config, env_config, rag_config,log_config,web_config = params['MODEL'], params['AGENT'], params['ENV'], params.get('MAE_RAG', None),params.get('LOG',None),params.get('WEB',None)
        config = {}
        for i in [model_config, agent_config, env_config,rag_config,log_config,web_config]:
            if i is not None:
                config.update(i)
        config = {k.lower(): v for k, v in config.items()}
    else:
        config = params
    return config