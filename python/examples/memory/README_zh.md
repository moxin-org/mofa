# MoFA中的Memory流程示例


## 1. 功能说明

**Memory**智能体通过管理和检索上下文记忆，辅助用户在与智能体交互过程中保持信息的一致性和相关性。其设计模式为：**上下文检索 + 推理响应 + 记忆记录**。该流程确保智能体能够利用之前的对话和任务信息，提供更加准确和相关的回答。

## 2. 使用场景

该智能体适用于需要维护长期或短期记忆的任务，确保在多轮对话或复杂任务中，智能体能够参考之前的信息来生成更好的响应。常见的应用场景包括：

- **客户支持**：在多轮对话中记住客户的需求和问题，提供连续性和个性化的服务。
- **项目管理**：跟踪和记录项目进展、任务分配及相关信息，辅助决策和报告生成。
- **个人助理**：记住用户的偏好、日程安排和历史交互，提供定制化的建议和提醒。
- **研究辅助**：在科研过程中记录和检索相关研究信息，辅助文献综述和数据分析。

## 3. 配置方法

### 配置说明

配置文件位于 `configs` 目录下，`.yml` 文件为实际运行的智能体配置。配置文件指定了各个Agent的行为、参数和模型设置。

| **文件**                      | **作用**                                   |
| ----------------------------- | ------------------------------------------ |
| `configs/memory_config.yml`   | 配置Memory流程的参数，包括模型和存储设置。 |
| `memory_retrieval.py`         | 执行上下文检索任务。                       |
| `reasoner_agent.py`           | 生成基于上下文的智能响应。                 |
| `memory_record.py`            | 记录交互中的关键信息到记忆库。             |

### 配置步骤

#### 1. 修改配置文件

根据具体需求，编辑 `configs/memory_config.yml` 文件。可以自定义修改里面的模型参数和存储路径，建议不要修改提示词。

#### 2. 配置文件示例

以下是Memory流程的配置文件示例：

```yaml
config:
  version: "v1.1"
  
  llm:
    provider: openai
    config:
      model: "Qwen/Qwen2.5-32B-Instruct"  # 替换为你的模型名称
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
  model_api_key: "sk-XXXXXXXXXXXXXXXXXXXXXXXX"  # 替换为你的API密钥
  model_api_url: "https://api.siliconflow.cn/v1/"  # 替换为你的API URL

user_id: "mofa"
```

### 配置项详解

#### `version`

- **version**: 配置文件的版本号，当前为 `v1.1`。

#### `llm`（大型语言模型配置）

- **provider**: 使用的语言模型提供商，这里是 `openai`。
- **config**: 模型相关配置。
  - **model**: 模型名称，需替换为实际使用的模型名称，例如 `"Qwen/Qwen2.5-32B-Instruct"`。
  - **max_tokens**: 设置模型生成的最大 token 数量，这里为 `1500`。

#### `vector_store`（向量存储配置）

- **provider**: 使用的向量存储提供商，这里是 `chroma`。
- **config**: 向量存储相关配置。
  - **collection_name**: 向量集合名称，这里设置为 `"memory_collection"`。
  - **path**: 数据库文件路径，这里是 `"./db"`。

#### `embedder`（嵌入模型配置）

- **provider**: 使用的嵌入模型提供商，这里是 `openai`。
- **config**: 嵌入模型相关配置。
  - **model**: 嵌入模型名称，这里是 `"BAAI/bge-large-zh-v1.5"`。

#### `model`（模型API配置）

- **model_api_key**: 你的模型API密钥，需替换为实际的API密钥，例如 `"sk-XXXXXXXXXXXXXXXXXXXXXXXX"`。
- **model_api_url**: 模型API的URL，这里是 `"https://api.siliconflow.cn/v1/"`。

#### `user_id`

- **user_id**: 用户标识，这里设置为 `"mofa"`。用于标识和管理不同用户的请求和数据。

## 4. 运行智能体

### 使用Dora-rs命令行运行

1. **安装MoFA项目包**

   确保你已经安装了MoFA项目的依赖包。

2. **启动智能体流程**

   执行以下命令以启动Memory智能体流程：

   ```bash
   dora up && dora build memory_dataflow.yml && dora start memory_dataflow.yml --attach
   ```

3. **启动任务输入**

   打开另一个终端，运行 `terminal-input`，然后输入相应任务以启动Memory流程。

   ```bash
   terminal-input
   Enter your task: 记录并检索有关机器学习的关键信息
   ```
