import json
import os
from dora import Node, DoraStatus
from mofa.utils.files.read import read_yaml
import pyarrow as pa
from mem0 import Memory
import os
from mofa.kernel.utils.log import write_agent_log
from mofa.kernel.utils.util import load_agent_config, load_dora_inputs_and_task, create_agent_output, load_node_result
from mofa.run.run_agent import run_dspy_agent, run_crewai_agent, run_dspy_or_crewai_agent
from mofa.utils.files.dir import get_relative_path
from mofa.utils.log.agent import record_agent_result_log


class Operator:
    def __init__(self):
        self.search_task = None
        self.resoner_results = None
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            if dora_event['id'] == "search_task": self.search_task =  dora_event["value"][0].as_py()
            if dora_event['id'] == "resoner_results": self.resoner_results =  load_node_result(dora_event["value"][0].as_py())
            if self.resoner_results is not None and self.search_task is not None:
            
                yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='memory_retrieval.yml')
                mem0_config = read_yaml(yaml_file_path).get('config')
                agent_prompt_config = read_yaml(get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='reasoner_agent.yml')).get('AGENT')
                
                os.environ["OPENAI_API_KEY"] = mem0_config.get('llm').get('config').get('api_key')
                del mem0_config["llm"]["config"]["api_key"]
                m = Memory.from_config(mem0_config)
                config = read_yaml(yaml_file_path)
                agent_prompt = ""
                for key,vaule in agent_prompt_config.items():
                    agent_prompt += f"{key}: {vaule}, "
                m.add(self.resoner_results.replace(":dataflow_status",""),user_id=config.get('user_id'),metadata={"search_task":self.search_task})
                
                send_output("memory_record", pa.array([create_agent_output(step_name='memory_record', output_data={"agent_prompt":agent_prompt,"resoner_results":self.resoner_results},dataflow_status=os.getenv('IS_DATAFLOW_END',True))]),dora_event['metadata'])
                self.resoner_results = None
                self.search_task = None
        return DoraStatus.CONTINUE