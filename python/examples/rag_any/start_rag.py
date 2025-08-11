#!/usr/bin/env python3
"""
RAG 系统快速启动脚本
"""

import asyncio
import subprocess
import sys
from pathlib import Path

def check_docker():
    """检查 Docker 是否运行"""
    try:
        result = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def start_qdrant():
    """启动 Qdrant 服务"""
    try:
        # 检查是否已经在运行
        result = subprocess.run(['docker', 'ps', '--filter', 'name=qdrant-vector-db', '--format', '{{.Names}}'], 
                              capture_output=True, text=True)
        if 'qdrant-vector-db' in result.stdout:
            return True
            
        # 启动服务
        compose_file = Path(__file__).parent / 'docker-compose.qdrant.yml'
        result = subprocess.run([
            'docker-compose', '-f', str(compose_file), 'up', '-d'
        ], capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"启动错误: {e}")
        return False

def check_dependencies():
    """检查 Python 依赖"""
    try:
        import qdrant_client
        import httpx
        return True
    except ImportError:
        return False

async def main():
    print("🚀 RAG 系统启动检查")
    print("=" * 40)
    
    # 检查 Docker
    print("🐳 检查 Docker...")
    if not check_docker():
        print("❌ Docker 未运行，请先启动 Docker")
        sys.exit(1)
    print("✅ Docker 正常")
    
    # 启动 Qdrant
    print("📊 启动 Qdrant...")
    if not start_qdrant():
        print("❌ Qdrant 启动失败")
        sys.exit(1)
    print("✅ Qdrant 已启动")
    
    # 检查依赖
    print("📦 检查 Python 依赖...")
    if not check_dependencies():
        print("❌ 缺少依赖，请运行: pip install qdrant-client httpx")
        sys.exit(1)
    print("✅ 依赖完整")
    
    print("\n🎉 系统检查完成，启动 RAG 问答系统...\n")
    
    # 启动主程序
    from qdrant_rag_interactive import main as rag_main
    await rag_main()

if __name__ == "__main__":
    asyncio.run(main())