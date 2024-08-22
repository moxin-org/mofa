import click
from posthog import flush


# def read_process_output(process):
#     try:
#         while True:
#             output = process.stdout.readline().replace('Provide the data you want to send:', '')
#             if output == '' and process.poll() is not None:
#                 break
#             if output:
#                 # print(output.strip())
#                 click.echo(output.strip())
#     except Exception as e:
#
#         click.echo(f"Error reading output: {e}")
#     finally:
#         process.terminate()
#
#         click.echo("Process terminated.")

# def read_process_output(process):
#     try:
#         for line in iter(process.stdout.readline, ''):
#             if line:
#                 safe_echo(line.strip())
#             if process.poll() is not None:
#                 break
#     except Exception as e:
#         safe_echo(f"Error reading output: {e}")
#     finally:
#         process.terminate()
#         safe_echo("Output process terminated.")