"""
文件操作相关工具函数
"""
import os
import shutil
from pathlib import Path
import yaml
import toml

def read_file(file_path):
    """读取文件内容"""
    if not os.path.exists(file_path):
        return None
    
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def write_file(file_path, content):
    """写入文件内容"""
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing file {file_path}: {e}")
        return False

def get_file_type(file_path):
    """根据文件扩展名获取文件类型"""
    ext = os.path.splitext(file_path)[1][1:].lower()
    
    # 映射文件扩展名到语言类型
    ext_map = {
        'py': 'python',
        'md': 'markdown',
        'yml': 'yaml',
        'yaml': 'yaml',
        'toml': 'toml',
        'json': 'json',
        'txt': 'plaintext',
        'env': 'plaintext',
    }
    
    return ext_map.get(ext, 'plaintext')

def scan_directory(directory, ignore_dirs=None):
    """扫描目录，返回文件列表"""
    if ignore_dirs is None:
        ignore_dirs = ['.git', '__pycache__', '.venv', 'node_modules']
    
    files = []
    for root, dirs, filenames in os.walk(directory):
        # 跳过忽略的目录
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        for filename in filenames:
            file_path = os.path.join(root, filename)
            rel_path = os.path.relpath(file_path, directory)
            
            files.append({
                'name': filename,
                'path': rel_path,
                'type': get_file_type(filename),
                'size': os.path.getsize(file_path)
            })
    
    return files

def parse_yaml(file_path):
    """解析YAML文件为Python对象"""
    try:
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error parsing YAML file {file_path}: {e}")
        return None

def write_yaml(file_path, data):
    """将Python对象写入YAML文件"""
    try:
        with open(file_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
        return True
    except Exception as e:
        print(f"Error writing YAML file {file_path}: {e}")
        return False

def parse_toml(file_path):
    """解析TOML文件为Python对象"""
    try:
        with open(file_path, 'r') as f:
            return toml.load(f)
    except Exception as e:
        print(f"Error parsing TOML file {file_path}: {e}")
        return None

def write_toml(file_path, data):
    """将Python对象写入TOML文件"""
    try:
        with open(file_path, 'w') as f:
            toml.dump(data, f)
        return True
    except Exception as e:
        print(f"Error writing TOML file {file_path}: {e}")
        return False

def parse_env_file(file_path):
    """解析.env文件为字典"""
    result = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                key, value = line.split('=', 1)
                result[key.strip()] = value.strip()
        return result
    except Exception as e:
        print(f"Error parsing .env file {file_path}: {e}")
        return {}

def write_env_file(file_path, data):
    """将字典写入.env文件"""
    try:
        with open(file_path, 'w') as f:
            for key, value in data.items():
                f.write(f"{key}={value}\n")
        return True
    except Exception as e:
        print(f"Error writing .env file {file_path}: {e}")
        return False
