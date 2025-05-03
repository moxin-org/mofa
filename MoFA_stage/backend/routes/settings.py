"""
设置相关的 API 路由
"""
from flask import Blueprint, request, jsonify
import os
import sys
import json

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.file_ops import read_file, write_file
from config import (DEFAULT_MOFA_ENV, DEFAULT_MOFA_DIR, USE_SYSTEM_MOFA, 
                   DEFAULT_AGENT_HUB_PATH, DEFAULT_EXAMPLES_PATH,
                   CUSTOM_AGENT_HUB_PATH, CUSTOM_EXAMPLES_PATH)

settings_bp = Blueprint('settings', __name__, url_prefix='/api/settings')

# 设置文件路径
SETTINGS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'settings.json')

# 默认设置
DEFAULT_SETTINGS = {
    "mofa_env_path": DEFAULT_MOFA_ENV,
    "mofa_dir": DEFAULT_MOFA_DIR,
    "use_system_mofa": USE_SYSTEM_MOFA,
    # 分开存储agent-hub和examples的路径
    "use_default_agent_hub_path": True,  # 是否使用默认agent-hub路径
    "use_default_examples_path": True,  # 是否使用默认examples路径
    "agent_hub_path": DEFAULT_AGENT_HUB_PATH,  # 默认agent-hub路径
    "examples_path": DEFAULT_EXAMPLES_PATH,  # 默认examples路径
    "custom_agent_hub_path": CUSTOM_AGENT_HUB_PATH,  # 自定义agent-hub路径
    "custom_examples_path": CUSTOM_EXAMPLES_PATH,  # 自定义examples路径
    "theme": "light",
    "editor_font_size": 14,
    "editor_tab_size": 4
}

def get_settings():
    """获取设置信息"""
    if not os.path.exists(SETTINGS_FILE):
        # 如果设置文件不存在，创建默认设置
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(DEFAULT_SETTINGS, f, indent=2)
        return DEFAULT_SETTINGS
    
    try:
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading settings file: {e}")
        return DEFAULT_SETTINGS

def save_settings(settings):
    """保存设置信息"""
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving settings file: {e}")
        return False

@settings_bp.route('/', methods=['GET'])
def get_all_settings():
    """获取所有设置"""
    settings = get_settings()
    return jsonify({"success": True, "settings": settings})

@settings_bp.route('/', methods=['PUT'])
def update_settings():
    """更新设置"""
    if not request.is_json:
        return jsonify({"success": False, "message": "Settings must be JSON"}), 400
    
    new_settings = request.json
    current_settings = get_settings()
    
    # 更新设置
    for key, value in new_settings.items():
        current_settings[key] = value
    
    # 保存设置
    if save_settings(current_settings):
        return jsonify({"success": True, "settings": current_settings})
    else:
        return jsonify({"success": False, "message": "Failed to save settings"}), 500

@settings_bp.route('/reset', methods=['POST'])
def reset_settings():
    """重置设置为默认值"""
    if save_settings(DEFAULT_SETTINGS):
        return jsonify({"success": True, "settings": DEFAULT_SETTINGS})
    else:
        return jsonify({"success": False, "message": "Failed to reset settings"}), 500
