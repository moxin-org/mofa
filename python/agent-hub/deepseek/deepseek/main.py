import argparse
import json
import os
from pathlib import Path

from dora import Node
from mofa.agent_build.base.base_agent import MofaAgent
from mofa.kernel.tools.web_search import search_web_with_serper
from mofa.kernel.utils.util import create_agent_output
import pyarrow as pa
import os
from dotenv import load_dotenv

from serper_search import agent_config_dir_path


def main():

    agent = MofaAgent(agent_name='serper_search')
    while True:
        load_dotenv(agent_config_dir_path + '/.env.secret')
        serper_result = search_web_with_serper(query=agent.receive_parameter(parameter_name='query'),subscription_key = os.getenv("SERPER_API_KEY"))
        agent.send_output(agent_output_name='serper_result',agent_result=serper_result)

if __name__ == "__main__":
    main()
