import os
from dora import Node, DoraStatus
import pyarrow as pa
from mofa.kernel.utils.log import write_agent_log
from mofa.kernel.utils.util import load_agent_config, load_dora_inputs_and_task, create_agent_output, load_node_result
from mofa.run.run_agent import run_dspy_agent, run_crewai_agent, run_dspy_or_crewai_agent
from mofa.utils.files.dir import get_relative_path
from mofa.utils.files.read import read_yaml
from mofa.utils.files.util import get_all_files
from mofa.utils.log.agent import record_agent_result_log


class Operator:
    def __init__(self):
        self.momery_data = None
        self.search_task = None
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            if dora_event['id'] == "search_task": self.search_task =  dora_event["value"][0].as_py()
            if dora_event['id'] == "momery_data": self.momery_data =  load_node_result(dora_event["value"][0].as_py())
            if self.search_task is not None and self.momery_data is not None:
                
                yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='reasoner_agent.yml')
                inputs = load_agent_config(yaml_file_path)
                inputs["task"] = self.search_task
                if len(self.momery_data)>0:
                    inputs['input_fields'] = {"memory_data":self.momery_data}
                agent_result = run_dspy_or_crewai_agent(agent_config=inputs)
            
                record_agent_result_log(agent_config=inputs,agent_result={"2, "+ inputs.get('log_step_name', "Step_one"): agent_result})

                
                send_output("resoner_results", pa.array([create_agent_output(step_name='resoner_results', output_data=agent_result,dataflow_status=os.getenv('IS_DATAFLOW_END',False))]),dora_event['metadata'])

                print('agent_output:',agent_result)
                self.momery_data = None
                self.search_task = None
        return DoraStatus.CONTINUE