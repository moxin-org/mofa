#!/bin/bash

# 设置错误时退出
set -e

# 定义颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 打印带颜色的信息
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查必要的命令是否存在
check_command() {
    if ! command -v $1 &> /dev/null; then
        print_error "$1 未安装，请先安装 $1"
        exit 1
    fi
}

# 检查 Python 和 Node.js
check_command python3
check_command node
check_command npm

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# 启动后端服务
start_backend() {
    print_info "正在启动后端服务..."
    cd "$SCRIPT_DIR/backend"
    
    # 安装 Python 依赖
    pip install -r requirements.txt
    
    # 在后台启动 Flask 服务
    python3 app.py &
    BACKEND_PID=$!
    print_info "后端服务已启动 (PID: $BACKEND_PID)"
}

# 启动前端服务
start_frontend() {
    print_info "正在启动前端服务..."
    cd "$SCRIPT_DIR/frontend"
    
    # 检查并安装 Node.js 依赖
    if [ ! -d "node_modules" ]; then
        print_info "安装前端依赖..."
        npm install
    fi
    
    # 在后台启动 Vite 开发服务器
    npm run dev &
    FRONTEND_PID=$!
    print_info "前端服务已启动 (PID: $FRONTEND_PID)"
}

# 清理函数
cleanup() {
    print_info "正在关闭服务..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    print_info "服务已关闭"
    exit 0
}

# 注册清理函数
trap cleanup SIGINT SIGTERM

# 启动服务
start_backend
start_frontend

print_info "所有服务已启动！"
print_info "后端服务运行在 http://localhost:5000"
print_info "前端服务运行在 http://localhost:5173"
print_info "按 Ctrl+C 停止所有服务"

# 保持脚本运行
wait 