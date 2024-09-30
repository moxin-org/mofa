
# 项目安装和启动指南
**语言**
- [English](README_en.md)


## 目录

1. [Mae项目安装](#1-mae项目安装)
   1. [项目环境部署](#11-项目环境部署)
   2. [安装项目](#12-安装项目)
2. [Rust环境安装](#2-rust环境安装)
3. [项目结构说明](#3-项目结构说明)
   1. [项目主目录 `mae/`](#项目主目录-mae)
      - [模块 `apps/`](#模块-apps)
      - [模块 `kernel/`](#模块-kernel)
      - [模块 `run/`](#模块-run)
      - [模块 `utils/`](#模块-utils)
   2. [目录 `tests/`](#目录-tests)
   3. [根目录文件](#根目录文件)
4. [Example项目启动](#4-example项目启动)
   1. [Example项结构说明](#41-example项结构说明)
   2. [配置说明](#42-配置说明)
      - [Rag-Agent 配置说明](#421-rag-agent-配置说明)
      - [Crewai 配置说明](#422-crewai-配置说明)
5. [启动事项](#5-启动事项)
6. [常见问题解答 (FAQ)](#6-常见问题解答-faq)

## 1. Mae项目安装

### 1.1 项目环境部署
建议使用`Dockerfile`来部署当前环境，我们已经在`Dockerfile`中安装了`Rust`和`Python`。
```sh
docker build -t mae_env:v1 .
```

### 1.2 安装项目

- 克隆此项目：
```sh
git clone <repository-url>
```
- 切换到Python 3.10环境：
  - 如果出现环境版本不匹配，请使用conda重新安装此环境：
  ```sh
  conda create -n py310 python=3.10.12 -y
  ```
- 安装mae项目：
```sh
pip3 install -r requirements.txt && pip3 install -e .
```

## 2. Rust环境安装
根据你的系统安装Rust环境：
```sh
https://www.rust-lang.org/tools/install
```

然后安装dora-rs的包：
```sh
cargo install dora-cli --locked
```

## 3. 项目结构说明

### 项目主目录 `mae/`
包含所有应用和内核代码。

#### 模块 `apps/`
包含多个Agent应用模块，每个模块都有特定功能的agent。

#### 模块 `kernel/`
app核心功能模块，包含记忆、规划、检索、工具和实用程序等子模块。
- **`memory/`**: 负责记忆相关的功能模块。
- **`planning/`**: 负责规划相关的功能模块。
- **`rag/`**: 负责检索增强生成（RAG）相关的功能模块。
- **`tools/`**: 包含Agent各种工具模块。
- **`utils/`**: 实用程序模块，提供各种辅助功能。

#### 模块 `run/`
负责运行的模块，包含运行时所需的脚本。
- **`run.py`**: 主运行脚本，启动项目的主要功能。

#### 模块 `utils/`
项目的通用工具模块。

### 目录 `tests/`
包含测试文件和配置，用于确保项目功能的正确性。

### 根目录文件
- **`.dockerignore`**: Docker忽略文件，定义哪些文件和目录在构建Docker镜像时被忽略。
- **`.gitignore`**: Git忽略文件，定义哪些文件和目录在版本控制中被忽略。
- **`CONTRIBUTING.rst`**: 项目贡献指南，指导如何为项目做出贡献。
- **`Dockerfile`**: Docker配置文件，用于构建项目的Docker镜像。
- **`HISTORY.rst`**: 项目历史记录文件，记录项目的更新和变化。
- **`MANIFEST.in`**: 定义哪些文件在项目打包时包含在内。
- **`README.md`**: 项目主要说明文件，提供项目的概述和使用指南。
- **`README.rst`**: 项目主要说明文件的reStructuredText版本。
- **`requirements.txt`**: Python依赖文件，列出项目所需的所有Python依赖包。
- **`setup.cfg`**: 项目配置文件，包含打包和元数据信息。
- **`setup.py`**: 项目安装脚本，用于安装和打包项目。

## 4. Example项目启动

### 4.1 Example项结构说明
```plaintext
agents
└── reasoner  # agent 名称
    ├── README.md  
    ├── data  # 数据存放地址
    │   └── input  # 输入数据
    │       └── moa_llm.pdf 
    ├── listener.py  # 负责监听dora流程中的结果
    ├── out # dora 流程输出
    │   ├── 019073e3-febd-7538-8ece-1ac71284ac4c
    │   └── 019073e6-71e7-7d81-87d3-d0726c9ceee5
    │       ├── log_agents.txt
    │       ├── log_listener.txt
    │       └── log_loader.txt
    ├── reasoner_dataflow.yml # dora 流程配置文件
    ├── reasoning_agent.py # agent 逻辑
    ├── reasoning_loader.py  # 加载agent 配置文件
    ├── result  # use_case输出结果保存地址
    └── use_case  # use_case配置文件
        ├── phrase_spelling_error_by_dspy.yml  # 语法错误案例
        ├── snake_game_build_by_dspy.yml  # 贪吃蛇案例
        └── summarize_pdf_by_rag.yml # 论文rag提取总结
```

### 4.2 配置说明
[Agent配置说明](config%2FAgent_Config_zh.md)

## 5. 启动事项

1. 启动dataflow流程：
```sh
dora up
```

2. 如果你需要切换不同的use_case,那么你需要到[reasoning_loader.py](..%2Fexamples%2Fagents%2Freasoner%2Freasoning_loader.py)，将里面的第17行,修改成你需要运行的use_case：
```python
params = read_yaml('use_case/summarize_pdf_by_rag.yml')  # 修改这个里面的yml文件地址和名称
```

3. 在每个use_case中,你都需要定义好你的模型的api-key是什么,否则是用不了的(建议使用 gpt-3.5-turbo)

4. 如何使用Rag-UseCase?
- Rag的use-Case是使用Rag做结尾的,例如 `summarize_pdf_by_rag.yml`
- 因为我们的Rag的Vector数据库使用的是Postgres-Vector,我们本地必须运行一个Vector数据库(基于Docker运行)
```sh
docker run --name pgvector-container -e POSTGRES_USER=langchain -e POSTGRES_PASSWORD=langchain -e POSTGRES_DB=langchain -p 6024:5432 -d pgvector/pgvector:pg16
```
- 如果你没有docker,那么可以使用我们公共测试的Pg-Vector账号密码. (注意,此账号密码可能因为安全原因被销毁,连接前请尝试去连接此数据库,确定此数据库可用)
```sh
postgresql+psycopg://mofa:MLbDGKC7d7IPBN@124.156.214.116:6024/mae_db
```
- Rag当前只支持`Txt`和`Pdf`文件格式

5.运行Dora流程
```sh
dora start  reasoner_dataflow.yml --attach
```

## 6. 常见问题解答 (FAQ)

**Q: 我在运行项目时遇到版本不兼容的问题怎么办？**
A: 请确保你的环境是Python 3.10版本以上，如果版本不兼容，建议使用conda创建一个Python 3.10的环境。

**Q: 如何切换不同的use_case？**
A: 请修改`reasoning_loader.py`文件中的第17行，将其指向你需要运行的use_case配置文件。

**Q: Postgres-Vector数据库的连接信息是什么？**
A: 如果使用本地Docker运行的数据库，连接信息为：
```sh
postgresql+psycopg://langchain:langchain@localhost:6024/langchain
```
如果使用公共测试的Pg-Vector数据库，连接信息为：
```sh
postgresql+psycopg://mofa:MLbDGKC7d7IPBN@124.156.214.116:6024/mae_db
```

**Q: 为什么我的Rag-UseCase没有返回预期的结果？**
A: 请检查你的embedding模型配置是否正确，并确保你的Postgres-Vector数据库正常运行。

希望这个文档对你有帮助，如果有任何问题，请随时联系我。
```

