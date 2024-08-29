#!/usr/bin/envs python3
# -*- coding: utf-8 -*-
import json
import os

from dora import DoraStatus
import pyarrow as pa

from mae.kernel.utils.log import write_agent_log
from mae.kernel.utils.util import load_agent_config, load_dora_inputs_and_task, create_agent_output
from mae.run.run_agent import run_dspy_agent, run_crewai_agent, run_dspy_or_crewai_agent
from mae.utils.files.dir import get_relative_path


class Operator:
    def __init__(self):
        self.search_task = None
        self.paper_analyze_result = None
        self.local_iterations = 1
    def on_event(
            self,
            dora_event,
            send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs',
                                               target_file_name='report_writer_agent.yml')
            inputs = load_agent_config(yaml_file_path)
            if dora_event['id'] =='search_task':
                self.search_task = dora_event["value"][0].as_py()
            if dora_event['id'] == 'paper_analyze_result':
                self.paper_analyze_result = dora_event["value"][0].as_py()
            if dora_event['id'] == 'local_iterations':
                local_iterations = dora_event["value"][0].as_py()
                if local_iterations != self.local_iterations:
                    self.local_iterations = local_iterations

            if self.search_task is not None and self.paper_analyze_result is not None and inputs.get('max_iterations',None)<=self.local_iterations:

                inputs['context'] = self.paper_analyze_result
                agent_result = run_dspy_or_crewai_agent(agent_config=inputs)

                # if inputs.get('max_iterations',None) is not None:
                #     max_iterations  = inputs.get('max_iterations',None)
                #     result = {'task':paper_analyze.get('task'),'max_iterations': max_iterations,'context':result,'local_iterations':1,'rag_data':paper_analyze.get('context')}
                # else:
                #     result = { 'task':paper_analyze.get('task'),'context': result,'local_iterations':1,'rag_data':paper_analyze.get('context')}
                # log_result = {"4, " +  inputs.get('log_step_name', "Step_one"): result['context']}
                write_agent_log(log_type=inputs.get('log_type', None), log_file_path=inputs.get('log_path', None),
                                data={"4, " +  inputs.get('log_step_name', "Step_one"): agent_result})
                send_output("writer_report", pa.array([create_agent_output(step_name='writer_report', output_data=agent_result,dataflow_status=os.getenv('IS_DATAFLOW_END',False))]),dora_event['metadata'])

                # send_output("writer_report", pa.array([json.dumps(result)]),dora_event['metadata'])  # add this line
                print('agent_output:',agent_result)
                self.search_task = None
                self.paper_analyze_result = None
                return DoraStatus.STOP
            return DoraStatus.CONTINUE



