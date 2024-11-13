import json
import os
from dora import Node, DoraStatus
import pyarrow as pa
from agent_core.connector_core import  load_search_box
from mofa.kernel.utils.util import load_agent_config, create_agent_output
from mofa.utils.files.dir import get_relative_path



class Operator:
    def __init__(self):
        self.task = None

    def on_event(self, dora_event, send_output) -> DoraStatus:
        if dora_event["type"] == "INPUT" and dora_event['id'] == "search_text":
            search_text = dora_event["value"][0].as_py()
            yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs',
                                               target_file_name='search_box_connector_agent.yml')
            configs = load_agent_config(yaml_file=yaml_file_path)
            json_data = ''
            with open(configs.get('file_path'), 'r', encoding='utf-8') as f:
                # 读取JSON文件内容并解析为Python字典
                json_data = json.load(f)
            max_iteration = configs.get('max_iteration',3)
            for num in range(0,max_iteration):
                search_box_html_datas = load_search_box(url=json_data['url'], search_box_html_result=json_data['search_box_list'],search_text=search_text)
                if len(search_box_html_datas)>0:
                    break
            send_output("search_box_connector_response", pa.array([create_agent_output(step_name='search_box_connector_response', output_data=search_box_html_datas, dataflow_status=os.getenv('IS_DATAFLOW_END', False))]), dora_event['metadata'])
            print('-------  , ',search_box_html_datas)
        return DoraStatus.CONTINUE




# search_text = 'opea'
# yaml_file_path = '/Users/chenzi/project/zcbc/mofa/python/examples/search/data/output/discovery_search_box_agent_response.json'
# json_data = load_agent_config(yaml_file=yaml_file_path)
#
# search_box_html_datas = load_search_box(url=json_data['url'], search_box_html_result=json_data['search_box_list'],search_text=search_text)
# print(search_box_html_datas)

