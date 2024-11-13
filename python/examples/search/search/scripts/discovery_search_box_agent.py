import json
import os
from os import mkdir

from dora import Node, DoraStatus
import pyarrow as pa
import asyncio

from agent_core.connector_core import load_url_with_crawl4ai, load_url_with_selenium
from agent_core.discovery_search_box_core import find_search_box

from mofa.kernel.utils.util import load_agent_config, create_agent_output, load_node_result
from mofa.utils.ai.conn import create_openai_client
from mofa.utils.files.dir import get_relative_path
from mofa.utils.files.write import ensure_directory_exists


class Operator:
    def __init__(self):
        self.task = None

    def on_event(self, dora_event, send_output) -> DoraStatus:
        if dora_event["type"] == "INPUT" and dora_event['id'] == "load_url_connector_response":
            html_content = json.loads(load_node_result(dora_event["value"][0].as_py()))
            print('---------',type(html_content))
            yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='discovery_search_box_agent.yml')
            configs = load_agent_config(yaml_file = yaml_file_path,is_expand=True)
            print('-----------  : configs ',configs)
            os.environ["OPENAI_API_KEY"] = configs.get('model_api_key')
            llm_client = create_openai_client(api_key=configs.get('model_api_key'),**configs.get('llm_args',{}))
            url = html_content.get('url')
            is_google_url = False
            if url in ['https://google.com/', 'https://google.com']: is_google_url = True
            search_box_list = find_search_box(html_content.get('html_content'), llm_client=llm_client,is_google_url=is_google_url)
            discovery_search_box_result = {'search_box_list': search_box_list, 'html_content': html_content,'url':html_content.get('url')}
            ensure_directory_exists(configs.get('out_path'))
            with open(configs.get('out_path'), 'w', encoding='utf-8') as f:
                json.dump(discovery_search_box_result, f, ensure_ascii=False, indent=4)
            print(discovery_search_box_result)
            send_output("discovery_search_box_response", pa.array([create_agent_output(step_name='discovery_search_box_response', output_data=discovery_search_box_result, dataflow_status=os.getenv('IS_DATAFLOW_END', True))]), dora_event['metadata'])

        return DoraStatus.CONTINUE
