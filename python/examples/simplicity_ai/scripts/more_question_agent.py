import json
import os

from dora import Node, DoraStatus
import pyarrow as pa

from mofa.kernel.utils.log import write_agent_log
from mofa.kernel.utils.util import load_agent_config, create_agent_output
from mofa.run.run_agent import run_dspy_agent, run_crewai_agent, run_dspy_or_crewai_agent
from mofa.utils.files.dir import get_relative_path
from mofa.utils.files.read import read_yaml
from mofa.utils.log.agent import record_agent_prompt_log, record_agent_result_log


class Operator:
    def __init__(self):
        self.web_search_results = None
        self.web_search_resource = None
        self.search_task = None

    def call_agent(self,dora_event,send_output):
        # yaml_file_path = 'use_case/more_question_agent.yml'
        yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs',
                                           target_file_name='more_question_agent.yml')
        inputs = load_agent_config(yaml_file_path)
        log_result = {}
        record_agent_prompt_log(agent_config=inputs, config_file_path=yaml_file_path, log_key_name='3 , More Question  Prompt',
                                task=self.search_task)

        write_agent_log(log_type=inputs.get('log_type', None), log_file_path=inputs.get('log_path', None),
                        data=log_result)

        inputs['context'] = self.web_search_results
        inputs['input_fields'] = {'web_search_resource': json.dumps(self.web_search_resource, ensure_ascii=False),
                                  'search_task': self.search_task}
        agent_result = run_dspy_or_crewai_agent(agent_config=inputs)

        record_agent_result_log(agent_config=inputs,
                                agent_result={inputs.get('log_step_name', "4, More Question Result"): agent_result})

        send_output("more_question_results", pa.array([create_agent_output(step_name='more_question_results',
                                                                           output_data=agent_result,
                                                                           dataflow_status=os.getenv("IS_DATAFLOW_END",
                                                                                                     True))]),dora_event['metadata'])
        self.web_search_results = None
        self.web_search_resource = None
        self.search_task = None
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            if dora_event["id"] =='web_search_results':
                self.web_search_results = dora_event["value"][0].as_py()
                if self.web_search_resource is not None and self.search_task is not None:
                    self.call_agent(dora_event, send_output)
                    return DoraStatus.CONTINUE
            elif dora_event["id"] =='web_search_resource':
                self.web_search_resource = dora_event["value"][0].as_py()
                if self.web_search_results is not None and self.search_task is not None:
                    self.call_agent(dora_event, send_output)
                return DoraStatus.CONTINUE
            elif dora_event["id"] =='search_task':
                self.search_task = dora_event["value"][0].as_py()
                return DoraStatus.CONTINUE
                # print('agent_output:',{'more_question_results':result})
        return DoraStatus.CONTINUE