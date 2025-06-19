"""
封装对 MoFA CLI 命令的调用
"""
import os
import subprocess
import json
import shutil
import time
from pathlib import Path
import sys

class MofaCLI:
    def __init__(self, settings=None):
        import sys
        import os
        # 添加项目根目录到 Python 路径
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from config import (
            DEFAULT_MOFA_ENV, DEFAULT_MOFA_DIR, USE_SYSTEM_MOFA,
            DEFAULT_AGENT_HUB_PATH, DEFAULT_EXAMPLES_PATH,
            CUSTOM_AGENT_HUB_PATH, CUSTOM_EXAMPLES_PATH,
            AGENT_HUB_PATH, EXAMPLES_PATH,
            DEFAULT_MOFA_MODE, DEFAULT_DOCKER_CONTAINER
        )
        
        self.settings = settings or {}
        self.mofa_env_path = self.settings.get('mofa_env_path', DEFAULT_MOFA_ENV)
        # 先取 mofa_mode，之后才能根据它设置 mofa_dir 默认值
        self.mofa_mode = self.settings.get('mofa_mode', DEFAULT_MOFA_MODE)
        self.mofa_dir = self.settings.get('mofa_dir', DEFAULT_MOFA_DIR)
        if self.mofa_mode == 'docker' and not self.mofa_dir:
            # 默认容器内MoFA根目录
            self.mofa_dir = "/app/mofa"
        
        # 兼容旧字段 use_system_mofa（布尔）
        if 'use_system_mofa' in self.settings:
            legacy_system = self.settings.get('use_system_mofa', USE_SYSTEM_MOFA)
            if self.mofa_mode == DEFAULT_MOFA_MODE and legacy_system is not None:
                # 如果用户只设置了旧字段，则推断 mode
                self.mofa_mode = 'system' if legacy_system else 'venv'

        self.use_system_mofa = True if self.mofa_mode == 'system' else False
        # docker模式时，也把use_system_mofa设为True 以复用原有系统分支，但后续会替换 mofa_cmd
        if self.mofa_mode == 'docker':
            self.use_system_mofa = True
        
        # 设置原子化Agent（agent-hub）存储路径
        use_default_agent_hub = self.settings.get('use_default_agent_hub_path', True)
        if use_default_agent_hub:
            # 如果使用默认路径，应该是mofa_dir/python/agent-hub
            self.agent_hub_dir = os.path.join(self.mofa_dir, AGENT_HUB_PATH)
        else:
            custom_agent_hub = self.settings.get('custom_agent_hub_path', '')
            self.agent_hub_dir = custom_agent_hub if custom_agent_hub else DEFAULT_AGENT_HUB_PATH
        
        # 设置示例组合（examples）存储路径
        use_default_examples = self.settings.get('use_default_examples_path', True)
        if use_default_examples:
            # 如果使用默认路径，应该是mofa_dir/python/examples
            self.examples_dir = os.path.join(self.mofa_dir, EXAMPLES_PATH)
        else:
            custom_examples = self.settings.get('custom_examples_path', '')
            self.examples_dir = custom_examples if custom_examples else DEFAULT_EXAMPLES_PATH
            
        if self.mofa_mode != 'docker':
            try:
                agent_hub_parent = os.path.dirname(self.agent_hub_dir)
                examples_parent = os.path.dirname(self.examples_dir)
                if use_default_agent_hub or use_default_examples:
                    python_dir = os.path.join(self.mofa_dir, 'python')
                    if not os.path.exists(python_dir):
                        os.makedirs(python_dir, exist_ok=True)

                if os.path.exists(agent_hub_parent):
                    os.makedirs(self.agent_hub_dir, exist_ok=True)
                else:
                    print(f"Warning: Parent directory for agent_hub_dir does not exist: {agent_hub_parent}")
                    self.agent_hub_dir = os.path.join(os.path.dirname(__file__), '../temp/agent-hub')
                    os.makedirs(self.agent_hub_dir, exist_ok=True)

                if os.path.exists(examples_parent):
                    os.makedirs(self.examples_dir, exist_ok=True)
                else:
                    print(f"Warning: Parent directory for examples_dir does not exist: {examples_parent}")
                    self.examples_dir = os.path.join(os.path.dirname(__file__), '../temp/examples')
                    os.makedirs(self.examples_dir, exist_ok=True)
            except Exception as e:
                print(f"Error creating directories: {e}")
                temp_dir = os.path.join(os.path.dirname(__file__), '../temp')
                os.makedirs(temp_dir, exist_ok=True)
                self.agent_hub_dir = os.path.join(temp_dir, 'agent-hub')
                self.examples_dir = os.path.join(temp_dir, 'examples')
                os.makedirs(self.agent_hub_dir, exist_ok=True)
                os.makedirs(self.examples_dir, exist_ok=True)
        
        # 存储正在运行的进程信息
        self._running_processes = {}
        
        # 存储所有可能的目录路径，用于搜索
        self.agent_dirs = [self.agent_hub_dir]  # agent-hub目录
        self.example_dirs = [self.examples_dir]  # examples目录
        
        # 兼容旧版本的代码，保留agents_dir和possible_agent_dirs属性
        self.agents_dir = self.agent_hub_dir
        self.possible_agent_dirs = [self.agent_hub_dir, self.examples_dir]
        
        # 根据运行模式设置命令
        if self.mofa_mode == 'system':
            self.mofa_cmd = "mofa"
            self.activate_cmd = ""
        elif self.mofa_mode == 'venv':
            self.activate_cmd = f"source {self.mofa_env_path}/bin/activate"
            self.mofa_cmd = "mofa"
        elif self.mofa_mode == 'docker':
            # Docker执行：docker exec -i -w <workdir> <container> mofa
            self.docker_container = self.settings.get('docker_container_name', DEFAULT_DOCKER_CONTAINER)
            if not self.docker_container:
                print("警告: docker模式但未指定container name, 将使用'mofa'")
                self.docker_container = 'mofa'
            # 使用双引号包裹工作目录，避免空格问题
            workdir_flag = f"-w \"{self.mofa_dir}\"" if self.mofa_dir else ""
            self.mofa_cmd = f"docker exec -i {workdir_flag} {self.docker_container} mofa"
            self.activate_cmd = ""
            
        if not os.path.exists(self.mofa_dir):
            print(f"警告: 指定的MoFA目录不存在: {self.mofa_dir}")
            
        # 检查mofa命令是否可用
        if self.mofa_mode == 'system':
            if not shutil.which("mofa"):
                print("警告: 系统中找不到mofa命令，请确保已安装")
    
    def _run_command(self, command, cwd=None):
        """运行shell命令并返回输出"""
        # 替换命令中的mofa为正确的命令
        command = command.replace("mofa", self.mofa_cmd)
        
        # docker模式直接执行并返回，避免进入后续system/venv逻辑
        if self.mofa_mode == 'docker':
            try:
                print(f"使用 Docker 执行: {command}")
                result = subprocess.run(
                    command,
                    shell=True,
                    executable="/bin/bash",
                    check=False,
                    text=True,
                    capture_output=True,
                    cwd=None  # 不指定cwd，避免本地主机路径不存在
                )
                if result.returncode == 0:
                    return result.stdout.strip()
                else:
                    print(f"docker exec 命令失败，返回码: {result.returncode}")
                    print(f"错误输出: {result.stderr}")
                    return ""
            except Exception as e:
                print(f"执行docker命令时出错: {e}")
                return ""
        
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
                    cwd=cwd if cwd else (self.mofa_dir if self.mofa_dir else None)
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
                    cwd=cwd if cwd else (self.mofa_dir if self.mofa_dir else None)
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
                            cwd=cwd if cwd else (self.mofa_dir if self.mofa_dir else None)
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
        """获取所有 agent 列表，分别从 agent-hub 和 examples 目录扫描"""
        try:
            # Docker 模式：直接列举容器内目录并返回，跳过宿主机扫描
            if self.mofa_mode == 'docker':
                hub_agents_list = sorted(self._docker_ls(self.agent_hub_dir))
                example_agents_list = sorted(self._docker_ls(self.examples_dir))
                return {
                    "hub_agents": hub_agents_list,
                    "example_agents": example_agents_list
                }

            # 非 docker 模式继续原有流程
            print(f"Current agent_hub_dir = {self.agent_hub_dir}")
            print(f"Current examples_dir = {self.examples_dir}")
            print(f"Current settings: use_system_mofa = {self.use_system_mofa}, mofa_dir = {self.mofa_dir}")
            
            # 创建两个集合分别存储不同来源的agents
            hub_agents = set()  # agent-hub目录的agents（原子化单位）
            example_agents = set()  # examples目录的agents
            cli_success = False
            
            # 1. 先尝试使用 mofa CLI 命令，但不直接使用结果，因为我们需要知道每个agent的来源
            try:
                output = self._run_command("mofa agent-list")
                if output:
                    for line in output.split("\n"):
                        if line.startswith("[") and line.endswith("]"):
                            agents_text = line.strip("[]").replace("'", "").replace(" ", "")
                            cli_agents = [agent for agent in agents_text.split(",") if agent]
                            cli_success = True
                            print(f"CLI 命令成功获取到 {len(cli_agents)} 个 agents: {cli_agents}")
                            break
            except Exception as cli_err:
                print(f"CLI 命令出错: {cli_err}")
            
            # 2. 扫描 agent-hub 目录（原子化单位）
            print(f"扫描 agent-hub 目录: {self.agent_hub_dir}")
            if os.path.exists(self.agent_hub_dir) and os.path.isdir(self.agent_hub_dir):
                try:
                    for item in os.listdir(self.agent_hub_dir):
                        item_path = os.path.join(self.agent_hub_dir, item)
                        if os.path.isdir(item_path) and not item.startswith('.'):
                            hub_agents.add(item)
                    print(f"从 agent-hub 目录读取到 {len(hub_agents)} 个原子化Agent")
                except Exception as dir_err:
                    print(f"读取 agent-hub 目录时出错: {dir_err}")
            else:
                print(f"agent-hub 目录不存在或无法访问: {self.agent_hub_dir}")
            
            # 3. 扫描 examples 目录
            print(f"扫描 examples 目录: {self.examples_dir}")
            if os.path.exists(self.examples_dir) and os.path.isdir(self.examples_dir):
                try:
                    for item in os.listdir(self.examples_dir):
                        item_path = os.path.join(self.examples_dir, item)
                        if os.path.isdir(item_path) and not item.startswith('.'):
                            example_agents.add(item)
                    print(f"从 examples 目录读取到 {len(example_agents)} 个dataflow示例")
                except Exception as dir_err:
                    print(f"读取 examples 目录时出错: {dir_err}")
            else:
                print(f"examples 目录不存在或无法访问: {self.examples_dir}")
            
            if self.mofa_mode == 'docker':
                # 分别列举 container 内的两级目录
                hub_agents_list = sorted(self._docker_ls(self.agent_hub_dir))
                example_agents_list = sorted(self._docker_ls(self.examples_dir))
                print(f"Docker 模式列出 {len(hub_agents_list)} 个hub agents, {len(example_agents_list)} 个dataflows")
            else:
                # 将集合转为列表并排序
                hub_agents_list = sorted(list(hub_agents))
                example_agents_list = sorted(list(example_agents))
                print(f"最终找到 {len(hub_agents_list)} 个原子化Agent和 {len(example_agents_list)} 个dataflow示例")

            # 如果都没有找到，提供占位示例
            if not hub_agents_list and not example_agents_list:
                print("未找到任何 agent，返回默认示例")
                return {
                    "hub_agents": ["hello_world", "reasoner"],
                    "example_agents": ["memory", "rag"]
                }
            
            return {
                "hub_agents": hub_agents_list,
                "example_agents": example_agents_list
            }
            
        except Exception as e:
            import traceback
            print(f"Error listing agents: {e}")
            print(traceback.format_exc())
            # 在出错时返回一些默认的 agent 示例
            return {
                "hub_agents": ["hello_world", "reasoner"],
                "example_agents": ["memory", "rag"]
            }
    
    def get_agent_details(self, agent_name):
        """获取 agent 的详细信息"""
        try:
            if self.mofa_mode == 'docker':
                # Determine agent root inside container
                candidate_paths = [
                    os.path.join(self.agent_hub_dir, agent_name),
                    os.path.join(self.examples_dir, agent_name)
                ]
                agent_path = None
                for p in candidate_paths:
                    test_cmd = f"docker exec -i {self.docker_container} bash -c 'test -d \"{p}\"'"
                    if subprocess.run(test_cmd, shell=True, executable="/bin/bash").returncode == 0:
                        agent_path = p
                        break
                if not agent_path:
                    return None

                files = self._docker_find(agent_path)
                return {
                    "name": agent_name,
                    "path": agent_path,
                    "files": self._file_dict_list(agent_path, files)
                }

            # 原有本地模式
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
        except Exception as e:
            import traceback
            print(f"Error getting agent details: {e}")
            print(traceback.format_exc())
            return None
    
    def _get_agent_files(self, agent_path):
        """递归获取 agent 目录下的所有文件"""
        if self.mofa_mode == 'docker':
            return self._file_dict_list(agent_path, self._docker_find(agent_path))
        files_list = []
        for root, _, filenames in os.walk(agent_path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                rel_path = os.path.relpath(file_path, agent_path)
                files_list.append({
                    "name": filename,
                    "path": rel_path,
                    "type": os.path.splitext(filename)[1][1:] or "txt"
                })
        return files_list
    
    def create_agent(self, agent_name, version="0.0.1", authors="MoFA_Stage User", agent_type="agent-hub"):
        """创建一个新的 agent
        
        Args:
            agent_name: Agent 的名称
            version: Agent 的版本号
            authors: Agent 的作者
            agent_type: Agent 的类型，可以是 'agent-hub'（原子 agent）或 'examples'（组合示例）
        """
        try:
            # 根据 agent_type 选择输出目录
            if agent_type == "agent-hub":
                output_dir = self.agent_hub_dir
            elif agent_type == "examples":
                output_dir = self.examples_dir
            else:
                return {"success": False, "message": f"Invalid agent_type: {agent_type}. Must be 'agent-hub' or 'examples'"}
            
            print(f"创建 {agent_type} 类型的 Agent: {agent_name} 到目录: {output_dir}")
            
            # 确保目录存在
            os.makedirs(output_dir, exist_ok=True)
            
            # 使用不同的模板，根据 agent 类型
            template_path = ""
            if agent_type == "agent-hub":
                template_path = os.path.join(self.agent_hub_dir, "hello-world")
            else:  # examples
                template_path = os.path.join(self.examples_dir, "hello_world")
            
            # 检查模板是否存在
            if not os.path.exists(template_path):
                print(f"警告: 模板路径不存在: {template_path}，将尝试使用 mofa new-agent 命令")
                cmd = f"mofa new-agent {agent_name} --version {version} --output {output_dir} --authors \"{authors}\""
                result = self._run_command(cmd)
            else:
                # 使用模板复制创建新 agent
                agent_dir = os.path.join(output_dir, agent_name)
                if os.path.exists(agent_dir):
                    return {"success": False, "message": f"Agent directory already exists: {agent_dir}"}
                
                # 复制模板目录
                import shutil
                shutil.copytree(template_path, agent_dir)
                
                # 更新 agent 名称和版本
                template_name = os.path.basename(template_path)
                self._update_agent_name_in_files(agent_dir, template_name, agent_name)
                
                # 更新 README.md
                readme_path = os.path.join(agent_dir, "README.md")
                if os.path.exists(readme_path):
                    with open(readme_path, "r") as f:
                        content = f.read()
                    content = content.replace(template_name, agent_name)
                    content = content.replace("# " + template_name, "# " + agent_name)
                    with open(readme_path, "w") as f:
                        f.write(content)
                else:
                    # 创建一个基本的 README.md
                    with open(readme_path, "w") as f:
                        f.write(f"# {agent_name} Agent\n\nCreated by {authors}\nVersion: {version}\n\nThis is a {agent_type} agent.")
                
                result = f"Created {agent_type} agent '{agent_name}' from template '{template_name}'"
        
            if not result:
                # 命令失败，尝试手动创建一个基本agent目录
                print(f"尝试手动创建基本agent目录: {agent_name}")
                agent_dir = os.path.join(output_dir, agent_name)
                
                if not os.path.exists(agent_dir):
                    os.makedirs(agent_dir, exist_ok=True)
                    
                    # 创建一个基本的README.md
                    readme_path = os.path.join(agent_dir, "README.md")
                    with open(readme_path, "w") as f:
                        f.write(f"# {agent_name} Agent\n\nCreated by {authors}\nVersion: {version}\n\nThis is a {agent_type} agent.")
                    
                    # 创建一个基本的dataflow配置
                    dataflow_path = os.path.join(agent_dir, f"{agent_name}_dataflow.yml")
                    with open(dataflow_path, "w") as f:
                        f.write(f"# {agent_name} Agent Dataflow Configuration\n\nname: {agent_name}\nversion: {version}\n\nnodes: []\n\nlinks: []")
                        
                    return {"success": True, "message": f"Created basic {agent_type} agent structure for {agent_name}"}
                else:
                    return {"success": False, "message": f"Agent directory already exists: {agent_name}"}
            
            return {"success": True, "message": result}
        except Exception as e:
            import traceback
            trace = traceback.format_exc()
            print(f"创建 Agent 时出错: {str(e)}\n{trace}")
            return {"success": False, "message": str(e)}
    
    def run_agent(self, agent_name, timeout=5):
        """运行指定的原子化agent（非阻塞方式）
        这个方法专门用于运行 agent-hub 中的原子化agent
        """
        try:
            # 首先检查这个agent是否存在于agent-hub目录中
            agent_path = os.path.join(self.agent_hub_dir, agent_name)
            if not os.path.exists(agent_path) or not os.path.isdir(agent_path):
                return {
                    "success": False, 
                    "message": f"Agent {agent_name} not found in agent-hub directory. If this is an example, use run_example instead."
                }
            
            # 使用适合原子化agent的命令运行
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
                "message": f"Atomic agent {agent_name} started", 
                "process_id": process.pid,
                "agent_type": "atomic"
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
            
    def run_example(self, example_name, timeout=5):
        """运行指定的dataflow示例（非阻塞方式）
        这个方法专门用于运行 examples 目录中的dataflow示例
        dataflow示例可能需要不同的启动参数或环境设置
        
        新的运行方式：使用 dora 命令运行 dataflow
        1. cd 到示例目录
        2. dora up
        3. dora build xxx_dataflow.yml
        4. dora start xxx_dataflow.yml
        """
        print(f"\n\n===== 开始运行 example: {example_name} =====")
        try:
            # 首先检查这个示例是否存在于examples目录中
            example_path = os.path.join(self.examples_dir, example_name)
            if not os.path.exists(example_path) or not os.path.isdir(example_path):
                return {
                    "success": False, 
                    "message": f"Example {example_name} not found in examples directory. If this is an atomic agent, use run_agent instead."
                }
            
            # 查找 dataflow 配置文件
            dataflow_files = [f for f in os.listdir(example_path) if f.endswith('_dataflow.yml') or f.endswith('.yml')]
            if not dataflow_files:
                return {
                    "success": False,
                    "message": f"No dataflow configuration file found in {example_name}"
                }
            
            # 选择第一个找到的 dataflow 文件
            dataflow_file = dataflow_files[0]
            print(f"使用 dataflow 文件: {dataflow_file}")
            
            # 新的运行方式：使用单个命令执行所有 dora 操作
            print(f"Running dora commands in {example_path}...")
            
            # 创建一个单一的命令，执行所有 dora 操作
            dora_cmd = f"cd {example_path} && echo '=== Running dora up ===' && dora up && echo '\n=== Building dataflow {dataflow_file} ===' && dora build {dataflow_file} && echo '\n=== Starting dataflow {dataflow_file} ===' && dora start {dataflow_file}"
            
            # 初始化输出行列表
            output_lines = [
                f"Running dora commands in {example_path}...",
                f"Dataflow file: {dataflow_file}",
                "Command: dora up && dora build && dora start",
                "----------------------------------------"
            ]
            
            # 在后台运行 dora 命令
            process = subprocess.Popen(
                dora_cmd,
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True,
                cwd=example_path  # 设置工作目录
            )
            
            # 保存进程信息，以便后续获取输出
            self._running_processes[example_name] = {
                "process": process,
                "start_time": time.time(),
                "output_lines": output_lines,  # 已经有了前面命令的输出
                "type": "example"
            }
            
            # 返回结果
            return {
                "success": True, 
                "message": f"Example {example_name} started with dora", 
                "process_id": process.pid,
                "agent_type": "example",
                "dataflow_file": dataflow_file
            }
            
            # 旧的运行方式（注释掉）
            '''
            # 使用适合组合式示例的命令运行
            cmd = f"cd {self.mofa_dir} && mofa run --agent-name {example_name} --example"
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
                "message": f"Example {example_name} started", 
                "process_id": process.pid,
                "agent_type": "example"
            }
            '''
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
            
    def get_process_output(self, agent_name):
        """获取正在运行的进程的输出
        
        Args:
            agent_name: Agent 的名称
            
        Returns:
            包含进程输出的字典
        """
        try:
            if agent_name not in self._running_processes:
                return {
                    "success": False,
                    "message": f"No running process found for {agent_name}"
                }
                
            process_info = self._running_processes[agent_name]
            process = process_info["process"]
            
            # 读取新的输出
            new_output = []
            
            # 非阻塞地读取所有可用的输出
            def read_output(pipe, prefix=""):
                output = []
                try:
                    # 将文件描述符设置为非阻塞模式
                    import fcntl
                    import os
                    fd = pipe.fileno()
                    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
                    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
                    
                    # 尝试读取所有可用的输出
                    while True:
                        try:
                            line = pipe.readline()
                            if not line:
                                break
                            line = line.strip()
                            if prefix:
                                line = f"{prefix}{line}"
                            output.append(line)
                        except:
                            break
                except Exception as e:
                    output.append(f"Error reading output: {str(e)}")
                return output
            
            # 读取标准输出和错误输出
            stdout_lines = read_output(process.stdout)
            stderr_lines = read_output(process.stderr, prefix="ERROR: ")
            
            # 合并输出
            new_output = stdout_lines + stderr_lines
            process_info["output_lines"].extend(new_output)
            
            # 检查进程是否已经结束
            is_running = process.poll() is None
            
            return {
                "success": True,
                "is_running": is_running,
                "new_output": new_output,
                "all_output": process_info["output_lines"],
                "process_type": process_info["type"],
                "start_time": process_info["start_time"],
                "elapsed_time": time.time() - process_info["start_time"]
            }
        except Exception as e:
            import traceback
            trace = traceback.format_exc()
            print(f"获取进程输出时出错: {str(e)}\n{trace}")
            return {"success": False, "message": str(e)}
    
    def delete_agent(self, agent_name):
        """删除指定的 agent
        
        会自动检查 agent-hub 和 examples 目录
        """
        try:
            # 首先检查 agent-hub 目录
            agent_hub_path = os.path.join(self.agent_hub_dir, agent_name)
            # 然后检查 examples 目录
            examples_path = os.path.join(self.examples_dir, agent_name)
            
            # 检查 agent 是否存在于任一目录
            if os.path.exists(agent_hub_path):
                agent_path = agent_hub_path
                agent_type = "agent-hub"
            elif os.path.exists(examples_path):
                agent_path = examples_path
                agent_type = "examples"
            else:
                # 兼容旧版本，检查 self.agents_dir
                agent_path = os.path.join(self.agents_dir, agent_name)
                if not os.path.exists(agent_path):
                    return {"success": False, "message": f"Agent {agent_name} not found in any directory"}
                agent_type = "unknown"
            
            # 递归删除目录
            import shutil
            print(f"删除 {agent_type} 类型的 Agent: {agent_name} 路径: {agent_path}")
            shutil.rmtree(agent_path)
            return {"success": True, "message": f"{agent_type} Agent {agent_name} deleted"}
        except Exception as e:
            import traceback
            trace = traceback.format_exc()
            print(f"删除 Agent 时出错: {str(e)}\n{trace}")
            return {"success": False, "message": str(e)}
    
    def copy_agent(self, source_agent, target_agent, agent_type=None):
        """复制一个 agent 作为新的 agent
        
        Args:
            source_agent: 源 Agent 的名称
            target_agent: 目标 Agent 的名称
            agent_type: Agent 的类型，可以是 'agent-hub'（原子 agent）或 'examples'（组合示例）
                       如果为 None，则会自动检测源 Agent 的类型
        """
        try:
            # 输出日志以便于调试
            print(f"尝试复制 Agent {source_agent} 到 {target_agent}")
            
            # 首先检查源 Agent 的类型，如果没有指定 agent_type
            if agent_type is None:
                # 检查在 agent-hub 目录中
                if os.path.exists(os.path.join(self.agent_hub_dir, source_agent)):
                    agent_type = "agent-hub"
                    source_path = os.path.join(self.agent_hub_dir, source_agent)
                # 检查在 examples 目录中
                elif os.path.exists(os.path.join(self.examples_dir, source_agent)):
                    agent_type = "examples"
                    source_path = os.path.join(self.examples_dir, source_agent)
                else:
                    # 尝试在其他可能的目录中查找
                    print(f"在默认目录中找不到源 Agent: {source_agent}")
                    source_path = None
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
                            # 根据路径判断 agent 类型
                            if "agent-hub" in other_path:
                                agent_type = "agent-hub"
                            elif "examples" in other_path:
                                agent_type = "examples"
                            else:
                                # 默认使用 agent-hub
                                agent_type = "agent-hub"
                            break
                    
                    if source_path is None:
                        return {"success": False, "message": f"Source agent '{source_agent}' not found. Searched in agent-hub, examples, and {other_locations}"}
            else:
                # 根据指定的 agent_type 选择源路径
                if agent_type == "agent-hub":
                    source_path = os.path.join(self.agent_hub_dir, source_agent)
                elif agent_type == "examples":
                    source_path = os.path.join(self.examples_dir, source_agent)
                else:
                    return {"success": False, "message": f"Invalid agent_type: {agent_type}. Must be 'agent-hub' or 'examples'"}
            
            # 根据 agent_type 选择目标路径
            if agent_type == "agent-hub":
                target_path = os.path.join(self.agent_hub_dir, target_agent)
            else:  # examples
                target_path = os.path.join(self.examples_dir, target_agent)
            
            print(f"source_path = {source_path}")
            print(f"target_path = {target_path}")
            print(f"agent_type = {agent_type}")
            
            # 检查源路径是否存在
            if not os.path.exists(source_path):
                return {"success": False, "message": f"Source agent '{source_agent}' not found at {source_path}"}
            
            # 检查目标路径是否已存在
            if os.path.exists(target_path):
                return {"success": False, "message": f"Target agent '{target_agent}' already exists at {target_path}"}
            
            # 创建目标目录的父目录（如果不存在）
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            # 复制目录
            import shutil
            print(f"正在复制 {agent_type} agent: {source_path} -> {target_path}")
            shutil.copytree(source_path, target_path)
            
            # 更新配置文件中的名称
            self._update_agent_name_in_files(target_path, source_agent, target_agent)
            
            return {"success": True, "message": f"{agent_type} agent '{source_agent}' successfully copied to '{target_agent}'"}
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
        5. 各种可能的log文件夹和子文件夹
        """
        try:
            # 首先检查agent是否存在于任何可能的目录中
            agent_paths = []
            
            # 检查主要agent目录
            primary_agent_path = os.path.join(self.agents_dir, agent_name)
            if os.path.exists(primary_agent_path):
                agent_paths.append(primary_agent_path)
            
            # 检查所有可能的agent目录
            for possible_dir in self.possible_agent_dirs:
                possible_path = os.path.join(possible_dir, agent_name)
                if os.path.exists(possible_path) and possible_path not in agent_paths:
                    agent_paths.append(possible_path)
            
            # 如果没有找到agent，尝试在examples目录中查找
            if not agent_paths:
                for example_dir in self.example_dirs:
                    example_path = os.path.join(example_dir, agent_name)
                    if os.path.exists(example_path):
                        agent_paths.append(example_path)
            
            if not agent_paths:
                return f"未找到名为 {agent_name} 的Agent。请检查名称是否正确。"
            
            # 可能的日志位置
            log_locations = []
            
            # 为每个找到的agent路径添加可能的日志位置
            for agent_path in agent_paths:
                # 1. agent目录下的logs子目录
                log_locations.append(os.path.join(agent_path, "logs"))
                # 2. agent目录下直接的log文件
                log_locations.append(os.path.join(agent_path, f"{agent_name}.log"))
                # 3. agent目录下的log子目录
                log_locations.append(os.path.join(agent_path, "log"))
                # 4. agent目录下的output子目录
                log_locations.append(os.path.join(agent_path, "output"))
            
            # 5. MoFA目录下的logs子目录
            log_locations.append(os.path.join(self.mofa_dir, "logs", f"{agent_name}.log"))
            # 6. MoFA目录下的通用logs目录
            log_locations.append(os.path.join(self.mofa_dir, "logs"))
            # 7. MoFA目录下的log子目录
            log_locations.append(os.path.join(self.mofa_dir, "log"))
            
            logs_content = []
            
            # 检查所有agent路径下的out目录
            for agent_path in agent_paths:
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
                                    logs_content.append(f"=== Dora Daemon 日志 ({os.path.basename(agent_path)}) ===\n{content}\n")
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
                                    logs_content.append(f"=== Dora Coordinator 日志 ({os.path.basename(agent_path)}) ===\n{content}\n")
                        except Exception as e:
                            logs_content.append(f"无法读取Dora Coordinator日志: {str(e)}")
                
                    # 检查out目录下的其他日志文件
                    for file in os.listdir(out_dir):
                        file_path = os.path.join(out_dir, file)
                        # 只处理文件，不处理目录
                        if os.path.isfile(file_path) and file != "dora-daemon.txt" and file != "dora-coordinator.txt":
                            # 检查是否是日志文件（有文本扩展名或包含"log"或"日志"字样）
                            if file.endswith(".txt") or file.endswith(".log") or "log" in file.lower() or "日志" in file:
                                try:
                                    with open(file_path, "r") as f:
                                        # 只读取最后100行，避免文件过大
                                        lines = f.readlines()
                                        content = "".join(lines[-100:] if len(lines) > 100 else lines)
                                        if content:
                                            logs_content.append(f"=== {file} ({os.path.basename(agent_path)}/out) ===\n{content}\n")
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
                                # 添加更多日志文件模式
                                elif file.endswith(".txt") or file.endswith(".log") or "log" in file.lower() or "日志" in file:
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
                                        logs_content.append(f"=== 运行实例 {instance_name} - {file_name} ({os.path.basename(agent_path)}) ===\n{content}\n")
                            except Exception as e:
                                logs_content.append(f"无法读取实例日志 {log_file}: {str(e)}")
            
            # 遍历所有可能的日志位置
            for location in log_locations:
                if os.path.exists(location):
                    if os.path.isdir(location):
                        # 如果是目录，查找与agent相关的所有日志文件
                        log_files = []
                        for file in os.listdir(location):
                            # 扩展匹配条件，包括更多可能的日志文件
                            if (file.endswith(".log") or file.endswith(".txt") or "log" in file.lower() or "日志" in file) and \
                               (agent_name in file or "agent" in file.lower() or "mofa" in file.lower()):
                                log_files.append(os.path.join(location, file))
                        
                        # 按修改时间排序，最新的日志排在前面
                        log_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                        
                        # 读取最新的几个日志文件
                        for log_file in log_files[:5]:  # 增加到最多读取5个最新的日志文件
                            try:
                                with open(log_file, "r") as f:
                                    # 只读取最后200行，避免文件过大
                                    lines = f.readlines()
                                    content = "".join(lines[-200:] if len(lines) > 200 else lines)
                                    if content:
                                        logs_content.append(f"=== {os.path.basename(log_file)} ({os.path.basename(os.path.dirname(log_file))}) ===\n{content}\n")
                            except Exception as e:
                                logs_content.append(f"无法读取日志文件 {log_file}: {str(e)}")
                        
                        # 递归查找子目录中的日志文件
                        for root, dirs, files in os.walk(location):
                            if root != location:  # 跳过已处理的顶级目录
                                log_files = []
                                for file in files:
                                    if (file.endswith(".log") or file.endswith(".txt") or "log" in file.lower() or "日志" in file) and \
                                       (agent_name in file or "agent" in file.lower() or "mofa" in file.lower()):
                                        log_files.append(os.path.join(root, file))
                                
                                # 按修改时间排序，最新的日志排在前面
                                log_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                                
                                # 读取最新的几个日志文件
                                for log_file in log_files[:3]:  # 最多读取3个最新的日志文件
                                    try:
                                        with open(log_file, "r") as f:
                                            # 只读取最后100行，避免文件过大
                                            lines = f.readlines()
                                            content = "".join(lines[-100:] if len(lines) > 100 else lines)
                                            if content:
                                                rel_path = os.path.relpath(log_file, location)
                                                logs_content.append(f"=== {rel_path} ===\n{content}\n")
                                    except Exception as e:
                                        logs_content.append(f"无法读取日志文件 {log_file}: {str(e)}")
                    else:
                        # 如果是文件，直接读取
                        try:
                            with open(location, "r") as f:
                                # 只读取最后200行，避免文件过大
                                lines = f.readlines()
                                content = "".join(lines[-200:] if len(lines) > 200 else lines)
                                if content:
                                    logs_content.append(f"=== {os.path.basename(location)} ===\n{content}")
                        except Exception as e:
                            # 不记录错误，因为很多路径可能不存在
                            pass
            
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
        if self.mofa_mode == 'docker':
            # 尝试 hub 目录
            candidate_paths = [
                os.path.join(self.agent_hub_dir, agent_name, file_path),
                os.path.join(self.examples_dir, agent_name, file_path)
            ]
            for p in candidate_paths:
                cmd = f"docker exec -i {self.docker_container} bash -c 'test -f \"{p}\"'"
                if subprocess.run(cmd, shell=True, executable="/bin/bash").returncode == 0:
                    # 文件存在，读取
                    cat_cmd = f"docker exec -i {self.docker_container} bash -c 'cat \"{p}\"'"
                    result = subprocess.run(cat_cmd, shell=True, executable="/bin/bash", text=True, capture_output=True)
                    if result.returncode == 0:
                        return {"success": True, "content": result.stdout}
                    else:
                        return {"success": False, "message": result.stderr}
            return {"success": False, "message": f"File {file_path} not found in container"}

        # ---- 本地模式 ----
        full_path = os.path.join(self.agents_dir, agent_name, file_path)
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
        if self.mofa_mode == 'docker':
            # 选择写入到 agent-hub 目录（若存在），否则 examples
            base_path = os.path.join(self.agent_hub_dir, agent_name)
            test_cmd = f"docker exec -i {self.docker_container} bash -c 'test -d \"{base_path}\"'"
            if subprocess.run(test_cmd, shell=True, executable="/bin/bash").returncode != 0:
                base_path = os.path.join(self.examples_dir, agent_name)

            full_path = os.path.join(base_path, file_path)
            dir_path = os.path.dirname(full_path)

            # 确保目录存在
            mkdir_cmd = f"docker exec -i {self.docker_container} bash -c 'mkdir -p \"{dir_path}\"'"
            subprocess.run(mkdir_cmd, shell=True, executable="/bin/bash")

            # 通过 stdin 写入文件
            write_cmd = f"docker exec -i {self.docker_container} bash -c 'cat > \"{full_path}\"'"
            result = subprocess.run(write_cmd, shell=True, executable="/bin/bash", text=True, input=content)
            if result.returncode == 0:
                return {"success": True, "message": f"File {file_path} saved"}
            else:
                return {"success": False, "message": result.stderr}

        # ---- 本地模式 ----
        agent_path = os.path.join(self.agents_dir, agent_name)
        if not os.path.exists(agent_path):
            for possible_dir in self.possible_agent_dirs:
                possible_path = os.path.join(possible_dir, agent_name)
                if os.path.exists(possible_path):
                    agent_path = possible_path
                    break
        if not os.path.exists(agent_path):
            agent_path = os.path.join(self.agents_dir, agent_name)
            os.makedirs(agent_path, exist_ok=True)

        full_path = os.path.join(agent_path, file_path)
        dir_path = os.path.dirname(full_path)
        try:
            os.makedirs(dir_path, exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(content)
            return {"success": True, "message": f"File {file_path} saved"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    # ------------------------------ Docker Helpers ------------------------------
    def _docker_ls(self, directory):
        """Return list of subdirectories (one level) inside given directory of container."""
        try:
            cmd = f"docker exec -i {self.docker_container} bash -c 'ls -1 {directory} 2>/dev/null'"
            result = subprocess.run(cmd, shell=True, executable="/bin/bash", text=True, capture_output=True)
            if result.returncode == 0:
                items = [item.strip() for item in result.stdout.split("\n") if item.strip()]
                return items
            else:
                return []
        except Exception:
            return []

    def _docker_find(self, directory):
        """Return list of all files (relative paths) under directory inside container."""
        try:
            cmd = f"docker exec -i {self.docker_container} bash -c 'cd \"{directory}\" 2>/dev/null && find . -type f'"
            result = subprocess.run(cmd, shell=True, executable="/bin/bash", text=True, capture_output=True)
            if result.returncode == 0:
                files = [line.lstrip('./') for line in result.stdout.split("\n") if line.strip()]
                return files
            return []
        except Exception:
            return []

    def _file_dict_list(self, base_path, rel_paths):
        """Helper: given list of relative paths, return list of dicts like original."""
        result = []
        for rel in rel_paths:
            name = os.path.basename(rel)
            ext = os.path.splitext(name)[1][1:] or "txt"
            result.append({"name": name, "path": rel, "type": ext})
        return result
