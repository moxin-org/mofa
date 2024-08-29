import json
import pyarrow as pa
from dora import DoraStatus

class Operator:
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            agent_inputs = ['web_search_aggregate_output']
            if dora_event['id'] in agent_inputs:
                task_result = json.loads(dora_event["value"][0].as_py())
                print(f'{task_result}')
                send_output("web_search_output", pa.array([json.dumps(task_result)]), dora_event['metadata'])
                send_output("web_search_results", pa.array([json.dumps({'web_search_results':task_result.get('web_search_results')})]), dora_event['metadata'])
                send_output("web_search_resource", pa.array([json.dumps({'web_search_resource':task_result.get('web_search_resource')})]), dora_event['metadata'])
                send_output("more_question_results", pa.array([json.dumps({'more_question_results':task_result.get('more_question_results')})]), dora_event['metadata'])
                send_output("web_search_task", pa.array([json.dumps({'web_search_task':task_result.get('task')})]), dora_event['metadata'])
        return DoraStatus.CONTINUE