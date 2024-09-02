import argparse
import json
import os
import ast
import sys

import click
import pyarrow as pa
from dora import Node

RUNNER_CI = True if os.getenv("CI") == "true" else False




def clean_string(input_string:str):
    return input_string.encode('utf-8', 'replace').decode('utf-8')
def send_task_and_receive_data(node):
    while True:
        data = input(
            " Send You Task :  ",
        )
        node.send_output("data", pa.array([clean_string(data)]))
        event = node.next(timeout=200)
        if event is not None:
            while True:
                if event is not None:
                    node_results = json.loads(event['value'].to_pylist()[0])
                    results = node_results.get('node_results')
                    # print(f"------------------{node_results.get('step_name')}-------------------", flush=True)
                    # print(f"{node_results.get('step_name')}: {results}", flush=True)
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

    # Handle dynamic nodes, ask for the name of the node in the dataflow, and the same values as the ENV variables.
    parser = argparse.ArgumentParser(description="Simple arrow sender")

    parser.add_argument(
        "--name",
        type=str,
        required=False,
        help="The name of the node in the dataflow.",
        default="terminal-input",
    )
    parser.add_argument(
        "--data",
        type=str,
        required=False,
        help="Arrow Data as string.",
        default=None,
    )

    args = parser.parse_args()

    data = os.getenv("DATA", args.data)

    node = Node(
        args.name
    )  # provide the name to connect to the dataflow if dynamic node

    if data is None and os.getenv("DORA_NODE_CONFIG") is None:
        send_task_and_receive_data(node)


if __name__ == "__main__":
    main()
