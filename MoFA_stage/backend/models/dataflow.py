"""
数据流模型 - 管理Agent之间的连接和数据流
"""
import os
import json
import uuid
from datetime import datetime

class DataFlow:
    def __init__(self, flow_id=None, name=None, description=None):
        self.flow_id = flow_id or str(uuid.uuid4())
        self.name = name or f"Flow-{self.flow_id[:8]}"
        self.description = description or ""
        self.nodes = []  # 代表流程中的Agent节点
        self.connections = []  # 代表节点之间的连接
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at
        self.status = "idle"  # idle, running, completed, failed
        self.execution_history = []

    def add_node(self, agent_name, node_id=None, position=None, config=None):
        """添加一个Agent节点到数据流"""
        node_id = node_id or str(uuid.uuid4())
        node = {
            "id": node_id,
            "agent_name": agent_name,
            "position": position or {"x": 0, "y": 0},
            "config": config or {},
            "inputs": [],  # 输入端口定义
            "outputs": []  # 输出端口定义
        }
        self.nodes.append(node)
        self.updated_at = datetime.now().isoformat()
        return node_id

    def add_connection(self, source_node_id, source_output, target_node_id, target_input):
        """在两个节点之间创建连接"""
        connection_id = str(uuid.uuid4())
        connection = {
            "id": connection_id,
            "source_node_id": source_node_id,
            "source_output": source_output,
            "target_node_id": target_node_id,
            "target_input": target_input
        }
        self.connections.append(connection)
        self.updated_at = datetime.now().isoformat()
        return connection_id

    def remove_node(self, node_id):
        """从数据流中移除节点及其相关连接"""
        # 移除与该节点相关的所有连接
        self.connections = [c for c in self.connections 
                           if c["source_node_id"] != node_id and c["target_node_id"] != node_id]
        
        # 移除节点
        self.nodes = [n for n in self.nodes if n["id"] != node_id]
        self.updated_at = datetime.now().isoformat()

    def remove_connection(self, connection_id):
        """移除指定的连接"""
        self.connections = [c for c in self.connections if c["id"] != connection_id]
        self.updated_at = datetime.now().isoformat()

    def to_dict(self):
        """将数据流转换为字典格式"""
        return {
            "flow_id": self.flow_id,
            "name": self.name,
            "description": self.description,
            "nodes": self.nodes,
            "connections": self.connections,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "status": self.status,
            "execution_history": self.execution_history
        }

    @classmethod
    def from_dict(cls, data):
        """从字典创建数据流对象"""
        flow = cls(
            flow_id=data.get("flow_id"),
            name=data.get("name"),
            description=data.get("description")
        )
        flow.nodes = data.get("nodes", [])
        flow.connections = data.get("connections", [])
        flow.created_at = data.get("created_at", flow.created_at)
        flow.updated_at = data.get("updated_at", flow.updated_at)
        flow.status = data.get("status", "idle")
        flow.execution_history = data.get("execution_history", [])
        return flow


class DataFlowManager:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.flows_dir = os.path.join(base_dir, "dataflows")
        os.makedirs(self.flows_dir, exist_ok=True)

    def create_flow(self, name=None, description=None):
        """创建新的数据流"""
        flow = DataFlow(name=name, description=description)
        self._save_flow(flow)
        return flow

    def get_flow(self, flow_id):
        """获取指定ID的数据流"""
        flow_path = os.path.join(self.flows_dir, f"{flow_id}.json")
        if not os.path.exists(flow_path):
            return None
        
        with open(flow_path, 'r', encoding='utf-8') as f:
            flow_data = json.load(f)
        
        return DataFlow.from_dict(flow_data)

    def list_flows(self):
        """列出所有数据流"""
        flows = []
        for filename in os.listdir(self.flows_dir):
            if filename.endswith(".json"):
                flow_id = filename[:-5]  # 移除 .json 后缀
                flow = self.get_flow(flow_id)
                if flow:
                    flows.append(flow.to_dict())
        return flows

    def update_flow(self, flow):
        """更新数据流"""
        flow.updated_at = datetime.now().isoformat()
        self._save_flow(flow)
        return flow

    def delete_flow(self, flow_id):
        """删除数据流"""
        flow_path = os.path.join(self.flows_dir, f"{flow_id}.json")
        if os.path.exists(flow_path):
            os.remove(flow_path)
            return True
        return False

    def _save_flow(self, flow):
        """保存数据流到文件"""
        flow_path = os.path.join(self.flows_dir, f"{flow.flow_id}.json")
        with open(flow_path, 'w', encoding='utf-8') as f:
            json.dump(flow.to_dict(), f, ensure_ascii=False, indent=2)
