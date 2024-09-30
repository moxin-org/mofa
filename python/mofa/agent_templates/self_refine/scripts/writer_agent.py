#!/usr/bin/envs python3
# -*- coding: utf-8 -*-
import json
import os

from dora import DoraStatus
import pyarrow as pa

from mofa.kernel.utils.util import load_agent_config, create_agent_output
from mofa.run.run_agent import run_dspy_agent, run_crewai_agent, run_dspy_or_crewai_agent
from mofa.utils.files.dir import get_relative_path
from mofa.utils.log.agent import record_agent_result_log


class Operator:
    def on_event(
            self,
            dora_event,
            send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT" and dora_event['id'] in ['task','data']:
            task = dora_event["value"][0].as_py()
            yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs',
                                               target_file_name='writer_agent.yml')
            inputs = load_agent_config(yaml_file_path)
            inputs['task'] = task
            agent_result = run_dspy_or_crewai_agent(agent_config=inputs)
            record_agent_result_log(agent_config=inputs,
                                    agent_result={
                                        "1, " + inputs.get('log_step_name', "Writer Report"): {task: agent_result}})
            send_output("writer_report", pa.array([create_agent_output(step_name='writer_report_results',
                                                                          output_data=agent_result,
                                                                          dataflow_status=os.getenv('IS_DATAFLOW_END',
                                                                                                    False))]),
                        dora_event['metadata'])
            print('writer_report_result: ',agent_result)
        return DoraStatus.CONTINUE



