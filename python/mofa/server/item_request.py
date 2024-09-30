from fastapi import UploadFile
from pydantic import BaseModel
from datetime import datetime
from typing import Union, List
from fastapi import FastAPI, UploadFile, File, HTTPException
from mofa.server.util import get_agent_template_dir_path


# 定义用于存储 API 请求格式的类
class AgentDataflow(BaseModel):
    agent_name: str

class AgentNodeConfig(AgentDataflow):
    node_id: str

class RunAgent(AgentDataflow):
    agent_path: str = None
    task_input: str
    is_load_node_log :bool = True
    work_dir: Union[str,None] = None

class UploadAgentNodeConfig(AgentNodeConfig):
    node_config: dict

class UploadFiles(AgentDataflow):
    files: List[UploadFile] = File(...)

class AgentEvaluation(BaseModel):
    primary_data:str
    second_data:str
    comparison_data_task:str