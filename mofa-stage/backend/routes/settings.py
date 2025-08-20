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
                   REL_DEFAULT_AGENT_HUB_PATH, REL_DEFAULT_EXAMPLES_PATH,
                   DEFAULT_MOFA_MODE, DEFAULT_DOCKER_CONTAINER,
                   AGENT_HUB_PATH, EXAMPLES_PATH)

# Configure logging
logger = logging.getLogger('settings_routes')

settings_bp = Blueprint('settings', __name__, url_prefix='/api/settings')

# 设置文件路径
SETTINGS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'settings.json')

# 默认设置
DEFAULT_SETTINGS = {
    "mofa_env_path": DEFAULT_MOFA_ENV,
    "mofa_dir": DEFAULT_MOFA_DIR,
    "mofa_mode": DEFAULT_MOFA_MODE,  # 'system', 'venv', or 'docker'
    "docker_container_name": DEFAULT_DOCKER_CONTAINER,  # name or id of docker container
    "use_system_mofa": USE_SYSTEM_MOFA,  # deprecated, kept for backward compatibility
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
    "ttyd_port": 8080,  # 默认ttyd端口
    # ---- AI API Settings ----
    # OpenAI
    "openai_api_key": "",
    "openai_base_url": "https://api.openai.com/v1",
    # Azure OpenAI
    "azure_openai_api_key": "",
    "azure_openai_endpoint": "",  # e.g. https://your-resource.openai.azure.com/
    "azure_openai_api_version": "2023-05-15-preview",
    # Google Gemini
    "gemini_api_key": "",
    "gemini_api_endpoint": "https://generativelanguage.googleapis.com/v1beta"
}

def get_absolute_path(relative_path):
    """将相对路径转换为绝对路径"""
    if os.path.isabs(relative_path):
        return relative_path
    return os.path.normpath(os.path.join(MOFA_STAGE_DIR, relative_path))

def detect_mofa_root():
    """自动检测MOFA项目根目录
    通过从当前目录向上查找特征文件/目录来确定MOFA根目录
    """
    # 首先尝试使用REL_MOFA_DIR计算
    mofa_dir = get_absolute_path(REL_MOFA_DIR)
    
    # 检查这个目录是否有效：查找python/agent-hub和python/examples目录
    if os.path.exists(os.path.join(mofa_dir, 'python')) and \
       (os.path.exists(os.path.join(mofa_dir, 'python/agent-hub')) or \
        os.path.exists(os.path.join(mofa_dir, 'python/examples'))):
        logger.info(f"检测到MOFA根目录: {mofa_dir}")
        return mofa_dir
    
    # 如果计算出的目录无效，尝试寻找真实的根目录
    # 从当前目录开始，向上查找
    current_dir = os.path.abspath(MOFA_STAGE_DIR)
    
    # 最多向上查找3级目录
    for _ in range(4):
        parent_dir = os.path.dirname(current_dir)
        
        # 检查是否存在python/agent-hub和python/examples目录
        python_dir = os.path.join(parent_dir, 'python')
        if os.path.exists(python_dir) and \
           (os.path.exists(os.path.join(python_dir, 'agent-hub')) or \
            os.path.exists(os.path.join(python_dir, 'examples'))):
            logger.info(f"自动检测到MOFA根目录: {parent_dir}")
            return parent_dir
        
        current_dir = parent_dir
    
    # 如果找不到，返回默认值
    logger.warning(f"无法自动检测MOFA根目录，使用默认值: {DEFAULT_MOFA_DIR}")
    return DEFAULT_MOFA_DIR

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
            
            # 确保mofa_dir是有效的
            if not settings.get("mofa_dir") or not os.path.exists(settings.get("mofa_dir")):
                settings["mofa_dir"] = detect_mofa_root()
            
            # ------------------------------------------------------------------
            # 使用 mofa_dir 重新计算默认的 agent_hub_path / examples_path
            # 之前的实现用 get_absolute_path() 以 backend 目录为基准，
            # 会得到诸如 /Users/xxx/Code/python/agent-hub 这样的错误路径。
            # 这里统一用 mofa_dir 拼接 python/agent-hub | python/examples，
            # 只有在 *使用默认路径* 且 *允许使用相对路径* 的场景才覆盖。
            # ------------------------------------------------------------------
            if settings.get("use_default_agent_hub_path", True):
                settings["agent_hub_path"] = os.path.join(settings["mofa_dir"], AGENT_HUB_PATH)
            if settings.get("use_default_examples_path", True):
                settings["examples_path"] = os.path.join(settings["mofa_dir"], EXAMPLES_PATH)
            
            # 处理路径设置
            if settings.get("use_relative_paths", True):
                # 如果使用默认路径和相对路径
                if not settings.get("use_default_agent_hub_path", True):
                    # 使用自定义路径
                    settings["agent_hub_path"] = settings.get("custom_agent_hub_path", CUSTOM_AGENT_HUB_PATH)
                    
                if not settings.get("use_default_examples_path", True):
                    # 使用自定义路径
                    settings["examples_path"] = settings.get("custom_examples_path", CUSTOM_EXAMPLES_PATH)
                    
                # 仅在用户未指定mofa_dir时使用计算的相对路径
                if settings.get("mofa_dir") == DEFAULT_MOFA_DIR:
                    settings["mofa_dir"] = detect_mofa_root()
            else:
                # 如果不使用相对路径，但使用默认路径
                if settings.get("use_default_agent_hub_path", True):
                    settings["agent_hub_path"] = os.path.join(settings.get("mofa_dir", DEFAULT_MOFA_DIR), AGENT_HUB_PATH)
                else:
                    # 使用自定义路径
                    settings["agent_hub_path"] = settings.get("custom_agent_hub_path", CUSTOM_AGENT_HUB_PATH)
                    
                if settings.get("use_default_examples_path", True):
                    settings["examples_path"] = os.path.join(settings.get("mofa_dir", DEFAULT_MOFA_DIR), EXAMPLES_PATH)
                else:
                    # 使用自定义路径
                    settings["examples_path"] = settings.get("custom_examples_path", CUSTOM_EXAMPLES_PATH)
            
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
        
        # 确保mofa_dir是有效的
        if not new_settings.get("mofa_dir") or not os.path.exists(new_settings.get("mofa_dir")):
            new_settings["mofa_dir"] = detect_mofa_root()
        
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
            if not new_settings.get("use_default_agent_hub_path", True):
                # 使用自定义路径
                new_settings["agent_hub_path"] = new_settings.get("custom_agent_hub_path", CUSTOM_AGENT_HUB_PATH)
                
            if not new_settings.get("use_default_examples_path", True):
                # 使用自定义路径
                new_settings["examples_path"] = new_settings.get("custom_examples_path", CUSTOM_EXAMPLES_PATH)
                
            # 仅在用户未指定mofa_dir时使用计算的相对路径
            if not new_settings.get("mofa_dir") or new_settings.get("mofa_dir") == DEFAULT_MOFA_DIR:
                new_settings["mofa_dir"] = detect_mofa_root()
        else:
            # 如果不使用相对路径，但使用默认路径
            if new_settings.get("use_default_agent_hub_path", True):
                new_settings["agent_hub_path"] = os.path.join(new_settings.get("mofa_dir", DEFAULT_MOFA_DIR), AGENT_HUB_PATH)
            else:
                # 使用自定义路径
                new_settings["agent_hub_path"] = new_settings.get("custom_agent_hub_path", CUSTOM_AGENT_HUB_PATH)
                
            if new_settings.get("use_default_examples_path", True):
                new_settings["examples_path"] = os.path.join(new_settings.get("mofa_dir", DEFAULT_MOFA_DIR), EXAMPLES_PATH)
            else:
                # 使用自定义路径
                new_settings["examples_path"] = new_settings.get("custom_examples_path", CUSTOM_EXAMPLES_PATH)
        
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
