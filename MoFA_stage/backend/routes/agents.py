"""
Agent 相关的 API 路由
"""
from flask import Blueprint, request, jsonify
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.mofa_cli import MofaCLI
from utils.file_ops import read_file, write_file, get_file_type
from routes.settings import get_settings

agents_bp = Blueprint('agents', __name__, url_prefix='/api/agents')

# 从设置中获取配置参数初始化MofaCLI
def get_mofa_cli():
    settings = get_settings()
    return MofaCLI(settings)

@agents_bp.route('/', methods=['GET'])
def get_agents():
    """获取所有 agents 列表，按来源分类"""
    mofa_cli = get_mofa_cli()
    agents_data = mofa_cli.list_agents()
    return jsonify({
        "success": True, 
        "hub_agents": agents_data["hub_agents"],
        "example_agents": agents_data["example_agents"]
    })

@agents_bp.route('/<agent_name>', methods=['GET'])
def get_agent_details(agent_name):
    """获取指定 agent 的详细信息"""
    mofa_cli = get_mofa_cli()
    details = mofa_cli.get_agent_details(agent_name)
    if details:
        return jsonify({"success": True, "agent": details})
    else:
        return jsonify({"success": False, "message": f"Agent {agent_name} not found"}), 404

@agents_bp.route('/', methods=['POST'])
def create_agent():
    """创建新的 agent"""
    data = request.json
    agent_name = data.get('name')
    version = data.get('version', '0.0.1')
    authors = data.get('authors', 'MoFA_Stage User')
    agent_type = data.get('agent_type', 'agent-hub')  # 默认为 agent-hub 类型
    
    if not agent_name:
        return jsonify({"success": False, "message": "Agent name is required"}), 400
    
    # 验证 agent_type 是否有效
    if agent_type not in ['agent-hub', 'examples']:
        return jsonify({"success": False, "message": "Invalid agent_type. Must be 'agent-hub' or 'examples'"}), 400
    
    mofa_cli = get_mofa_cli()
    result = mofa_cli.create_agent(agent_name, version, authors, agent_type)
    return jsonify(result)

@agents_bp.route('/copy', methods=['POST'])
def copy_agent():
    """复制现有 agent"""
    data = request.json
    source_agent = data.get('source')
    target_agent = data.get('target')
    agent_type = data.get('agent_type')  # 可以是 None，这样会自动检测源 Agent 的类型
    
    if not source_agent or not target_agent:
        return jsonify({"success": False, "message": "Source and target agent names are required"}), 400
    
    # 如果指定了 agent_type，验证其是否有效
    if agent_type is not None and agent_type not in ['agent-hub', 'examples']:
        return jsonify({"success": False, "message": "Invalid agent_type. Must be 'agent-hub' or 'examples'"}), 400
    
    mofa_cli = get_mofa_cli()
    result = mofa_cli.copy_agent(source_agent, target_agent, agent_type)
    return jsonify(result)

@agents_bp.route('/<agent_name>', methods=['DELETE'])
def delete_agent(agent_name):
    """删除指定 agent"""
    mofa_cli = get_mofa_cli()
    result = mofa_cli.delete_agent(agent_name)
    return jsonify(result)

@agents_bp.route('/<agent_name>/run', methods=['POST'])
def run_agent(agent_name):
    """运行指定的 agent或示例"""
    data = request.json
    timeout = data.get('timeout', 5)  # 默认超时5秒
    agent_type = data.get('agent_type', 'auto')  # 默认自动检测类型
    
    mofa_cli = get_mofa_cli()
    
    # 根据类型或自动检测运行不同的agent
    if agent_type == 'example':
        # 明确指定为示例，直接运行示例
        result = mofa_cli.run_example(agent_name, timeout)
    elif agent_type == 'atomic':
        # 明确指定为原子化agent，直接运行原子化agent
        result = mofa_cli.run_agent(agent_name, timeout)
    else:
        # 自动检测类型
        # 首先检查是否为原子化agent
        agent_path = os.path.join(mofa_cli.agent_hub_dir, agent_name)
        if os.path.exists(agent_path) and os.path.isdir(agent_path):
            result = mofa_cli.run_agent(agent_name, timeout)
        else:
            # 检查是否为示例
            example_path = os.path.join(mofa_cli.examples_dir, agent_name)
            if os.path.exists(example_path) and os.path.isdir(example_path):
                result = mofa_cli.run_example(agent_name, timeout)
            else:
                # 都不存在，返回错误
                result = {
                    "success": False,
                    "message": f"Agent or example '{agent_name}' not found in either agent-hub or examples directory"
                }
    
    return jsonify(result)

@agents_bp.route('/<agent_name>/logs', methods=['GET'])
def get_agent_logs(agent_name):
    """获取指定agent的运行日志"""
    try:
        mofa_cli = get_mofa_cli()
        logs = mofa_cli.get_agent_logs(agent_name)
        
        # 即使日志为None也返回空字符串而不是404
        if logs is None:
            logs = f"未找到 {agent_name} 的日志文件。可能是该Agent还未运行过。"
        
        return jsonify({"success": True, "logs": logs})
    except Exception as e:
        return jsonify({"success": False, "error": str(e), "logs": "获取日志时出错"})

@agents_bp.route('/<agent_name>/process-output', methods=['GET'])
def get_process_output(agent_name):
    """获取正在运行的进程的输出"""
    mofa_cli = get_mofa_cli()
    result = mofa_cli.get_process_output(agent_name)
    return jsonify(result)

@agents_bp.route('/stop/<process_id>', methods=['POST'])
def stop_agent(process_id):
    """停止正在运行的 agent"""
    mofa_cli = get_mofa_cli()
    result = mofa_cli.stop_agent(process_id)
    return jsonify(result)

@agents_bp.route('/<agent_name>/files', methods=['GET'])
def get_agent_files(agent_name):
    """获取 agent 的所有文件"""
    mofa_cli = get_mofa_cli()
    details = mofa_cli.get_agent_details(agent_name)
    if not details:
        return jsonify({"success": False, "message": f"Agent {agent_name} not found"}), 404
    
    return jsonify({"success": True, "files": details.get('files', [])})

@agents_bp.route('/<agent_name>/files/<path:file_path>', methods=['GET'])
def get_file_content(agent_name, file_path):
    """获取文件内容"""
    mofa_cli = get_mofa_cli()
    result = mofa_cli.read_file(agent_name, file_path)
    if result.get('success'):
        file_type = get_file_type(file_path)
        return jsonify({
            "success": True, 
            "content": result.get('content'),
            "type": file_type
        })
    else:
        return jsonify(result), 404

@agents_bp.route('/<agent_name>/files/<path:file_path>', methods=['PUT'])
def update_file_content(agent_name, file_path):
    """更新文件内容"""
    if not request.is_json:
        return jsonify({"success": False, "message": "Content must be JSON"}), 400
    
    content = request.json.get('content')
    if content is None:
        return jsonify({"success": False, "message": "Content is required"}), 400
    
    mofa_cli = get_mofa_cli()
    result = mofa_cli.write_file(agent_name, file_path, content)
    return jsonify(result)
