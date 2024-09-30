import time
import uuid
import subprocess
from mofa import agent_dir_path

import click
import sys
from mofa.run.agent_evealution import agent_evaluation_cmd
from mofa.utils.files.dir import get_subdirectories
from mofa.utils.process.util import stop_process, stop_dora_dataflow


@click.group()
def mofa_cli_group():
    """Main CLI for MAE"""
    pass


@mofa_cli_group.command()
def agent_list():
    """List all agents"""
    print("agent_dir_path ",agent_dir_path)
    agent_names = get_subdirectories(agent_dir_path)
    click.echo(agent_names)
    return agent_names

@mofa_cli_group.command()
def evaluation():
    """
    Score and compare the results of agents
    """
    agent_evaluation_cmd()

@mofa_cli_group.command()
@click.option('--agent-name', default='reasoner', help='agent name')
def run(agent_name: str = 'reasoner'):
    agent_path = agent_dir_path + f'/{agent_name}'
    agent_dataflow_path = agent_path + f'/{agent_name}_dataflow.yml'

    dora_up_process = subprocess.Popen(
        # conda_cmd_list + ['dora', 'up'] if is_conda_run else ['dora', 'up'],
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
            ['terminal-input'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=agent_path,
            bufsize=0,
            universal_newlines=True
        )

        try:
            while True:
                task_input = input(">>>  ")
                if task_input.lower() in ["exit", "quit"]:
                    stop_process([dora_dataflow_process,task_input_process])
                    stop_dora_dataflow(dataflow_name=dataflow_name)
                    break

                if task_input_process.poll() is None:
                    task_input_process.stdin.write(task_input + '\n')
                    task_input_process.stdin.flush()
                else:
                    print("Process has already terminated. Cannot send input.")
                    break
                time.sleep(2)
                while True:
                    # ready, _, _ = select.select([task_input_process.stdout], [], [], 0.2)
                    # if ready:
                    output = task_input_process.stdout.readline()
                    if output:
                        print(output.strip().replace('Send You Task :', '').replace('Answer:', '').replace(':dataflow_status',''), flush=True)
                        sys.stdout.flush()
                        if ":dataflow_status" in output:
                            break
                    else:
                        print('wait agent result')
        except KeyboardInterrupt:
            stop_process([dora_dataflow_process, task_input_process])
            stop_dora_dataflow(dataflow_name=dataflow_name)
        finally:
            stop_process([dora_dataflow_process,task_input_process])
            stop_dora_dataflow(dataflow_name=dataflow_name)
            click.echo("Main process terminated.")

if __name__ == '__main__':
    mofa_cli_group()