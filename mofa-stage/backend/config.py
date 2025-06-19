"""
MoFA_Stage 配置文件
"""
import os

# 获取MoFA_stage目录的绝对路径
MOFA_STAGE_DIR = os.path.dirname(os.path.abspath(__file__))

# Flask 配置
DEBUG = True
SECRET_KEY = 'mofa-stage-secret-key'

# MoFA 配置
DEFAULT_MOFA_ENV = ''
DEFAULT_MOFA_DIR = ''
DEFAULT_MOFA_MODE = 'docker'  # system | venv | docker
DEFAULT_DOCKER_CONTAINER = ''  # Docker container name when using docker mode
# 默认使用系统MOFA
USE_SYSTEM_MOFA = True
# 原子化Agent存储位置（agent-hub）
AGENT_HUB_PATH = 'python/agent-hub'  # 官方推荐的agent-hub目录
# 示例组合存储位置（examples）
EXAMPLES_PATH = 'python/examples'  # 示例目录

# 相对路径设置（相对于MoFA_stage目录）
REL_MOFA_DIR = '../../'  # MoFA目录相对于backend目录的位置（backend -> MoFA_stage -> MOFA根目录）
DEFAULT_AGENT_HUB_PATH = os.path.join(DEFAULT_MOFA_DIR, AGENT_HUB_PATH)
DEFAULT_EXAMPLES_PATH = os.path.join(DEFAULT_MOFA_DIR, EXAMPLES_PATH)

# 使用相对路径的默认路径
REL_DEFAULT_AGENT_HUB_PATH = os.path.join(REL_MOFA_DIR, AGENT_HUB_PATH)
REL_DEFAULT_EXAMPLES_PATH = os.path.join(REL_MOFA_DIR, EXAMPLES_PATH)

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
