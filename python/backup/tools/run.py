import subprocess

def run_command(command:str):
    """
    在本地运行指定的命令或任务，并返回输出和错误信息。

    参数:
    command (str): 要运行的命令字符串

    返回:
    dict: 包含输出和错误信息的字典
    """
    try:
        # 使用subprocess.run来执行命令
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # 返回结果
        return {
            'stdout': result.stdout.strip(),  # 标准输出
            'stderr': result.stderr.strip(),  # 错误输出
            'returncode': result.returncode    # 返回码
        }
    except Exception as e:
        return {
            'error': str(e)
        }