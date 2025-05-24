#!/bin/bash

# 强制使用bash执行
if [ -z "$BASH_VERSION" ]; then
    exec bash "$0" "$@"
    exit 1
fi

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # 恢复默认颜色

# 定义语言选择
LANG_ZH=1
LANG_EN=2
current_lang=$LANG_ZH

# 语言文本
# 中文
ZH_TITLE="==== MoFA_Stage 安装脚本 ===="
ZH_INTRO="这个脚本会帮你安装所有依赖"
ZH_SYSTEM_TYPE="系统类型:"
ZH_BACKEND_INSTALL="正在安装后端依赖..."
ZH_BACKEND_DIR_NOT_FOUND="找不到backend目录!"
ZH_PYTHON_VERSION="Python版本:"
ZH_CREATE_VENV="要创建虚拟环境吗? (y/n)"
ZH_CREATING_VENV="创建虚拟环境..."
ZH_PIP_INSTALL="pip安装依赖..."
ZH_BACKEND_DEPS_SUCCESS="后端依赖安装完成"
ZH_BACKEND_DEPS_FAIL="后端依赖安装失败"
ZH_FRONTEND_INSTALL="安装前端依赖..."
ZH_FRONTEND_DIR_NOT_FOUND="找不到frontend目录!"
ZH_INSTALL_NODEJS="请安装nodejs"
ZH_NODE_VERSION="Node.js版本:"
ZH_NPM_VERSION="npm版本:"
ZH_NPM_INSTALL="npm install..."
ZH_NPM_SUCCESS="npm包安装成功!"
ZH_NPM_FAIL="npm安装出错"
ZH_FRONTEND_BUILD="开始构建前端..."
ZH_BUILD_TIME="这可能要花一点时间..."
ZH_BUILD_SUCCESS="前端构建成功!"
ZH_BUILD_FAIL="构建失败"
ZH_CHECK_TTYD="检查ttyd..."
ZH_TTYD_INSTALLED="ttyd已安装，版本:"
ZH_INSTALL_TTYD="是否安装ttyd(y/n)"
ZH_SKIP_TTYD="跳过ttyd安装。提示: 终端功能可能会有问题"
ZH_DEBIAN_SYSTEM="Debian/Ubuntu系统，用apt安装..."
ZH_REDHAT_SYSTEM="RedHat/CentOS/Fedora系统，用yum安装..."
ZH_COMPILING="从源码编译中"
ZH_INSTALL_TTYD_MANUAL="请自行安装ttyd"
ZH_REFERENCE="参考:"
ZH_MACOS_SYSTEM="macOS系统，用brew安装..."
ZH_INSTALL_BREW="请先安装brew"
ZH_VISIT="访问:"
ZH_UNSUPPORTED_SYSTEM="不支持的系统"
ZH_TTYD_SUCCESS="ttyd安装完成!"
ZH_TTYD_FAIL="ttyd装失败，请手动安装"
ZH_BUILD_PROD="npm run devh或者构建生产环境"
ZH_BUILD_PROD_CONFIRM="要构建生产版本吗? (y/n)"
ZH_COMPLETE="==== 完成！ ===="
ZH_START_BACKEND="启动后端: cd backend && python app.py"
ZH_FRONTEND_DEPLOY="前端部署方式:"
ZH_NGINX_CONFIG="1. 配置Nginx指向frontend/dist目录"
ZH_SIMPLE_SERVER="2. 或者: cd frontend/dist && python -m http.server 3000"
ZH_INSTALL_COMPLETE="==== 安装完成 ===="
ZH_FRONTEND_DEV="前端开发模式: cd frontend && npm run dev"
ZH_FUTURE_BUILD="以后要构建生产版本: cd frontend && npm run build"
ZH_ACCESS_URL="访问地址: http://localhost:3000"
ZH_HAVE_FUN="祝您使用愉快!"
ZH_SWITCH_LANG="切换语言 (1: 中文, 2: 英文):"

# 英文
EN_TITLE="==== MoFA_Stage Installation Script ===="
EN_INTRO="This script will help you install all dependencies"
EN_SYSTEM_TYPE="System type:"
EN_BACKEND_INSTALL="Installing backend dependencies..."
EN_BACKEND_DIR_NOT_FOUND="Backend directory not found!"
EN_PYTHON_VERSION="Python version:"
EN_CREATE_VENV="Create virtual environment? (y/n)"
EN_CREATING_VENV="Creating virtual environment..."
EN_PIP_INSTALL="Installing pip dependencies..."
EN_BACKEND_DEPS_SUCCESS="Backend dependencies installed successfully"
EN_BACKEND_DEPS_FAIL="Backend dependencies installation failed"
EN_FRONTEND_INSTALL="Installing frontend dependencies..."
EN_FRONTEND_DIR_NOT_FOUND="Frontend directory not found!"
EN_INSTALL_NODEJS="Please install nodejs"
EN_NODE_VERSION="Node.js version:"
EN_NPM_VERSION="npm version:"
EN_NPM_INSTALL="npm install..."
EN_NPM_SUCCESS="npm packages installed successfully!"
EN_NPM_FAIL="npm installation error"
EN_FRONTEND_BUILD="Building frontend..."
EN_BUILD_TIME="This might take some time..."
EN_BUILD_SUCCESS="Frontend built successfully!"
EN_BUILD_FAIL="Build failed"
EN_CHECK_TTYD="Checking ttyd..."
EN_TTYD_INSTALLED="ttyd is installed, version:"
EN_INSTALL_TTYD="Install ttyd? (y/n)"
EN_SKIP_TTYD="Skipping ttyd installation. Note: Terminal functions may have issues"
EN_DEBIAN_SYSTEM="Debian/Ubuntu system, using apt to install..."
EN_REDHAT_SYSTEM="RedHat/CentOS/Fedora system, using yum to install..."
EN_COMPILING="Compiling from source"
EN_INSTALL_TTYD_MANUAL="Please install ttyd manually"
EN_REFERENCE="Reference:"
EN_MACOS_SYSTEM="macOS system, using brew to install..."
EN_INSTALL_BREW="Please install brew first"
EN_VISIT="Visit:"
EN_UNSUPPORTED_SYSTEM="Unsupported system"
EN_TTYD_SUCCESS="ttyd installed successfully!"
EN_TTYD_FAIL="ttyd installation failed, please install manually"
EN_BUILD_PROD="npm run devh or build production environment"
EN_BUILD_PROD_CONFIRM="Build production version? (y/n)"
EN_COMPLETE="==== Complete! ===="
EN_START_BACKEND="Start backend: cd backend && python app.py"
EN_FRONTEND_DEPLOY="Frontend deployment methods:"
EN_NGINX_CONFIG="1. Configure Nginx to point to frontend/dist directory"
EN_SIMPLE_SERVER="2. Or simpler: cd frontend/dist && python -m http.server 3000"
EN_INSTALL_COMPLETE="==== Installation Complete ===="
EN_FRONTEND_DEV="Frontend development mode: cd frontend && npm run dev"
EN_FUTURE_BUILD="For future production builds: cd frontend && npm run build"
EN_ACCESS_URL="Access URL: http://localhost:3000"
EN_HAVE_FUN="Have fun!"
EN_SWITCH_LANG="Switch language (1: Chinese, 2: English):"

# 显示语言选择函数
select_language() {
    echo -e "${YELLOW}请选择语言 / Please select language:${NC}"
    echo "1. 中文"
    echo "2. English"
    read -p "选择/Select (1/2): " lang_choice
    
    if [ "$lang_choice" = "2" ]; then
        current_lang=$LANG_EN
    else
        current_lang=$LANG_ZH
    fi
}

# 语言切换函数
switch_language() {
    if [ $current_lang -eq $LANG_ZH ]; then
        read -p "$(echo -e ${YELLOW}$ZH_SWITCH_LANG${NC}) " lang_choice
    else
        read -p "$(echo -e ${YELLOW}$EN_SWITCH_LANG${NC}) " lang_choice
    fi
    
    if [ "$lang_choice" = "2" ]; then
        current_lang=$LANG_EN
    else
        current_lang=$LANG_ZH
    fi
}

# 输出函数
print_msg() {
    local zh_msg="$1"
    local en_msg="$2"
    
    if [ $current_lang -eq $LANG_ZH ]; then
        echo -e "$zh_msg"
    else
        echo -e "$en_msg"
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

# 启动脚本
select_language

# 显示标题
if [ $current_lang -eq $LANG_ZH ]; then
    echo -e "${GREEN}$ZH_TITLE${NC}"
    echo "$ZH_INTRO"
else
    echo -e "${GREEN}$EN_TITLE${NC}"
    echo "$EN_INTRO"
fi

# 检查系统
sys=$(uname -s)
print_color_msg "$YELLOW" "$ZH_SYSTEM_TYPE $sys" "$EN_SYSTEM_TYPE $sys"

# 安装后端依赖
install_backend() {
    print_color_msg "$GREEN" "$ZH_BACKEND_INSTALL" "$EN_BACKEND_INSTALL"
    cd backend || { 
        print_color_msg "$RED" "$ZH_BACKEND_DIR_NOT_FOUND" "$EN_BACKEND_DIR_NOT_FOUND"; 
        exit 1; 
    }
    
    # Python版本检查
    py_ver=$(python3 --version 2>&1 | cut -d ' ' -f 2)
    print_color_msg "$YELLOW" "$ZH_PYTHON_VERSION $py_ver" "$EN_PYTHON_VERSION $py_ver"
    
    # 虚拟环境 - 可选但推荐
    print_color_msg "$YELLOW" "$ZH_CREATE_VENV" "$EN_CREATE_VENV"
    read REPLY
    if [ "$REPLY" = "y" ] || [ "$REPLY" = "Y" ]; then
        print_color_msg "$GREEN" "$ZH_CREATING_VENV" "$EN_CREATING_VENV"
        python3 -m venv venv
        
        # 根据系统激活虚拟环境
        if [ "$sys" = "Linux" ] || [ "$sys" = "Darwin" ]; then
            source venv/bin/activate
        else
            # Windows
            venv\\Scripts\\activate
        fi
    fi
    
    # 装依赖
    print_color_msg "$GREEN" "$ZH_PIP_INSTALL" "$EN_PIP_INSTALL"
    pip install -r requirements.txt
    
    # 检查结果
    if [ $? -eq 0 ]; then
        print_color_msg "$GREEN" "$ZH_BACKEND_DEPS_SUCCESS" "$EN_BACKEND_DEPS_SUCCESS"
    else
        print_color_msg "$RED" "$ZH_BACKEND_DEPS_FAIL" "$EN_BACKEND_DEPS_FAIL"
        exit 1
    fi
    
    cd ..
}

# 安装前端依赖
install_frontend() {
    print_color_msg "$GREEN" "$ZH_FRONTEND_INSTALL" "$EN_FRONTEND_INSTALL"
    cd frontend || { 
        print_color_msg "$RED" "$ZH_FRONTEND_DIR_NOT_FOUND" "$EN_FRONTEND_DIR_NOT_FOUND"; 
        exit 1; 
    }
    
    # 检查Node
    node_ver=$(node -v 2>/dev/null)
    if [ $? -ne 0 ]; then
        print_color_msg "$RED" "$ZH_INSTALL_NODEJS" "$EN_INSTALL_NODEJS"
        echo "https://nodejs.org/"
        exit 1
    fi
    
    print_color_msg "$YELLOW" "$ZH_NODE_VERSION $node_ver" "$EN_NODE_VERSION $node_ver"
    
    # npm版本
    npm_ver=$(npm -v 2>/dev/null)
    print_color_msg "$YELLOW" "$ZH_NPM_VERSION $npm_ver" "$EN_NPM_VERSION $npm_ver"
    
    # 安装npm包
    print_color_msg "$GREEN" "$ZH_NPM_INSTALL" "$EN_NPM_INSTALL"
    npm install
    
    # 安装失败的情况很常见...
    if [ $? -eq 0 ]; then
        print_color_msg "$GREEN" "$ZH_NPM_SUCCESS" "$EN_NPM_SUCCESS"
    else
        print_color_msg "$RED" "$ZH_NPM_FAIL" "$EN_NPM_FAIL"
        exit 1
    fi
    
    cd ..
}

# 构建前端
build_frontend() {
    print_color_msg "$GREEN" "$ZH_FRONTEND_BUILD" "$EN_FRONTEND_BUILD"
    cd frontend || { 
        print_color_msg "$RED" "$ZH_FRONTEND_DIR_NOT_FOUND" "$EN_FRONTEND_DIR_NOT_FOUND"; 
        exit 1; 
    }
    
    print_msg "$ZH_BUILD_TIME" "$EN_BUILD_TIME"
    npm run build
    
    # 检查结果
    if [ $? -eq 0 ]; then
        print_color_msg "$GREEN" "$ZH_BUILD_SUCCESS" "$EN_BUILD_SUCCESS"
    else
        print_color_msg "$RED" "$ZH_BUILD_FAIL" "$EN_BUILD_FAIL"
        exit 1
    fi
    
    cd ..
}

install_ttyd() {
    print_color_msg "$GREEN" "$ZH_CHECK_TTYD" "$EN_CHECK_TTYD"
    
    if command -v ttyd &> /dev/null; then
        local version=$(ttyd --version | head -n 1)
        print_color_msg "$YELLOW" "$ZH_TTYD_INSTALLED $version" "$EN_TTYD_INSTALLED $version"
        return 0
    fi
    
    print_color_msg "$YELLOW" "$ZH_INSTALL_TTYD" "$EN_INSTALL_TTYD"
    read REPLY
    if [ "$REPLY" != "y" ] && [ "$REPLY" != "Y" ]; then
        print_color_msg "$YELLOW" "$ZH_SKIP_TTYD" "$EN_SKIP_TTYD"
        return 0
    fi
    
    # 根据系统安装
    if [ "$sys" = "Linux" ]; then
        # 判断Linux发行版
        if [ -f /etc/debian_version ] || [ -f /etc/ubuntu_version ]; then
            print_color_msg "$GREEN" "$ZH_DEBIAN_SYSTEM" "$EN_DEBIAN_SYSTEM"
            sudo apt-get update
            sudo apt-get install -y build-essential cmake git libjson-c-dev libwebsockets-dev
            
            # 编译安装
            print_msg "$ZH_COMPILING" "$EN_COMPILING"
            mkdir -p ~/tmp_ttyd
            cd ~/tmp_ttyd
            git clone https://github.com/tsl0922/ttyd.git
            cd ttyd
            mkdir build
            cd build
            cmake ..
            make
            sudo make install
            cd ~/
            rm -rf ~/tmp_ttyd
        elif [ -f /etc/redhat-release ]; then
            print_color_msg "$GREEN" "$ZH_REDHAT_SYSTEM" "$EN_REDHAT_SYSTEM"
            sudo yum install -y cmake gcc gcc-c++ git json-c-devel libwebsockets-devel
            
            # 编译安装
            print_msg "$ZH_COMPILING" "$EN_COMPILING"
            mkdir -p ~/tmp_ttyd
            cd ~/tmp_ttyd
            git clone https://github.com/tsl0922/ttyd.git
            cd ttyd
            mkdir build
            cd build
            cmake ..
            make
            sudo make install
            cd ~/
            rm -rf ~/tmp_ttyd
        else
            print_color_msg "$RED" "$ZH_INSTALL_TTYD_MANUAL" "$EN_INSTALL_TTYD_MANUAL"
            print_msg "$ZH_REFERENCE https://github.com/tsl0922/ttyd" "$EN_REFERENCE https://github.com/tsl0922/ttyd"
            return 1
        fi
    elif [ "$sys" = "Darwin" ]; then
        print_color_msg "$GREEN" "$ZH_MACOS_SYSTEM" "$EN_MACOS_SYSTEM"
        # 检查brew
        if ! command -v brew &> /dev/null; then
            print_color_msg "$RED" "$ZH_INSTALL_BREW" "$EN_INSTALL_BREW"
            print_msg "$ZH_VISIT: https://brew.sh/" "$EN_VISIT: https://brew.sh/"
            return 1
        fi
        brew install ttyd
    else
        print_color_msg "$RED" "$ZH_UNSUPPORTED_SYSTEM $sys" "$EN_UNSUPPORTED_SYSTEM $sys"
        print_msg "https://github.com/tsl0922/ttyd" "https://github.com/tsl0922/ttyd"
        return 1
    fi
    
    # 安装后再检查一下
    if command -v ttyd &> /dev/null; then
        print_color_msg "$GREEN" "$ZH_TTYD_SUCCESS" "$EN_TTYD_SUCCESS"
        return 0
    else
        print_color_msg "$RED" "$ZH_TTYD_FAIL" "$EN_TTYD_FAIL"
        return 1
    fi
}

# 主流程
main() {
    # 询问切换语言
    switch_language
    
    # 后端
    install_backend
    
    # 询问切换语言
    switch_language
    
    # 前端
    install_frontend
    
    # 询问切换语言
    switch_language
    
    # ttyd - 可选
    install_ttyd
    
    # 询问切换语言
    switch_language
   
    echo
    print_msg "$ZH_BUILD_PROD" "$EN_BUILD_PROD"
    print_color_msg "$YELLOW" "$ZH_BUILD_PROD_CONFIRM" "$EN_BUILD_PROD_CONFIRM"
    read REPLY
    if [ "$REPLY" = "y" ] || [ "$REPLY" = "Y" ]; then
        build_frontend
        
        print_color_msg "$GREEN" "$ZH_COMPLETE" "$EN_COMPLETE"
        print_color_msg "$YELLOW" "$ZH_START_BACKEND" "$EN_START_BACKEND"
        print_color_msg "$YELLOW" "$ZH_FRONTEND_DEPLOY" "$EN_FRONTEND_DEPLOY"
        print_msg "$ZH_NGINX_CONFIG" "$EN_NGINX_CONFIG"
        print_msg "$ZH_SIMPLE_SERVER" "$EN_SIMPLE_SERVER"
    else
        print_color_msg "$GREEN" "$ZH_INSTALL_COMPLETE" "$EN_INSTALL_COMPLETE"
        print_color_msg "$YELLOW" "$ZH_START_BACKEND" "$EN_START_BACKEND"
        print_color_msg "$YELLOW" "$ZH_FRONTEND_DEV" "$EN_FRONTEND_DEV"
        print_color_msg "$YELLOW" "$ZH_FUTURE_BUILD" "$EN_FUTURE_BUILD"
    fi
    
    print_color_msg "$GREEN" "$ZH_ACCESS_URL" "$EN_ACCESS_URL"
    print_msg "$ZH_HAVE_FUN" "$EN_HAVE_FUN"
}

# 执行
main 