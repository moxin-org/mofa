#!/usr/bin/envs python3
# -*- coding: utf-8 -*-
import json
from dora import DoraStatus
import pyarrow as pa

from mofa.kernel.utils.log import write_agent_log
from mofa.run.run_agent import run_dspy_agent, run_crewai_agent



class Operator:
    def on_event(
            self,
            dora_event,
            send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            if dora_event['id'] == 'agent_config':
                inputs = dora_event["value"][0].as_py()
                inputs = json.loads(inputs)
                print(inputs)
                result = ''
                if 'agents' not in inputs.keys():
                    result = run_dspy_agent(agent_config=inputs)
                else:
                    result = run_crewai_agent(crewai_config=inputs)

                if isinstance(result, dict):
                    log_result = {"2, " + inputs.get('log_step_name', "Step_one"): {d.get('name'):d.get('url')  for d in json.loads(result.get('web_result') )}}
                    log_result['Answer'] = result.get('answer')
                else:
                    log_result = {"2, " + inputs.get('log_step_name', "Step_one"): result}

                write_agent_log(log_type=inputs.get('log_type', None), log_file_path=inputs.get('log_path', None),
                                data=log_result)

                send_output("result", pa.array([json.dumps(result)]),dora_event['metadata'])  # add this line
                return DoraStatus.CONTINUE
        return DoraStatus.CONTINUE



