#!/usr/bin/envs python3
# -*- coding: utf-8 -*-
import json
from dora import DoraStatus

class Operator:
    def on_event(
            self,
            dora_event,
            send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            # print(dora_event)
            if dora_event['id'] == 'task_input' :
                writer_result = json.loads(dora_event["value"][0].as_py())
                print('我接受到的任务是  ',writer_result)

                return DoraStatus.STOP
        return DoraStatus.CONTINUE


