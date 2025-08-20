#!/bin/bash

# 设置错误时退出
set -e

# 定义颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 定义语言选择
LANG_ZH=1
LANG_EN=2
current_lang=$LANG_ZH

# 中文语言包
ZH_INFO="[信息]"
ZH_ERROR="[错误]"
ZH_PERMISSION_CHECK="检查脚本权限..."
ZH_PERMISSION_DENIED="脚本没有执行权限!"
ZH_PERMISSION_FIX="请运行以下命令赋予权限:"
ZH_CMD_NOT_FOUND="未安装，请先安装"
ZH_STARTING_BACKEND="正在启动后端服务..."
ZH_INSTALL_PYTHON_DEPS="安装 Python 依赖"
ZH_BACKEND_STARTED="后端服务已启动 (PID:"
ZH_STARTING_FRONTEND="正在启动前端服务..."
ZH_INSTALL_FRONTEND_DEPS="安装前端依赖..."
ZH_FRONTEND_STARTED="前端服务已启动 (PID:"
ZH_SHUTTING_DOWN="正在关闭服务..."
ZH_SERVICES_SHUTDOWN="服务已关闭"
ZH_ALL_SERVICES_STARTED="所有服务已启动！"
ZH_BACKEND_RUNNING="后端服务运行在"
ZH_FRONTEND_RUNNING="前端服务运行在"
ZH_PRESS_CTRL_C="按 Ctrl+C 停止所有服务"
ZH_SELECT_LANGUAGE="请选择语言 / Please select language:"

# 英文语言包
EN_INFO="[INFO]"
EN_ERROR="[ERROR]"
EN_PERMISSION_CHECK="Checking script permissions..."
EN_PERMISSION_DENIED="Script does not have execute permission!"
EN_PERMISSION_FIX="Please run the following command to grant permissions:"
EN_CMD_NOT_FOUND="is not installed, please install"
EN_STARTING_BACKEND="Starting backend service..."
EN_INSTALL_PYTHON_DEPS="Installing Python dependencies"
EN_BACKEND_STARTED="Backend service started (PID:"
EN_STARTING_FRONTEND="Starting frontend service..."
EN_INSTALL_FRONTEND_DEPS="Installing frontend dependencies..."
EN_FRONTEND_STARTED="Frontend service started (PID:"
EN_SHUTTING_DOWN="Shutting down services..."
EN_SERVICES_SHUTDOWN="Services shut down"
EN_ALL_SERVICES_STARTED="All services started!"
EN_BACKEND_RUNNING="Backend service running at"
EN_FRONTEND_RUNNING="Frontend service running at"
EN_PRESS_CTRL_C="Press Ctrl+C to stop all services"
EN_SELECT_LANGUAGE="Please select language:"

# 显示语言选择函数
select_language() {
    echo -e "${YELLOW}$ZH_SELECT_LANGUAGE${NC}"
    echo "1. 中文"
    echo "2. English"
    read -p "选择/Select (1/2, default: 1): " lang_choice
    
    if [ "$lang_choice" = "2" ]; then
        current_lang=$LANG_EN
    else
        current_lang=$LANG_ZH
    fi
}

# 打印带颜色的信息
print_info() {
    if [ $current_lang -eq $LANG_ZH ]; then
        echo -e "${GREEN}$ZH_INFO${NC} $1"
    else
        echo -e "${GREEN}$EN_INFO${NC} $1"
    fi
}

print_error() {
    if [ $current_lang -eq $LANG_ZH ]; then
        echo -e "${RED}$ZH_ERROR${NC} $1"
    else
        echo -e "${RED}$EN_ERROR${NC} $1"
    fi
}

# 带颜色输出函数
print_color_msg() {
    local color="$1"
    local zh_msg="$2"
    local en_msg="$3"
    
    if [ $current_lang -eq $LANG_ZH ]; then
        echo -e "${color}${zh_msg}${NC}"
    else
        echo -e "${color}${en_msg}${NC}"
    fi
}

# 权限检查函数
check_permissions() {
    print_color_msg "$YELLOW" "$ZH_PERMISSION_CHECK" "$EN_PERMISSION_CHECK"
    
    if [ ! -x "$0" ]; then
        print_color_msg "$RED" "$ZH_PERMISSION_DENIED" "$EN_PERMISSION_DENIED"
        print_color_msg "$YELLOW" "$ZH_PERMISSION_FIX" "$EN_PERMISSION_FIX"
        echo "chmod +x $(basename "$0")"
        exit 1
    fi
}

# 检查必要的命令是否存在
check_command() {
    if ! command -v $1 &> /dev/null; then
        if [ $current_lang -eq $LANG_ZH ]; then
            print_error "$1 $ZH_CMD_NOT_FOUND $1"
        else
            print_error "$1 $EN_CMD_NOT_FOUND $1"
        fi
        exit 1
    fi
}

# 初始化语言选择 - 优先使用环境变量，否则询问用户
if [ ! -z "$MOFA_LANG" ]; then
    current_lang=$MOFA_LANG
else
    select_language
fi

# 权限检查
check_permissions

# 检查 Python 和 Node.js
check_command python3
check_command node
check_command npm

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# 启动后端服务
start_backend() {
    if [ $current_lang -eq $LANG_ZH ]; then
        print_info "$ZH_STARTING_BACKEND"
    else
        print_info "$EN_STARTING_BACKEND"
    fi
    cd "$SCRIPT_DIR/backend"
    
    # 安装 Python 依赖
    if [ $current_lang -eq $LANG_ZH ]; then
        print_info "$ZH_INSTALL_PYTHON_DEPS"
    else
        print_info "$EN_INSTALL_PYTHON_DEPS"
    fi
    pip3 install -r requirements.txt
    
    # 在后台启动 Flask 服务
    python3 app.py &
    BACKEND_PID=$!
    if [ $current_lang -eq $LANG_ZH ]; then
        print_info "$ZH_BACKEND_STARTED $BACKEND_PID)"
    else
        print_info "$EN_BACKEND_STARTED $BACKEND_PID)"
    fi
}

# 启动前端服务
start_frontend() {
    if [ $current_lang -eq $LANG_ZH ]; then
        print_info "$ZH_STARTING_FRONTEND"
    else
        print_info "$EN_STARTING_FRONTEND"
    fi
    cd "$SCRIPT_DIR/frontend"
    
    # 检查并安装 Node.js 依赖
    if [ ! -d "node_modules" ]; then
        if [ $current_lang -eq $LANG_ZH ]; then
            print_info "$ZH_INSTALL_FRONTEND_DEPS"
        else
            print_info "$EN_INSTALL_FRONTEND_DEPS"
        fi
        npm install
    fi
    
    # 在后台启动 Vite 开发服务器
    npm run dev &
    FRONTEND_PID=$!
    if [ $current_lang -eq $LANG_ZH ]; then
        print_info "$ZH_FRONTEND_STARTED $FRONTEND_PID)"
    else
        print_info "$EN_FRONTEND_STARTED $FRONTEND_PID)"
    fi
}

# 清理函数
cleanup() {
    if [ $current_lang -eq $LANG_ZH ]; then
        print_info "$ZH_SHUTTING_DOWN"
    else
        print_info "$EN_SHUTTING_DOWN"
    fi
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    if [ $current_lang -eq $LANG_ZH ]; then
        print_info "$ZH_SERVICES_SHUTDOWN"
    else
        print_info "$EN_SERVICES_SHUTDOWN"
    fi
    exit 0
}

# 注册清理函数
trap cleanup SIGINT SIGTERM

# 启动服务
start_backend

start_frontend

if [ $current_lang -eq $LANG_ZH ]; then
    print_info "$ZH_ALL_SERVICES_STARTED"
    print_info "$ZH_BACKEND_RUNNING http://localhost:5000"
    print_info "$ZH_FRONTEND_RUNNING http://localhost:5173"
    print_info "$ZH_PRESS_CTRL_C"
else
    print_info "$EN_ALL_SERVICES_STARTED"
    print_info "$EN_BACKEND_RUNNING http://localhost:5000"
    print_info "$EN_FRONTEND_RUNNING http://localhost:5173"
    print_info "$EN_PRESS_CTRL_C"
fi

# 保持脚本运行
wait 