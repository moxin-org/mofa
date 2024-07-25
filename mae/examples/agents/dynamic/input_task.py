import json

from dora import Node
import pyarrow as pa

node = Node("task_input")

event = node.next()
task_data = input('请输入你的任务  : ',)
node.send_output('task',pa.array([json.dumps(task_data)]),event["metadata"])