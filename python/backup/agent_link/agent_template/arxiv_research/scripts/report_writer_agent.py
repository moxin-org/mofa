#!/usr/bin/envs python3
# -*- coding: utf-8 -*-
import json
from dora import DoraStatus
import pyarrow as pa

from mofa.kernel.utils.log import write_agent_log
from mofa.kernel.utils.util import load_agent_config, load_dora_inputs_and_task
from mofa.run.run_agent import run_dspy_agent, run_crewai_agent
from mofa.utils.files.dir import get_relative_path


class Operator:
    def on_event(
            self,
            dora_event,
            send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            agent_inputs = ['paper_analyze_result']
            if dora_event['id'] in agent_inputs:

                task_inputs, dora_result, task = load_dora_inputs_and_task(dora_event)
                yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='report_writer_agent.yml')
                inputs = load_agent_config(yaml_file_path)
                paper_analyze = dora_result
                inputs['context'] = paper_analyze.get('context')
                if 'agents' not in inputs.keys():
                    inputs['task'] = paper_analyze.get('task')
                    result = run_dspy_agent(agent_config=inputs)
                else:
                    result = run_crewai_agent(crewai_config=inputs)
                if inputs.get('max_iterations',None) is not None:
                    max_iterations  = inputs.get('max_iterations',None)
                    result = {'task':paper_analyze.get('task'),'max_iterations': max_iterations,'context':result,'local_iterations':1,'rag_data':paper_analyze.get('context')}
                else:
                    result = { 'task':paper_analyze.get('task'),'context': result,'local_iterations':1,'rag_data':paper_analyze.get('context')}
                log_result = {"4, " +  inputs.get('log_step_name', "Step_one"): result['context']}
                write_agent_log(log_type=inputs.get('log_type', None), log_file_path=inputs.get('log_path', None),
                                data=log_result)
                send_output("writer_report", pa.array([json.dumps(result)]),dora_event['metadata'])  # add this line
                print('agent_output:',result['context'])
                return DoraStatus.STOP
        return DoraStatus.CONTINUE



