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
            agent_inputs = ['refinement_result']
            if dora_event['id'] in agent_inputs:
                task_inputs, dora_result, task = load_dora_inputs_and_task(dora_event)
                yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='evaluation_agent.yml')
                inputs = load_agent_config(yaml_file_path)
                inputs['context'] = dora_result.get('context')
                local_iterations = dora_result.get('local_iterations', None)
                if local_iterations is not None:
                    max_iterations = inputs.get('max_iterations')
                    if local_iterations > max_iterations:
                        print('Task Result:  ',dora_result.get('context'))
                        log_result = {"7, " + inputs.get('log_step_name', "Step_one"): dora_result.get('context')}

                        write_agent_log(log_type=inputs.get('log_type', None),
                                        log_file_path=inputs.get('log_path', None),
                                        data=log_result)
                        return DoraStatus.STOP
                    else:
                        print('inputs    :  ',inputs)
                        print("dora_result   :", dora_result)
                        if 'agents' not in inputs.keys():
                            inputs['task'] = dora_result['task']

                            result = run_dspy_agent(agent_config=inputs)
                        else:
                            result = run_crewai_agent(crewai_config=inputs)
                        log_result = {"7, " + inputs.get('log_step_name', "Step_one"): result}

                        if 'Yes' in result or 'yes' in result or '是' in result:
                            print(f"In the {dora_result.get('local_iterations')} iteration result  : ", inputs['context'])
                            write_agent_log(log_type=inputs.get('log_type', None),
                                            log_file_path=inputs.get('log_path', None),
                                            data=log_result)
                            return DoraStatus.STOP
                        else:
                            inputs['local_iterations'] = local_iterations + 1
                            if inputs['local_iterations'] <= max_iterations :
                                result = { 'context': dora_result.get('context'),'local_iterations':inputs['local_iterations'],'rag_data':dora_result['rag_data'],'task':dora_result['task']}
                                send_output("evaluation_result", pa.array([json.dumps(result)]),dora_event['metadata'])
                                return DoraStatus.CONTINUE
                            else:
                                return DoraStatus.STOP
        return DoraStatus.CONTINUE


