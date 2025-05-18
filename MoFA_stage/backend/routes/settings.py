"""
设置相关的 API 路由
"""
from flask import Blueprint, request, jsonify, current_app
import os
import sys
import json
import fcntl  # 用于文件锁
import logging

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.file_ops import read_file, write_file
from utils.ttyd_manager import restart_ttyd
from config import (DEFAULT_MOFA_ENV, DEFAULT_MOFA_DIR, USE_SYSTEM_MOFA, 
                   DEFAULT_AGENT_HUB_PATH, DEFAULT_EXAMPLES_PATH,
                   CUSTOM_AGENT_HUB_PATH, CUSTOM_EXAMPLES_PATH,
                   MOFA_STAGE_DIR, REL_MOFA_DIR, 
                   REL_DEFAULT_AGENT_HUB_PATH, REL_DEFAULT_EXAMPLES_PATH)

# Configure logging
logger = logging.getLogger('settings_routes')

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
    "use_relative_paths": True,  # 是否使用相对路径
    "theme": "light",
    "editor_font_size": 14,
    "editor_tab_size": 4,
    # SSH连接设置
    "ssh": {
        "hostname": "127.0.0.1",
        "port": 22,
        "username": "",
        "password": "",
        "auto_connect": True  # 是否自动连接
    },
    "terminal_display_mode": "both",  # 终端显示模式: both, terminal, webssh
    "ttyd_port": 8080  # 默认ttyd端口
}

def get_absolute_path(relative_path):
    """将相对路径转换为绝对路径"""
    if os.path.isabs(relative_path):
        return relative_path
    return os.path.normpath(os.path.join(MOFA_STAGE_DIR, relative_path))

def get_settings():
    """获取设置信息，使用文件锁防止并发访问问题"""
    if not os.path.exists(SETTINGS_FILE):
        # 如果设置文件不存在，创建默认设置
        with open(SETTINGS_FILE, 'w') as f:
            fcntl.flock(f, fcntl.LOCK_EX)  # 独占锁
            json.dump(DEFAULT_SETTINGS, f, indent=2)
            fcntl.flock(f, fcntl.LOCK_UN)  # 释放锁
        return DEFAULT_SETTINGS
    
    try:
        with open(SETTINGS_FILE, 'r') as f:
            fcntl.flock(f, fcntl.LOCK_SH)  # 共享锁
            settings = json.load(f)
            fcntl.flock(f, fcntl.LOCK_UN)  # 释放锁
            
            # 确保设置中包含新增的字段
            for key, value in DEFAULT_SETTINGS.items():
                if key not in settings:
                    settings[key] = value
            
            # 处理路径设置
            if settings.get("use_relative_paths", True):
                # 如果使用默认路径和相对路径
                if settings.get("use_default_agent_hub_path", True):
                    settings["agent_hub_path"] = get_absolute_path(REL_DEFAULT_AGENT_HUB_PATH)
                if settings.get("use_default_examples_path", True):
                    settings["examples_path"] = get_absolute_path(REL_DEFAULT_EXAMPLES_PATH)
                if not settings.get("mofa_dir") or settings.get("mofa_dir") == DEFAULT_MOFA_DIR:
                    settings["mofa_dir"] = get_absolute_path(REL_MOFA_DIR)
            
            return settings
    except Exception as e:
        print(f"Error reading settings file: {e}")
        return DEFAULT_SETTINGS

def save_settings_to_file(settings):
    """保存设置信息，使用文件锁防止并发写入冲突"""
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
        
        with open(SETTINGS_FILE, 'w') as f:
            fcntl.flock(f, fcntl.LOCK_EX)  # 独占锁
            json.dump(settings, f, indent=2)
            fcntl.flock(f, fcntl.LOCK_UN)  # 释放锁
        logger.info(f"Settings saved successfully to {SETTINGS_FILE}")
        return True
    except Exception as e:
        logger.error(f"Error saving settings file: {e}")
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
    if save_settings_to_file(current_settings):
        return jsonify({"success": True, "settings": current_settings})
    else:
        return jsonify({"success": False, "message": "Failed to save settings"}), 500

@settings_bp.route('/reset', methods=['POST'])
def reset_settings():
    """重置设置为默认值"""
    if save_settings_to_file(DEFAULT_SETTINGS):
        return jsonify({"success": True, "settings": DEFAULT_SETTINGS})
    else:
        return jsonify({"success": False, "message": "Failed to reset settings"}), 500

@settings_bp.route('/save', methods=['POST'])
def api_save_settings():
    """保存设置 API endpoint"""
    try:
        # Get the settings from the request body
        new_settings = request.json
        
        # Check if ttyd_port was changed
        ttyd_port_changed = False
        try:
            with open(SETTINGS_FILE, 'r') as f:
                current_settings = json.load(f)
                if 'ttyd_port' in new_settings and 'ttyd_port' in current_settings:
                    if new_settings['ttyd_port'] != current_settings['ttyd_port']:
                        ttyd_port_changed = True
                        logger.info(f"ttyd port changed from {current_settings['ttyd_port']} to {new_settings['ttyd_port']}")
        except Exception as e:
            logger.warning(f"Could not read current settings: {e}")
            # If settings file doesn't exist, considering it a new file
            pass
        
        # 处理路径设置
        if new_settings.get("use_relative_paths", True):
            # 如果使用默认路径和相对路径
            if new_settings.get("use_default_agent_hub_path", True):
                new_settings["agent_hub_path"] = get_absolute_path(REL_DEFAULT_AGENT_HUB_PATH)
            if new_settings.get("use_default_examples_path", True):
                new_settings["examples_path"] = get_absolute_path(REL_DEFAULT_EXAMPLES_PATH)
            if not new_settings.get("mofa_dir") or new_settings.get("mofa_dir") == DEFAULT_MOFA_DIR:
                new_settings["mofa_dir"] = get_absolute_path(REL_MOFA_DIR)
        
        # Save the settings to the file
        if not save_settings_to_file(new_settings):
            return jsonify({"success": False, "message": "Failed to save settings to file"}), 500
        
        # If ttyd_port was changed, restart the ttyd service
        if ttyd_port_changed:
            try:
                logger.info("Restarting ttyd service due to port change")
                restart_ttyd()
            except Exception as e:
                # Log the error but don't fail the request
                logger.error(f"Failed to restart ttyd service: {e}")
        
        return jsonify({"success": True, "message": "Settings saved successfully"})
    except Exception as e:
        logger.error(f"Error saving settings: {e}")
        return jsonify({"success": False, "message": f"Failed to save settings: {str(e)}"}), 500
