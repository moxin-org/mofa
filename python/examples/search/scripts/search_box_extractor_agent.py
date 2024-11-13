import json
import os
from dora import Node, DoraStatus
import pyarrow as pa
from agent_core.extractor_core import extractor_search_box
from mofa.kernel.utils.util import load_agent_config, create_agent_output, load_node_result
from mofa.utils.ai.conn import create_openai_client
from mofa.utils.files.dir import get_relative_path
from mofa.utils.log.agent import record_agent_result_log


class Operator:
    def __init__(self):
        self.search_text = None
        self.search_box_connector_response = None


    def on_event(self, dora_event, send_output) -> DoraStatus:
        if dora_event["type"] == "INPUT" and dora_event['id'] == "search_box_connector_response":
            self.search_box_connector_response = json.loads(load_node_result(dora_event["value"][0].as_py()))

        if dora_event["type"] == "INPUT" and dora_event['id'] == "search_text":
            self.search_text = dora_event["value"][0].as_py()

        if self.search_box_connector_response is not None and self.search_text is not None:
            yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs',
                                               target_file_name='search_box_extractor_agent.yml')
            print('-----------    ',self.search_box_connector_response)
            configs = load_agent_config(yaml_file=yaml_file_path, is_expand=True)
            os.environ["OPENAI_API_KEY"] = configs.get('model_api_key')
            llm_client = create_openai_client(api_key=configs.get('model_api_key'), **configs.get('llm_args', {}))

            search_box_extractor_response = extractor_search_box(llm_client=llm_client,datas=self.search_box_connector_response,search_text=self.search_text,is_load_homepage=configs.get('is_load_homepage',False),home_page_html=configs.get('home_page_html',None))
            print(search_box_extractor_response)
            log_result = {
                "3, " + configs.get('log_step_name', "search_box_extractor_agent"): search_box_extractor_response}
            record_agent_result_log(agent_config={'log_path':'./data/output/log/search_box_extractor_agent.md'},
                                    agent_result=log_result)
            send_output("search_box_extractor_response", pa.array([create_agent_output(step_name='search_box_extractor_response', output_data=search_box_extractor_response, dataflow_status=os.getenv('IS_DATAFLOW_END', True))]), dora_event['metadata'])
            self.search_box_connector_response = None

        return DoraStatus.CONTINUE

