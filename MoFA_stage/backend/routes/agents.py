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
    """获取所有 agents 列表"""
    mofa_cli = get_mofa_cli()
    agents = mofa_cli.list_agents()
    return jsonify({"success": True, "agents": agents})

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
    
    if not agent_name:
        return jsonify({"success": False, "message": "Agent name is required"}), 400
    
    mofa_cli = get_mofa_cli()
    result = mofa_cli.create_agent(agent_name, version, authors)
    return jsonify(result)

@agents_bp.route('/copy', methods=['POST'])
def copy_agent():
    """复制现有 agent"""
    data = request.json
    source_agent = data.get('source')
    target_agent = data.get('target')
    
    if not source_agent or not target_agent:
        return jsonify({"success": False, "message": "Source and target agent names are required"}), 400
    
    mofa_cli = get_mofa_cli()
    result = mofa_cli.copy_agent(source_agent, target_agent)
    return jsonify(result)

@agents_bp.route('/<agent_name>', methods=['DELETE'])
def delete_agent(agent_name):
    """删除指定 agent"""
    mofa_cli = get_mofa_cli()
    result = mofa_cli.delete_agent(agent_name)
    return jsonify(result)

@agents_bp.route('/<agent_name>/run', methods=['POST'])
def run_agent(agent_name):
    """运行指定的 agent"""
    data = request.json
    timeout = data.get('timeout', 5)  # 默认超时5秒
    
    mofa_cli = get_mofa_cli()
    result = mofa_cli.run_agent(agent_name, timeout)
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
        print(f"获取日志发生错误: {str(e)}")
        # 出错时也返回200状态码，避免前端显示404
        return jsonify({"success": False, "logs": f"获取日志时发生错误: {str(e)}"})

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
