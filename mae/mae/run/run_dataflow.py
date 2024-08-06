import subprocess
import time
from mae.agent_link.merge_agents.merge_dataflow import MergeDataflow
from mae.utils.files.dir import remove_dir
from mae.utils.files.read import read_yaml, read_text
from mae.utils.files.util import get_all_files, find_file
def load_dataflow_output(work_dir:str,dataflow_file_path:str,is_load_node_log:bool=True):
    if '.yml' not in dataflow_file_path:
        dataflow_file_path += '.yml'
    dataflow = read_yaml(f"{work_dir}/{dataflow_file_path}")
    merge_dataflow = MergeDataflow()
    log_data = {}
    if is_load_node_log:
        nodes_ids = merge_dataflow.list_node_ids(dataflow=dataflow)
    else:
        nodes_ids = [merge_dataflow.list_node_ids(dataflow=dataflow)[-1]]
    for node_id in nodes_ids:
        log_file = find_file(target_filename=f"log_{node_id}.txt", search_directory=work_dir+'/out')
        if log_file is not None:
            log_file_data = read_text(file_path=log_file,is_loda_lines=True)
            log_data[node_id] = log_file_data[-1]
    return log_data

def run_dora_dataflow(work_dir:str,dataflow_file_path:str,task_input:str,dataflow_name:str='agents',is_load_node_log:bool=True):
    remove_dir(dir_path=work_dir+'/out')
    # 定义工作目录
    if '.yml' not in dataflow_file_path:
        dataflow_file_path += '.yml'
    dataflow = read_yaml(f"{work_dir}/{dataflow_file_path}")
    merge_dataflow = MergeDataflow()
    dynamic_node_ids = merge_dataflow.get_dataflow_dynamic_node_ids(dataflow=dataflow)
    task_input_node,task_input_path = dynamic_node_ids[0],''
    for py_file_path in get_all_files(dir_path=work_dir+'/scripts') :
        if 'task_input'  in py_file_path:
            with open(py_file_path,'r',encoding='utf-8') as file:
                context = file.read()
                if f'Node("{task_input_node}")' in context:
                    task_input_path = py_file_path
                    break

    if task_input_path  == '':
        raise RuntimeError('No dynamic files required for Dora Dataflow were found.')

    dora_process = subprocess.Popen(
        ['dora', 'start', dataflow_file_path, '--name',dataflow_name],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=work_dir
    )

    time.sleep(1)

    print(work_dir + '/scripts' )
    task_input_process = subprocess.Popen(
        ['python3', task_input_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=work_dir + '/scripts'
    )

    task_input_process.stdin.write(task_input + '\n')
    task_input_process.stdin.flush()


    while True:
        output = dora_process.stdout.readline()
        if output == '' and dora_process.poll() is not None:
            break
        if output:
            print(output.strip())
    return load_dataflow_output(work_dir=work_dir,dataflow_file_path=dataflow_file_path,is_load_node_log=is_load_node_log)


# output_params = f"{task_input_node}/{merge_dataflow.get_node_id_outputs(dataflow=dataflow,node_id=task_input_node)[0]}"
#
# for node_id in merge_dataflow.list_node_ids(dataflow=dataflow):
#     if node_id not in  dynamic_node_ids:
#         node_inputs = merge_dataflow.get_node_inputs(dataflow=dataflow,node_id=node_id)
#         for k ,v in node_inputs.items():
#             if v == output_params:
#                 task_input_node_data = merge_dataflow.get_node_id_data(dataflow=dataflow,node_id=node_id)
#                 task_input_path = work_dir + task_input_node_data['operator'].get('python')[1:]


# work_dir = '/Users/chenzi/project/zcbc/Moxin-App-Engine/mae/examples/generate'
# dataflow_file_path = 'web_search_dataflow.yml'
# input_value = "Paris Olympics\n"
# log_data = run_dora_dataflow(work_dir=work_dir,dataflow_file_path=dataflow_file_path,is_load_node_log=False,task_input=input_value)
# print(log_data)
