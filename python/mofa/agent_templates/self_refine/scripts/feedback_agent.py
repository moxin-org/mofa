
import os

from dora import DoraStatus
import pyarrow as pa

from mofa.kernel.utils.util import load_agent_config, create_agent_output, load_node_result
from mofa.run.run_agent import run_dspy_agent, run_crewai_agent, run_dspy_or_crewai_agent
from mofa.utils.files.dir import get_relative_path
from mofa.utils.log.agent import record_agent_result_log


class Operator:
    def __init__(self):
        self.search_task = None
        self.writer_report = None
        self.refinement_report = None
    def on_event(
            self,
            dora_event,
            send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs',
                                               target_file_name='feedback_agent.yml')
            inputs = load_agent_config(yaml_file_path)

            if dora_event['id'] == 'search_task' :
                self.search_task = dora_event["value"][0].as_py()
            if dora_event['id'] == 'writer_report':
                self.writer_report = load_node_result(dora_event["value"][0].as_py())

            if dora_event['id'] == 'refinement_report':
                self.refinement_report = load_node_result(dora_event["value"][0].as_py())

            if (self.writer_report is not None and self.search_task is not None) or (self.refinement_report is not None and self.search_task is not None):
                inputs['context'] = self.writer_report if self.writer_report is not None else self.refinement_report
                inputs['task'] = self.writer_report
              
                agent_suggestion = run_dspy_or_crewai_agent(agent_config=inputs)
                record_agent_result_log(agent_config=inputs,
                                        agent_result={
                                            "2, " + inputs.get('log_step_name', "suggestion "): {self.search_task: agent_suggestion}})
                send_output("suggestion", pa.array([create_agent_output(step_name='feedback_result', output_data=agent_suggestion,dataflow_status=os.getenv('IS_DATAFLOW_END',False))]),dora_event['metadata'])
                print('agent_suggestion',agent_suggestion)
                if self.writer_report is not None: self.writer_report= None
                if self.refinement_report is not None: self.refinement_report= None

    
        return DoraStatus.CONTINUE



