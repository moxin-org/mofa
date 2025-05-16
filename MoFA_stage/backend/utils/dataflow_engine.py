"""
数据流执行引擎 - 负责执行Agent数据流
"""
import os
import json
import time
import asyncio
import logging
import subprocess
from datetime import datetime
from queue import Queue
from threading import Thread, Lock

from models.dataflow import DataFlow

logger = logging.getLogger(__name__)

class DataNode:
    """数据节点，代表数据流中的一个Agent实例"""
    def __init__(self, node_id, agent_name, config=None):
        self.node_id = node_id
        self.agent_name = agent_name
        self.config = config or {}
        self.process = None
        self.status = "idle"  # idle, running, completed, failed
        self.input_queues = {}  # 输入队列，键为输入端口名称
        self.output_data = {}  # 输出数据，键为输出端口名称
        self.start_time = None
        self.end_time = None
        self.error = None
        self.lock = Lock()

    def initialize(self):
        """初始化节点，创建必要的输入/输出队列"""
        # 这里可以从agent的配置中读取输入/输出端口定义
        pass

    async def run(self, input_data=None):
        """运行节点对应的Agent"""
        with self.lock:
            if self.status == "running":
                logger.warning(f"Node {self.node_id} ({self.agent_name}) is already running")
                return False
            
            self.status = "running"
            self.start_time = datetime.now().isoformat()
            self.error = None
        
        try:
            # 准备输入数据
            if input_data:
                for port, data in input_data.items():
                    if port not in self.input_queues:
                        self.input_queues[port] = Queue()
                    self.input_queues[port].put(data)
            
            # 执行Agent
            result = await self._execute_agent()
            
            # 处理输出
            if result.get("success", False):
                self.output_data = result.get("output", {})
                with self.lock:
                    self.status = "completed"
            else:
                with self.lock:
                    self.status = "failed"
                    self.error = result.get("message", "Unknown error")
                    
            self.end_time = datetime.now().isoformat()
            return result.get("success", False)
        except Exception as e:
            logger.exception(f"Error running node {self.node_id} ({self.agent_name})")
            with self.lock:
                self.status = "failed"
                self.error = str(e)
                self.end_time = datetime.now().isoformat()
            return False

    async def _execute_agent(self):
        """执行Agent的实际逻辑"""
        # 这里实现调用Agent的逻辑
        # 可以使用subprocess调用命令行，或者直接导入并调用Agent的Python代码
        
        # 示例实现：通过命令行运行Agent
        try:
            # 构建命令行参数
            cmd = ["python", "-m", f"mofa.run", self.agent_name]
            
            # 添加输入参数
            for port, queue in self.input_queues.items():
                if not queue.empty():
                    data = queue.get()
                    # 将输入数据写入临时文件
                    input_file = f"/tmp/mofa_input_{self.node_id}_{port}.json"
                    with open(input_file, 'w') as f:
                        json.dump(data, f)
                    cmd.extend(["--input", f"{port}={input_file}"])
            
            # 添加输出参数
            output_file = f"/tmp/mofa_output_{self.node_id}.json"
            cmd.extend(["--output", output_file])
            
            # 运行进程
            logger.info(f"Running agent: {' '.join(cmd)}")
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            self.process = process
            stdout, stderr = await process.communicate()
            
            # 检查进程退出状态
            if process.returncode != 0:
                logger.error(f"Agent process failed with code {process.returncode}")
                logger.error(f"STDERR: {stderr.decode()}")
                return {
                    "success": False,
                    "message": f"Agent process failed with code {process.returncode}: {stderr.decode()}"
                }
            
            # 读取输出文件
            if os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    output_data = json.load(f)
                
                # 清理临时文件
                os.remove(output_file)
                
                return {
                    "success": True,
                    "output": output_data
                }
            else:
                return {
                    "success": False,
                    "message": "Agent did not produce output file"
                }
        
        except Exception as e:
            logger.exception(f"Error executing agent {self.agent_name}")
            return {
                "success": False,
                "message": str(e)
            }

    def stop(self):
        """停止节点的执行"""
        if self.process and self.status == "running":
            try:
                self.process.terminate()
                with self.lock:
                    self.status = "stopped"
                    self.end_time = datetime.now().isoformat()
                return True
            except Exception as e:
                logger.exception(f"Error stopping node {self.node_id}")
                return False
        return False

    def get_status(self):
        """获取节点的状态信息"""
        with self.lock:
            return {
                "node_id": self.node_id,
                "agent_name": self.agent_name,
                "status": self.status,
                "start_time": self.start_time,
                "end_time": self.end_time,
                "error": self.error
            }


class DataFlowExecutor:
    """数据流执行器，负责执行整个数据流"""
    def __init__(self, flow, agents_dir):
        self.flow = flow
        self.agents_dir = agents_dir
        self.nodes = {}  # 节点实例，键为节点ID
        self.status = "idle"  # idle, running, completed, failed
        self.start_time = None
        self.end_time = None
        self.error = None
        self.lock = Lock()
        self.execution_id = f"exec_{int(time.time())}"

    async def initialize(self):
        """初始化执行器，创建所有节点实例"""
        for node_def in self.flow.nodes:
            node_id = node_def["id"]
            agent_name = node_def["agent_name"]
            config = node_def.get("config", {})
            
            node = DataNode(node_id, agent_name, config)
            node.initialize()
            self.nodes[node_id] = node
        
        return True

    async def execute(self):
        """执行整个数据流"""
        with self.lock:
            if self.status == "running":
                logger.warning(f"DataFlow {self.flow.flow_id} is already running")
                return False
            
            self.status = "running"
            self.start_time = datetime.now().isoformat()
            self.error = None
        
        try:
            # 初始化节点
            await self.initialize()
            
            # 构建依赖图
            dependencies = self._build_dependency_graph()
            
            # 找出没有依赖的起始节点
            start_nodes = [node_id for node_id, deps in dependencies.items() if not deps]
            
            # 如果没有起始节点，可能是循环依赖
            if not start_nodes:
                with self.lock:
                    self.status = "failed"
                    self.error = "No start nodes found, possible circular dependency"
                    self.end_time = datetime.now().isoformat()
                return False
            
            # 执行起始节点
            tasks = [self._execute_node(node_id) for node_id in start_nodes]
            await asyncio.gather(*tasks)
            
            # 检查所有节点是否都执行完成
            all_completed = all(node.status == "completed" for node in self.nodes.values())
            
            with self.lock:
                if all_completed:
                    self.status = "completed"
                else:
                    self.status = "failed"
                    failed_nodes = [node_id for node_id, node in self.nodes.items() if node.status == "failed"]
                    self.error = f"Some nodes failed: {', '.join(failed_nodes)}"
                
                self.end_time = datetime.now().isoformat()
            
            # 记录执行历史
            self._record_execution()
            
            return all_completed
        
        except Exception as e:
            logger.exception(f"Error executing dataflow {self.flow.flow_id}")
            with self.lock:
                self.status = "failed"
                self.error = str(e)
                self.end_time = datetime.now().isoformat()
            
            # 记录执行历史
            self._record_execution()
            
            return False

    async def _execute_node(self, node_id):
        """执行单个节点，并在完成后触发依赖节点"""
        node = self.nodes.get(node_id)
        if not node:
            logger.error(f"Node {node_id} not found")
            return False
        
        # 收集输入数据
        input_data = self._collect_input_data(node_id)
        
        # 执行节点
        success = await node.run(input_data)
        
        if success:
            # 找出依赖此节点的下游节点
            next_nodes = self._find_dependent_nodes(node_id)
            
            # 检查每个下游节点的所有依赖是否都已完成
            for next_node_id in next_nodes:
                if self._check_dependencies_completed(next_node_id):
                    # 所有依赖都已完成，可以执行此节点
                    await self._execute_node(next_node_id)
        
        return success

    def _build_dependency_graph(self):
        """构建节点依赖图"""
        dependencies = {node["id"]: set() for node in self.flow.nodes}
        
        for conn in self.flow.connections:
            target_node_id = conn["target_node_id"]
            source_node_id = conn["source_node_id"]
            dependencies[target_node_id].add(source_node_id)
        
        return dependencies

    def _find_dependent_nodes(self, node_id):
        """找出依赖指定节点的所有下游节点"""
        dependent_nodes = []
        for conn in self.flow.connections:
            if conn["source_node_id"] == node_id:
                dependent_nodes.append(conn["target_node_id"])
        return dependent_nodes

    def _check_dependencies_completed(self, node_id):
        """检查节点的所有依赖是否都已完成"""
        for conn in self.flow.connections:
            if conn["target_node_id"] == node_id:
                source_node_id = conn["source_node_id"]
                source_node = self.nodes.get(source_node_id)
                if not source_node or source_node.status != "completed":
                    return False
        return True

    def _collect_input_data(self, node_id):
        """收集节点的输入数据"""
        input_data = {}
        for conn in self.flow.connections:
            if conn["target_node_id"] == node_id:
                source_node_id = conn["source_node_id"]
                source_output = conn["source_output"]
                target_input = conn["target_input"]
                
                source_node = self.nodes.get(source_node_id)
                if source_node and source_node.status == "completed":
                    output_data = source_node.output_data.get(source_output)
                    if output_data is not None:
                        input_data[target_input] = output_data
        
        return input_data

    def stop(self):
        """停止数据流的执行"""
        with self.lock:
            if self.status != "running":
                return False
        
        # 停止所有正在运行的节点
        for node in self.nodes.values():
            if node.status == "running":
                node.stop()
        
        with self.lock:
            self.status = "stopped"
            self.end_time = datetime.now().isoformat()
        
        # 记录执行历史
        self._record_execution()
        
        return True

    def get_status(self):
        """获取数据流的状态信息"""
        with self.lock:
            status_info = {
                "flow_id": self.flow.flow_id,
                "execution_id": self.execution_id,
                "status": self.status,
                "start_time": self.start_time,
                "end_time": self.end_time,
                "error": self.error,
                "nodes": {node_id: node.get_status() for node_id, node in self.nodes.items()}
            }
        return status_info

    def _record_execution(self):
        """记录执行历史"""
        execution_record = {
            "execution_id": self.execution_id,
            "status": self.status,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "error": self.error,
            "nodes": {node_id: node.get_status() for node_id, node in self.nodes.items()}
        }
        
        self.flow.execution_history.append(execution_record)
        
        # 更新流程状态
        self.flow.status = self.status
        self.flow.updated_at = datetime.now().isoformat()
