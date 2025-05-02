"""
数据流 API 路由
"""
import os
import json
from flask import Blueprint, jsonify, request, current_app
import threading
import asyncio

from models.dataflow import DataFlow, DataFlowManager
from utils.dataflow_engine import DataFlowExecutor

# 创建蓝图
dataflows_bp = Blueprint('dataflows', __name__, url_prefix='/api/dataflows')

# 获取基础目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENTS_DIR = os.path.join(BASE_DIR, "agents")

# 初始化数据流管理器
dataflow_manager = DataFlowManager(BASE_DIR)

# 存储正在运行的数据流执行器
active_executors = {}

@dataflows_bp.route('/', methods=['GET'])
def list_dataflows():
    """获取所有数据流列表"""
    try:
        flows = dataflow_manager.list_flows()
        return jsonify({"success": True, "flows": flows})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@dataflows_bp.route('/', methods=['POST'])
def create_dataflow():
    """创建新的数据流"""
    try:
        data = request.json
        name = data.get("name")
        description = data.get("description")
        
        flow = dataflow_manager.create_flow(name, description)
        
        return jsonify({"success": True, "flow": flow.to_dict()})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@dataflows_bp.route('/<flow_id>', methods=['GET'])
def get_dataflow(flow_id):
    """获取指定数据流的详细信息"""
    try:
        flow = dataflow_manager.get_flow(flow_id)
        if not flow:
            return jsonify({"success": False, "message": f"DataFlow {flow_id} not found"}), 404
        
        return jsonify({"success": True, "flow": flow.to_dict()})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@dataflows_bp.route('/<flow_id>', methods=['PUT'])
def update_dataflow(flow_id):
    """更新数据流"""
    try:
        data = request.json
        flow = dataflow_manager.get_flow(flow_id)
        if not flow:
            return jsonify({"success": False, "message": f"DataFlow {flow_id} not found"}), 404
        
        # 更新基本信息
        if "name" in data:
            flow.name = data["name"]
        if "description" in data:
            flow.description = data["description"]
        
        # 更新节点和连接
        if "nodes" in data:
            flow.nodes = data["nodes"]
        if "connections" in data:
            flow.connections = data["connections"]
        
        # 保存更新
        dataflow_manager.update_flow(flow)
        
        return jsonify({"success": True, "flow": flow.to_dict()})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@dataflows_bp.route('/<flow_id>', methods=['DELETE'])
def delete_dataflow(flow_id):
    """删除数据流"""
    try:
        # 检查数据流是否正在运行
        if flow_id in active_executors:
            return jsonify({"success": False, "message": f"DataFlow {flow_id} is currently running"}), 400
        
        success = dataflow_manager.delete_flow(flow_id)
        if not success:
            return jsonify({"success": False, "message": f"DataFlow {flow_id} not found"}), 404
        
        return jsonify({"success": True, "message": f"DataFlow {flow_id} deleted"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@dataflows_bp.route('/<flow_id>/nodes', methods=['POST'])
def add_node(flow_id):
    """向数据流添加节点"""
    try:
        data = request.json
        flow = dataflow_manager.get_flow(flow_id)
        if not flow:
            return jsonify({"success": False, "message": f"DataFlow {flow_id} not found"}), 404
        
        agent_name = data.get("agent_name")
        if not agent_name:
            return jsonify({"success": False, "message": "agent_name is required"}), 400
        
        node_id = data.get("node_id")
        position = data.get("position")
        config = data.get("config")
        
        node_id = flow.add_node(agent_name, node_id, position, config)
        dataflow_manager.update_flow(flow)
        
        return jsonify({"success": True, "node_id": node_id, "flow": flow.to_dict()})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@dataflows_bp.route('/<flow_id>/nodes/<node_id>', methods=['DELETE'])
def remove_node(flow_id, node_id):
    """从数据流中移除节点"""
    try:
        flow = dataflow_manager.get_flow(flow_id)
        if not flow:
            return jsonify({"success": False, "message": f"DataFlow {flow_id} not found"}), 404
        
        flow.remove_node(node_id)
        dataflow_manager.update_flow(flow)
        
        return jsonify({"success": True, "flow": flow.to_dict()})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@dataflows_bp.route('/<flow_id>/connections', methods=['POST'])
def add_connection(flow_id):
    """添加节点之间的连接"""
    try:
        data = request.json
        flow = dataflow_manager.get_flow(flow_id)
        if not flow:
            return jsonify({"success": False, "message": f"DataFlow {flow_id} not found"}), 404
        
        source_node_id = data.get("source_node_id")
        source_output = data.get("source_output")
        target_node_id = data.get("target_node_id")
        target_input = data.get("target_input")
        
        if not all([source_node_id, source_output, target_node_id, target_input]):
            return jsonify({"success": False, "message": "Missing required connection parameters"}), 400
        
        connection_id = flow.add_connection(source_node_id, source_output, target_node_id, target_input)
        dataflow_manager.update_flow(flow)
        
        return jsonify({"success": True, "connection_id": connection_id, "flow": flow.to_dict()})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@dataflows_bp.route('/<flow_id>/connections/<connection_id>', methods=['DELETE'])
def remove_connection(flow_id, connection_id):
    """移除连接"""
    try:
        flow = dataflow_manager.get_flow(flow_id)
        if not flow:
            return jsonify({"success": False, "message": f"DataFlow {flow_id} not found"}), 404
        
        flow.remove_connection(connection_id)
        dataflow_manager.update_flow(flow)
        
        return jsonify({"success": True, "flow": flow.to_dict()})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

def run_dataflow_in_thread(flow_id):
    """在线程中运行异步数据流执行"""
    async def _run_flow():
        try:
            flow = dataflow_manager.get_flow(flow_id)
            if not flow:
                print(f"Error: DataFlow {flow_id} not found")
                return
            
            executor = DataFlowExecutor(flow, AGENTS_DIR)
            active_executors[flow_id] = executor
            
            try:
                await executor.execute()
            finally:
                # 更新数据流状态
                dataflow_manager.update_flow(flow)
                
                # 从活动执行器中移除
                if flow_id in active_executors:
                    del active_executors[flow_id]
        except Exception as e:
            print(f"Error running dataflow {flow_id}: {str(e)}")
    
    # 创建新的事件循环
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # 运行异步任务
    loop.run_until_complete(_run_flow())
    loop.close()

@dataflows_bp.route('/<flow_id>/run', methods=['POST'])
def run_dataflow(flow_id):
    """运行数据流"""
    try:
        flow = dataflow_manager.get_flow(flow_id)
        if not flow:
            return jsonify({"success": False, "message": f"DataFlow {flow_id} not found"}), 404
        
        # 检查是否已经在运行
        if flow_id in active_executors:
            return jsonify({"success": False, "message": f"DataFlow {flow_id} is already running"}), 400
        
        # 在后台线程中运行数据流
        thread = threading.Thread(target=run_dataflow_in_thread, args=(flow_id,))
        thread.daemon = True
        thread.start()
        
        return jsonify({"success": True, "message": f"DataFlow {flow_id} started"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@dataflows_bp.route('/<flow_id>/stop', methods=['POST'])
def stop_dataflow(flow_id):
    """停止数据流"""
    try:
        # 检查是否正在运行
        if flow_id not in active_executors:
            return jsonify({"success": False, "message": f"DataFlow {flow_id} is not running"}), 400
        
        executor = active_executors[flow_id]
        success = executor.stop()
        
        if success:
            # 更新数据流状态
            flow = dataflow_manager.get_flow(flow_id)
            if flow:
                dataflow_manager.update_flow(flow)
            
            # 从活动执行器中移除
            del active_executors[flow_id]
            
            return jsonify({"success": True, "message": f"DataFlow {flow_id} stopped"})
        else:
            return jsonify({"success": False, "message": f"Failed to stop DataFlow {flow_id}"}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@dataflows_bp.route('/<flow_id>/status', methods=['GET'])
def get_dataflow_status(flow_id):
    """获取数据流的运行状态"""
    try:
        flow = dataflow_manager.get_flow(flow_id)
        if not flow:
            return jsonify({"success": False, "message": f"DataFlow {flow_id} not found"}), 404
        
        # 检查是否正在运行
        if flow_id in active_executors:
            executor = active_executors[flow_id]
            status = executor.get_status()
        else:
            # 返回最后一次执行的状态
            if flow.execution_history:
                status = flow.execution_history[-1]
            else:
                status = {
                    "flow_id": flow.flow_id,
                    "status": flow.status,
                    "nodes": {}
                }
        
        return jsonify({"success": True, "status": status})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
