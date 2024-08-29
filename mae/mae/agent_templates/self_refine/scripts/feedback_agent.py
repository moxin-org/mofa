#!/usr/bin/envs python3
# -*- coding: utf-8 -*-
import json
from dora import DoraStatus
import pyarrow as pa

from mae.kernel.utils.util import load_agent_config
from mae.run.run_agent import run_dspy_agent, run_crewai_agent
from mae.utils.files.dir import get_relative_path


class Operator:
    def on_event(
            self,
            dora_event,
            send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            # print(dora_event)
            if dora_event['id'] == 'writer_result' :
                yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs',
                                                   target_file_name='feedback_agent.yml')
                inputs = load_agent_config(yaml_file_path)


                writer_result = json.loads(dora_event["value"][0].as_py())

                inputs['context'] = writer_result.get('result')
                if 'agents' not in inputs.keys():
                    result = run_dspy_agent(agent_config=inputs)
                else:
                    result = run_crewai_agent(crewai_config=inputs)
                if inputs.get('max_iterations',None) is not None:

                    result = {'suggestion':result,'context':writer_result.get('result'),'local_iterations':writer_result.get('local_iterations', None)}
                else:
                    result = {'suggestion':result,'context':writer_result.get('result'),}

                print(result)
                send_output("feedback_result", pa.array([json.dumps(result)]),dora_event['metadata'])  # add this line
        return DoraStatus.CONTINUE



