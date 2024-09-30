import argparse
import json
import os
from dora import Node
from mofa.kernel.utils.log import write_agent_log
from mofa.kernel.utils.util import load_agent_config
from mofa.run.run_agent import run_dspy_agent, run_crewai_agent
from mofa.utils.files.read import read_yaml
import pyarrow as pa
import os
RUNNER_CI = True if os.getenv("CI") == "true" else False


def main():
    agent_config_dir_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), )
    parser = argparse.ArgumentParser(description="Beauty Context Agent")

    parser.add_argument(
        "--name",
        type=str,
        required=False,
        help="The name of the node in the dataflow.",
        default="Beauty Context",
    )
    parser.add_argument(
        "--task",
        type=str,
        required=False,
        help="Tasks required for the Reasoner agent.",
        default="",
    )

    args = parser.parse_args()
    task = os.getenv("TASK", args.task)

    node = Node(
        args.name
    )

    for event in node:
        if event["type"] == "INPUT":
            node_results = json.loads(event["value"][0].as_py())
            yaml_file_path = f'{agent_config_dir_path}/beauty_context_agent.yml'
            inputs = load_agent_config(yaml_file_path)
            result,node_returns = '',node_results.get('node_results')
            if isinstance(node_returns, dict):
                node_returns = json.dumps(node_returns)
            if 'agents' not in inputs.keys():
                inputs['input_fields'] = {'beauty_context':node_returns}
                result = run_dspy_agent(agent_config=inputs)
                print('--------  beauty_context:',result)
            node_results['node_results'] = result
            node.send_output("node_results", pa.array([json.dumps(node_results)]), event['metadata'])


if __name__ == "__main__":
    main()
