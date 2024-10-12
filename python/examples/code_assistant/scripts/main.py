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
from mofa.utils.files.dir import get_relative_path
from mofa.utils.log.agent import record_agent_prompt_log, record_agent_result_log
import tkinter as tk
from tkinter import messagebox

RUNNER_CI = True if os.getenv("CI") == "true" else False


def main():
    inputs = {}
    agent_result = {}
    results = {}
    # Handle dynamic nodes, ask for the name of the node in the dataflow, and the same values as the ENV variables.
    parser = argparse.ArgumentParser(description="Reasoner Agent")

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
        if event["type"] == "INPUT":
            if event['id'] in ['output']:
                code = event["value"][0].as_py()
                root = tk.Tk()
                root.withdraw()  # 隐藏主窗口
                messagebox.showinfo("Analysis Information", f"Code: {code}")
                root.destroy()
                task2 = f"请根据相关代码文件完成{task}，相关代码文件如下（格式为 文件名：代码内容： ）：{code}"
                record_agent_prompt_log(agent_config=inputs, config_file_path=yaml_file_path, log_key_name='Agent Prompt',
                                        task=task2)

                agent_result = run_dspy_or_crewai_agent(agent_config=inputs)
                
                record_agent_result_log(agent_config=inputs,
                                        agent_result={inputs.get('log_step_name', "Step_one"): agent_result})

                results['task'] = task2
                results['result'] = agent_result
                print('agent_output:', results)
                node.send_output("code_assistant_result", pa.array([create_agent_output(step_name='code_assistant',
                                                                                    output_data=agent_result,
                                                                                    dataflow_status=os.getenv(
                                                                                        "IS_DATAFLOW_END",
                                                                                        True))]), event['metadata']) 

            elif event['id'] in ['task','data','reasoner_task']:
                task = event["value"][0].as_py()
                yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs',
                                                target_file_name='code_assistant_agent.yml')
                inputs = load_agent_config(yaml_file_path)
                inputs['task'] = task
                # 弹窗显示 task 的内容
                root = tk.Tk()
                root.withdraw()  # 隐藏主窗口
                messagebox.showinfo("Task Information", f"Task: {task}")
                root.destroy()
                #print(inputs)
                node.send_output("get_code", pa.array([create_agent_output(step_name='code_assistant',
                                                                                    output_data=agent_result,
                                                                                    dataflow_status=os.getenv(
                                                                                        "IS_DATAFLOW_END",
                                                                                        True))]), event['metadata'])
if __name__ == "__main__":
    main()
