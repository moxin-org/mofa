import json
from dora import Node, DoraStatus
import pyarrow as pa

from mofa.kernel.utils.log import write_agent_log
from mofa.kernel.utils.util import load_agent_config
from mofa.run.run_agent import run_dspy_agent, run_crewai_agent
from mofa.utils.files.read import read_yaml



class Operator:
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            if dora_event["id"] == "task":
                task = json.loads(dora_event["value"][0].as_py())
                yaml_file_path = 'use_case/web_search_agent.yml'
                inputs = load_agent_config(yaml_file_path)
                if inputs.get('check_log_prompt', None) is True:
                    log_config = {}
                    agent_config =  read_yaml(yaml_file_path).get('AGENT', '')
                    agent_config['task'] = task
                    log_config['1 , Web_Search_Config'] = agent_config
                    write_agent_log(log_type=inputs.get('log_type', None), log_file_path=inputs.get('log_path', None),
                                    data=log_config)
                result = """
                                """
                if 'agents' not in inputs.keys():
                    inputs['task'] = task
                    result = run_dspy_agent(agent_config=inputs)
                else:
                    result = run_crewai_agent(crewai_config=inputs)
                # log_result = {"2, Web Search Resource":{d.get('name'):d.get('url')  for d in json.loads(,'3, Web Search Answer':result.get('answer')}
                log_result = {'2, Web Search Resource ' :{d.get('name'):d.get('url') for d in json.loads(result.get('web_search_resource'))}}
                log_result['3, Web Search Answer '] = result.get('web_search_results')
                write_agent_log(log_type=inputs.get('log_type',None),log_file_path=inputs.get('log_path',None),data=log_result)
                result['task'] = task
                print(result)
                send_output("web_search_result", pa.array([json.dumps(result)]),dora_event['metadata'])
                return DoraStatus.STOP

        return DoraStatus.CONTINUE