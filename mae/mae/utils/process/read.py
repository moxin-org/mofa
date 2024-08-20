import click
from posthog import flush


def read_process_output(process):
    try:
        while True:
            output = process.stdout.readline().replace('Provide the data you want to send:', '')
            if output == '' and process.poll() is not None:
                break
            if output:
                # print(output.strip())
                click.echo(output.strip())
    except Exception as e:

        click.echo(f"Error reading output: {e}")
    finally:
        process.terminate()

        click.echo("Process terminated.")