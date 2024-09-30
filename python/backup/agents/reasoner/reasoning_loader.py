import json

from dora import Node, DoraStatus
import pyarrow as pa

from mofa.kernel.utils.log import write_agent_log
from mofa.kernel.utils.util import load_agent_config
from mofa.utils.files.read import read_yaml



class Operator:
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            yaml_file = 'use_case/web_search_by_dspy.yml'
            config = load_agent_config(yaml_file)
            log_result = {}
            if config.get('check_log_prompt', None) is True:
                log_result['1 , Load_Agent_Config'] = read_yaml(yaml_file).get('AGENT','')
            write_agent_log(log_type=config.get('log_type', None), log_file_path=config.get('log_path', None),
                            data=log_result)
            if dora_event["type"] == "INPUT":
                send_output("agent_config", pa.array([json.dumps(config)]),dora_event['metadata'])
        return DoraStatus.STOP