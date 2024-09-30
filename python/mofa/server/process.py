from pathlib import Path

# from mofa.agent_link.agent_template import agent_template_path

from backup.agent_link.merge_agents.merge_dataflow import MergeDataflow


from mofa.server.util import load_agent_dataflow, get_agent_template_dir_path
from mofa.utils.files.delete import delete_file
from mofa.utils.files.util import get_files_in_directory, get_all_files
from mofa.utils.files.write import write_dict_to_yml


def load_node_config(agent_name:str,node_id:str):
    agent_dataflow = load_agent_dataflow(agent_name=agent_name)
    merge_dataflow = MergeDataflow()
    node_data = merge_dataflow.get_node_id_data(dataflow=agent_dataflow,node_id=node_id)
    if node_data is None:
        return 'node id does not exist '
    else:
        return merge_dataflow.get_node_config(dataflow=agent_dataflow,node_id=node_id,search_directory=get_agent_template_dir_path())
# def upload_node_config(agent_name:str,node_id:str,node_config:dict):
#     dataflow_config_dir = agent_template_path + f'/{agent_name}/configs'
#     for file_path in get_all_files(dataflow_config_dir):
#         if node_id in Path(file_path).name:
#             delete_file(file_path=file_path)
#             write_dict_to_yml(data= node_config,file_path=file_path)
#             break
#     return 'upload '