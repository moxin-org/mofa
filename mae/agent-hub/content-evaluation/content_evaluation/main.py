import argparse
import json
import os
from dora import Node
from mae.kernel.utils.log import write_agent_log
from mae.kernel.utils.util import load_agent_config
from mae.run.run import run_dspy_agent, run_crewai_agent
from mae.utils.files.read import read_yaml
import pyarrow as pa
import os
RUNNER_CI = True if os.getenv("CI") == "true" else False


def main():

    agent_config_dir_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), )

    parser = argparse.ArgumentParser(description="Content Evaluation Agent")

    parser.add_argument(
        "--name",
        type=str,
        required=False,
        help="The name of the node in the dataflow.",
        default="content_evaluation",
    )
    parser.add_argument(
        "--evaluation-data",
        type=str,
        required=False,
        help="Objects to be evaluated",
    )

    args = parser.parse_args()

    node = Node(
        args.name
    )
    for event in node:
        if event["type"] == "INPUT" and event['id'] in ['task','data','evaluation_data']:
            evaluation_data = event["value"][0].as_py()
            yaml_file_path = f'{agent_config_dir_path}/content_evaluation_agent.yml'
            inputs = load_agent_config(yaml_file_path)
            if inputs.get('check_log_prompt', None) is True:
                log_config = {}
                agent_config = read_yaml(yaml_file_path).get('AGENT', '')
                agent_config['evaluation_data'] = evaluation_data
                log_config[' Agent Prompt'] = agent_config
                write_agent_log(log_type=inputs.get('log_type', None), log_file_path=inputs.get('log_path', None),
                                data=log_config)

            if 'agents' not in inputs.keys():
                inputs['input_fields'] = {'evaluation_data':evaluation_data}
                result = run_dspy_agent(inputs=inputs)
            else:
                result = run_crewai_agent(crewai_config=inputs)
            log_result = {inputs.get('log_step_name', "Step_one"): result}
            results = {}
            write_agent_log(log_type=inputs.get('log_type', None), log_file_path=inputs.get('log_path', None),
                            data=log_result)
            results['result'] = result
            print('content_evaluation_result:', results)
            node.send_output("content_evaluation_result", pa.array([json.dumps(results)]), event['metadata'])


if __name__ == "__main__":
    main()
