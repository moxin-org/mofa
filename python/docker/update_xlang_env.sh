#!/bin/bash

# =====================================================================
# Script Name: build_xMind.sh
# Description: 自动化构建 xMind 项目的脚本
# Author: ChengChen
# Date: 2024-04-27
# =====================================================================

# 设置脚本在遇到错误时退出，并在使用未声明的变量时提醒
set -euo pipefail

# 定义变量
PROJECT_DIR="/project/xMind"
THIRD_PARTY_DIR="$PROJECT_DIR/ThirdParty/xlang"
COPY_DIR="/project/copy"
OUT_DIR="$PROJECT_DIR/out"
CONFIG_DIR="$PROJECT_DIR/Config"
EXAMPLES_DIR="$PROJECT_DIR/Examples"
MOFA_DIR="/project/mofa"

# 函数：打印日志
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*"
}

# 开始脚本执行
log "开始构建 xMind 项目..."

# 切换到项目目录
cd "$PROJECT_DIR"

# 配置 Git 安全目录
log "配置 Git 安全目录..."
git config --global --add safe.directory "$PROJECT_DIR/ThirdParty/xlang"
git config --global --add safe.directory "$PROJECT_DIR"
git config --global --add safe.directory "$MOFA_DIR"

# 创建复制目录并备份 Config 和 Examples
log "创建备份目录并复制 Config 和 Examples..."
mkdir -p "$COPY_DIR"
cp -r "$CONFIG_DIR" "$COPY_DIR/"
cp -r "$EXAMPLES_DIR" "$COPY_DIR/"

# 删除原有的 Config 和 Examples 目录
log "删除原有的 Config 和 Examples 目录..."
rm -rf "$CONFIG_DIR"
rm -rf "$EXAMPLES_DIR"

# 更新主仓库
log "更新主仓库..."
git fetch origin
git reset --hard origin/main

# 切换到 ThirdParty/xlang 目录并更新
log "更新 ThirdParty/xlang 仓库..."
cd "$THIRD_PARTY_DIR"
git fetch origin
git reset --hard origin/main

# 复制备份的 Config 和 Examples 回项目目录
log "恢复 Config 和 Examples 目录..."
cp -r "$COPY_DIR/Config" "$PROJECT_DIR/"
cp -r "$COPY_DIR/Examples" "$PROJECT_DIR/"

# 删除并重新创建输出目录
log "准备构建输出目录..."
rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"
cd "$OUT_DIR"

# 运行 CMake 和 Make 构建项目
log "运行 CMake 配置..."
cmake ..

log "开始编译项目..."
make -j"$(nproc)"

log "开始更新安装Mofa项目"
cd "$MOFA_DIR"
git fetch origin
git reset --hard origin/main
pip3 install -e .

log "项目构建完成！"



