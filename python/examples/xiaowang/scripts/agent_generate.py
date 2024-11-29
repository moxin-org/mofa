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
        if dora_event["type"] == "INPUT":
            if dora_event['id'] == "task":
                self.task = js.loads(dora_event['value'].to_pylist()[0])
                #node_results = js.loads(dora_event['value'].to_pylist()[0])
                input_gene=self.task.get("user_input")
                layer=self.task.get("layer")
                #node_results.get('layer')
            
            if dora_event['id'] == "agent_reflectionout":
                self.task = js.loads(dora_event['value'].to_pylist()[0])
                node_results = js.loads(dora_event['value'].to_pylist()[0])
                input_gene=self.task.get("user_input")
                layer=self.task.get("layer")
                #node_results.get('layer')
            
            # 创建一个字典对象
            data = {
                "node_results": f"我接收到一条命令{self.task}",
                "layer": (layer),
                "dataflow_status": self.task.get('dataflow_status', False),
                "user_input": input_gene
                }# 将字典对象转换为 JSON 字符串
            json_string = js.dumps(data)
            #send_output("agent_generateout", pa.array([json_string]))

            if input_gene is not None:
                yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='agent_generate.yml')
                inputs = load_agent_config(yaml_file_path)
                
                if dora_event['id'] == "agent_reflectionout":
                    USER_INPUT= "USER_INPUT:"+input_gene
                    PREVIOUS_ANSWER= "PREVIOUS_ANSWER:"+self.task.get("previous_anser")
                    TASK= "TASK:"+self.task.get("node_results")
                else:
                    USER_INPUT=self.task.get("user_input")
                    PREVIOUS_ANSWER= ""
                    TASK=""
                
                inputs["task"] = USER_INPUT+PREVIOUS_ANSWER+TASK
                

                #处理原始输入数据inputs
                dataflow_status=False
                #根据输入生成改进的prompt
                agent_generateout = run_dspy_or_crewai_agent(agent_config=inputs)
                
                #解析模型运行层数并输出结果
                #根据文本里面@的个数解析出模型运行层数，有几个@字符就给layer赋值为几
                #dora.send_output("int_output",layer
                


                layer=self.task.get("layer")
                if layer==1:
                    dataflow_status=True
                # 创建一个字典对象
                data = {
                    "node_results": agent_generateout,
                    "layer": (layer-1),
                    "dataflow_status": dataflow_status,
                    "user_input": input_gene
                    }# 将字典对象转换为 JSON 字符串
                json_string = js.dumps(data)


                #输出模型运行结果
                #send_output("agent_DLCout", pa.array([create_agent_output(step_name='agent_DLCout_step', output_data=self.task, dataflow_status=os.getenv('IS_DATAFLOW_END', False))]), dora_event['metadata'])
                #send_output("status", pa.array([json_string]))
                send_output("agent_generateout", pa.array([json_string]))
                #输出模型层数信息
                #send_output("agent_DLClayer", pa.array([create_agent_output(step_name='agent_DLClayer_step', output_data=layer, dataflow_status=os.getenv('IS_DATAFLOW_END', False))]), dora_event['metadata'])
                



                record_agent_result_log(agent_config=inputs, 
                                        agent_result={"agent_generateout": agent_generateout})
                #send_output("agent_DLCout", pa.array([create_agent_output(step_name='agent_DLCout_step', output_data=agent_DLC, dataflow_status=os.getenv('IS_DATAFLOW_END', False))]), dora_event['metadata'])
                self.task = None
        return DoraStatus.CONTINUE  # 返回继续处理事件的状态