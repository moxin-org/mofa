import subprocess
import time
from mae.agent_link.merge_agents.merge_dataflow import MergeDataflow
from mae.kernel.utils.log import load_dataflow_log
from mae.utils.files.dir import remove_dir
from mae.utils.files.read import read_yaml
from mae.utils.files.util import get_all_files


def run_dora_dataflow(work_dir:str, agent_name:str, task_input:str, dataflow_name:str= 'agents', is_load_node_log:bool=True):
    remove_dir(dir_path=work_dir+f'/{agent_name}/out')
    work_dir += f'/{agent_name}'
    agent_data_dataflow_file_path = agent_name + '_dataflow'
    dataflow = read_yaml(f"{work_dir}/{agent_data_dataflow_file_path}.yml")
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
        ['dora', 'start', agent_name+'_dataflow.yml', '--name', dataflow_name],
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
    return load_dataflow_log(work_dir=work_dir, agent_name=agent_name, is_load_node_log=is_load_node_log)


