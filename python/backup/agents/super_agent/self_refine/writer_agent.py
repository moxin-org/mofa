#!/usr/bin/envs python3
# -*- coding: utf-8 -*-
import json
from dora import DoraStatus
import pyarrow as pa

from mofa.kernel.utils.util import load_agent_config
from mofa.run.run_agent import run_dspy_agent, run_crewai_agent



class Operator:
    def on_event(
            self,
            dora_event,
            send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":

            inputs = load_agent_config('use_case/writer_agent.yml')
            result = """
            """
            if 'agents' not in inputs.keys():
                result = run_dspy_agent(agent_config=inputs)
            else:
                result = run_crewai_agent(crewai_config=inputs)
            print(result)
            if inputs.get('max_iterations',None) is not None:
                max_iterations  = inputs.get('max_iterations',None)

                result = {'max_iterations': max_iterations,'result':result,'local_iterations':1}
            else:
                result = { 'context': result,'local_iterations':1}
            send_output("writer_result", pa.array([json.dumps(result)]),dora_event['metadata'])  # add this line
            return DoraStatus.STOP
        return DoraStatus.CONTINUE



