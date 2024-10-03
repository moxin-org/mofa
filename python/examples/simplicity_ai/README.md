
---

# Simplicity Ai组合智能体

## 1. 功能说明

该Simplicity Ai智能体用于根据用户任务输入的内容，从Google中搜索相关数据，自动生成总结，并提出与任务相关联的进一步问题。设计模式为：**Google搜索 + 内容总结 + 生成相关问题**。

## 2. 使用场景

该智能体适用于需要从Google搜索结果中获取相关信息并生成总结，同时提出与用户问题相关联的问题。常见的应用场景包括：

- 根据特定问题，从Web中检索内容，并对检索内容进行总结。
- 为用户问题生成进一步的相关问题，帮助用户深入探索主题。
- 自动化的信息提取和问题生成流程，提高研究或问题分析的效率。

## 3. 配置方法

Web Search Task模板通过调整配置信息来生成一个能够进行Web搜索、内容总结和相关问题生成的智能体。以下是详细的配置步骤和说明。(图为simplicity.ai 组合Agent的Dora Data Flow)

![image-20241003210034719](images/mermaid.png)


### 配置说明

配置文件位于`configs`目录下，`.py`文件为实际运行的智能体代码。配置文件指定了各个Agent的行为、搜索参数、生成逻辑等。

| **文件**                          | **作用**                                                                 |
| ---------------------------------- | ------------------------------------------------------------------------ |
| `configs/web_search_agent.yml`     | 配置Web搜索代理的参数，定义如何从Google中检索信息，并提取内容和网址。       |
| `configs/more_question_agent.yml`  | 配置生成问题的逻辑，结合搜索结果，生成与用户提出问题相关的进一步问题。      |
| `web_search_agent.py`              | 实际执行Web搜索操作，根据用户问题从Google中搜索相关信息并提取内容。          |
| `more_question_agent.py`           | 实际生成与问题相关的进一步问题，帮助用户探索更深层次的内容。               |

### 配置步骤

根据具体需求，编辑`configs`目录下的`.yml`配置文件。
可以自定义修改里面的模型参数，建议不要修改以及提示词。
使用的时候需要配置`SERPER_API_KEY`，如果没有，可以到https://serper.dev/ 注册一个(有免费额度)。


## 4. 运行智能体

使用Dora-rs命令行运行

1. 安装MoFA项目包。
2. 执行以下命令以启动智能体流程：
   ```bash
   dora up && dora build simplexity_ai_dataflow.yml && dora start simplexity_ai_dataflow.yml --attach
   ```
3. 启动另一个终端，运行`terminal-input`，然后输入相应任务以启动Web Search流程。

