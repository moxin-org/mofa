"""
封装对 MoFA CLI 命令的调用
"""
import os
import subprocess
import json
import shutil
from pathlib import Path
import sys

class MofaCLI:
    def __init__(self, settings=None):
        import sys
        import os
        # 添加项目根目录到 Python 路径
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from config import DEFAULT_MOFA_ENV, DEFAULT_MOFA_DIR, AGENT_STORAGE_OPTIONS, DEFAULT_AGENT_STORAGE, USE_SYSTEM_MOFA
        
        self.settings = settings or {}
        self.mofa_env_path = self.settings.get('mofa_env_path', DEFAULT_MOFA_ENV)
        self.mofa_dir = self.settings.get('mofa_dir', DEFAULT_MOFA_DIR)
        self.use_system_mofa = self.settings.get('use_system_mofa', USE_SYSTEM_MOFA)
        
        # 设置Agent存储路径
        agent_storage = self.settings.get('agent_storage', DEFAULT_AGENT_STORAGE)
        custom_path = self.settings.get('custom_agent_path', '')
        
        if agent_storage == 'custom' and custom_path:
            # 使用用户提供的自定义路径
            self.agents_dir = custom_path
        else:
            # 使用预定义的路径
            relative_path = AGENT_STORAGE_OPTIONS.get(agent_storage, AGENT_STORAGE_OPTIONS[DEFAULT_AGENT_STORAGE])
            self.agents_dir = os.path.join(self.mofa_dir, relative_path)
            
        # 创建agent目录如果不存在
        os.makedirs(self.agents_dir, exist_ok=True)
        
        # 存储所有可能的agent目录路径，用于搜索agent
        self.possible_agent_dirs = [self.agents_dir]  # 当前配置的路径
        
        # 添加所有配置项中的路径
        for storage_key, rel_path in AGENT_STORAGE_OPTIONS.items():
            if rel_path:  # 如果不是空路径
                full_path = os.path.join(self.mofa_dir, rel_path)
                if full_path not in self.possible_agent_dirs:
                    self.possible_agent_dirs.append(full_path)
        
        # 如果存在自定义路径，也添加到搜索路径中
        if custom_path and os.path.exists(custom_path) and custom_path not in self.possible_agent_dirs:
            self.possible_agent_dirs.append(custom_path)
        
        # 根据设置决定是否使用系统命令或虚拟环境
        if self.use_system_mofa:
            # 使用系统安装的mofa
            self.mofa_cmd = "mofa"
            self.activate_cmd = ""
        else:
            # 使用虚拟环境
            self.activate_cmd = f"source {self.mofa_env_path}/bin/activate"
            self.mofa_cmd = "mofa"
            
            # 检查MOFA环境是否存在
            if not os.path.exists(self.mofa_env_path):
                print(f"警告: 指定的MoFA环境路径不存在: {self.mofa_env_path}")
                
        if not os.path.exists(self.mofa_dir):
            print(f"警告: 指定的MoFA目录不存在: {self.mofa_dir}")
            
        # 检查mofa命令是否可用
        if self.use_system_mofa:
            if not shutil.which("mofa"):
                print("警告: 系统中找不到mofa命令，请确保已安装")
    
    def _run_command(self, command, cwd=None):
        """运行shell命令并返回输出"""
        # 替换命令中的mofa为正确的命令
        command = command.replace("mofa", self.mofa_cmd)
        
        try:
            # 使用系统安装的MOFA
            if self.use_system_mofa:
                print(f"使用系统MOFA执行: {command}")
                result = subprocess.run(
                    command,
                    shell=True,
                    executable="/bin/bash",
                    check=False,
                    text=True,
                    capture_output=True,
                    cwd=cwd or self.mofa_dir
                )
                
                if result.returncode == 0:
                    return result.stdout.strip()
                else:
                    print(f"系统命令执行失败，返回码: {result.returncode}")
                    print(f"错误输出: {result.stderr}")
            
            # 如果使用虚拟环境或者系统命令失败，尝试虚拟环境方式
            if not self.use_system_mofa or result.returncode != 0:
                # 方法1: 使用bash执行source命令
                full_cmd = f"{self.activate_cmd} && {command}" if self.activate_cmd else command
                print(f"执行虚拟环境命令: {full_cmd}")
                
                venv_result = subprocess.run(
                    full_cmd,
                    shell=True,
                    executable="/bin/bash",  # 明确使用bash而不是sh
                    check=False,
                    text=True,
                    capture_output=True,
                    cwd=cwd or self.mofa_dir
                )
                
                if venv_result.returncode == 0:
                    return venv_result.stdout.strip()
                else:
                    print(f"虚拟环境命令执行失败，返回码: {venv_result.returncode}")
                    print(f"错误输出: {venv_result.stderr}")
                    
                    # 方法2: 直接使用虚拟环境中的Python解释器
                    python_executable = os.path.join(self.mofa_env_path, "bin", "python")
                    if os.path.exists(python_executable):
                        mofa_mod_cmd = command.replace(self.mofa_cmd, "-m mofa.cli")
                        alt_cmd = f"{python_executable} {mofa_mod_cmd}"
                        print(f"执行替代命令: {alt_cmd}")
                        
                        py_result = subprocess.run(
                            alt_cmd,
                            shell=True,
                            check=False,
                            text=True, 
                            capture_output=True,
                            cwd=cwd or self.mofa_dir
                        )
                        
                        if py_result.returncode == 0:
                            return py_result.stdout.strip()
                        else:
                            print(f"替代命令也失败了，返回码: {py_result.returncode}")
                            print(f"错误输出: {py_result.stderr}")
            
            # 所有方法都失败，返回空字符串
            print("所有方法都失败，将尝试使用文件系统操作")
            return ""
        except Exception as e:
            print(f"执行命令时出错: {e}")
            return ""
    
    def list_agents(self):
        """获取所有 agent 列表，从多个可能的目录扫描"""
        try:
            # 输出当前使用的目录和设置
            print(f"Current agents_dir = {self.agents_dir}")
            print(f"Current settings: use_system_mofa = {self.use_system_mofa}, mofa_dir = {self.mofa_dir}")
            
            agents = set()  # 使用集合避免重复
            cli_success = False
            
            # 1. 先尝试使用 mofa CLI 命令
            try:
                output = self._run_command("mofa agent-list")
                
                # 如果命令成功，解析输出
                if output:
                    for line in output.split("\n"):
                        if line.startswith("[") and line.endswith("]"):
                            # 解析 agent 列表
                            agents_text = line.strip("[]").replace("'", "").replace(" ", "")
                            cli_agents = [agent for agent in agents_text.split(",") if agent]
                            agents.update(cli_agents)
                            cli_success = True
                            print(f"CLI 命令成功获取到 {len(cli_agents)} 个 agents: {cli_agents}")
                            break
            except Exception as cli_err:
                print(f"CLI 命令出错: {cli_err}")
            
            # 2. 不管CLI命令是否成功，都尝试扫描所有可能的目录
            print(f"将根据以下路径扫描 Agent: {self.possible_agent_dirs}")
            
            # 迭代所有可能的目录
            for agent_dir in self.possible_agent_dirs:
                if os.path.exists(agent_dir) and os.path.isdir(agent_dir):
                    try:
                        # 获取目录下的所有文件夹
                        for item in os.listdir(agent_dir):
                            item_path = os.path.join(agent_dir, item)
                            if os.path.isdir(item_path) and not item.startswith('.'):
                                agents.add(item)
                        print(f"从 {agent_dir} 读取到 Agent。当前总计: {len(agents)}个")
                    except Exception as dir_err:
                        print(f"读取目录 {agent_dir} 时出错: {dir_err}")
                else:
                    print(f"目录不存在或无法访问: {agent_dir}")
            
            # 将集合转为列表并排序
            agents_list = sorted(list(agents))
            print(f"最终找到 {len(agents_list)} 个 agents: {agents_list}")
            
            # 如果没有找到任何agent，返回一些默认示例
            if not agents_list:
                default_agents = ["hello_world", "reasoner", "memory", "rag"]
                print(f"未找到任何 agent，返回默认示例: {default_agents}")
                return default_agents
                
            return agents_list
            
        except Exception as e:
            import traceback
            print(f"Error listing agents: {e}")
            print(traceback.format_exc())
            # 在出错时返回一些默认的 agent 示例
            return ["hello_world", "reasoner", "memory", "rag"]
    
    def get_agent_details(self, agent_name):
        """获取特定 agent 的详细信息"""
        # 首先尝试在当前配置的agent目录中查找
        agent_path = os.path.join(self.agents_dir, agent_name)
        
        # 如果在当前配置的目录中找不到，则尝试在所有可能的目录中查找
        if not os.path.exists(agent_path):
            for possible_dir in self.possible_agent_dirs:
                possible_path = os.path.join(possible_dir, agent_name)
                if os.path.exists(possible_path):
                    agent_path = possible_path
                    break
        
        if not os.path.exists(agent_path):
            return None
        
        # 获取 agent 的基本信息
        details = {
            "name": agent_name,
            "path": agent_path,
            "files": self._get_agent_files(agent_path),
        }
        
        # 尝试读取 README.md 获取描述
        readme_path = os.path.join(agent_path, "README.md")
        if os.path.exists(readme_path):
            with open(readme_path, "r") as f:
                details["description"] = f.read()
        
        return details
    
    def _get_agent_files(self, agent_path):
        """获取 agent 目录下的所有文件"""
        files = []
        for root, _, filenames in os.walk(agent_path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                rel_path = os.path.relpath(file_path, agent_path)
                files.append({
                    "name": filename,
                    "path": rel_path,
                    "type": os.path.splitext(filename)[1][1:] or "txt"
                })
        return files
    
    def create_agent(self, agent_name, version="0.0.1", authors="MoFA_Stage User"):
        """创建一个新的 agent"""
        try:
            # 确保目录存在
            output_dir = os.path.dirname(self.agents_dir) if not self.agents_dir.endswith('/agent-hub') and not self.agents_dir.endswith('/examples') else self.agents_dir
            os.makedirs(output_dir, exist_ok=True)
            
            cmd = f"mofa new-agent {agent_name} --version {version} --output {output_dir} --authors \"{authors}\""
            result = self._run_command(cmd)
            
            if not result:
                # 命令失败，尝试手动创建一个基本agent目录
                print(f"尝试手动创建基本agent目录: {agent_name}")
                agent_dir = os.path.join(self.agents_dir, agent_name)
                
                if not os.path.exists(agent_dir):
                    os.makedirs(agent_dir, exist_ok=True)
                    
                    # 创建一个基本的README.md
                    readme_path = os.path.join(agent_dir, "README.md")
                    with open(readme_path, "w") as f:
                        f.write(f"# {agent_name} Agent\n\nCreated by {authors}\nVersion: {version}\n\nThis is a basic agent template.")
                    
                    # 创建一个基本的dataflow配置
                    dataflow_path = os.path.join(agent_dir, f"{agent_name}_dataflow.yml")
                    with open(dataflow_path, "w") as f:
                        f.write(f"# {agent_name} Agent Dataflow Configuration\n\nname: {agent_name}\nversion: {version}\n\nnodes: []\n\nlinks: []")
                        
                    return {"success": True, "message": f"Created basic agent structure for {agent_name}"}
                else:
                    return {"success": False, "message": f"Agent directory already exists: {agent_name}"}
            
            return {"success": True, "message": result}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def run_agent(self, agent_name, timeout=5):
        """运行指定的 agent（非阻塞方式）
        这个方法仅启动 agent，然后在指定时间后返回
        实际应用中，应该通过 WebSocket 或其他方式实时返回输出
        """
        try:
            # 这里仅模拟启动，实际应用需要更复杂的进程管理
            cmd = f"cd {self.mofa_dir} && mofa run --agent-name {agent_name}"
            # 在后台运行，以便不阻塞 API 响应
            process = subprocess.Popen(
                cmd, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            
            # 仅等待 timeout 秒，然后返回进程 ID
            return {
                "success": True, 
                "message": f"Agent {agent_name} started", 
                "process_id": process.pid
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def stop_agent(self, process_id):
        """停止正在运行的 agent 进程"""
        try:
            cmd = f"kill {process_id}"
            self._run_command(cmd)
            return {"success": True, "message": f"Agent process {process_id} stopped"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def delete_agent(self, agent_name):
        """删除指定的 agent"""
        try:
            agent_path = os.path.join(self.agents_dir, agent_name)
            if not os.path.exists(agent_path):
                return {"success": False, "message": f"Agent {agent_name} not found"}
            
            # 递归删除目录
            import shutil
            shutil.rmtree(agent_path)
            return {"success": True, "message": f"Agent {agent_name} deleted"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def copy_agent(self, source_agent, target_agent):
        """复制一个 agent 作为新的 agent"""
        try:
            # 输出日志以便于调试
            print(f"尝试复制 Agent {source_agent} 到 {target_agent}")
            print(f"agents_dir = {self.agents_dir}")
            
            # 处理源和目标路径
            source_path = os.path.join(self.agents_dir, source_agent)
            target_path = os.path.join(self.agents_dir, target_agent)
            
            print(f"source_path = {source_path}")
            print(f"target_path = {target_path}")
            
            # 检查源路径是否存在
            if not os.path.exists(source_path):
                print(f"错误: 源 Agent 路径不存在: {source_path}")
                
                # 尝试在其他可能的目录中查找
                other_locations = []
                
                # 导入配置文件中的AGENT_STORAGE_OPTIONS
                import sys
                sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                from config import AGENT_STORAGE_OPTIONS
                
                for key, rel_path in AGENT_STORAGE_OPTIONS.items():
                    other_path = os.path.join(self.mofa_dir, rel_path, source_agent)
                    other_locations.append(other_path)
                    if os.path.exists(other_path):
                        print(f"在其他位置找到了源 Agent: {other_path}")
                        source_path = other_path
                        target_path = os.path.join(self.agents_dir, target_agent)  # 目标仍然写到选定的存储位置
                        break
                
                if not os.path.exists(source_path):
                    return {"success": False, "message": f"Source agent '{source_agent}' not found. Searched in: {source_path} and {other_locations}"}
            
            # 检查目标路径是否已存在
            if os.path.exists(target_path):
                return {"success": False, "message": f"Target agent '{target_agent}' already exists at {target_path}"}
            
            # 创建目标目录的父目录（如果不存在）
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            # 复制目录
            import shutil
            print(f"正在复制: {source_path} -> {target_path}")
            shutil.copytree(source_path, target_path)
            
            # 更新配置文件中的名称
            self._update_agent_name_in_files(target_path, source_agent, target_agent)
            
            return {"success": True, "message": f"Agent '{source_agent}' successfully copied to '{target_agent}'"}
        except Exception as e:
            import traceback
            trace = traceback.format_exc()
            print(f"复制 Agent 时出错: {str(e)}\n{trace}")
            return {"success": False, "message": f"Failed to copy agent: {str(e)}"}
    
    def get_agent_logs(self, agent_name):
        """获取指定agent的运行日志
        尝试从以下位置获取日志：
        1. agent目录下的logs子目录
        2. agent目录下的out目录及其子目录
        3. MoFA目录下的logs子目录中与agent相关的日志
        4. 系统临时目录中可能的日志文件
        """
        try:
            agent_path = os.path.join(self.agents_dir, agent_name)
            if not os.path.exists(agent_path):
                return None
            
            # 可能的日志位置
            log_locations = [
                # 1. agent目录下的logs子目录
                os.path.join(agent_path, "logs"),
                # 2. agent目录下直接的log文件
                os.path.join(agent_path, f"{agent_name}.log"),
                # 3. MoFA目录下的logs子目录
                os.path.join(self.mofa_dir, "logs", f"{agent_name}.log"),
                # 4. MoFA目录下的通用logs目录
                os.path.join(self.mofa_dir, "logs")
            ]
            
            logs_content = []
            
            # 检查agent目录下的out目录
            out_dir = os.path.join(agent_path, "out")
            if os.path.exists(out_dir) and os.path.isdir(out_dir):
                # 检查dora-daemon.txt文件
                daemon_log = os.path.join(out_dir, "dora-daemon.txt")
                if os.path.exists(daemon_log) and os.path.isfile(daemon_log):
                    try:
                        with open(daemon_log, "r") as f:
                            # 只读取最后200行，避免文件过大
                            lines = f.readlines()
                            content = "".join(lines[-200:] if len(lines) > 200 else lines)
                            if content:
                                logs_content.append(f"=== Dora Daemon 日志 ===\n{content}\n")
                    except Exception as e:
                        logs_content.append(f"无法读取Dora Daemon日志: {str(e)}")
                
                # 检查dora-coordinator.txt文件
                coordinator_log = os.path.join(out_dir, "dora-coordinator.txt")
                if os.path.exists(coordinator_log) and os.path.isfile(coordinator_log):
                    try:
                        with open(coordinator_log, "r") as f:
                            # 只读取最后200行，避免文件过大
                            lines = f.readlines()
                            content = "".join(lines[-200:] if len(lines) > 200 else lines)
                            if content:
                                logs_content.append(f"=== Dora Coordinator 日志 ===\n{content}\n")
                    except Exception as e:
                        logs_content.append(f"无法读取Dora Coordinator日志: {str(e)}")
                
                # 检查out目录下的其他日志文件
                for file in os.listdir(out_dir):
                    file_path = os.path.join(out_dir, file)
                    # 只处理文件，不处理目录
                    if os.path.isfile(file_path) and file != "dora-daemon.txt" and file != "dora-coordinator.txt":
                        # 检查是否是日志文件（有文本扩展名或包含“log”或“日志”字样）
                        if file.endswith(".txt") or file.endswith(".log") or "log" in file.lower() or "日志" in file:
                            try:
                                with open(file_path, "r") as f:
                                    # 只读取最后100行，避免文件过大
                                    lines = f.readlines()
                                    content = "".join(lines[-100:] if len(lines) > 100 else lines)
                                    if content:
                                        logs_content.append(f"=== {file} ===\n{content}\n")
                            except Exception as e:
                                logs_content.append(f"无法读取日志文件 {file}: {str(e)}")
                
                # 查找运行实例目录（UUID格式的目录）
                instance_dirs = []
                for item in os.listdir(out_dir):
                    item_path = os.path.join(out_dir, item)
                    # 检查是否是目录且看起来像UUID（包含连字符且长度合适）
                    if os.path.isdir(item_path) and "-" in item and len(item) > 30:
                        instance_dirs.append(item_path)
                
                # 按修改时间排序，最新的排在前面
                instance_dirs.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                
                # 处理所有实例目录
                for instance_dir in instance_dirs:
                    # 查找agent日志文件
                    agent_log_pattern = f"log_{agent_name}*.txt"
                    agent_logs = []
                    
                    # 使用glob模式查找匹配的日志文件
                    for root, _, files in os.walk(instance_dir):
                        for file in files:
                            if file.startswith(f"log_{agent_name}") or file.startswith("log_") and "agent" in file.lower():
                                agent_logs.append(os.path.join(root, file))
                    
                    # 处理找到的日志文件
                    for log_file in agent_logs:
                        try:
                            with open(log_file, "r") as f:
                                # 只读取最后100行，避免文件过大
                                lines = f.readlines()
                                content = "".join(lines[-100:] if len(lines) > 100 else lines)
                                if content:
                                    instance_name = os.path.basename(instance_dir)
                                    file_name = os.path.basename(log_file)
                                    logs_content.append(f"=== 运行实例 {instance_name} - {file_name} ===\n{content}\n")
                        except Exception as e:
                            logs_content.append(f"无法读取实例日志 {log_file}: {str(e)}")
            
            # 遍历所有可能的日志位置
            for location in log_locations:
                if os.path.exists(location):
                    if os.path.isdir(location):
                        # 如果是目录，查找与agent相关的所有日志文件
                        log_files = []
                        for file in os.listdir(location):
                            if file.endswith(".log") and (agent_name in file or "agent" in file.lower()):
                                log_files.append(os.path.join(location, file))
                        
                        # 按修改时间排序，最新的日志排在前面
                        log_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                        
                        # 读取最新的几个日志文件
                        for log_file in log_files[:3]:  # 最多读取3个最新的日志文件
                            try:
                                with open(log_file, "r") as f:
                                    content = f.read()
                                    if content:
                                        logs_content.append(f"=== {os.path.basename(log_file)} ===\n{content}\n")
                            except Exception as e:
                                logs_content.append(f"无法读取日志文件 {log_file}: {str(e)}")
                    else:
                        # 如果是文件，直接读取
                        try:
                            with open(location, "r") as f:
                                content = f.read()
                                if content:
                                    logs_content.append(f"=== {os.path.basename(location)} ===\n{content}")
                        except Exception as e:
                            logs_content.append(f"无法读取日志文件 {location}: {str(e)}")
            
            # 尝试读取所有正在运行的进程，替代使用self.runningAgents
            if not logs_content:
                try:
                    # 尝试查找与agent相关的正在运行的进程
                    cmd = f"ps aux | grep -v grep | grep mofa | grep {agent_name} | head -n 1"
                    process_info = self._run_command(cmd)
                    
                    if process_info:
                        logs_content.append(f"当前运行进程信息:\n{process_info}\n")
                        
                        # 提取进程ID
                        process_parts = process_info.split()
                        if len(process_parts) > 1:
                            process_id = process_parts[1]  # 第二列通常是进程ID
                            
                            # 尝试获取进程最近的输出
                            cmd = f"tail -n 50 /proc/{process_id}/fd/1 2>/dev/null || echo '无法读取进程输出'"
                            process_output = self._run_command(cmd)
                            if process_output and process_output != '无法读取进程输出':
                                logs_content.append(f"进程输出:\n{process_output}")
                except Exception as e:
                    logs_content.append(f"无法获取进程信息: {str(e)}")
            
            # 如果仍然没有找到日志，返回一个默认消息
            if not logs_content:
                logs_content.append(f"未找到 {agent_name} 的日志文件。可能是该Agent还未运行过。")
            
            return "\n\n".join(logs_content)
        except Exception as e:
            print(f"获取agent日志时出错: {e}")
            return f"获取日志时发生错误: {str(e)}"
    
    def _update_agent_name_in_files(self, agent_path, old_name, new_name):
        """在复制的 agent 文件中更新名称"""
        for root, _, filenames in os.walk(agent_path):
            for filename in filenames:
                if filename.endswith(('.py', '.yml', '.yaml', '.toml', '.md')):
                    file_path = os.path.join(root, filename)
                    try:
                        with open(file_path, 'r') as f:
                            content = f.read()
                        
                        # 替换名称
                        content = content.replace(old_name, new_name)
                        
                        with open(file_path, 'w') as f:
                            f.write(content)
                    except Exception as e:
                        print(f"Error updating file {file_path}: {e}")
    
    def read_file(self, agent_name, file_path):
        """读取 agent 文件内容"""
        # 首先尝试在当前配置的agent目录中查找
        full_path = os.path.join(self.agents_dir, agent_name, file_path)
        
        # 如果在当前配置的目录中找不到，则尝试在所有可能的目录中查找
        if not os.path.exists(full_path):
            for possible_dir in self.possible_agent_dirs:
                possible_path = os.path.join(possible_dir, agent_name, file_path)
                if os.path.exists(possible_path):
                    full_path = possible_path
                    break
        
        if not os.path.exists(full_path):
            return {"success": False, "message": f"File {file_path} not found"}
        
        try:
            with open(full_path, 'r') as f:
                content = f.read()
            return {"success": True, "content": content}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def write_file(self, agent_name, file_path, content):
        """写入 agent 文件内容"""
        # 首先尝试在当前配置的agent目录中查找agent
        agent_path = os.path.join(self.agents_dir, agent_name)
        
        # 如果在当前配置的目录中找不到，则尝试在所有可能的目录中查找
        if not os.path.exists(agent_path):
            for possible_dir in self.possible_agent_dirs:
                possible_path = os.path.join(possible_dir, agent_name)
                if os.path.exists(possible_path):
                    agent_path = possible_path
                    break
        
        # 如果仍然找不到，则使用当前配置的目录创建新的agent
        if not os.path.exists(agent_path):
            agent_path = os.path.join(self.agents_dir, agent_name)
            os.makedirs(agent_path, exist_ok=True)
        
        full_path = os.path.join(agent_path, file_path)
        dir_path = os.path.dirname(full_path)
        
        try:
            # 确保目录存在
            os.makedirs(dir_path, exist_ok=True)
            
            with open(full_path, 'w') as f:
                f.write(content)
            return {"success": True, "message": f"File {file_path} saved"}
        except Exception as e:
            return {"success": False, "message": str(e)}
