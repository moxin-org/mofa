import json

from dora import DoraStatus


class Operator:
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            # if dora_event['id'] == 'result':
            input = dora_event["value"][0].as_py()
            print(f'reasoner_result: {json.loads(input)}')
            # return DoraStatus.CONTINUE
        return DoraStatus.CONTINUE