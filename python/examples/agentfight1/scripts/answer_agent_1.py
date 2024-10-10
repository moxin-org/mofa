import os
from dora import Node, DoraStatus
import pyarrow as pa
from mofa.kernel.utils.util import load_agent_config, create_agent_output
from mofa.run.run_agent import run_dspy_or_crewai_agent
from mofa.utils.files.dir import get_relative_path
from mofa.utils.log.agent import record_agent_result_log

class Operator:
    def __init__(self):
        self.task = None

    def on_event(self, dora_event, send_output) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            if dora_event['id'] == "task":
                self.task = dora_event["value"][0].as_py()

            if self.task is not None:
                yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='answer_agent_1.yml')
                inputs = load_agent_config(yaml_file_path)
                inputs["task"] = self.task

                agent_result = run_dspy_or_crewai_agent(agent_config=inputs)

                record_agent_result_log(agent_config=inputs, 
                                        agent_result={"Answer 1": agent_result})
                send_output("answer_1_response", pa.array([create_agent_output(step_name='answer_1_response', output_data=agent_result, dataflow_status=os.getenv('IS_DATAFLOW_END', False))]), dora_event['metadata'])

                #print('Agent 1 Output:', agent_result)
                self.task = None
        return DoraStatus.CONTINUE
