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

echo -e "${GREEN}==== MoFA_Stage 安装脚本 ====${NC}"
echo "这个脚本会帮你安装所有依赖"

# 检查系统
sys=$(uname -s)
echo -e "${YELLOW}系统类型: ${sys}${NC}"

# 安装后端依赖
install_backend() {
    echo -e "${GREEN}正在安装后端依赖...${NC}"
    cd backend || { echo -e "${RED}找不到backend目录!${NC}"; exit 1; }
    
    # Python版本检查
    py_ver=$(python3 --version 2>&1 | cut -d ' ' -f 2)
    echo -e "${YELLOW}Python版本: ${py_ver}${NC}"
    
    # 虚拟环境 - 可选但推荐
    echo -e "${YELLOW}要创建虚拟环境吗? (y/n)${NC}"
    read REPLY
    if [ "$REPLY" = "y" ] || [ "$REPLY" = "Y" ]; then
        echo -e "${GREEN}创建虚拟环境...${NC}"
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
    echo -e "${GREEN}pip安装依赖...${NC}"
    pip install -r requirements.txt
    
    # 检查结果
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}后端依赖安装完成${NC}"
    else
        echo -e "${RED}后端依赖安装失败${NC}"
        exit 1
    fi
    
    cd ..
}

# 安装前端依赖
install_frontend() {
    echo -e "${GREEN}安装前端依赖...${NC}"
    cd frontend || { echo -e "${RED}找不到frontend目录!${NC}"; exit 1; }
    
    # 检查Node
    node_ver=$(node -v 2>/dev/null)
    if [ $? -ne 0 ]; then
        echo -e "${RED}请安装nodejs${NC}"
        echo "https://nodejs.org/"
        exit 1
    fi
    
    echo -e "${YELLOW}Node.js版本: ${node_ver}${NC}"
    
    # npm版本
    npm_ver=$(npm -v 2>/dev/null)
    echo -e "${YELLOW}npm版本: ${npm_ver}${NC}"
    
    # 安装npm包
    echo -e "${GREEN}npm install...${NC}"
    npm install
    
    # 安装失败的情况很常见...
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}npm包安装成功!${NC}"
    else
        echo -e "${RED}npm安装出错${NC}"
        exit 1
    fi
    
    cd ..
}

# 构建前端
build_frontend() {
    echo -e "${GREEN}开始构建前端...${NC}"
    cd frontend || { echo -e "${RED}找不到frontend目录!${NC}"; exit 1; }
    
    
    echo "这可能要花一点时间..."
    npm run build
    
    # 检查结果
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}前端构建成功!${NC}"
    else
        echo -e "${RED}构建失败${NC}"
        exit 1
    fi
    
    cd ..
}


install_ttyd() {
    
    echo -e "${GREEN}检查ttyd...${NC}"
    
    if command -v ttyd &> /dev/null; then
        echo -e "${YELLOW}ttyd已安装，版本: $(ttyd --version | head -n 1)${NC}"
        return 0
    fi
    
    
    echo -e "${YELLOW}是否安装ttyd(y/n)${NC}"
    read REPLY
    if [ "$REPLY" != "y" ] && [ "$REPLY" != "Y" ]; then
        echo -e "${YELLOW}跳过ttyd安装。提示: 终端功能可能会有问题${NC}"
        return 0
    fi
    
    # 根据系统安装
    if [ "$sys" = "Linux" ]; then
        # 判断Linux发行版
        if [ -f /etc/debian_version ] || [ -f /etc/ubuntu_version ]; then
            echo -e "${GREEN}Debian/Ubuntu系统，用apt安装...${NC}"
            sudo apt-get update
            sudo apt-get install -y build-essential cmake git libjson-c-dev libwebsockets-dev
            
            # 编译安装
            echo "从源码编译中"
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
            echo -e "${GREEN}RedHat/CentOS/Fedora系统，用yum安装...${NC}"
            sudo yum install -y cmake gcc gcc-c++ git json-c-devel libwebsockets-devel
            
            # 编译安装
            echo "从源码编译中."
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
            echo -e "${RED}请自行安装ttyd${NC}"
            echo "参考: https://github.com/tsl0922/ttyd"
            return 1
        fi
    elif [ "$sys" = "Darwin" ]; then
        echo -e "${GREEN}macOS系统，用brew安装...${NC}"
        # 检查brew
        if ! command -v brew &> /dev/null; then
            echo -e "${RED}请先安装brew${NC}"
            echo "访问: https://brew.sh/"
            return 1
        fi
        brew install ttyd
    else
        echo -e "${RED}不支持的系统 ${sys}${NC}"
        echo "https://github.com/tsl0922/ttyd"
        return 1
    fi
    
    # 安装后再检查一下
    if command -v ttyd &> /dev/null; then
        echo -e "${GREEN}ttyd安装完成!${NC}"
        return 0
    else
        echo -e "${RED}ttyd装失败，请手动安装${NC}"
        return 1
    fi
}

# 主流程
main() {
    # 后端
    install_backend
    
    # 前端
    install_frontend
    
    # ttyd - 可选
    install_ttyd
    
   
    echo
    echo "npm run devh或者构建生产环境"
    echo -e "${YELLOW}要构建生产版本吗? (y/n)${NC}"
    read REPLY
    if [ "$REPLY" = "y" ] || [ "$REPLY" = "Y" ]; then
        build_frontend
        
        echo -e "${GREEN}==== 完成！ ====${NC}"
        echo -e "${YELLOW}启动后端: cd backend && python app.py${NC}"
        echo -e "${YELLOW}前端部署方式:${NC}"
        echo "1. 配置Nginx指向frontend/dist目录"
        echo "2. 或简单点: cd frontend/dist && python -m http.server 3000"
    else
        echo -e "${GREEN}==== 安装完成 ====${NC}"
        echo -e "${YELLOW}后端启动: cd backend && python app.py${NC}"
        echo -e "${YELLOW}前端开发模式: cd frontend && npm run dev${NC}"
        echo -e "${YELLOW}以后要构建生产版本: cd frontend && npm run build${NC}"
    fi
    
    echo -e "${GREEN}访问地址: http://localhost:3000${NC}"
    echo "Have fun!"
}

# 执行
main 