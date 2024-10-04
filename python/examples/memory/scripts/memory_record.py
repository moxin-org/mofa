import json
import os
from dora import Node, DoraStatus

from mofa.kernel.utils.util import create_agent_output, load_node_result
from mofa.kernel.memory.util import load_mem0_client, load_user_id
import pyarrow as pa
import os
from mofa.utils.files.dir import get_relative_path


class Operator:
    def __init__(self):
        self.task = None
        self.reasoner_response = None
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            if dora_event['id'] == "task": self.task =  dora_event["value"][0].as_py()
            if dora_event['id'] == "reasoner_response": self.reasoner_response =  load_node_result(dora_event["value"][0].as_py())
            if self.reasoner_response is not None and self.task is not None:
            
                yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='memory_retrieval.yml')

                m = load_mem0_client(yaml_file_path)
                user_id = load_user_id(yaml_file_path)

                m.add(self.reasoner_response.replace(":dataflow_status",""),user_id=user_id,metadata={"task":self.task})
                
                send_output("memory_log", pa.array([create_agent_output(step_name='memory_record', output_data={"reasoner_response":self.reasoner_response},dataflow_status=os.getenv('IS_DATAFLOW_END',True))]),dora_event['metadata'])
                self.reasoner_response = None
                self.task = None
        return DoraStatus.CONTINUE