import click
import json as js
import json
import os
from dora import Node, DoraStatus
import sys
import pyarrow as pa
from mofa.kernel.utils.util import load_agent_config, load_dora_inputs_and_task, create_agent_output
from mofa.run.run_agent import run_dspy_agent, run_crewai_agent, run_dspy_or_crewai_agent
from mofa.utils.files.dir import get_relative_path
from mofa.utils.log.agent import record_agent_result_log
def clean_string(input_string:str):
    return input_string.encode('utf-8', 'replace').decode('utf-8')
class Operator:
    def on_event(
        self,
        dora_event,  # Dora 事件对象，包含事件类型和相关数据
        send_output,  # 用于发送输出结果的回调函数
    ) -> DoraStatus:  # 返回值为 DoraStatus 枚举类型，表示事件处理状态
        if dora_event["type"] == "INPUT":
            try:
                node_results = json.loads(dora_event['value'].to_pylist()[0])
                results = node_results.get('node_results')
                is_dataflow_end = node_results.get('dataflow_status', False)
                layer = node_results.get('layer', -1)
                if dora_event['id'] == "agent_DLCout":
                    layer = node_results.get('layer')
                    # 这是动态规划节点不做任何操作
                    print(f"DynamicNeuron:{layer}")

                if dora_event['id'] == "agent_generateout":
                    layer = node_results.get('layer')
                    # agent节点，看情况决定是否最终输出
                    print(f"-{layer + 1}-agent:{results}")

                if dora_event['id'] == "agent_reflectionout":
                    # layer=node_results.get('layer')
                    # agent节点，看情况决定是否最终输出
                    # print("------========")
                    print(f"reflectionagent:{results}")
                if layer == 0:
                    is_dataflow_end = True
                sys.stdout.flush()
                # if input("是否继续？(y/n)") == "n":
                # ptint("好的")
                # break
                if is_dataflow_end:
                    print("回答结束")
                    send_output("agent_result", pa.array([results]))
                return DoraStatus.CONTINUE  # 返回继续处理事件的状态

            except Exception as e :

                if dora_event['id'] == "data":
                    data_result = dora_event["value"][0].as_py()

                    send_output("data", pa.array([data_result]))
                    print('xiaowang_terminal Task is : ',data_result)
                    return DoraStatus.CONTINUE

        return DoraStatus.CONTINUE  # 返回继续处理事件的状态

