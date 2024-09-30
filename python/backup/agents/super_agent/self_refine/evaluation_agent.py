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
            if dora_event['id'] == 'refinement_result':
                inputs = load_agent_config('use_case/evaluation_agent.yml')
                result = """
                """
                dora_result = json.loads(dora_event["value"][0].as_py())
                inputs['context'] = dora_result.get('context')
                local_iterations = dora_result.get('local_iterations', None)
                if local_iterations is not None:
                    max_iterations = inputs.get('max_iterations')
                    if local_iterations > max_iterations:
                        print('Task Result:  ',dora_result.get('context'))
                        return DoraStatus.STOP
                    else:
                        print(inputs)
                        if 'agents' not in inputs.keys():
                            result = run_dspy_agent(agent_config=inputs)
                        else:
                            result = run_crewai_agent(crewai_config=inputs)
                        if 'Yes' in result or 'yes' in result:
                            print(f"In the {max_iterations} iteration result  : ", dora_result.get('context'))
                            return DoraStatus.STOP
                        else:
                            inputs['local_iterations'] = local_iterations + 1
                            result = { 'context': dora_result.get('context'),'local_iterations':inputs['local_iterations']}
                            print(f"The {inputs['local_iterations']} iteration Result:  ",)
                            send_output("evaluation_result", pa.array([json.dumps(result)]),dora_event['metadata'])

                            return DoraStatus.CONTINUE
                # send_output("feedback_result", pa.array([json.dumps(result)]),dora_event['metadata'])  # add this line
                return DoraStatus.STOP
        return DoraStatus.CONTINUE



