import json

from dora import Node, DoraStatus
import pyarrow as pa

from mofa.kernel.utils.log import write_agent_log
from mofa.kernel.utils.util import load_agent_config, load_dora_inputs_and_task
from mofa.run.run_agent import run_dspy_agent, run_crewai_agent
from mofa.utils.files.dir import get_relative_path
from mofa.utils.files.read import read_yaml



class Operator:
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            agent_inputs = ['keywords']
            if dora_event['id'] in agent_inputs:
                task_inputs, dora_result, task = load_dora_inputs_and_task(dora_event)
                yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='paper_downloader_agent.yml')

                inputs = load_agent_config(yaml_file_path)
                print('inputs   : ',inputs)
                result = """
"""
                inputs.get('tasks')[0]['description'] = f"keywords: {dora_result.get('keywords')}"
                if 'agents' not in inputs.keys():
                    result = run_dspy_agent(agent_config=inputs)
                else:
                    result = run_crewai_agent(crewai_config=inputs)

                log_config = inputs.get('log')
                log_result =  {"2, "+log_config.get('log_step_name',"Step_one"):result}
                write_agent_log(log_type=log_config.get('log_type',None),log_file_path=log_config.get('log_path',None),data=log_result)

                result_dict = {'task':dora_result.get('task')}
                send_output("papers_info", pa.array([json.dumps(result_dict)]),dora_event['metadata'])
                print('agent_output:',result)

                return  DoraStatus.STOP
        return DoraStatus.CONTINUE