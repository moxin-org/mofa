import os
from pathlib import Path
from typing import List

from mofa.utils.files.read import read_yaml
from mofa.utils.files.util import get_files_in_directory


def get_agent_template_dir_path(agent_template_dir:str=None)->str:
    if agent_template_dir is None:
        agent_template_dir = os.path.join(os.path.dirname(__file__), '..', 'agent_link', 'agent_template')
    return agent_template_dir
def get_agent_list(agent_template_dir:str=None)->list[str]:
    if agent_template_dir is None:
        agent_template_dir = get_agent_template_dir_path()
    try:
        # 仅获取目录名称
        agent_list = [d for d in os.listdir(agent_template_dir) if os.path.isdir(os.path.join(agent_template_dir, d))]
        return agent_list
    except Exception as e:
        return str(e)






def load_agent_dataflow(agent_name:str,agent_template_dir:str=None)->dict:
    if agent_template_dir is None:
        agent_template_dir = get_agent_template_dir_path()
    if agent_name in get_agent_list(agent_template_dir=agent_template_dir):
        agent_dataflow_dir_path = agent_template_dir + '/' + agent_name
        local_files = get_files_in_directory(directory=agent_dataflow_dir_path)
        for file in local_files:
            if agent_name in Path(file).name:
                data = read_yaml(file_path=file)
                return data
        else:
            return {'error': 'agent_dataflow_file_path not exists'}
