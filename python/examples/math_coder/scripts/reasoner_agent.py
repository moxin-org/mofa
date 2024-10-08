import json
import os
import subprocess
from dora import Node, DoraStatus
import pyarrow as pa
from mofa.kernel.utils.util import load_agent_config, load_dora_inputs_and_task, create_agent_output
from mofa.run.run_agent import run_dspy_agent, run_crewai_agent, run_dspy_or_crewai_agent
from mofa.utils.files.dir import get_relative_path
from mofa.utils.log.agent import record_agent_result_log


def execute_python_code(code):
    # 创建一个临时文件来保存代码
    with open('temp_script.py', 'w') as f:
        f.write(code)
    
    # 使用 subprocess 执行临时文件
    result = subprocess.run(
        ['python', 'temp_script.py'],
        capture_output=True,
        text=True
    )
    
    # 获取标准输出和标准错误输出
    stdout = result.stdout
    stderr = result.stderr
    
    return stdout, stderr


class Operator:
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            agent_inputs = ['data','task']
            if dora_event["id"] in agent_inputs:
                task = dora_event["value"][0].as_py()
                yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='reasoner_agent.yml')
                inputs = load_agent_config(yaml_file_path)
                inputs["task"] = task
                agent_result = run_dspy_or_crewai_agent(agent_config=inputs)
                agent_result_str = str(agent_result)

                code_strs = agent_result_str.strip().split('```')
                code_strs = [code_str.strip() for code_str in code_strs]
                code_strs = [code_str[7:] for code_str in code_strs if code_str[:7] == 'python\n']

                record_agent_result_log(agent_config=inputs,
                                        agent_result={
                                            "1, "+ inputs.get('log_step_name', "Step_one"): {task:agent_result}})
                # send_output("reasoner_results", pa.array([create_agent_output(step_name='keyword_results', output_data='\n'.join([f'\nCode {index+1}:\n\n{code_str}\n' for index, code_str in enumerate(code_strs)])
                #                                                               ,dataflow_status=os.getenv('IS_DATAFLOW_END',True))]),dora_event['metadata'])
                
                code_res = [execute_python_code(code_str) for code_str in code_strs]

                send_output("reasoner_results", pa.array([create_agent_output(step_name='keyword_results', output_data=agent_result_str + '\n'.join([f'\n{stdout}\n{stderr}' for index, (stdout, stderr) in enumerate(code_res)])
                                                                              ,dataflow_status=os.getenv('IS_DATAFLOW_END',True))]),dora_event['metadata'])
                print('reasoner_results:', agent_result)

        return DoraStatus.CONTINUE