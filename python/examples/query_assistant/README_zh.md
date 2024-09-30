# Query Assistant Example in MoFA

**语言**: 中文

## 1. 功能说明

Query Assistant 是一个简单的问答智能体，旨在根据用户输入的问题提供直接的答案。其设计模式为：**接收问题 + 查询 + 返回答案**。

## 2. 使用场景

Query Assistant 适用于需要简单快速响应用户问题的场景。常见的应用场景包括：

- 为用户提供快速的知识性查询和回答。
- 处理简单的FAQ问答系统。
- 提供基于用户输入问题的即时答案。

## 3. 配置方法

Query Assistant 模板通过简单的配置来实现一个问答智能体。以下是详细的配置步骤和说明。

### 配置说明

配置文件位于`query_assistant`目录下，`.yml`文件为定义该智能体的数据流文件。配置文件指定了智能体的工作流，包括如何接收问题并生成答案。

| **文件**                               | **作用**                                                                 |
| -------------------------------------- | ------------------------------------------------------------------------ |
| `query_assistant_dataflow.yml`         | 配置问答任务的数据流，包括如何接收用户问题并查询对应答案。                  |

## 4. 运行智能体

### 方法一：使用Dora-rs命令行运行

1. 安装MoFA项目包。
2. 执行以下命令以启动智能体流程：
   ```bash
   dora up && dora build query_assistant_dataflow.yml && dora start query_assistant_dataflow.yml --attach
   ```
3. 启动另一个终端，运行`terminal-input`，然后输入相应任务以启动Query Assistant流程。

### 方法二：在MoFA运行环境中运行

此方法待定（TBD）。

