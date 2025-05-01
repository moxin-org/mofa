"""
MoFA_Stage 配置文件
"""
import os

# Flask 配置
DEBUG = True
SECRET_KEY = 'mofa-stage-secret-key'

# MoFA 配置
DEFAULT_MOFA_ENV = '/mnt/c/Users/ufop/Desktop/code/mofa_second_stage/mofa/mofa_test_env'
DEFAULT_MOFA_DIR = '/mnt/c/Users/ufop/Desktop/code/mofa_second_stage/mofa'
# 默认使用系统MOFA
USE_SYSTEM_MOFA = True
# Agent存储位置选项
AGENT_STORAGE_OPTIONS = {
    'examples': 'python/examples',   # 示例目录
    'agent-hub': 'python/agent-hub',  # 官方推荐的agent-hub目录
    'custom': ''  # 自定义目录，用户可指定完整路径
}
# 默认使用examples目录
DEFAULT_AGENT_STORAGE = 'examples'
AGENTS_DIR = os.path.join(DEFAULT_MOFA_DIR, AGENT_STORAGE_OPTIONS[DEFAULT_AGENT_STORAGE])

# 编辑器配置
SUPPORTED_FILE_TYPES = {
    'py': 'python',
    'md': 'markdown',
    'yml': 'yaml',
    'yaml': 'yaml',
    'toml': 'toml',
    'env': 'plaintext'
}
