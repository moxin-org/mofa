import json
import os
from dora import Node, DoraStatus
import pyarrow as pa
from mofa.kernel.utils.util import load_agent_config, load_dora_inputs_and_task, create_agent_output
from mofa.run.run_agent import run_dspy_agent, run_crewai_agent, run_dspy_or_crewai_agent
from mofa.utils.files.dir import get_relative_path
from mofa.utils.log.agent import record_agent_result_log
from mofa.utils.files.read import read_yaml
from mofa.utils.install_pkg.task_weaver import download_and_install_taskweaver
from mofa.utils.install_pkg.load_task_weaver_result import extract_important_content


class Operator:
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            agent_inputs = ['data','task']
            if dora_event["id"] in agent_inputs:
                task = dora_event["value"][0].as_py()
                yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='planning_agent.yml')
                agent_config = read_yaml(yaml_file_path)
                download_and_install_taskweaver(temp_dir=agent_config.get("PKG").get("PKG_INSTALL_PATH"))
                app_dir = agent_config.get("PKG").get("PKG_APP_DIR")
                from taskweaver.app.app import TaskWeaverApp
                taskweaver_config = {
  "llm.api_base": agent_config.get("MODEL").get("MODEL_API_URL"),
  "llm.api_key": agent_config.get("MODEL").get("MODEL_API_KEY"),
  "llm.model": agent_config.get("MODEL").get("MODEL_NAME")}
                taskweaver_config_path = app_dir + "/taskweaver_config.json"
                if os.path.exists(taskweaver_config_path):
                    os.remove(taskweaver_config_path)
                with open(taskweaver_config_path, 'w', encoding='utf-8') as outfile:
                    json.dump(taskweaver_config, outfile, ensure_ascii=False, indent=4)

                app = TaskWeaverApp(app_dir=app_dir)
                session = app.get_session()
                response_round = session.send_message(task)

                agent_result = response_round.to_dict()
                # agent_result = extract_important_content(agent_result)
                send_output("planning_results", pa.array([create_agent_output(step_name='planning_results', output_data=agent_result,dataflow_status=os.getenv('IS_DATAFLOW_END',True))]),dora_event['metadata'])
                print('reasoner_results:', agent_result)

        return DoraStatus.CONTINUE