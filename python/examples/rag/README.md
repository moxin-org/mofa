# RAG 过程示例在 MoFA 中

## 1. 功能

在 MoFA 中，**RAG（检索增强生成）** 代理负责通过结合检索和生成模型来提供更为精准和相关的响应。RAG 代理的设计模式包括：**文件上传与编码 + 向量检索 + 上下文生成 + 智能响应**。这一过程确保代理能够利用外部文档和上下文信息，生成高质量且基于具体内容的回答，从而提升用户交互体验。

## 2. 用例

RAG 代理适用于需要结合外部知识库或文档进行信息检索和生成的任务，确保在多轮对话或复杂任务中，代理能够引用相关的外部资料以生成更为详尽和准确的响应。常见应用包括：

- **知识问答**：通过检索相关文档提供准确的答案，适用于教育、培训等领域。
- **内容生成**：基于特定文档或资料生成定制化内容，如报告、文章撰写等。
- **技术支持**：检索技术文档或手册，提供详细的解决方案和操作指导。
- **法律咨询**：参考法律文献和案例，生成合规且有依据的法律建议。

## 3. 配置方法

### 配置概述

RAG 代理的配置文件位于 `configs` 目录中。`.yml` 文件定义了 RAG 过程的各项参数，包括模型设置、存储路径及相关操作。节点配置则在配置文件中定义，负责具体的任务执行和数据流转。

### 配置步骤

#### 1. 修改配置文件

根据您的具体需求编辑 `configs/rag_retrieval.yml` 文件。您可以自定义 RAG 相关的参数，如模型名称、API 密钥、文件路径等。确保所有必要的路径和密钥信息已正确配置，以便代理能够正常运行。

#### 2. 配置文件示例

以下是 RAG 过程的示例配置文件：

```yaml
RAG:
  RAG_ENABLE: true
  MODULE_PATH: null  # 如果有自定义模块路径，请取消注释并设置路径
  COLLECTION_NAME: mofa
  IS_UPLOAD_FILE: true
  CHROMA_PATH: ./data/output/chroma_store
  FILES_PATH:
    - /Users/chenzi/project/zcbc/mofa/python/examples/rag/data/input/2410.02742v1.pdf
  ENCODING: utf-8
  CHUNK_SIZE: 256
  RAG_SEARCH_NUM: 6
  RAG_MODEL_NAME: netease-youdao/bce-embedding-base_v1
  RAG_MODEL_API_URL: https://api.siliconflow.cn/v1
  RAG_MODEL_API_KEY: sk-

MODEL:
  MODEL_API_KEY: sk-XXXXXXXXXXXXXXXXXXXXXXXX  # 替换为您的 API 密钥
  MODEL_NAME: Qwen/Qwen2.5-72B-Instruct  # 替换为您的模型名称
  MODEL_API_URL: https://api.siliconflow.cn/v1/chat/completions
```

### 配置详情

#### `RAG_ENABLE`

- **RAG_ENABLE**：启用或禁用 RAG 功能。设置为 `true` 以启用 RAG。

#### `MODULE_PATH`

- **MODULE_PATH**：自定义模块的路径。如果使用默认模块，请保持 `null`。

#### `COLLECTION_NAME`

- **COLLECTION_NAME**：向量存储集合的名称，设置为 `"mofa"`。

#### `IS_UPLOAD_FILE`

- **IS_UPLOAD_FILE**：是否启用文件上传功能。设置为 `true` 以允许上传文件。

#### `CHROMA_PATH`

- **CHROMA_PATH**：向量存储数据库的路径，设置为 `"./data/output/chroma_store"`。

#### `FILES_PATH`

- **FILES_PATH**：需要上传和处理的文件路径列表。例如：
  ```yaml
  FILES_PATH:
    - /path/to/your/document1.pdf
    - /path/to/your/document2.pdf
  ```

#### `ENCODING`

- **ENCODING**：文件编码格式，通常设置为 `"utf-8"`。

#### `CHUNK_SIZE`

- **CHUNK_SIZE**：文档分块的大小，设置为 `256`，以确保有效的向量检索。

#### `RAG_SEARCH_NUM`

- **RAG_SEARCH_NUM**：每次检索返回的相关文档数量，设置为 `6`。

#### `RAG_MODEL_NAME`

- **RAG_MODEL_NAME**：用于嵌入的模型名称，例如 `"netease-youdao/bce-embedding-base_v1"`。

#### `RAG_MODEL_API_URL`

- **RAG_MODEL_API_URL**：RAG 模型的 API URL，例如 `"https://api.siliconflow.cn/v1"`。

#### `RAG_MODEL_API_KEY`

- **RAG_MODEL_API_KEY**：RAG 模型的 API 密钥，请替换为您的实际密钥，例如 `"   "`。

#### `MODEL`（生成模型配置）

- **MODEL_API_KEY**：您的生成模型 API 密钥，请替换为您的实际密钥，例如 `"sk-XXXXXXXXXXXXXXXXXXXXXXXX"`。
- **MODEL_NAME**：生成模型的名称，例如 `"Qwen/Qwen2.5-72B-Instruct"`。
- **MODEL_API_URL**：生成模型的 API URL，例如 `"https://api.siliconflow.cn/v1/chat/completions"`。


### 节点配置

RAG 代理的节点配置如下所示：

```yaml
nodes:
  - id: terminal-input
    build: pip install -e ../../node-hub/terminal-input
    path: dynamic
    outputs:
      - data
    inputs:
      context_rag: rag-retrieval/context_rag
      reasoner_response: reasoner-agent/reasoner_response

  - id: rag-retrieval
    operator:
      python: ./scripts/rag_retrieval.py
      inputs:
        task: terminal-input/data
      outputs:
        - context_rag

  - id: reasoner-agent
    operator:
      python: scripts/reasoner_agent.py
      inputs:
        task: terminal-input/data
        context_rag: rag-retrieval/context_rag
      outputs:
        - reasoner_response
```

#### 节点说明

- **terminal-input**：负责接收用户输入的任务，并将数据传递给下游节点。
- **rag-retrieval**：执行 RAG 检索任务，根据用户输入的任务从向量存储中检索相关上下文。
- **reasoner-agent**：基于检索到的上下文和用户任务生成智能响应。


## 4. 运行代理

### 使用 Dora-rs 命令行


1. **启动 RAG 代理进程**

   执行以下命令以启动 RAG 代理进程：

   ```bash
   dora up && dora build rag_dataflow.yml && dora start rag_dataflow.yml --attach
   ```

2. **初始化任务输入**

   打开另一个终端窗口并运行 `terminal-input`，然后输入相应的任务以启动 RAG 过程。

   ```bash
   terminal-input
   Enter your task: 提供有关机器学习的关键信息记录与检索
   ```



