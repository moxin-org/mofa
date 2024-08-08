import json

from dora import Node
import pyarrow as pa

node = Node("reasoner_task_input")

event = node.next()
task_data = input('Please enter your task:  ',)
node.send_output('reasoner_task',pa.array([json.dumps(task_data)]),event["metadata"])
while True:
    event = node.next()
    if event["type"] == "INPUT":
        if event["id"] == "reasoner_log":
            print('-----------  ：',event["value"])