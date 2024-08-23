import subprocess


def stop_process(process):
    if isinstance(process,list):
        for p in process:
            p.terminate()
    else:
        process.terminate()

def stop_dora_dataflow(dataflow_name:str):
    dora_stop_process = subprocess.Popen(
        ['dora', 'stop','--name',dataflow_name],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = dora_stop_process.communicate()
    return None