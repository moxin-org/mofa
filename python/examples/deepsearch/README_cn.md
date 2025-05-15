
# DeepSearch Dataflow 部署与功能说明

## 目录

- [DeepSearch Dataflow 部署与功能说明](#deepsearch-dataflow-部署与功能说明)
  - [目录](#目录)
  - [1. 项目简介与核心功能](#1-项目简介与核心功能)
    - [DeepSearch 智能研究代理系统](#deepsearch-智能研究代理系统)
  - [2. 环境准备与 MoFA 框架安装](#2-环境准备与-mofa-框架安装)
  - [3. 环境变量配置（API Key）](#3-环境变量配置api-key)
    - [步骤一：复制 `.env.example` 文件](#步骤一复制-envexample-文件)
    - [步骤二：填写密钥](#步骤二填写密钥)
  - [4. openai-server-stream 节点说明](#4-openai-server-stream-节点说明)
  - [5. DeepSearch Dataflow 构建与启动](#5-deepsearch-dataflow-构建与启动)
    - [步骤一：进入示例目录](#步骤一进入示例目录)
    - [步骤二：构建 Dataflow 节点](#步骤二构建-dataflow-节点)
    - [步骤三：启动 Dataflow](#步骤三启动-dataflow)
  - [6. 交互测试与结果示例](#6-交互测试与结果示例)
    - [启动 Python 测试客户端](#启动-python-测试客户端)
      - [结果示例](#结果示例)
  - [7. 常见问题与多系统兼容](#7-常见问题与多系统兼容)
    - [多操作系统兼容说明](#多操作系统兼容说明)
  - [8. 参考资料与扩展阅读](#8-参考资料与扩展阅读)

---

## 1. 项目简介与核心功能

### DeepSearch 智能研究代理系统

DeepSearch 是基于 [MoFA](../../README.md) 智能体开发框架的端到端流式研究代理。其核心亮点包括：

- **多阶段推理与分块流式输出**：每次用户提问，系统自动完成“检索 → 文章处理 → 多阶段推理 → 内容生成 → 综合报告”，每个阶段实时输出 chunk，便于前端流式展示。
- **智能 Web 检索与可信度评估**：集成 SERPER API，自动抓取高质量网络资料，去重、排序、提取上下文并评估可信度。
- **多轮内容生成与综合**：通过多轮 LLM 调用，先思考、再总结、再生成内容，最后合成完整报告。
- **可扩展的数据流式架构**：所有节点均可独立扩展、复用，支持企业级知识检索、情报分析等场景。

详细数据流与阶段说明请参考 [DeepSearch Agent 设计文档](../../agent-hub/deep-search/README.md)。

---

## 2. 环境准备与 MoFA 框架安装

请严格按照 [MoFA 主项目文档](../../README.md) 的说明完成 Python、Rust、Dora 及 MoFA 框架的安装。

- **Linux/Mac**：推荐使用 bash/zsh 终端
- **Windows**：推荐使用 PowerShell 或 WSL（Windows Subsystem for Linux）

> **注意**：本地环境需 Python 3.10+，Rust 1.70+，Dora CLI 0.3.9+。

---

## 3. 环境变量配置（API Key）

### 步骤一：复制 `.env.example` 文件

在 `python/examples/deepsearch/` 目录下执行：

```bash
# Linux/Mac
cp .env.example .env.secret

# Windows (PowerShell)
copy .env.example .env.secret
```

### 步骤二：填写密钥

- **LLM_API_KEY**：在 [OpenAI](https://platform.openai.com/account/api-keys) 或 DeepSeek/火山方舟等平台注册获取
- **SERPER_API_KEY**：在 [Serper.dev](https://serper.dev/) 注册并获取

编辑 `.env.secret`，填写如下内容：

```ini
LLM_API_KEY=你的大模型API密钥
LLM_BASE_URL=https://api.openai.com/v1   # 或其他兼容API地址
LLM_MODEL_NAME=gpt-3.5-turbo             # 或其他模型名称
SERPER_API_KEY=你的serper密钥
```

> **安全提示**：`.env.secret` 已在 `.gitignore` 中，切勿上传至代码仓库。

---

## 4. openai-server-stream 节点说明

本项目集成的 `openai-server-stream` 节点，基于 FastAPI + Dora 实现，具备如下特性：

- **完全兼容 OpenAI ChatCompletions 流式 API**，可无缝对接 OpenAI 官方 SDK
- **自动转发请求到 Dora Dataflow**，并实时流式返回智能体生成内容

详细接口与用法请参考 [openai-server-stream 说明文档](../../node-hub/openai-server-stream/README.md)。

---

## 5. DeepSearch Dataflow 构建与启动

### 步骤一：进入示例目录

```bash
cd python/examples/deepsearch
```

### 步骤二：构建 Dataflow 节点

```bash
dora up  && dora build deepsearch-dataflow.yml
```

- 自动安装所有节点依赖
- 检查 YAML 配置，确保无误

### 步骤三：启动 Dataflow

```bash
dora start deepsearch-dataflow.yml
```

- 启动成功后，系统监听本地 8000 端口，等待客户端请求

---

## 6. 交互测试与结果示例

### 启动 Python 测试客户端

确保 Dataflow 已启动，在新终端执行：

```bash
cd python/examples/deepsearch && python3 moly_client_stream.py
```

- 可在 `moly_client_stream.py` 文件中修改 `user_input` 变量，输入任意研究主题
- 支持流式输出，终端实时展示多阶段推理与最终报告

#### 结果示例

```json
{
  "type": "thinking",
  "content": "正在分析来自arXiv的3篇论文...",
  "articles": [
    {"title": "LLM对抗训练新方法", "url": "https://arxiv.org/abs/2405.12345", "relevance": 0.95}
  ],
  "metadata": {"stage": "Context Extraction"},
  "id": "0-1"
}
```


---

## 7. 常见问题与多系统兼容

| 问题描述 | 可能原因 | 解决方案 |
|----------|----------|----------|
| 端口占用 | 8000端口被占用 | 修改 Dataflow 配置或释放端口 |
| API Key 报错 | Key 未配置或无效 | 检查 `.env.secret` 文件，确保 Key 正确 |
| 无法访问外网 | 网络受限 | 配置代理或使用 proxychains4 启动 dora |
| 依赖安装失败 | Python/Rust 环境异常 | 检查 Python/Rust 版本，重装依赖 |
| 日志无输出 | Dataflow 未启动或节点异常 | 检查 dora 日志，确认各节点正常运行 |

### 多操作系统兼容说明

- **Linux/Mac**：所有命令均可直接在 bash/zsh 终端执行
- **Windows**：推荐使用 PowerShell 或 WSL，部分命令如 `cp` 需替换为 `copy`

---

## 8. 参考资料与扩展阅读

- [MoFA 主项目文档（安装与原理）](../README.md)
- [DeepSearch Agent 设计说明](../../agent-hub/deep-search/README.md)
- [openai-server-stream 节点文档](../../node-hub/openai-server-stream/README.md)
- [Serper.dev 官方文档](https://serper.dev/)
- [OpenAI API 官方文档](https://platform.openai.com/docs/api-reference)
- [Dora Runtime 官方文档](https://dora-rs.ai/)

---

如需进一步技术支持，请联系 MoFA 官方团队或提交 issue。


