import json
import os
from dora import Node, DoraStatus
from mofa.utils.files.read import read_yaml
import pyarrow as pa
from mem0 import Memory
import os
from mofa.kernel.utils.log import write_agent_log
from mofa.kernel.utils.util import load_agent_config, load_dora_inputs_and_task, create_agent_output
from mofa.run.run_agent import run_dspy_agent, run_crewai_agent, run_dspy_or_crewai_agent
from mofa.utils.files.dir import get_relative_path
from mofa.utils.log.agent import record_agent_result_log


class Operator:
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            agent_inputs = ['data','task','search_task']
            if dora_event["id"] in agent_inputs:
                task = dora_event["value"][0].as_py()
                yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='memory_retrieval.yml')
                mem0_config = read_yaml(yaml_file_path).get('config')
                
                os.environ["OPENAI_API_KEY"] = mem0_config.get('llm').get('config').get('api_key')
                del mem0_config["llm"]["config"]["api_key"]
                m = Memory.from_config(mem0_config)
                config = read_yaml(yaml_file_path)
                # if config.get('is_reset') is True:
                #     m.reset()
                memory_result = m.search(task, user_id=config.get('user_id'))
                results = [memory_data.get("text") for memory_data in memory_result]
                send_output("memory_result", pa.array([create_agent_output(step_name='keyword_results', output_data=results,dataflow_status=os.getenv('IS_DATAFLOW_END',False))]),dora_event['metadata'])
                print('agent_result:', results)
        return DoraStatus.CONTINUE