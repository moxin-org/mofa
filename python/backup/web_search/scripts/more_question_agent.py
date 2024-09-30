import json
import os

from dora import Node, DoraStatus
import pyarrow as pa

from mofa.kernel.utils.log import write_agent_log
from mofa.kernel.utils.util import load_agent_config, create_agent_output
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
            agent_inputs = ['web_search_aggregate_output']
            if dora_event["id"] in agent_inputs:
                dora_result = json.loads(dora_event["value"][0].as_py())
                # yaml_file_path = 'use_case/more_question_agent.yml'
                yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='more_question_agent.yml')
                inputs = load_agent_config(yaml_file_path)
                log_result = {}
                if inputs.get('check_log_prompt', None) is True:
                    log_config = read_yaml(yaml_file_path).get('AGENT', '')
                    log_config['Task'] = dora_result.get('task')
                    log_result['3 , More Question Config'] = log_config
                write_agent_log(log_type=inputs.get('log_type', None), log_file_path=inputs.get('log_path', None),
                                data=log_result)
                result = """
                                """
                if 'agents' not in inputs.keys():
                    inputs['context'] = dora_result.get('web_search_results')
                    inputs['input_fields'] = {'web_search_resource': json.dumps(dora_result.get('web_result')),'search_task':dora_result.get('task')}
                    result = run_dspy_agent(agent_config=inputs)
                else:
                    result = run_crewai_agent(crewai_config=inputs)
                log_result = {"4, More Question Result":result}
                write_agent_log(log_type=inputs.get('log_type',None),log_file_path=inputs.get('log_path',None),data=log_result)
                dora_result.update({'more_question_results':result})
                send_output("more_question_results", pa.array([create_agent_output(step_name='more_question_results', output_data=result,dataflow_status=os.getenv("IS_DATAFLOW_END", True))]), dora_event['metadata'])
                # print('agent_output:',{'more_question_results':result})
        return DoraStatus.CONTINUE