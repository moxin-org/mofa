
import json
import os

from dora import DoraStatus
import pyarrow as pa

from mofa.kernel.utils.util import load_agent_config, create_agent_output, load_node_result
from mofa.run.run_agent import run_dspy_agent, run_crewai_agent, run_dspy_or_crewai_agent
from mofa.utils.files.dir import get_relative_path


class Operator:
    def __init__(self):
        self.suggestion = None
        self.writer_report = None
        self.search_task = None
    def on_event(
            self,
            dora_event,
            send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            if dora_event['id'] == 'search_task': self.search_task = dora_event["value"][0].as_py()
            if dora_event['id'] == 'writer_report': self.writer_report = load_node_result(dora_event["value"][0].as_py())
            if dora_event['id'] == 'suggestion': self.suggestion = load_node_result(dora_event["value"][0].as_py())

            if self.suggestion is not None and self.writer_report is not None and self.search_task is not None:
                yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs',
                                                   target_file_name='refinement_agent.yml')
                inputs = load_agent_config(yaml_file_path)
                inputs['input_fields'] = {'search_task_suggestion':self.suggestion,'search_task':self.search_task,'task_result':self.writer_report}
                agent_result = run_dspy_or_crewai_agent(agent_config=inputs)
                print('inputs: ',inputs)
                send_output("refinement_result", pa.array([create_agent_output(step_name='refinement_result', output_data=agent_result,dataflow_status=os.getenv('IS_DATAFLOW_END',False))]),dora_event['metadata'])
                print('refinement_result : ',agent_result)
                self.suggestion,self.writer_report = None,None
        return DoraStatus.CONTINUE



