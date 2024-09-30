import click

import time
import uuid
import subprocess
from mofa import agent_dir_path
import click
import sys
from mofa.utils.process.util import stop_process, stop_dora_dataflow, send_task_or_stop_process
from mofa.utils.variable.util import while_input


def agent_evaluation_cmd():
    agent_name = 'agent_fight'
    agent_path = agent_dir_path + f'/{agent_name}'
    agent_dataflow_path = agent_path + f'/{agent_name}_dataflow.yml'

    dora_up_process = subprocess.Popen(
        ['dora', 'up'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=agent_path,
    )
    time.sleep(1)

    dora_build_node = subprocess.Popen(
        ['dora', 'build', agent_dataflow_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=agent_path
    )

    time.sleep(3)
    stdout, stderr = dora_build_node.communicate()
    dataflow_name = str(uuid.uuid4()).replace('-','')
    if dora_build_node.returncode == 0:
        # 启动 dora_dataflow_process 进程并等待其启动
        dora_dataflow_process = subprocess.Popen(
            ['dora', 'start', agent_dataflow_path,'--name',dataflow_name],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=agent_path
        )

        time.sleep(2)

        task_input_process = subprocess.Popen(
            ['multiple-terminal-input'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=agent_path,
            bufsize=0,
            universal_newlines=True
        )

        try:
            while True:
                primary_data = while_input("Send primary data: ")
                if send_task_or_stop_process(task=primary_data,dora_dataflow_process=dora_dataflow_process,task_input_process=task_input_process,dataflow_name=dataflow_name) == False:
                    break
                secondary_task = while_input("Send secondary data: ")
                if send_task_or_stop_process(task=secondary_task,dora_dataflow_process=dora_dataflow_process,task_input_process=task_input_process,dataflow_name=dataflow_name) == False:
                    break
                generate_data_task = while_input("Send source task: ")
                if send_task_or_stop_process(task=generate_data_task,dora_dataflow_process=dora_dataflow_process,task_input_process=task_input_process,dataflow_name=dataflow_name) == False:
                    break
                while True:
                    output = task_input_process.stdout.readline()
                    if output:
                        print(output.strip().replace('Send You Task:', '').replace('Answer:', '').replace(
                            ':dataflow_status', ''), flush=True)
                        sys.stdout.flush()
                        if ":dataflow_status" in output:
                            break
                    else:
                        print('wait agent result')
        except KeyboardInterrupt:
            stop_process([dora_dataflow_process, task_input_process])
            stop_dora_dataflow(dataflow_name=dataflow_name)
        finally:
            stop_process([dora_dataflow_process, task_input_process])
            stop_dora_dataflow(dataflow_name=dataflow_name)
            click.echo("Main process terminated.")


def agent_evaluation_api(primary_data:str,second_data:str,comparison_data_task:str):
    agent_name = 'agent_evaluation'
    agent_path = agent_dir_path + f'/{agent_name}'
    agent_dataflow_path = agent_path + f'/{agent_name}_dataflow.yml'

    dora_up_process = subprocess.Popen(
        ['dora', 'up'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=agent_path,
    )
    time.sleep(1)

    dora_build_node = subprocess.Popen(
        ['dora', 'build', agent_dataflow_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=agent_path
    )

    time.sleep(3)
    stdout, stderr = dora_build_node.communicate()
    dataflow_name = str(uuid.uuid4()).replace('-','')
    if dora_build_node.returncode == 0:
        # 启动 dora_dataflow_process 进程并等待其启动
        dora_dataflow_process = subprocess.Popen(
            ['dora', 'start', agent_dataflow_path,'--name',dataflow_name],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=agent_path
        )

        time.sleep(2)

        task_input_process = subprocess.Popen(
            ['multiple-terminal-input'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=agent_path,
            bufsize=0,
            universal_newlines=True
        )


        if send_task_or_stop_process(task=primary_data,dora_dataflow_process=dora_dataflow_process,task_input_process=task_input_process,dataflow_name=dataflow_name) == False:
            return ''

        if send_task_or_stop_process(task=second_data,dora_dataflow_process=dora_dataflow_process,task_input_process=task_input_process,dataflow_name=dataflow_name) == False:
            return ''

        if send_task_or_stop_process(task=comparison_data_task,dora_dataflow_process=dora_dataflow_process,task_input_process=task_input_process,dataflow_name=dataflow_name) == False:
            return ''
        results = ''
        while True:
            output = task_input_process.stdout.readline()
            if output:
                results += output.strip().replace('Send You Task:', '').replace('Answer:', '').replace(
                    ':dataflow_status', '')
                print(output.strip().replace('Send You Task:', '').replace('Answer:', '').replace(
                    ':dataflow_status', ''), flush=True)
                sys.stdout.flush()
                if ":dataflow_status" in output:
                    stop_process([dora_dataflow_process, task_input_process])
                    stop_dora_dataflow(dataflow_name=dataflow_name)
                    break
            else:
                print('wait agent result')
        return results