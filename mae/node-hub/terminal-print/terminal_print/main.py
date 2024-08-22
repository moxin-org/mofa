import argparse
import json
import os
from dora import Node
import click
RUNNER_CI = True if os.getenv("CI") == "true" else False


def main():

    # Handle dynamic nodes, ask for the name of the node in the dataflow, and the same values as the ENV variables.
    parser = argparse.ArgumentParser(description="Simple ")

    parser.add_argument(
        "--name",
        type=str,
        required=False,
        help="The name of the node in the dataflow.",
        default="terminal-print",
    )

    args = parser.parse_args()

    node = Node(
        args.name
    )  # provide the name to connect to the dataflow if dynamic node
    for event in node:
        if event["type"] == "INPUT":
            try:
                print(f" {json.loads(event['value'].to_pylist()[0])}",flush=True)
                # click.echo(json.loads(event['value'].to_pylist()[0]))
            except:
                print(f" {event['value'].to_pylist()}",flush=True)
                # click.echo(event['value'].to_pylist())



if __name__ == "__main__":
    main()