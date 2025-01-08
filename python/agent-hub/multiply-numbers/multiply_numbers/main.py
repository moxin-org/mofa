from pathlib import Path
from mofa.agent_build.base.base_agent import MofaAgent
import os

def multiply(a, b:int=2):
    return a * b

def main():
    agent = MofaAgent(agent_name='add_numbers_agent',)
    while True:
        # TODO: 在下面添加你的Agent代码,其中agent_inputs是你的Agent的需要输入的参数
        """----------------"""
        # 获取用户输入的两个整数
        num1 = agent.receive_parameter(parameter_name='num1')
        print(f"用户输入的1个整数是: {num1}")
        # 调用函数并输出结果
        result = multiply(num1)
        print(f"乘法结果是: {result}")
        """-------------"""
        print('IS_DATAFLOW_END: ',os.getenv('IS_DATAFLOW_END', True))
        agent.send_output(agent_output_name='multiply_numbers_result',agent_result=result)

