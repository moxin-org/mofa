#!/bin/bash

# 构建Docker镜像
echo "构建Ubuntu Linux容器..."
docker build -t mofa-linux -f Dockerfile.simple .

# 运行容器并映射端口，同时挂载当前目录作为卷
echo "启动Linux容器..."
docker run -it --rm \
  -p 8000:8000 \
  -v $(pwd):/app/mofa \
  --name mofa-linux-container \
  mofa-linux

echo "容器已退出" 