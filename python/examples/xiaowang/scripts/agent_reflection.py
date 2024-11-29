import click
import json as js
import os
from dora import Node, DoraStatus
import pyarrow as pa
from mofa.kernel.utils.util import load_agent_config, load_dora_inputs_and_task, create_agent_output
from mofa.run.run_agent import run_dspy_agent, run_crewai_agent, run_dspy_or_crewai_agent
from mofa.utils.files.dir import get_relative_path
from mofa.utils.log.agent import record_agent_result_log

class Operator:
    def on_event(
        self,
        dora_event,  # Dora 事件对象，包含事件类型和相关数据
        send_output,  # 用于发送输出结果的回调函数
    ) -> DoraStatus:  # 返回值为 DoraStatus 枚举类型，表示事件处理状态
        # 创建一个字典对象
        if dora_event["type"] == "INPUT":
            if dora_event['id'] == "task":
                self.task = js.loads(dora_event['value'].to_pylist()[0])
                USER_INPUT=self.task.get("user_input")
                AGENT_RESPONSE=self.task.get("node_results")
                layer=self.task.get("layer")

            if self.task is not None:
                yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='agent_reflection.yml')
                inputs = load_agent_config(yaml_file_path)
                inputs["task"] = "USER_INPUT:"+USER_INPUT+"\n"+"AGENT_RESPONSE:"+AGENT_RESPONSE
                dataflow_status=self.task.get("dataflow_status")
                if dataflow_status==False:
                    agent_reflectionout = run_dspy_agent(agent_config=inputs)
                else:
                    agent_reflectionout = "无"
                #agent_reflectionout = run_dspy_or_crewai_agent(agent_config=inputs)
                dataflow_status=self.task.get("dataflow_status")
                #根据文本里面@的个数解析出模型运行层数，有几个@字符就给layer赋值为几
                #dora.send_output("int_output",layer)


                layer=self.task.get("layer")
                # 创建一个字典对象
                data = {
                    "node_results": agent_reflectionout,
                    "layer": layer,
                    "user_input": USER_INPUT,
                    "previous_anser":AGENT_RESPONSE,
                    "dataflow_status": False
                    }# 将字典对象转换为 JSON 字符串
                json_string = js.dumps(data)


                #输出模型运行结果
                #send_output("agent_DLCout", pa.array([create_agent_output(step_name='agent_DLCout_step', output_data=self.task, dataflow_status=os.getenv('IS_DATAFLOW_END', False))]), dora_event['metadata'])
                #send_output("status", pa.array([json_string]))
                if dataflow_status==False:
                    send_output("agent_reflectionout", pa.array([json_string]))
                #输出模型层数信息
                #send_output("agent_DLClayer", pa.array([create_agent_output(step_name='agent_DLClayer_step', output_data=layer, dataflow_status=os.getenv('IS_DATAFLOW_END', False))]), dora_event['metadata'])
                



                record_agent_result_log(agent_config=inputs, 
                                        agent_result={"agent_reflectionout": agent_reflectionout})
                #send_output("agent_DLCout", pa.array([create_agent_output(step_name='agent_DLCout_step', output_data=agent_DLC, dataflow_status=os.getenv('IS_DATAFLOW_END', False))]), dora_event['metadata'])
                self.task = None
        return DoraStatus.CONTINUE  # 返回继续处理事件的状态