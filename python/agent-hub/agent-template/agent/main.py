import argparse
import json
import os
from dora import Node
from mofa.agent_build.base.base_agent import MofaAgent
from mofa.kernel.utils.util import create_agent_output
import pyarrow as pa
import os
RUNNER_CI = True if os.getenv("CI") == "true" else False


def main():
    agent_config_dir_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/configs'
    agent_name = 'agent-template'
    agent = MofaAgent(agent_name=agent_name)
    while True:
        agent.recevice_parameters()
        print('agent_inputs : ',agent.agent_inputs)
        # TODO: 在下面添加你的Agent代码
        # reasoner = ReasonerAgent(config_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/configs/config.yml',
        #                     llm_config_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/.env.secret')
        # result = reasoner.run(**agent.agent_inputs)
        # print('reasoner_result : ',result)
        result = 'agent_result'
        output_name = 'reasoner_result'
        agent.send_output(agent_output_name=output_name,agent_result=result)
        agent.init_agent_inputs
    # TODO: 在下面添加你的内容
if __name__ == "__main__":
    main()
