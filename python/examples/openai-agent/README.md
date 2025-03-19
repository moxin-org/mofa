
# OpenAI Agent 使用指南

## 概述

本数据流实现了一个基于 OpenAI 的问答 Agent，包含两个节点：

1. **terminal-input**: 终端输入节点，用于接收用户输入
2. **openai-agent**: OpenAI 问答节点，处理用户输入并返回 OpenAI 的响应

## 快速开始

### 1. 环境准备

确保已安装以下依赖：
- Python 3.10+
- OpenAI Python SDK
- Dora 运行时

### 2. 配置 API 密钥

在项目根目录创建 `.env.secret` 文件，并添加 OpenAI API 密钥：

```plaintext
OPENAI_API_KEY=your_openai_api_key
```

### 3. 启动数据流

```bash
# 构建数据流
dora build openai-agent-dataflow.yml

# 启动数据流并附加到终端
dora start openai-agent-dataflow.yml --attach
```

### 4. 使用说明

1. 启动数据流后，在终端输入问题
2. 数据流将返回 OpenAI 的响应

### 5. 示例

```bash
> 你好，请介绍一下自己
{
  "response": "你好！我是一个基于 OpenAI 的 AI 助手..."
}
```

## 数据流配置 (openai-agent-dataflow.yml)

```yaml
nodes:
  - id: terminal-input
    build: pip install -e ../../node-hub/terminal-input
    path: dynamic
    outputs: data
    inputs:
      openai_agent_result: openai-agent/openai_agent_result

  - id: openai-agent
    build: pip install -e ../../agent-hub/openai-agent
    path: openai-agent
    outputs: openai_agent_result
    inputs:
      query: terminal-input/data
    env:
      IS_DATAFLOW_END: true
      WRITE_LOG: true
```

## 环境变量

- `IS_DATAFLOW_END`: 设置为 true 表示这是数据流的最后一个节点
- `WRITE_LOG`: 设置为 true 启用日志记录

## 日志文件

- `logs/log_openai-agent.txt`: OpenAI Agent 运行日志
- `logs/dora-coordinator.txt`: 协调器日志
- `logs/dora-daemon.txt`: 守护进程日志

## 注意事项

1. 确保 `.env.secret` 已添加到 `.gitignore`
2. API 密钥要妥善保管
3. 保持代码结构简单清晰
4. 遵循与 hello-world 相似的实现方式

### 1. 如何添加系统提示词？

在 `openai-agent/main.py` 中修改 `messages` 参数：

```python
messages=[
    {"role": "system", "content": "你是一个专业的 AI 助手..."},
    {"role": "user", "content": user_input}
]
```


