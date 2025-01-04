import json
import os

from dora import Node, DoraStatus
import pyarrow as pa
from pathlib import Path

from mofa.kernel.utils.log import write_agent_log
from mofa.kernel.utils.util import load_agent_config, load_dora_inputs_and_task, create_agent_output
from mofa.run.run_agent import run_dspy_agent, run_crewai_agent, run_dspy_or_crewai_agent
from mofa.utils.files.dir import get_relative_path
from mofa.utils.files.read import read_yaml
from mofa.utils.files.util import get_all_files
from mofa.utils.log.agent import record_agent_result_log


class Operator:
    def __init__(self):
        self.search_task = None
        self.papers_info = None
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            agent_inputs = ['papers_info','search_task']
            if dora_event['id'] == 'papers_info':
                self.papers_info = dora_event["value"][0].as_py()
            if dora_event['id'] == 'search_task':
                self.search_task = dora_event["value"][0].as_py()
            if self.search_task is not None and  self.papers_info is not None:


                yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='paper_analyze_agent.yml')
                inputs = load_agent_config(yaml_file_path)

                all_result = []
                for file_path in  inputs.get('files_path'):
                    if Path(file_path).is_dir():
                        files_path = list(get_all_files(file_path))
                        for local_file_path in files_path:
                            try:
                                inputs['files_path'] = [local_file_path]
                                inputs['collection_name'] = Path(local_file_path).name
                                agent_result = run_dspy_or_crewai_agent(agent_config=inputs)

                                print(inputs)
                                all_result.append({local_file_path:agent_result})
                                print('local_file_rag_summary    : ' , {local_file_path:agent_result,'inputs':inputs})
                            except Exception as e :
                                print('pdf analysis appearance problem  :',e)
                                continue

                    else:
                        agent_result = run_dspy_or_crewai_agent(agent_config=inputs)

                        all_result.append(agent_result)

                log_result = {"3, " + inputs.get('log_step_name', "Step_one"): {k.split('/')[-1]: v for d in all_result for k, v in d.items()}}
                record_agent_result_log(agent_config=inputs,
                                        agent_result=log_result)
                send_output("paper_analyze_result", pa.array([create_agent_output(agent_name='paper_analyze_result', agent_result=json.dumps(all_result), dataflow_status=os.getenv('IS_DATAFLOW_END', False))]), dora_event['metadata'])
                self.search_task,self.papers_info = None,None
                print('agent_output:',all_result)
            return DoraStatus.CONTINUE



