import json
from dora import Node, DoraStatus
import pyarrow as pa

from mofa.kernel.utils.log import write_agent_log
from mofa.kernel.utils.util import load_agent_config
from mofa.run.run_agent import run_dspy_agent, run_crewai_agent
from mofa.utils.files.read import read_yaml



class Operator:
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            if dora_event["id"] == "web_search_result":
                dora_result = json.loads(dora_event["value"][0].as_py())
                yaml_file_path = 'use_case/more_question_agent.yml'
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
                    inputs['input_fields'] = {'web_search_resource': json.dumps(dora_result.get('web_search_resource')),'search_task':dora_result.get('task')}
                    result = run_dspy_agent(agent_config=inputs)
                else:
                    result = run_crewai_agent(crewai_config=inputs)
                log_result = {"4, More Question Result":result}
                write_agent_log(log_type=inputs.get('log_type',None),log_file_path=inputs.get('log_path',None),data=log_result)
                print(result)
                return DoraStatus.STOP
        return DoraStatus.CONTINUE