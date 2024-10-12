# Code Assistant Example in MoFA

**语言**: 中文

## 1. 功能说明

Code Assistant 是一个简单的代码助手，旨在根据用户输入的需求提供代码。其设计模式为：**接收问题 + 查询代码相应部分 + 返回代码**。

## 2. 使用场景

Code Assistant 适用于需要简单编写代码的场景。常见的应用场景包括：

- 帮助用户查找代码中的错误。
- 帮助用户编写一定代码。

## 3. 配置方法

Code Assistant 模板通过简单的配置来实现一个问答智能体。以下是详细的配置步骤和说明。

### 配置说明

配置文件位于`configs`目录下，`.yml`文件为定义该智能体的数据流文件。配置文件指定了智能体的工作流，包括如何接收问题并生成答案。

| **文件**                               | **作用**                                                                 |
| -------------------------------------- | ------------------------------------------------------------------------ |
| `code_assistant_agent    .yml`         | 根据用户给出的问题即代码片段，给出新的代码。                        |
| `code_content_agent    .yml`           | 根据用户给出的问题，从代码中提取关键片段。                          |

## 4. 运行智能体

### 方法一：使用Dora-rs命令行运行

1. 安装MoFA项目包。
2. 安装code-assistants依赖库
   ```bash
   pip install -r requirements.txt
   ```
3. 执行以下命令以启动智能体流程：
   ```bash
   dora up && dora build code_assistant_dataflow.yml && dora start code_assistant_dataflow.yml --attach
   ```
34. 启动另一个终端，运行`terminal-input`，然后输入相应任务以启动Code Assistant流程。

### 注意
如果你希望将你的代码作为上下文传递给智能体，你需要将你的代码放入code_assistant目录(不支持子目录)，并以.py文件命名。
并且所有直接放入code_assistant目录下的.py文件都会作为智能体的上下文
