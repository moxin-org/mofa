import argparse
import json
import os
from dora import Node
from mae.kernel.utils.log import write_agent_log
from mae.kernel.utils.util import load_agent_config
from mae.run.run import run_dspy_agent, run_crewai_agent
from mae.utils.files.read import read_yaml
import pyarrow as pa
import os
# RUNNER_CI = True if os.getenv("CI") == "true" else False
#
# evaluation_data = {'task': '第二第二次世界大战', 'result': 'Answer: 第二次世界大战是从1939年到1945年间发生的一场全球性战争，主要涉及大多数国家，分为两个主要对立阵营：同盟国和轴心国。战争的起因包括德国的扩张主义政策、意大利和日本的侵略行为，以及国际社会对这些行为的反应。战争的关键事件包括1941年的珍珠港事件、1944年的诺曼底登陆和1945年对日本的原子弹轰炸。最终，同盟国在1945年取得胜利，导致了轴心国的崩溃和战后国际秩序的重建。第二次世界大战对全球政治、经济和社会产生了深远的影响。'}
# yaml_file_path = f'/Users/chenzi/project/zcbc/Moxin-App-Engine/mae/agent-hub/content-evaluation/content_evaluation/content_evaluation_agent.yml'
# inputs = load_agent_config(yaml_file_path)
# if inputs.get('check_log_prompt', None) is True:
#     log_config = {}
#     agent_config = read_yaml(yaml_file_path).get('AGENT', '')
#     agent_config['evaluation_data'] = evaluation_data
#     log_config[' Agent Prompt'] = agent_config
#     write_agent_log(log_type=inputs.get('log_type', None), log_file_path=inputs.get('log_path', None),
#                     data=log_config)
#
# if 'agents' not in inputs.keys():
#     inputs['input_fields'] = {'evaluation_data':evaluation_data}
#     result = run_dspy_agent(inputs=inputs)
# else:
#     result = run_crewai_agent(crewai_config=inputs)
# log_result = {inputs.get('log_step_name', "Step_one"): result}
# results = {}
# write_agent_log(log_type=inputs.get('log_type', None), log_file_path=inputs.get('log_path', None),
#                 data=log_result)
# results['result'] = result
# print('content_evaluation_result:', results)
#

