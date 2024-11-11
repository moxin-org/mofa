import json
import os
from dora import Node, DoraStatus
import pyarrow as pa
import asyncio

from agent_core.connector_core import load_url_with_crawl4ai, load_url_with_selenium

from mofa.kernel.utils.util import load_agent_config, create_agent_output
from mofa.utils.files.dir import get_relative_path



class Operator:
    def __init__(self):
        self.task = None

    def on_event(self, dora_event, send_output) -> DoraStatus:
        if dora_event["type"] == "INPUT" and dora_event['id'] == "search_text":
            search_text = dora_event["value"][0].as_py()
            yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs',
                                               target_file_name='discovery_search_box_agent.yml')
            configs = load_agent_config(yaml_file=yaml_file_path, is_expand=True)
            file_data = ''
            with open(configs.get('file_path'), 'r', encoding='utf-8') as f:
                # 读取JSON文件内容并解析为Python字典
                file_data = json.load(f)

            result = {'html_content':html_content,'url':url}
            print(result)
            send_output("load_url_connector_response", pa.array([create_agent_output(step_name='load_url_connector_response', output_data=result, dataflow_status=os.getenv('IS_DATAFLOW_END', False))]), dora_event['metadata'])

        return DoraStatus.CONTINUE
