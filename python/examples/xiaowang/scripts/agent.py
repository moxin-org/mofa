import json
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
        # 检查事件类型是否为输入事件
        if dora_event["type"] == "INPUT":
            agent_inputs = ['data', 'task']  # 定义代理输入的类型
            # 判断事件 ID 是否在代理输入中
            if dora_event["id"] in agent_inputs:
                # 从事件值中提取任务
                task = dora_event["value"][0].as_py()
                # 获取 YAML 配置文件的路径
                yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='agent.yml')
                # 加载代理配置
                inputs = load_agent_config(yaml_file_path)
                inputs["task"] = task  # 将任务添加到输入配置中
                # 运行代理，并获取结果
                agent_result = run_dspy_or_crewai_agent(agent_config=inputs)
                # 记录代理的结果日志
                record_agent_result_log(agent_config=inputs,
                                        agent_result={
                                            "1, " + inputs.get('log_step_name', "Step_one"): {task: agent_result}})
                # 发送代理的响应输出
                send_output("agent_response", pa.array([create_agent_output(step_name='agent_response', output_data=agent_result, dataflow_status=os.getenv('IS_DATAFLOW_END', True))]), dora_event['metadata'])
                print('agent_response:', agent_result)  # 打印代理的响应结果

        return DoraStatus.CONTINUE  # 返回继续处理事件的状态