from pathlib import Path
from mofa.agent_build.base.base_agent import MofaAgent
import os

def add_two_numbers(a:int, b:int):
    a,b = int(a),int(b) # convert to int
    return a + b

def main():
    agent = MofaAgent(agent_name='add_numbers_agent',)
    while True:
        # num2 = agent.receive_parameter(parameter_name='num2')
        # print('num2 : ',num2)
        # num1 = agent.receive_parameter(parameter_name='num1')
        # print('num1 : ',num1)
        parameters_data = agent.receive_parameters(parameter_names=['num2','num1'])
        print('parameters_data  : ', parameters_data )
        result = add_two_numbers(a=parameters_data['num1'],b=parameters_data['num2'])
        agent.send_output(agent_output_name='add_numbers_result',agent_result=result)

