import argparse
import json
import os
from dora import Node
from dora import Node, DoraStatus
from mofa.kernel.utils.log import write_agent_log
from mofa.kernel.utils.util import load_agent_config
from mofa.run.run_agent import run_dspy_agent, run_crewai_agent
from mofa.utils.files.dir import get_relative_path
from mofa.utils.files.read import read_yaml
import pyarrow as pa
import os
class Operator:
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT" and dora_event['id'] in ['task','data','evaluation_data','ollama_reasoner_result']:
            evaluation_data = dora_event["value"][0].as_py()
            if isinstance(evaluation_data, dict): evaluation_data = json.dumps(evaluation_data)
            yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='evaluation_judge_agent.yml')
            inputs = load_agent_config(yaml_file_path)
            if inputs.get('check_log_prompt', None) is True:
                log_config = {}
                agent_config = read_yaml(yaml_file_path).get('AGENT', '')
                agent_config['evaluation_data'] = evaluation_data
                log_config[' Agent Prompt'] = agent_config
                write_agent_log(log_type=inputs.get('log_type', None), log_file_path=inputs.get('log_path', None),
                                data=log_config)

            if 'agents' not in inputs.keys():
                inputs['input_fields'] = {'evaluation_data':evaluation_data}
                result = run_dspy_agent(agent_config=inputs)
            else:
                result = run_crewai_agent(crewai_config=inputs)
            log_result = {inputs.get('log_step_name', "Step_one"): result}
            results = {}
            write_agent_log(log_type=inputs.get('log_type', None), log_file_path=inputs.get('log_path', None),
                            data=log_result)
            results['result'] = result
            print('evaluation_result:', results)
            send_output("evaluation_result", pa.array([json.dumps(results)]), dora_event['metadata'])

        return DoraStatus.CONTINUE

