"""
数据流 API 路由
"""
import os
import json
from fastapi import APIRouter, HTTPException, BackgroundTasks
import asyncio

from ..models.dataflow import DataFlow, DataFlowManager
from ..utils.dataflow_engine import DataFlowExecutor

router = APIRouter(prefix="/api/dataflows", tags=["dataflows"])

# 获取基础目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENTS_DIR = os.path.join(BASE_DIR, "agents")

# 初始化数据流管理器
dataflow_manager = DataFlowManager(BASE_DIR)

# 存储正在运行的数据流执行器
active_executors = {}

@router.get("/")
async def list_dataflows():
    """获取所有数据流列表"""
    try:
        flows = dataflow_manager.list_flows()
        return {"success": True, "flows": flows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def create_dataflow(data: dict):
    """创建新的数据流"""
    try:
        name = data.get("name")
        description = data.get("description")
        
        flow = dataflow_manager.create_flow(name, description)
        
        return {"success": True, "flow": flow.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{flow_id}")
async def get_dataflow(flow_id: str):
    """获取指定数据流的详细信息"""
    try:
        flow = dataflow_manager.get_flow(flow_id)
        if not flow:
            raise HTTPException(status_code=404, detail=f"DataFlow {flow_id} not found")
        
        return {"success": True, "flow": flow.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{flow_id}")
async def update_dataflow(flow_id: str, data: dict):
    """更新数据流"""
    try:
        flow = dataflow_manager.get_flow(flow_id)
        if not flow:
            raise HTTPException(status_code=404, detail=f"DataFlow {flow_id} not found")
        
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
        
        return {"success": True, "flow": flow.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{flow_id}")
async def delete_dataflow(flow_id: str):
    """删除数据流"""
    try:
        # 检查数据流是否正在运行
        if flow_id in active_executors:
            raise HTTPException(status_code=400, detail=f"DataFlow {flow_id} is currently running")
        
        success = dataflow_manager.delete_flow(flow_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"DataFlow {flow_id} not found")
        
        return {"success": True, "message": f"DataFlow {flow_id} deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{flow_id}/nodes")
async def add_node(flow_id: str, data: dict):
    """向数据流添加节点"""
    try:
        flow = dataflow_manager.get_flow(flow_id)
        if not flow:
            raise HTTPException(status_code=404, detail=f"DataFlow {flow_id} not found")
        
        agent_name = data.get("agent_name")
        if not agent_name:
            raise HTTPException(status_code=400, detail="agent_name is required")
        
        node_id = data.get("node_id")
        position = data.get("position")
        config = data.get("config")
        
        node_id = flow.add_node(agent_name, node_id, position, config)
        dataflow_manager.update_flow(flow)
        
        return {"success": True, "node_id": node_id, "flow": flow.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{flow_id}/nodes/{node_id}")
async def remove_node(flow_id: str, node_id: str):
    """从数据流中移除节点"""
    try:
        flow = dataflow_manager.get_flow(flow_id)
        if not flow:
            raise HTTPException(status_code=404, detail=f"DataFlow {flow_id} not found")
        
        flow.remove_node(node_id)
        dataflow_manager.update_flow(flow)
        
        return {"success": True, "flow": flow.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{flow_id}/connections")
async def add_connection(flow_id: str, data: dict):
    """添加节点之间的连接"""
    try:
        flow = dataflow_manager.get_flow(flow_id)
        if not flow:
            raise HTTPException(status_code=404, detail=f"DataFlow {flow_id} not found")
        
        source_node_id = data.get("source_node_id")
        source_output = data.get("source_output")
        target_node_id = data.get("target_node_id")
        target_input = data.get("target_input")
        
        if not all([source_node_id, source_output, target_node_id, target_input]):
            raise HTTPException(status_code=400, detail="Missing required connection parameters")
        
        connection_id = flow.add_connection(source_node_id, source_output, target_node_id, target_input)
        dataflow_manager.update_flow(flow)
        
        return {"success": True, "connection_id": connection_id, "flow": flow.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{flow_id}/connections/{connection_id}")
async def remove_connection(flow_id: str, connection_id: str):
    """移除连接"""
    try:
        flow = dataflow_manager.get_flow(flow_id)
        if not flow:
            raise HTTPException(status_code=404, detail=f"DataFlow {flow_id} not found")
        
        flow.remove_connection(connection_id)
        dataflow_manager.update_flow(flow)
        
        return {"success": True, "flow": flow.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def run_dataflow_task(flow_id: str):
    """在后台运行数据流"""
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

@router.post("/{flow_id}/run")
async def run_dataflow(flow_id: str, background_tasks: BackgroundTasks):
    """运行数据流"""
    try:
        flow = dataflow_manager.get_flow(flow_id)
        if not flow:
            raise HTTPException(status_code=404, detail=f"DataFlow {flow_id} not found")
        
        # 检查是否已经在运行
        if flow_id in active_executors:
            raise HTTPException(status_code=400, detail=f"DataFlow {flow_id} is already running")
        
        # 在后台运行数据流
        background_tasks.add_task(run_dataflow_task, flow_id)
        
        return {"success": True, "message": f"DataFlow {flow_id} started"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{flow_id}/stop")
async def stop_dataflow(flow_id: str):
    """停止数据流"""
    try:
        # 检查是否正在运行
        if flow_id not in active_executors:
            raise HTTPException(status_code=400, detail=f"DataFlow {flow_id} is not running")
        
        executor = active_executors[flow_id]
        success = executor.stop()
        
        if success:
            # 更新数据流状态
            flow = dataflow_manager.get_flow(flow_id)
            if flow:
                dataflow_manager.update_flow(flow)
            
            # 从活动执行器中移除
            del active_executors[flow_id]
            
            return {"success": True, "message": f"DataFlow {flow_id} stopped"}
        else:
            raise HTTPException(status_code=500, detail=f"Failed to stop DataFlow {flow_id}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{flow_id}/status")
async def get_dataflow_status(flow_id: str):
    """获取数据流的运行状态"""
    try:
        flow = dataflow_manager.get_flow(flow_id)
        if not flow:
            raise HTTPException(status_code=404, detail=f"DataFlow {flow_id} not found")
        
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
        
        return {"success": True, "status": status}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
