#!/usr/bin/envs python3
# -*- coding: utf-8 -*-
import json
from dora import DoraStatus
import pyarrow as pa

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
                result = ''
                print(inputs)
                if 'agents' not in inputs.keys():
                    result = run_dspy_agent(agent_config=inputs)
                else:
                    result = run_crewai_agent(crewai_config=inputs)
                print(result)
                send_output("result", pa.array([json.dumps(result)]),dora_event['metadata'])  # add this line
                return DoraStatus.CONTINUE
        return DoraStatus.CONTINUE



