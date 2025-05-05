import argparse
import json
import os
import ast
import sys

import click
import pyarrow as pa
from dora import Node
from mofa.utils.variable.util import clean_string, while_input

RUNNER_CI = True if os.getenv("CI") == "true" else False




def send_task_and_receive_data(node):
    while True:
        input_data = while_input( " Send  data :  ")
        print('------ data ----- ',input_data,)
        data = json.loads(input_data)
        print('----- data -----',data)
        if isinstance(data, dict):
            for key,value in data.items():

                node.send_output(key, pa.array([clean_string(value)]))
        event = node.next(timeout=200)
        if event is not None:
            while True:
                node_results = json.loads(event['value'].to_pylist()[0])
                results = node_results.get('node_results')
                is_dataflow_end = node_results.get('dataflow_status', False)
                if is_dataflow_end == False:
                    click.echo(f"{node_results.get('step_name','')}: {results} ",)
                else:
                    click.echo(f"{node_results.get('step_name','')}: {results} :dataflow_status",)
                sys.stdout.flush()
                if is_dataflow_end:
                    break
                event = node.next(timeout=200)
def main():

    parser = argparse.ArgumentParser(description="Simple arrow sender")

    parser.add_argument(
        "--name",
        type=str,
        required=False,
        help="The name of the node in the dataflow.",
        default="multiple-return-terminal-input",
    )
    parser.add_argument(
        "--receive-data",
        type=str,
        required=False,
        help="",
        default="multiple-return-terminal-input",
    )


    args = parser.parse_args()


    node = Node(
        args.name
    )

    if os.getenv("DORA_NODE_CONFIG") is None:
        send_task_and_receive_data(node)


if __name__ == "__main__":
    main()




