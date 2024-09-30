
import json
import os

from dora import DoraStatus
import pyarrow as pa
from mofa.kernel.utils.util import load_agent_config, create_agent_output, load_node_result
from mofa.run.run_agent import run_dspy_agent, run_crewai_agent, run_dspy_or_crewai_agent
from mofa.utils.files.dir import get_relative_path



class Operator:
    def __init__(self):
        self.search_task = None
        self.refinement_report = None
        self.local_iterations = 1
    def on_event(
            self,
            dora_event,
            send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs',
                                               target_file_name='evaluation_agent.yml')
            inputs = load_agent_config(yaml_file_path)
            max_iterations = inputs.get('max_iterations')
            if dora_event['id'] == 'search_task':
                    self.search_task = dora_event["value"][0].as_py()
            if dora_event['id'] == 'refinement_report':
                self.refinement_report = load_node_result(dora_event["value"][0].as_py())

            if self.refinement_report is not None and self.search_task is not None :
                print('inputs: ',inputs)
                if self.local_iterations < max_iterations:
                    inputs['context'] = self.refinement_report
                    inputs['task'] = self.search_task
                    agent_result = run_dspy_or_crewai_agent(agent_config=inputs)
                    self.local_iterations +=1
                    if 'Yes' in agent_result or 'yes' in agent_result:
                        send_output("self_refine_end", pa.array([create_agent_output(step_name='self_refine_end',output_data=agent_result,dataflow_status=True)]),dora_event['metadata'])
                        self.search_task, self.refinement_report = None, None
                    else:
                        send_output("evaluation_result", pa.array([create_agent_output(step_name='evaluation_result',output_data=self.refinement_report,dataflow_status=False)]),dora_event['metadata'])
                        self.refinement_report = None
                else:
                    send_output("self_refine_end", pa.array([create_agent_output(step_name='self_refine_end',output_data='self_refine_end',dataflow_status=True)]),dora_event['metadata'])
                    self.search_task,self.refinement_report = None,None
        return DoraStatus.CONTINUE



