# MoFA_Stage

[English](README.md) | 中文

MoFA_Stage 是为 MoFA (Modular Framework for Agents) 框架打造的一个可视化管理平台。通过简单直观的 Web 界面，你可以创建、编辑和运行 Agent，无需直接操作命令行。

## 主要功能

- **Agent 管理**
  - 浏览和搜索现有 Agent
  - 基于模板创建新 Agent，或复制已有 Agent
  - 修改 Agent 代码和配置
  - 启动/停止 Agent 运行
  - 删除不再需要的 Agent


- **终端集成**
  - Web SSH 访问（无需额外SSH客户端）
  - ttyd 终端直接集成到页面
  - 便捷的命令行环境

- **编辑器功能**
  - 基于 Monaco 的代码编辑（VS Code同款编辑器引擎）
  - 代码高亮和自动完成
  - Markdown 即时预览
  - 项目文件导航

## 技术栈

**后端**
- Python + Flask
- WebSocket 支持
- SSH 终端集成
- RESTful API

**前端**
- Vue 3 
- Element Plus 组件库
- Monaco 编辑器
- XTerm.js 终端模拟
- 多语言支持
- Pinia 状态管理

**第三方依赖**
- ttyd 终端服务（可选）

## 快速开始

### 环境要求

- Python 3.8 或更高
- Node.js 14 或更高
- 已安装 MoFA 框架

### 安装和运行脚本

项目提供了两个脚本：

- **install.sh**: 一键安装所有依赖
  ```bash
  chmod +x install.sh
  ./install.sh
  ```
  自动安装后端/前端依赖，并根据需要安装 ttyd、构建前端。

- **run.sh**: 一键启动服务
  ```bash
  chmod +x run.sh
  ./run.sh
  ```


### 开发模式

1. 启动后端
```bash
cd backend
python app.py
```

2. 启动前端（开发模式）
```bash
cd frontend
npm run dev
```

访问 http://localhost:3000 。

### 生产部署


1. 构建前端
```bash
cd frontend
npm run build  # 生成在 dist 目录
```

2. 部署方式（二选一）

**使用 Nginx**

```nginx
server {
    listen 80;
    
    # 静态文件
    location / {
        root /path/to/mofa_stage/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    
    # API 转发
    location /api {
        proxy_pass http://localhost:5002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # WebSocket
    location /api/webssh {
        proxy_pass http://localhost:5001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

**简易部署**

使用 Python 自带的 HTTP 服务器：
```bash
cd frontend/dist
python -m http.server 3000
```

启动后端：
```bash
cd backend
python app.py
```

## 常见问题

### 端口占用

如果遇到端口占用问题，可以用这条命令释放端口：

```bash
for port in 3000 5001 5002 7681; do
    pid=$(lsof -t -i:$port)
    if [ -n "$pid" ]; then
        kill -9 $pid
        echo "释放了端口 $port"
    fi
done
```

### 端口说明

- 3000: 前端服务
- 5001: WebSSH 服务
- 5002: 主后端 API
- 7681: ttyd 终端

### ttyd 安装失败

如果 ttyd 自动安装失败，可以参考 [ttyd GitHub 页面](https://github.com/tsl0922/ttyd) 手动安装。

## 目录结构

核心目录和文件：

```
MoFA_Stage/
├── backend/                # Flask 后端
│   ├── app.py              # 主应用入口
│   ├── routes/             # API 路由
│   │   ├── agents.py       # Agent API
│   │   ├── dataflows.py    # 数据流 API
│   │   ├── webssh.py       # SSH API等
│   ├── utils/              # 工具函数
│   │   ├── mofa_cli.py     # mofa 命令行封装
│   │   ├── dataflow_engine.py # 数据流引擎
│   └── models/             # 数据模型
├── frontend/               # Vue3 前端
│   ├── src/
│       ├── views/          # 页面视图
│       ├── components/     # 组件
│       ├── api/            # API 调用
├── install.sh              # 安装脚本
├── run.sh                  # 服务启动脚本
└── README.md               
``` 