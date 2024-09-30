import json
import os
from dora import Node, DoraStatus
import pyarrow as pa
from mofa.kernel.utils.util import load_agent_config, create_agent_output
from mofa.run.run_agent import run_dspy_agent, run_crewai_agent, run_dspy_or_crewai_agent
from mofa.utils.files.dir import get_relative_path
from mofa.utils.log.agent import record_agent_prompt_log, record_agent_result_log


class Operator:

    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            agent_inputs = ['web_search_task']
            if dora_event["id"] in agent_inputs:

                task = dora_event["value"][0].as_py()
                yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='web_search_agent.yml')
                inputs = load_agent_config(yaml_file_path)
                record_agent_prompt_log(agent_config=inputs, config_file_path=yaml_file_path,
                                        log_key_name='1 , Web_Search_Config',
                                        task=task)
                inputs['task'] = task
                agent_result = run_dspy_or_crewai_agent(agent_config=inputs)
                record_agent_result_log(agent_config=inputs,
                                        agent_result={
                                            inputs.get('log_step_name', "3, Web Search Answer "): {d.get('name'):d.get('url') for d in json.loads(agent_result.get('web_search_resource'))}})
                send_output("web_search_results", pa.array([create_agent_output(step_name='web_search_results', output_data=agent_result.get('web_search_results'),dataflow_status=os.getenv('IS_DATAFLOW_END',False))]),dora_event['metadata'])
                send_output("web_search_resource", pa.array([create_agent_output(step_name='web_search_resource', output_data=agent_result.get('web_search_resource'),dataflow_status=os.getenv('IS_DATAFLOW_END',False))]),dora_event['metadata'])
        return DoraStatus.CONTINUE