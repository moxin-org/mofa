import argparse
import json
from dora import Node
from mofa.kernel.utils.log import write_agent_log
from mofa.kernel.utils.util import load_agent_config, create_agent_output
from mofa.run.run_agent import  run_dspy_or_crewai_agent
from mofa.utils.files.read import read_yaml, read_file_content
import pyarrow as pa
import os

from mofa.utils.log.agent import record_agent_prompt_log, record_agent_result_log

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
        "--primary-data",
        type=str,
        required=False,
        help="The first value to compare",
        default=None
    )

    parser.add_argument(
        "--second-data",
        type=str,
        required=False,
        help="The second value to compare",
        default=None
    )
    parser.add_argument(
        "--source-task",
        type=str,
        required=False,
        help="Evaluate the tasks corresponding to the two pieces of content.",
        default=None
    )
    args = parser.parse_args()
    node = Node(
        args.name
    )
    primary_data,second_data,source_task = args.primary_data,args.second_data,args.source_task
    for event in node:
        if event["type"] == "INPUT" :
            if event['id'] == 'primary_data': primary_data = event["value"][0].as_py()
            if event['id'] == 'second_data': second_data = event["value"][0].as_py()
            if event['id'] == 'source_task': source_task = event["value"][0].as_py()

            if source_task is not None and primary_data is not None and second_data is not None:
                primary_data = read_file_content(primary_data)
                second_data = read_file_content(second_data)
                evaluation_data = {'primary_data':primary_data,'second_data':second_data,'source_task':source_task}
                yaml_file_path = f'{agent_config_dir_path}/content_evaluation_agent.yml'
                inputs = load_agent_config(yaml_file_path)
                record_agent_prompt_log(agent_config=inputs, config_file_path=yaml_file_path, log_key_name='Agent Prompt', task=inputs.get('task'))
                inputs['input_fields'] = {'evaluation_data': json.dumps(evaluation_data,ensure_ascii=False)}
                agent_result = run_dspy_or_crewai_agent(agent_config=inputs)
                results = {}
                record_agent_result_log(agent_config=inputs,agent_result={inputs.get('log_step_name', "Step_one"): agent_result})
                results['evaluation_result'] = agent_result
                print('evaluation_result:', results)
                node.send_output("evaluation_result", pa.array([create_agent_output(step_name='content_evaluation',
                                                                                   output_data=agent_result,
                                                                                   dataflow_status=os.getenv(
                                                                                       "IS_DATAFLOW_END",
                                                                                       True))]), event['metadata'])
                primary_data,second_data,source_task = None,None,None


if __name__ == "__main__":
    main()
