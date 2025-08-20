import os
import subprocess
import signal
import psutil
import time
import json
import socket
from threading import Lock
from flask import Blueprint, jsonify, request, current_app
from routes.settings import get_settings
from urllib.parse import quote

vscode_bp = Blueprint('vscode', __name__)

# 全局变量存储 code-server 进程
_code_server_process = None
_code_server_lock = Lock()
_code_server_port = 8080  # 默认端口，避免与前端冲突
_MAX_PORT_TRIES = 20

def get_code_server_path():
    """获取 code-server 可执行文件路径"""
    # 首先尝试全局安装的 code-server
    try:
        result = subprocess.run(['which', 'code-server'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    
    # 尝试各种可能的安装路径
    possible_paths = [
        '/opt/homebrew/bin/code-server',  # Homebrew ARM64 macOS
        '/usr/local/bin/code-server',     # Homebrew Intel macOS 或 Linux
        '/opt/homebrew/opt/code-server/bin/code-server',  # Homebrew 完整路径
        '/usr/local/bin/code-server',
        os.path.expanduser('~/.local/bin/code-server'),
        os.path.expanduser('~/bin/code-server')
    ]
    
    for path in possible_paths:
        if os.path.exists(path) and os.access(path, os.X_OK):
            return path
    
    return None

def install_code_server():
    """安装 code-server"""
    try:
        # 优先使用 Homebrew 安装 code-server（在 macOS 上）
        import platform
        if platform.system() == 'Darwin':  # macOS
            result = subprocess.run([
                'brew', 'install', 'code-server'
            ], capture_output=True, text=True, timeout=300)
        else:
            # 在 Linux 上使用官方安装脚本
            result = subprocess.run([
                'curl', '-fsSL', 'https://code-server.dev/install.sh'
            ], capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                result = subprocess.run(['sh'], input=result.stdout, capture_output=True, text=True, timeout=300)
        
        # 如果上述方法失败，fallback 到 npm
        if result.returncode != 0:
            result = subprocess.run([
                'npm', 'install', '-g', 'code-server'
            ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            return True, "code-server installed successfully"
        else:
            return False, f"Failed to install code-server: {result.stderr}"
    except subprocess.TimeoutExpired:
        return False, "Installation timeout"
    except Exception as e:
        return False, f"Installation error: {str(e)}"

def kill_process_tree(pid):
    """递归杀死进程及其子进程"""
    try:
        parent = psutil.Process(pid)
        for child in parent.children(recursive=True):
            try:
                child.kill()
            except:
                pass
        parent.kill()
    except psutil.NoSuchProcess:
        pass

def _find_available_port(start_port):
    """从 start_port 开始查找可用端口"""
    port = start_port
    tries = 0
    while tries < _MAX_PORT_TRIES:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
        port += 1
        tries += 1
    return None

def start_code_server(workspace_path, port=None):
    """启动 code-server"""
    global _code_server_process, _code_server_port
    
    if port:
        _code_server_port = port
    else:
        # 找到可用端口（可能 8080 已被占用）
        avail = _find_available_port(_code_server_port)
        if avail is None:
            return False, "No available port for code-server"
        _code_server_port = avail
    
    with _code_server_lock:
        # 检查是否已经有实例在运行
        if _code_server_process and _code_server_process.poll() is None:
            return True, f"code-server already running on port {_code_server_port}"
        
        # 获取 code-server 路径
        code_server_path = get_code_server_path()
        if not code_server_path:
            # 尝试安装
            success, message = install_code_server()
            if not success:
                return False, f"code-server not found and installation failed: {message}"
            
            code_server_path = get_code_server_path()
            if not code_server_path:
                return False, "code-server installation completed but executable not found"
        
        # 确保工作目录存在
        if not os.path.exists(workspace_path):
            try:
                os.makedirs(workspace_path, exist_ok=True)
            except Exception as e:
                return False, f"Failed to create workspace directory: {str(e)}"
        
        # 创建 VS Code 配置文件
        try:
            create_vscode_settings(workspace_path)
        except Exception as e:
            # 配置创建失败不应该阻止启动，只记录警告
            print(f"Warning: Failed to create VS Code settings: {str(e)}")
        
        try:
            # 启动 code-server
            cmd = [
                code_server_path,
                '--bind-addr', f'0.0.0.0:{_code_server_port}',
                '--disable-telemetry',
                '--disable-update-check',
                '--auth', 'none',  # 暂时禁用认证，生产环境应该启用
                '--disable-workspace-trust',  # 禁用工作区信任提示
                '--disable-file-downloads',   # 禁用文件下载（可选）
                '--disable-getting-started-override',  # 禁用开始页面
                workspace_path
            ]
            
            _code_server_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid  # 创建新的进程组
            )
            
            # 等待一下确保启动成功
            time.sleep(2)
            if _code_server_process.poll() is None:
                return True, f"code-server started on port {_code_server_port}"
            else:
                stderr = _code_server_process.stderr.read().decode() if _code_server_process.stderr else "No error info"
                return False, f"code-server failed to start: {stderr}"
                
        except Exception as e:
            return False, f"Failed to start code-server: {str(e)}"

def stop_code_server():
    """停止 code-server"""
    global _code_server_process
    
    with _code_server_lock:
        if _code_server_process:
            try:
                # 先尝试优雅关闭
                kill_process_tree(_code_server_process.pid)
                _code_server_process.wait(timeout=5)
            except (subprocess.TimeoutExpired, psutil.NoSuchProcess):
                # 强制杀死
                try:
                    os.killpg(os.getpgid(_code_server_process.pid), signal.SIGKILL)
                except:
                    pass
            
            _code_server_process = None
            return True, "code-server stopped"
        else:
            return True, "code-server was not running"

def get_agent_workspace_path(agent_name, config):
    """根据配置获取 agent 工作目录路径，不论是 hub 还是 examples"""
    mofa_mode = config.get('mofa_mode', 'system')
    
    # 获取基础目录，如果没有配置则使用默认值
    mofa_dir = config.get('mofa_dir') or '/Users/liyao/Code/mofa'
    agent_hub_path = config.get('agent_hub_path') or os.path.join(mofa_dir, 'python/agent-hub')
    examples_path = config.get('examples_path') or os.path.join(mofa_dir, 'python/examples')

    # 注意：examples 目录中的可能使用下划线命名
    agent_name_underscore = agent_name.replace('-', '_')
    
    # system or venv path prefixes - 优先查找存在的目录
    candidate_paths = [
        os.path.join(agent_hub_path, agent_name),
        os.path.join(examples_path, agent_name),
        os.path.join(examples_path, agent_name_underscore),  # 处理命名差异
        os.path.join(mofa_dir, agent_name)
    ]

    if mofa_mode == 'docker':
        # Docker 模式下直接返回容器内统一路径，前端需自行映射
        container_name = config.get('docker_container_name', '')
        if container_name:
            return f"/workspace/{agent_name}"
        # 如果未配置容器则回退到默认

    for p in candidate_paths:
        if p and os.path.exists(p):
            print(f"Found agent workspace: {p}")
            return p
    
    print(f"Warning: Agent workspace not found for {agent_name}, candidates were: {candidate_paths}")
    # 如果找不到，返回第一个候选（可能不存在，但 code-server 会创建）
    return candidate_paths[0]

@vscode_bp.route('/api/vscode/start/<agent_name>', methods=['POST'])
def start_vscode_for_agent(agent_name):
    """为指定 agent 启动 VS Code Web"""
    try:
        config = get_settings()
        data = request.get_json() or {}

        # 优先使用请求体中显式提供的 workspace 路径
        override_path = data.get('path') or data.get('workspace_path')
        if override_path:
            workspace_path = os.path.expanduser(override_path)
        else:
            # 默认使用当前登录用户的 home 目录
            workspace_path = os.path.expanduser('~')
        
        if not workspace_path:
            return jsonify({
                'success': False,
                'error': 'Cannot determine workspace path for agent'
            }), 400
        
        # 获取可选的端口参数
        port = data.get('port', _code_server_port)
        
        success, message = start_code_server(workspace_path, port)
        
        if success:
            return jsonify({
                'success': True,
                'message': message,
                'port': _code_server_port,
                'url': f'http://localhost:{_code_server_port}?folder={quote(workspace_path)}'
            })
        else:
            return jsonify({
                'success': False,
                'error': message
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to start VS Code: {str(e)}'
        }), 500

@vscode_bp.route('/api/vscode/stop', methods=['POST'])
def stop_vscode():
    """停止 VS Code Web"""
    try:
        success, message = stop_code_server()
        
        return jsonify({
            'success': success,
            'message': message
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to stop VS Code: {str(e)}'
        }), 500

@vscode_bp.route('/api/vscode/status', methods=['GET'])
def get_vscode_status():
    """获取 VS Code Web 状态"""
    try:
        global _code_server_process, _code_server_port
        
        is_running = _code_server_process and _code_server_process.poll() is None
        
        return jsonify({
            'success': True,
            'running': is_running,
            'port': _code_server_port if is_running else None,
            'url': f'http://localhost:{_code_server_port}' if is_running else None
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to get VS Code status: {str(e)}'
        }), 500

@vscode_bp.route('/api/vscode/install', methods=['POST'])
def install_vscode():
    """安装 code-server"""
    try:
        success, message = install_code_server()
        
        return jsonify({
            'success': success,
            'message': message
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to install code-server: {str(e)}'
        }), 500

@vscode_bp.route('/api/vscode/install-extensions/<agent_name>', methods=['POST'])
def install_extensions_for_agent(agent_name):
    """为指定 agent 安装推荐的 VS Code 扩展"""
    try:
        config = get_settings()
        workspace_path = get_agent_workspace_path(agent_name, config)
        
        if not workspace_path:
            return jsonify({
                'success': False,
                'error': 'Cannot determine workspace path for agent'
            }), 400
        
        # 获取 code-server 路径
        code_server_path = get_code_server_path()
        if not code_server_path:
            return jsonify({
                'success': False,
                'error': 'code-server not found'
            }), 404
        
        # 推荐扩展列表
        extensions = [
            'ms-python.python',
            'ms-python.black-formatter', 
            'redhat.vscode-yaml',
            'yzhang.markdown-all-in-one',
            'ms-vscode.vscode-json',
            'tamasfe.even-better-toml',
            'be5invis.vscode-custom-css' # 用于加载自定义CSS
        ]
        
        installed = []
        failed = []
        
        for ext in extensions:
            try:
                result = subprocess.run([
                    code_server_path, '--install-extension', ext
                ], capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    installed.append(ext)
                else:
                    failed.append(ext)
            except Exception as e:
                failed.append(f"{ext} (error: {str(e)})")
        
        return jsonify({
            'success': True,
            'installed': installed,
            'failed': failed,
            'message': f'Installed {len(installed)} extensions, {len(failed)} failed'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to install extensions: {str(e)}'
        }), 500

@vscode_bp.route('/api/vscode/config/<agent_name>', methods=['POST'])
def update_vscode_config(agent_name):
    """更新指定 agent 的 VS Code 配置"""
    try:
        config = get_settings()
        workspace_path = get_agent_workspace_path(agent_name, config)
        
        if not workspace_path:
            return jsonify({
                'success': False,
                'error': 'Cannot determine workspace path for agent'
            }), 400
        
        # 重新创建配置文件
        success = create_vscode_settings(workspace_path)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'VS Code configuration updated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to update VS Code configuration'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to update config: {str(e)}'
        }), 500

def create_vscode_settings(workspace_path):
    """为工作区创建优化的 VS Code 设置"""
    vscode_dir = os.path.join(workspace_path, '.vscode')
    os.makedirs(vscode_dir, exist_ok=True)
    
    # VS Code 工作区设置
    settings = {
        "workbench.startupEditor": "none",  # 禁用欢迎页面
        "workbench.colorTheme": "Light High Contrast",  # 高对比浅色主题
        "workbench.preferredLightColorTheme": "Light High Contrast",
        "workbench.editor.showTabs": True, # 显示标签页，方便多文件切换
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "editor.insertSpaces": True,
        "editor.wordWrap": "on",
        "editor.minimap.enabled": False,
        "editor.renderLineHighlight": "none", # 禁用当前行高亮
        "editor.glyphMargin": False, # 禁用字形边距（断点、错误等图标）
        "editor.folding": False, # 禁用代码折叠
        "editor.lineNumbers": "off", # 禁用行号
        "editor.codeLens": False, # 禁用 CodeLens
        "editor.scrollbar.vertical": "hidden", # 隐藏垂直滚动条
        "editor.scrollbar.horizontal": "hidden", # 隐藏水平滚动条
        "editor.formatOnSave": True,
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 2000,
        "python.defaultInterpreterPath": "/usr/bin/python3",
        "python.formatting.provider": "black",
        "yaml.validate": True,
        "yaml.format.enable": True,
        "markdown.preview.doubleClickToSwitchToEditor": True,
        "terminal.integrated.shell.osx": "/bin/zsh",
        "terminal.integrated.shell.linux": "/bin/bash",
        "explorer.confirmDelete": False,
        "explorer.confirmDragAndDrop": False,
        "workbench.activityBar.visible": True,  # 显示活动栏，方便访问文件资源管理器
        "workbench.statusBar.visible": False,    # 隐藏底部状态栏
        "workbench.commandPalette.history": 0,
        "window.commandCenter": False, # 隐藏顶部 command center
        "workbench.tips.enabled": False, # 禁用提示
        "explorer.openEditors.visible": 0, # 隐藏打开的编辑器视图
        "debug.toolBarLocation": "hidden", # 隐藏调试工具栏
        "scm.diffDecorations": "none", # 禁用 SCM 差异装饰
        "git.enabled": False, # 禁用 Git 集成
        "search.showLineNumbers": False,
        "telemetry.telemetryLevel": "off",
        "workbench.editor.enablePreview": False,  # 禁用预览模式
        "breadcrumbs.enabled": False, # 禁用面包屑
        "editor.suggestSelection": "first",
        "vsintellicode.modify.editor.suggestSelection": "automaticallyOverrodeDefaultValue"
    }

    # 添加自定义CSS配置
    custom_css_file = os.path.join(vscode_dir, 'custom.css')
    settings['vscode_custom_css.imports'] = [f'file://{custom_css_file}']
    settings['vscode_custom_css.policy'] = True # 自动批准扩展

    settings_file = os.path.join(vscode_dir, 'settings.json')
    with open(settings_file, 'w') as f:
        json.dump(settings, f, indent=2)

    # 同步到全局 code-server 用户设置，确保在所有工作区生效
    try:
        user_settings_dir = os.path.expanduser('~/.local/share/code-server/User')
        os.makedirs(user_settings_dir, exist_ok=True)
        user_settings_file = os.path.join(user_settings_dir, 'settings.json')
        with open(user_settings_file, 'w') as f:
            json.dump(settings, f, indent=2)
    except Exception as e:
        print(f"Warning: Failed to write global code-server settings: {e}")

    # 创建自定义CSS文件
    custom_css_content = """
/* 
 * 自定义UI样式，打造纯净的编辑器环境。
 * 由 'Custom CSS and JS Loader' 扩展加载。
 * 如需生效，请使用 (Cmd+Shift+P) > "Reload Custom CSS and JS"。
 */

/* 隐藏状态栏和标题栏（保留侧边栏与活动栏） */
#workbench\\.parts\\.statusbar,
#workbench\\.parts\\.titlebar {
    display: none !important;
}

/* 隐藏顶部 Command Center */
.monaco-workbench .command-center,
.command-center {
    display: none !important;
}

/* 隐藏面包屑导航 */
.breadcrumbs-control {
    display: none !important;
}

/* 隐藏滚动条右侧的概览标尺 */
.monaco-editor .decorationsOverviewRuler {
    display: none !important;
}
"""
    with open(custom_css_file, 'w') as f:
        f.write(custom_css_content)
    
    # 推荐扩展配置
    extensions = {
        "recommendations": [
            "ms-python.python",              # Python 支持
            "ms-python.black-formatter",     # Python 格式化
            "redhat.vscode-yaml",            # YAML 支持
            "yzhang.markdown-all-in-one",   # Markdown 支持
            "ms-vscode.vscode-json",         # JSON 支持
            "tamasfe.even-better-toml",      # TOML 支持
            "ms-vscode-remote.remote-containers", # 容器支持
            "github.vscode-pull-request-github",  # Git 集成
            "eamodio.gitlens",                # Git 历史
            "be5invis.vscode-custom-css"       # 自定义CSS支持
        ]
    }
    
    extensions_file = os.path.join(vscode_dir, 'extensions.json')
    with open(extensions_file, 'w') as f:
        json.dump(extensions, f, indent=2)
    
    # 启动任务配置（用于运行 Agent）
    tasks = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Run Agent",
                "type": "shell",
                "command": "python",
                "args": ["${file}"],
                "group": {
                    "kind": "build",
                    "isDefault": True
                },
                "presentation": {
                    "echo": True,
                    "reveal": "always",
                    "focus": False,
                    "panel": "new"
                },
                "problemMatcher": []
            },
            {
                "label": "Run Agent with MoFA",
                "type": "shell",
                "command": "mofa",
                "args": ["run", "${workspaceFolder}"],
                "group": "build",
                "presentation": {
                    "echo": True,
                    "reveal": "always",
                    "focus": True,
                    "panel": "new"
                }
            }
        ]
    }
    
    tasks_file = os.path.join(vscode_dir, 'tasks.json')
    with open(tasks_file, 'w') as f:
        json.dump(tasks, f, indent=2)
    
    # 调试配置
    launch = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Debug Agent",
                "type": "python",
                "request": "launch",
                "program": "${file}",
                "console": "integratedTerminal",
                "justMyCode": True,
                "env": {
                    "PYTHONPATH": "${workspaceFolder}"
                }
            }
        ]
    }
    
    launch_file = os.path.join(vscode_dir, 'launch.json')
    with open(launch_file, 'w') as f:
        json.dump(launch, f, indent=2)
    
    return True 