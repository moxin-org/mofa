import argparse
import json
import os
from pathlib import Path
from dora import Node
from mofa.agent_build.base.base_agent import MofaAgent
from mofa.kernel.utils.util import create_agent_output
import pyarrow as pa
import os
 

def main():

    agent = MofaAgent(agent_name='mofa-agent')
    while True:
        agent.receive_parameter()
        print('agent_inputs : ',agent.agent_inputs)
        # TODO: 在下面添加你的Agent代码,其中agent_inputs是你的Agent的需要输入的参数
        # reasoner = ReasonerAgent(config_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/configs/config.yml',
        #                     llm_config_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/.env.secret')
        # result = reasoner.run(**agent.agent_inputs)
        # print('reasoner_result : ',result)
        result = 'agent_result' #
        agent_output_name = 'reasoner_result'
        agent.send_output(agent_output_name=agent_output_name,agent_result=result)
if __name__ == "__main__":
    main()
