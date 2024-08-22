import os
import pty
import time
from itertools import count
from pathlib import Path
import subprocess
import threading
import select

from mae import agent_dir_path
# from mae.utils.process.read import read_process_output
import click
import sys

from mae.utils.files.dir import get_subdirectories

@click.group()
def mae_cli_group():
    """Main CLI for MAE"""
    pass


@mae_cli_group.command()
def agent_list():
    """List all agents"""
    agent_names = get_subdirectories(agent_dir_path)
    click.echo(agent_names)
    return agent_names


@mae_cli_group.command()
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

    if dora_build_node.returncode == 0:
        # 启动 dora_dataflow_process 进程并等待其启动
        dora_dataflow_process = subprocess.Popen(
            ['dora', 'start', agent_dataflow_path],
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
            # text=True,
            cwd=agent_path,
            bufsize=0,
            universal_newlines=True
        )

        try:
            while True:
                # 用户输入任务
                task_input = input(">>>  ")
                if task_input.lower() in ["exit", "quit"]:
                    dora_dataflow_process.terminate()
                    task_input_process.terminate()
                    break

                if task_input_process.poll() is None:
                    task_input_process.stdin.write(task_input + '\n')
                    task_input_process.stdin.flush()
                else:
                    print("Process has already terminated. Cannot send input.")
                    break
                time.sleep(2)
                while True:
                    # ready, _, _ = select.select([task_input_process.stdout], [], [], 0.2)  # 1秒超时
                    # if ready:
                    output = task_input_process.stdout.readline()  # 使用 readline 逐行读取数据
                    if output:
                        print(output.strip().replace('Send You Task :', '').replace('Answer:', ''), flush=True)
                        sys.stdout.flush()
                        if ":dataflow_status" in output:
                            print("Agent End ")
                            break
                    else:
                        print('wait agent result')
        except KeyboardInterrupt:
            click.echo("Process interrupted by user.")
        finally:
            dora_dataflow_process.terminate()
            task_input_process.terminate()
            click.echo("Main process terminated.")
        #
        # try:
        #
        #     while True:
        #         task_input = input(">>>  ")
        #         if task_input.lower() in ["exit", "quit"]:
        #             dora_dataflow_process.terminate()
        #             task_input_process.terminate()
        #             break
        #         send_task_to_process(task_input_process, task_input)
        #
        #         ready, _, _ = select.select([task_input_process.stdout], [], [], 1)  # 1秒超时
        #         if ready:
        #             output = task_input_process.stdout.read(512)  # 使用 read 读取所有可用数据
        #             if output:
        #                 print(output.strip().replace('Send You Task :', '').replace('Answer:', ''), flush=True)
        #                 sys.stdout.flush()
        #
        #         # 在输出完成后，等待用户输入
        #
        #
        # except KeyboardInterrupt:
        #     click.echo("Process interrupted by user.")
        # finally:
        #     dora_dataflow_process.terminate()
        #     task_input_process.terminate()
        #     click.echo("Main process terminated.")



        # try:
        #
        #     while True:
        #         # 收集并处理所有输出
        #         output_complete = False
        #         while not output_complete:
        #             ready, _, _ = select.select([task_input_process.stdout], [], [], 1)  # 1秒超时
        #             if ready:
        #                 output = task_input_process.stdout.read(89340)  # 使用 read 读取所有可用数据
        #                 if output:
        #                     print(output.strip().replace('Send You Task :', '').replace('Answer:', ''), flush=True)
        #                     sys.stdout.flush()
        #                 else:
        #                     output_complete = True
        #             else:
        #                 output_complete = True
        #
        #         # 在输出完成后，等待用户输入
        #         task_input = input(">>>  ")
        #         if task_input.lower() in ["exit", "quit"]:
        #             dora_dataflow_process.terminate()
        #             task_input_process.terminate()
        #             break
        #         send_task_to_process(task_input_process, task_input)
        #
        # except KeyboardInterrupt:
        #     click.echo("Process interrupted by user.")
        # finally:
        #     dora_dataflow_process.terminate()
        #     task_input_process.terminate()
        #     click.echo("Main process terminated.")

        # try:
        #     while True:
        #         if task_count == 0:
        #             task_input = input(">>>  ")
        #             if task_input.lower() in ["exit", "quit"]:
        #                 dora_dataflow_process.terminate()
        #                 task_input_process.terminate()
        #                 break
        #             send_task_to_process(task_input_process, task_input=task_input)
        #             task_count += 1
        #
        #         # 使用 select 来检查 stdout 是否可读
        #         ready, _, _ = select.select([task_input_process.stdout], [], [], 1)  # 1秒超时
        #         if ready:
        #             output = task_input_process.stdout.readline()
        #
        #             if output:
        #                 click.echo("Received: ", nl=False)
        #                 sys.stdout.flush()
        #                 # print(outpt.strip().replace('Send You Task :', '').replace('Answer:', ''), flush=True)
        #
        #                 click.echo(output.strip().replace('Send You Task :', '').replace('Answer:', ''))
        #                 sys.stdout.flush()
        #
        #                 # 检查输出中是否包含 "Send You Task :"
        #                 if "Send You Task :" in output:
        #
        #                     task_input = input(">>>  ")
        #                     if task_input.lower() in ["exit", "quit"]:
        #                         dora_dataflow_process.terminate()
        #                         task_input_process.terminate()
        #                         break
        #                     send_task_to_process(task_input_process, task_input=task_input)
        #                     task_count += 1
        #                     task_input_process.stdout.flush()
        #             else:
        #                 # 如果没有更多输出，退出循环
        #                 break
        #         else:
        #             # 如果没有可读的输出,可以选择打印调试信息
        #             click.echo('Waiting for output...')
        #             sys.stdout.flush()
        #             time.sleep(0.5)  # 添加短暂的等待,避免过于频繁的输出
        # except KeyboardInterrupt:
        #     sys.stdout.flush()
        #     click.echo("Process interrupted by user.")
        # finally:
        #     sys.stdout.flush()
        #     dora_dataflow_process.terminate()
        #     task_input_process.terminate()
        #     click.echo("Main process terminated.")


if __name__ == '__main__':
    mae_cli_group()