import time
from pathlib import Path
from mofa.agent_build.base.base_agent import MofaAgent
import os

def multiply(a:int, b:int=2):
    a,b = int(a),int(b)
    return a * b

def main():
    agent = MofaAgent(agent_name='add_numbers_agent',)
    while True:
        num1 = agent.receive_parameter(parameter_name='num1')
        print('num1. : ', num1)
        result = multiply(num1)
        time.sleep(10)
        agent.send_output(agent_output_name='multiply_numbers_result',agent_result=result)

