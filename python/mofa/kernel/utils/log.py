
from mofa.utils.files.read import read_yaml, read_text
from mofa.utils.files.util import find_file
from mofa.utils.files.write import write_or_append_to_md_file
from typing import Optional

def write_agent_log(log_file_path:str=None,log_type:str='md',data:dict=None):
    if log_file_path is not None:
        if log_type == 'markdown' or log_type == 'md':
            write_or_append_to_md_file(data= data,file_path=log_file_path)




def extract_agent_output(file_path: str, agent_marker: str='agent_output:') -> Optional[str]:
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        agent_output = ""
        start_collecting = False

        for line in lines:
            if agent_marker in line:
                # Extract content after the marker
                agent_output = line.split(agent_marker, 1)[1].strip()
                start_collecting = True
            elif start_collecting:
                # Collect subsequent lines if any
                agent_output += "\n" + line.strip()

        return agent_output if agent_output else None

    except FileNotFoundError:
        return "The file was not found."
    except Exception as e:
        return f"An error occurred: {e}"


# def load_dataflow_log(work_dir:str, agent_name:str, is_load_node_log:bool=True):
#     agent_dataflow_file_path = work_dir + f'/{agent_name}_dataflow.yml'
#     dataflow = read_yaml(agent_dataflow_file_path)
#     merge_dataflow = MergeDataflow()
#     log_data_list = []
#
#     if is_load_node_log:
#         nodes_ids = merge_dataflow.list_node_ids(dataflow=dataflow)
#     else:
#         nodes_ids = [merge_dataflow.list_node_ids(dataflow=dataflow)[-1]]
#     for node_id in nodes_ids:
#         log_data = {}
#         log_file = find_file(target_filename=f"log_{node_id}.txt", search_directory=work_dir+'/out')
#         if log_file  is not None and 'output' not in log_file:
#             log_data[node_id] = extract_agent_output(file_path=log_file)
#             log_data_list.append(log_data)
#     return log_data_list
