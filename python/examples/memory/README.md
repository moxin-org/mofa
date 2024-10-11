# Memory Process Example in MoFA

## 1. 功能

MoFA 中的 **Memory** 代理负责管理和检索上下文记忆，以帮助用户在交互过程中保持一致性和相关性。其设计模式包括：**上下文检索 + 推理响应 + 记忆记录**。这一过程确保代理能够利用之前的对话和任务信息，提供更准确和相关的回答。

## 2. 用例

该代理适用于需要维护长期或短期记忆的任务，确保在多轮对话或复杂任务中，代理能够引用先前的信息以生成更好的响应。常见应用包括：

- **客户支持**：记住客户的需求和问题，跨多个互动提供持续和个性化的服务。
- **项目管理**：跟踪和记录项目进展、任务分配及相关信息，辅助决策和报告生成。
- **个人助理**：保留用户偏好、日程安排和交互历史，提供定制化的建议和提醒。
- **研究辅助**：在科学过程中记录和检索相关的研究信息，辅助文献综述和数据分析。

## 3. 配置方法

### 配置概述

配置文件位于 `configs` 目录中。`.yml` 文件定义了每个代理的行为、参数和模型设置。Python 脚本实现了每个代理的实际任务。

| **文件**                     | **用途**                                     |
| ---------------------------- | ----------------------------------------------- |
| `configs/memory_config.yml`  | 配置 Memory 过程的参数，包括模型和存储设置。 |
| `memory_retrieval.py`        | 执行上下文检索任务。            |
| `reasoner_agent.py`          | 基于上下文生成智能响应。 |
| `memory_record.py`           | 将关键交互信息记录到记忆存储中。 |

### 配置步骤

#### 1. 修改配置文件

根据您的具体需求编辑 `configs/memory_config.yml` 文件。您可以自定义模型参数和存储路径，但建议不要修改提示语。

#### 2. 配置文件示例

以下是 Memory 过程的示例配置文件：

```yaml
config:
  version: "v1.1"
  
  llm:
    provider: openai
    config:
      model: "Qwen/Qwen2.5-32B-Instruct"  # 替换为您的模型名称
      max_tokens: 1500

  vector_store:
    provider: chroma
    config:
      collection_name: "memory_collection"
      path: "./db"

  embedder:
    provider: openai
    config:
      model: "BAAI/bge-large-zh-v1.5"

model:
  model_api_key: "sk-XXXXXXXXXXXXXXXXXXXXXXXX"  # 替换为您的 API 密钥
  model_api_url: "https://api.siliconflow.cn/v1/"  # 替换为您的 API URL

user_id: "mofa"
```

### 配置详情

#### `version`

- **version**：配置文件的版本，目前设置为 `v1.1`。

#### `llm`（大型语言模型配置）

- **provider**：语言模型提供商，这里是 `openai`。
- **config**：与语言模型相关的配置。
  - **model**：模型名称，例如 `"Qwen/Qwen2.5-32B-Instruct"`。
  - **max_tokens**：模型生成的最大标记数，设置为 `1500`。

#### `vector_store`（向量存储配置）

- **provider**：向量存储提供商，这里是 `chroma`。
- **config**：与向量存储相关的配置。
  - **collection_name**：向量集合的名称，设置为 `"memory_collection"`。
  - **path**：数据库文件的路径，设置为 `"./db"`。

#### `embedder`（嵌入模型配置）

- **provider**：嵌入模型提供商，这里是 `openai`。
- **config**：与嵌入模型相关的配置。
  - **model**：嵌入模型的名称，例如 `"BAAI/bge-large-zh-v1.5"`。

#### `model`（模型 API 配置）

- **model_api_key**：您的模型 API 密钥，请替换为您的实际 API 密钥，例如 `"sk-XXXXXXXXXXXXXXXXXXXXXXXX"`。
- **model_api_url**：模型 API 的 URL，请替换为您的实际 API URL，例如 `"https://api.siliconflow.cn/v1/"`。

#### `user_id`

- **user_id**：用户标识符，设置为 `"mofa"`。用于识别和管理不同的用户请求和数据。

## 4. 运行代理

### 使用 Dora-rs 命令行

1. **安装 MoFA 项目依赖**

   确保您已安装 MoFA 项目的所有必要依赖。这通常涉及设置 Python 环境并安装所需的包。

2. **启动代理进程**

   执行以下命令以启动 Memory 代理进程：

   ```bash
   dora up && dora build memory_dataflow.yml && dora start memory_dataflow.yml --attach
   ```

3. **初始化任务输入**

   打开另一个终端窗口并运行 `terminal-input`，然后输入相应的任务以启动 Memory 过程。

   ```bash
   terminal-input
   Enter your task: Record and retrieve key information about machine learning
   ```

---

