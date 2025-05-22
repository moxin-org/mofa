---
title: 快速开始
description: 5分钟内开始使用 MoFA 构建你的第一个 AI 应用
---

# 快速开始

欢迎使用 MoFA！本指南将帮助你在 5 分钟内创建你的第一个 AI 代理。

## 系统要求

- Python 3.8 或更高版本
- pip 包管理器
- 至少 4GB 内存

## 安装

### 使用 pip 安装

```bash
pip install mofa
```

### 从源码安装

```bash
git clone https://github.com/moxin-org/mofa.git
cd mofa
pip install -e .
```

## 创建第一个代理

### 1. 导入必要的模块

```python
from mofa import Agent, Pipeline
from mofa.messages import HumanMessage
```

### 2. 创建一个简单的问答代理

```python
# 创建代理
agent = Agent(
    name="qna-agent",
    model="gpt-3.5-turbo",
    system_prompt="你是一个友好的 AI 助手，请用中文回答问题。"
)

# 创建管道
pipeline = Pipeline()
pipeline.add(agent)
```

### 3. 与代理对话

```python
# 发送消息
message = HumanMessage(content="什么是 MoFA？")
response = pipeline.run(message)

print(response.content)
```

## 下一步

恭喜！你已经成功创建了第一个 MoFA 代理。接下来你可以：

- 了解[核心概念](/docs/concepts/agent)
- 探索[更多示例](/examples)
- 查看[API 文档](/docs/api)
- 加入[社区讨论](https://discord.gg/mofa)

## 常见问题

### 安装失败怎么办？

确保你的 Python 版本是 3.8 或更高：

```bash
python --version
```

### 如何设置 API 密钥？

MoFA 支持环境变量配置：

```bash
export OPENAI_API_KEY="your-api-key"
```

或在代码中设置：

```python
agent = Agent(
    name="my-agent",
    model="gpt-3.5-turbo",
    api_key="your-api-key"
)
``` 