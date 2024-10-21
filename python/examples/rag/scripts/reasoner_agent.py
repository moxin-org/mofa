import os
from dora import Node, DoraStatus
import pyarrow as pa
from mofa.kernel.utils.util import load_agent_config,  create_agent_output, load_node_result
from mofa.run.run_agent import  run_dspy_or_crewai_agent
from mofa.utils.files.dir import get_relative_path
from mofa.utils.log.agent import record_agent_result_log


class Operator:
    def __init__(self):
        self.task = None
        self.context_rag = None
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            if dora_event['id'] == 'task':
                self.task = dora_event["value"][0].as_py()
            if dora_event['id'] == 'context_rag':
                self.context_rag = load_node_result(dora_event["value"][0].as_py())
            if self.context_rag is not None and self.task is not None:

                yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='reasoner_agent.yml')
                inputs = load_agent_config(yaml_file_path)
                inputs["task"] = self.task
                inputs['input_fields'] = {"content_rag":self.context_rag}
                print(inputs)
                agent_result = run_dspy_or_crewai_agent(agent_config=inputs)
                record_agent_result_log(agent_config=inputs,
                                        agent_result={
                                            "1, "+ inputs.get('log_step_name', "Step_one"): agent_result})
                send_output("reasoner_response", pa.array([create_agent_output(step_name='reasoner_response', output_data=agent_result,dataflow_status=os.getenv('IS_DATAFLOW_END',True))]),dora_event['metadata'])
                print({"task":self.task,'response':agent_result})
                print('reasoner_response:', agent_result)

        return DoraStatus.CONTINUE