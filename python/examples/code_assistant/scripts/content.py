import argparse
import json
import os
from dora import Node
from mofa.kernel.utils.log import write_agent_log
from mofa.kernel.utils.util import load_agent_config, create_agent_output
from mofa.run.run_agent import run_dspy_agent, run_crewai_agent, run_dspy_or_crewai_agent
from mofa.utils.files.read import read_yaml
import pyarrow as pa
import os
import glob
from mofa.utils.files.dir import get_relative_path
from mofa.utils.log.agent import record_agent_prompt_log, record_agent_result_log
import tkinter as tk
from tkinter import messagebox
RUNNER_CI = True if os.getenv("CI") == "true" else False

def get_python_files(directory):
    # 获取当前目录中的所有 .py 文件
    python_files = glob.glob(os.path.join(directory, "*.py"))
    return python_files

def read_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
def main():


    # Handle dynamic nodes, ask for the name of the node in the dataflow, and the same values as the ENV variables.
    parser = argparse.ArgumentParser(description="Analysis Agent")

    parser.add_argument(
        "--name",
        type=str,
        required=False,
        help="The name of the node in the dataflow.",
        default="arrow-assert",
    )
    parser.add_argument(
        "--task",
        type=str,
        required=False,
        help="Tasks required for the Reasoner agent.",
        default="Paris Olympics",
    )

    args = parser.parse_args()
    task = os.getenv("TASK", args.task)

    node = Node()  # provide the name to connect to the dataflow if dynamic node

    # assert_data = ast.literal_eval(data)

    for event in node:
        if event["type"] == "INPUT" and event['id'] in ['task','data','reasoner_task']:
            task = event["value"][0].as_py()
            
            yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs',
                                               target_file_name='code_content_agent.yml')
            inputs = load_agent_config(yaml_file_path)
            current_directory = os.getcwd()  # 获取当前工作目录
            python_files = get_python_files(current_directory)  # 获取所有 .py 文件
            files_content = {os.path.basename(file): read_file_content(file) for file in python_files}
            files_content_str = json.dumps(files_content, ensure_ascii=False, indent=4)
            task = f"源代码为：{files_content_str}，用户问题为{task}"
            inputs['task'] = task
            root = tk.Tk()
            root.withdraw()  # 隐藏主窗口
            messagebox.showinfo("Analysis Information", f"path:{current_directory} Code: {files_content_str}")
            root.destroy()
            record_agent_prompt_log(agent_config=inputs, config_file_path=yaml_file_path, log_key_name='Agent Prompt',
                                    task=task)

            agent_result = run_dspy_or_crewai_agent(agent_config=inputs)
            results = {}
            record_agent_result_log(agent_config=inputs,
                                    agent_result={inputs.get('log_step_name', "Step_one"): agent_result})

            results['task'] = task
            results['result'] = agent_result
            print('agent_output:', results)
            node.send_output("code_content_result", pa.array([create_agent_output(step_name='code_analsys',
                                                                                output_data=agent_result,
                                                                                dataflow_status=os.getenv(
                                                                                    "IS_DATAFLOW_END",
                                                                                    True))]), event['metadata'])

if __name__ == "__main__":
    main()
