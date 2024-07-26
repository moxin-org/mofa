from mae.kernel.utils.log import write_agent_log
from mae.utils.files.read import read_yaml


def record_agent_prompt_log(inputs:dict,config_file_path:str,log_key_name:str='Agent Prompt',task:str=None):
    log_config = {}
    agent_config = read_yaml(config_file_path).get('AGENT', '')
    if task is not None:
        agent_config['task'] = task
    log_config[log_key_name] = agent_config
    write_agent_log(log_type=inputs.get('log_type', None), log_file_path=inputs.get('log_path', None),
                    data=log_config)


