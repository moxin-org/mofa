import argparse
import os
from dora import Node

from mofa.kernel.utils.util import load_agent_config, create_agent_output
from mofa.run.run_agent import run_dspy_or_crewai_agent
from mofa.utils.files.read import read_yaml
import pyarrow as pa
import os

from mofa.utils.log.agent import record_agent_prompt_log, record_agent_result_log

RUNNER_CI = True if os.getenv("CI") == "true" else False


def main():
    # 获取当前文件（即 __init__.py）的绝对路径
    agent_config_dir_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), )

    # Handle dynamic nodes, ask for the name of the node in the dataflow, and the same values as the ENV variables.
    parser = argparse.ArgumentParser(description="LLM Agent")

    parser.add_argument(
        "--name",
        type=str,
        required=False,
        help="The name of the node in the dataflow.",
        default="arrow-assert",
    )

    args = parser.parse_args()

    node = Node(
        args.name
    )  # provide the name to connect to the dataflow if dynamic node

    # assert_data = ast.literal_eval(data)

    for event in node:
        if event["type"] == "INPUT" and event['id'] in ['task','data']:
            task = event["value"][0].as_py()
            yaml_file_path = f'{agent_config_dir_path}/llm_agent.yml'
            inputs = load_agent_config(yaml_file_path)
            inputs['task'] = task
            record_agent_prompt_log(agent_config=inputs, config_file_path=yaml_file_path, log_key_name='Agent Prompt',
                                    task=task)

            agent_result = run_dspy_or_crewai_agent(agent_config=inputs)
            results = {}
            record_agent_result_log(agent_config=inputs,
                                    agent_result={inputs.get('log_step_name', "Step_one"): agent_result})

            results['task'] = task
            results['result'] = agent_result
            print('agent_output:', results)
            node.send_output("llm_results", pa.array([create_agent_output(step_name='llm_results', 
                                                                          output_data=agent_result,
                                                                          dataflow_status=os.getenv('IS_DATAFLOW_END',True))]),
                                                                          event['metadata'])

if __name__ == "__main__":
    main()
