import subprocess
import time
from pathlib import Path
import subprocess
import threading
import click

from mae import agent_dir_path, cli_dir_path
from mae.server.server import run_agent
from mae.utils.process.read import read_process_output


@click.group()
def mae_cli_group():
    """Main CLI for MAE"""
    pass

@mae_cli_group.command()
def agent_list():
    """List all agents"""
    agent_names = [f.name.replace('.yml', '') for f in Path(agent_dir_path).iterdir() if f.is_file() and '.yml' in f.name]
    click.echo(agent_names)
    return agent_names
@mae_cli_group.command()
@click.option('--agent-name', default='reasoner', help='agent name')
# @click.option('--task', default='Paris Olympics', help='agent task ')
def run(agent_name:str):
    if '.yml' not in  agent_name: agent_name = agent_name + '.yml'


    dora_up_process =  subprocess.Popen(
        # conda_cmd_list + ['dora', 'up'] if is_conda_run else ['dora', 'up'],
        ['dora', 'up'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=agent_dir_path,
    )
    time.sleep(1)


    dora_build_node =  subprocess.Popen(
        ['dora', 'build',agent_name],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=agent_dir_path
    )

    time.sleep(3)
    stdout, stderr = dora_build_node.communicate()

    if dora_build_node.returncode == 0:
        dora_dataflow_process = subprocess.Popen(
            ['dora', 'start', agent_name,],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=agent_dir_path
        )
        time.sleep(1)
        task_input_process = subprocess.Popen(
                ['terminal-input'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=agent_dir_path
            )
        output_thread = threading.Thread(target=read_process_output, args=(task_input_process,))
        output_thread.start()
        try:
            while True:
                task_input = input(">>>")
                task_input_process.stdin.write(task_input + '\n')
                task_input_process.stdin.flush()

                if task_input.lower() in ["exit", "quit"]:
                    break

        except KeyboardInterrupt:
            click.echo("Process interrupted by user.")
        finally:
            task_input_process.terminate()
            output_thread.join()

            click.echo("Main process terminated.")
    dora_up_process =  subprocess.Popen(
        # conda_cmd_list + ['dora', 'up'] if is_conda_run else ['dora', 'up'],
        ['dora', 'up'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=agent_dir_path,
    )
    time.sleep(1)


    dora_build_node =  subprocess.Popen(
        ['dora', 'build',agent_name],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=agent_dir_path
    )

    time.sleep(3)
    stdout, stderr = dora_build_node.communicate()

    if dora_build_node.returncode == 0:
        dora_dataflow_process = subprocess.Popen(
            ['dora', 'start', agent_name,],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=agent_dir_path
        )
        time.sleep(1)
        task_input_process = subprocess.Popen(
                ['terminal-input'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=agent_dir_path
            )
        output_thread = threading.Thread(target=read_process_output, args=(task_input_process,))
        output_thread.start()
        try:
            # 持续输入命令
            while True:
                task_input = input("Enter your Task: ")  # 或者从其他地方获取输入
                task_input_process.stdin.write(task_input + '\n')
                task_input_process.stdin.flush()

                if task_input.lower() in ["exit", "quit"]:
                    break

        except KeyboardInterrupt:
            click.echo("Process interrupted by user.")
        finally:
            task_input_process.terminate()
            output_thread.join()  # 确保输出线程结束

            click.echo("Main process terminated.")

if __name__ == '__main__':
    mae_cli_group()