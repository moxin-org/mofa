# MoFA MCP 服务器完整安装指南

本文档提供了基于 MoFA 框架的 MCP (Model Context Protocol) 服务器的完整安装、配置和使用指南。

## 系统架构

MoFA 框架 → Intelligent Agent Creation + Deep Search → DORA 数据流 → MCP 服务器 → Voice Dialogue Client

## 功能特性

- **智能代理创建**: 基于 intelligent_agent_creation 自动生成代理配置、代码和依赖
- **深度搜索**: 基于 deepsearch 提供智能搜索和信息检索功能
- **MCP 协议**: 通过标准 MCP 协议提供工具服务
- **模型对话**: 支持 Ollama 模型集成

## 环境要求

- Python >= 3.10
- macOS 或 Linux

## 完整安装流程

### 步骤 1: 安装 MoFA 框架  

```bash
git clone git@github.com:moxin-org/mofa.git
# 进入 MoFA 项目目录
cd /mofa/python

# 安装 MoFA 框架
pip install -e .

# 验证安装
mofa --version
```

### 步骤 2: 启动 Intelligent Agent Creation 数据流

```bash
# 进入目录
cd mofa/python/examples/intelligent_agent_creation

# 配置密钥文件
vim .env.secret 
# 在 .env.secret 中添加以下内容
LLM_API_KEY=
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL_NAME=gpt-4.1

# 启动 DORA 运行时
dora up

# 构建数据流依赖
dora build intelligent_agent_creation_server_dataflow.yml

# 启动数据流
dora start intelligent_agent_creation_server_dataflow.yml
```

### 步骤 3: 启动 Deep Search 数据流

```bash
# 在新终端中进入目录
cd zcbc/mofa/python/examples/deepsearch

vim .env.secret 
# 在 .env.secret 中添加以下内容
LLM_API_KEY=
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL_NAME=gpt-4o

SERPER_API_KEY=

# 构建数据流依赖
dora build deepsearch-dataflow.yml

# 启动数据流
dora start deepsearch-dataflow.yml
```

### 步骤 4: 启动 MCP 服务器

```bash
# 在新终端中进入 MCP 目录
cd mofa/python/examples/dataflow_mcp

# 安装 MCP 服务器依赖
pip install fastmcp requests psutil

# 启动 MCP 服务器
python mofa_mcp_server.py

# 服务器将在 http://127.0.0.1:9000 启动
```

### 步骤 5: 启动语音对话客户端

```bash
# 在新终端中进入 VoiceDialogue 目录
cd mofa/python/examples/VoiceDialogue


# 启动语音对话客户端
python ollama_qwen_8b_run.py
```


