"""
MoFA_Stage 配置文件
"""
import os

# Flask 配置
DEBUG = True
SECRET_KEY = 'mofa-stage-secret-key'

# MoFA 配置
DEFAULT_MOFA_ENV = '/mnt/c/Users/ufop/Desktop/code/mofa_third_stage/mofa_venv'
DEFAULT_MOFA_DIR = '/mnt/c/Users/ufop/Desktop/code/mofa_second_stage/mofa'
# 默认使用系统MOFA
USE_SYSTEM_MOFA = True
# 原子化Agent存储位置（agent-hub）
AGENT_HUB_PATH = 'python/agent-hub'  # 官方推荐的agent-hub目录
DEFAULT_AGENT_HUB_PATH = os.path.join(DEFAULT_MOFA_DIR, AGENT_HUB_PATH)

# 示例组合存储位置（examples）
EXAMPLES_PATH = 'python/examples'  # 示例目录
DEFAULT_EXAMPLES_PATH = os.path.join(DEFAULT_MOFA_DIR, EXAMPLES_PATH)

# 自定义路径选项
CUSTOM_AGENT_HUB_PATH = ''  # 用户可指定完整路径
CUSTOM_EXAMPLES_PATH = ''  # 用户可指定完整路径

# 编辑器配置
SUPPORTED_FILE_TYPES = {
    'py': 'python',
    'md': 'markdown',
    'yml': 'yaml',
    'yaml': 'yaml',
    'toml': 'toml',
    'env': 'plaintext'
}
