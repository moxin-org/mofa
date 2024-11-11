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
        if dora_event["type"] == "INPUT" and dora_event['id'] == "url":
            url = dora_event["value"][0].as_py()
            html_content = ''

            yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='load_url_connector_agent.yml')
            configs = load_agent_config(yaml_file_path)
            if configs["request_type"] == 'crawl4ai':
                html_content = asyncio.run(load_url_with_crawl4ai(url=url))

            if configs["request_type"] == 'selenium':
                html_content  = load_url_with_selenium(url=url,time_out=configs.get('timeout',2),*configs.get('selenium_args',[]),)
            result = {'html_content':html_content,'url':url}
            print(result)
            send_output("load_url_connector_response", pa.array([create_agent_output(step_name='load_url_connector_response', output_data=result, dataflow_status=os.getenv('IS_DATAFLOW_END', False))]), dora_event['metadata'])

        return DoraStatus.CONTINUE
