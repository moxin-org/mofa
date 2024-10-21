import json
import os
from dora import Node, DoraStatus
import pyarrow as pa
import os
from mofa.kernel.utils.util import load_agent_config, load_dora_inputs_and_task, create_agent_output
from mofa.utils.files.dir import get_relative_path

from mofa.kernel.memory.util import load_mem0_client, load_user_id, get_mem0_search_text



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
                m = load_mem0_client(yaml_file_path)
                user_id = load_user_id(yaml_file_path)
                memory_result = m.search(task, user_id=user_id)
                results = get_mem0_search_text(memory_result)


                send_output("context_memory", pa.array([create_agent_output(step_name='context_memory', output_data=results,dataflow_status=os.getenv('IS_DATAFLOW_END',False))]),dora_event['metadata'])

        return DoraStatus.CONTINUE