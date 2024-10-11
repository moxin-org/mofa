import json
import os
import pyarrow as pa
from dora import Node, DoraStatus
import yaml
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List
from scrapegraphai.graphs import SearchGraph
from scrapegraphai.graphs import SmartScraperGraph
from mofa.utils.files.dir import get_relative_path
from mofa.kernel.utils.util import load_agent_config, load_dora_inputs_and_task, create_agent_output

# 加载配置文件的函数
def load_config(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)
# ************************************************
# Define the output schema for the graph
# ************************************************

class Project(BaseModel):
    title: str = Field(description="The title of the project")
    description: str = Field(description="The description of the project")

class Projects(BaseModel):
    projects: List[Project]
# Operator 类处理事件
class Operator:
    def __init__(self):
        # 加载配置
        yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='crawl_agent.yml')
        self.config = load_config(yaml_file_path)
        self.llm_model_instance = None
        self.smart_scraper_graph = None
    
    # for moonshot api
    def setup_llm_model(self):
        llm_config = self.config['llm']['config']
        instance_config = {
            "model": llm_config['model'],
            "openai_api_base": llm_config['openai_api_base'],
            "base_url": llm_config['base_url'],
            "api_key": llm_config['api_key'],
        }
        self.llm_model_instance = ChatOpenAI(**instance_config)

    def setup_scraper_graph(self, prompt: str, urls: List[str] = None):
        graph_config = {
            "llm": {
                "model": self.config['llm']['model'],
                "api_key": self.config['llm']['api_key'],
                "temperature": self.config['llm']['temperature']
            },
            "embeddings": {
                "model": self.config['embeddings']['model'],
            },
        }

        self.smart_scraper_graph = SmartScraperGraph(
            prompt=prompt,
            source=self.config['source'],
            config=graph_config,
        )

    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        # 处理输入事件
        if dora_event["type"] == "INPUT":
            print("hello world")
            if dora_event["id"] == "task":
                task_data = dora_event["value"][0].as_py()
                #self.setup_llm_model()
                self.setup_scraper_graph(prompt=task_data)

                # 运行 Scraper Graph
                #json_result = self.search_graph.run()
                # 运行 Scraper Graph
                json_result = self.smart_scraper_graph.run()
                result = json.dumps(json_result)
                # 发送输出
                send_output(
                    "crawl_result",
                    pa.array([create_agent_output(step_name='crawl_result', output_data=result,dataflow_status=os.getenv('IS_DATAFLOW_END',False))]),
                    dora_event['metadata']
                )
                
                print('Scraper Result:', result)

        return DoraStatus.CONTINUE
