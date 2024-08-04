from pathlib import Path

from mae.agent_link.merge_agents.merge_dataflow import MergeDataflow
from mae.server.util import load_agent_dataflow, get_agent_template_dir_path


def load_node_config(agent_name:str,node_id:str):
    agent_dataflow = load_agent_dataflow(agent_name=agent_name)
    merge_dataflow = MergeDataflow()
    node_data = merge_dataflow.get_node_id_data(dataflow=agent_dataflow,node_id=node_id)
    if node_data is None:
        return 'node id does not exis '
    else:
        return merge_dataflow.get_node_config(dataflow=agent_dataflow,node_id=node_id,search_directory=get_agent_template_dir_path())
