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

    agent = MofaAgent(agent_name='agent1')
    while True:
        from rich import print
        query = agent.receive_parameter('query')
        print(f" [bold magenta] {query} [/bold magenta]!", ":vampire:", locals())
        agent.send_output(agent_output_name="agent1_result",agent_result=query)
if __name__ == "__main__":
    main()

