import argparse
import json
import os
from pathlib import Path

from dora import Node
from mofa.agent_build.base.base_agent import MofaAgent
from mofa.kernel.utils.util import create_agent_output
import pyarrow as pa
import os
RUNNER_CI = True if os.getenv("CI") == "true" else False


def main():
    agent_config_dir_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/configs'
    agent_name = 'agent-template'
    agent = MofaAgent(agent_name=agent_name,
                      description_file_path = Path(os.path.join(os.path.abspath(os.path.dirname(__file__)), )).parent / 'description.json')
    while True:
        agent.receive_parameters()
        print('agent_inputs : ',agent.agent_inputs)
        # TODO: 在下面添加你的Agent代码,其中agent_inputs是你的Agent的需要输入的参数
        # reasoner = ReasonerAgent(config_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/configs/config.yml',
        #                     llm_config_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/.env.secret')
        # result = reasoner.run(**agent.agent_inputs)
        # print('reasoner_result : ',result)
        result = 'agent_result'
        agent_output_name = 'reasoner_result'
        agent.send_output(agent_output_name=agent_output_name,agent_result=result)
        agent.init_agent_inputs
if __name__ == "__main__":
    main()
