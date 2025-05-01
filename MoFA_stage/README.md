# MoFA_Stage

MoFA_Stage 是一个为 MoFA (Modular Framework for Agents) 框架设计的前后端分离的 Agent 管理平台。

它允许用户通过 Web 界面直观地创建、编辑、管理和运行 MoFA Agents，无需直接使用命令行。

## 功能特性

- **Agent 管理**
  - 列出、搜索所有 Agents
  - 创建新 Agent (基于 Hello World 模板或复制现有 Agent)
  - 编辑 Agent 代码和配置
  - 运行和停止 Agent
  - 删除 Agent

- **代码编辑**
  - 基于 Monaco Editor 的代码编辑器
  - 支持语法高亮
  - Markdown 预览功能
  - 文件树导航

- **配置编辑**
  - 环境变量 (.env) 编辑
  - 依赖管理 (pyproject.toml) 编辑
  - Agent 配置 (agent.yml) 编辑
  - 说明文档 (README.md) 编辑

## 技术栈

### 后端
- Python + Flask
- RESTful API

### 前端
- Vue 3 + Vite
- Element Plus UI
- Monaco Editor

## 项目结构

```
MoFA_Stage/
├── backend/                # Flask 后端
│   ├── app.py              # Flask 主应用
│   ├── config.py           # 配置文件
│   ├── routes/             # API 路由
│   │   ├── agents.py       # agent 相关 API
│   │   └── settings.py     # 设置相关 API
│   └── utils/              # 工具函数
│       ├── mofa_cli.py     # mofa CLI 调用封装
│       └── file_ops.py     # 文件操作工具
├── frontend/               # Vue3 前端
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.js
│       ├── App.vue
│       ├── components/     # Vue 组件
│       ├── views/          # 页面视图
│       ├── router/         # 路由配置
│       ├── store/          # 状态管理
│       ├── assets/         # 静态资源
│       └── api/            # API 调用
└── README.md               # 项目说明
```

## 安装和运行

### 前置条件

- Python 3.8+
- Node.js 14+
- MoFA 已安装并配置完成

### 后端设置

1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

2. 运行 Flask 服务器

```bash
python app.py
```

Flask 服务器将在 http://localhost:5000 上运行。

### 前端设置

1. 安装依赖

```bash
cd frontend
npm install
```

2. 启动开发服务器

```bash
npm run dev
```

前端开发服务器将在 http://localhost:3000 上运行。

