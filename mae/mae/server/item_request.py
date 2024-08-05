from pydantic import BaseModel
from datetime import datetime
from typing import Union

# 定义用于存储 API 请求格式的类
class AgentDataflow(BaseModel):
    agent_name: str

class AgentNodeConfig(AgentDataflow):
    node_id: str

class RunAgent(AgentDataflow):
    agent_path: str = None