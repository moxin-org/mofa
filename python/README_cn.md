# MoFA for Dora-RS

[English](README.md) | [简体中文](README_cn.md)

在这里，我们介绍如何安装、部署和启动建立在Dora-RS上的MoFA框架。

## Getting started

### 1. 安装

1. 克隆此项目切换到指定分支:

```sh
git clone <repository-url> && git checkout <branch-name> 
```

**示例**:

```sh
git clone git@github.com:moxin-org/mofa.git && cd mofa
```

2. 使用Python 3.10或以上环境：

- 如果出现环境版本不匹配，请使用conda重新安装此环境。例如：

```sh
conda create -n py310 python=3.10.12 -y
```

3. 项目环境部署

- 安装环境的依赖：

```sh
cd python && pip3 install -r requirements.txt && pip3 install -e .
```

安装完毕之后，可以使用`mofa --help`命令查看Cli帮助信息

4. Rust和Dora-RS安装

由于底层的Dora-RS计算框架基于Rust语言开发，请你访问下面的页面，根据你的操作系统安装Rust环境：

```sh
https://www.rust-lang.org/tools/install
```

然后安装 `cargo install dora-cli --locked`

### 2. 配置

在 `examples` 这个目录下, 我们提供一些可用的智能体案例。在使用时，首先需要对智能体的configs目录下面的yml文件进行配置。 
如果`node`如果使用的是pip的方式进行安装的. 那么请你到`agent-hub`中找到对应的node的名称,并且修改里面的`yml`文件

大语言模型推理 Api配置示例：
使用**Openai**API：

~~~yaml
MODEL:
  MODEL_API_KEY:  
  MODEL_NAME: gpt-4o-mini
  MODEL_MAX_TOKENS: 2048
~~~

当然你也可以配置成为Ollama模型，或Moxin提供的本地开源大模型：

使用**Ollama**示例:

~~~yaml
MODEL:
  MODEL_API_KEY: ollama
  MODEL_NAME: qwen:14b
  MODEL_MAX_TOKENS: 2048
  MODEL_API_URL: http://192.168.0.1:11434
~~~

### 3. 启动


---

### 操作步骤说明

以启动```examples```目录下的hello_world Agent为例：

1. **进入指定目录**  
   打开终端，切换到 `hello_world` 目录下，执行以下命令：  

   ```bash
   cd /mofa/python/examples/hello_world
   ```

2. **构建 Dataflow 文件**  
   在当前目录下新建一个终端窗口，执行以下命令构建和准备运行 Dataflow：  

   ```bash
   dora up && dora build dataflow.yml
   ```

   其中，`dataflow.yml` 是描述你要执行的 Agent 流程的配置文件。

3. **启动 Dataflow 流程**  
   在同一终端中，启动 Dataflow 流程：  

   ```bash
   dora start dataflow.yml
   ```

4. **处理动态节点 (Dynamic Node)**  
   如果 `dataflow.yml` 中某个节点的 `path` 被设置为 `dynamic`（例如：`path: dynamic`），需要在另一个终端窗口中单独运行该 Dynamic Node 的名称。  
   **示例：** 以下配置中的节点 `terminal-input` 是一个动态节点：  

   ```yaml
   nodes:
     - id: terminal-input
       build: pip install -e ../../node-hub/terminal-input
       path: dynamic
       outputs:
         - data
       inputs:
         agent_response: agent/agent_response
   ```

   对于上述节点，你需要开启一个新终端，并运行以下命令启动动态节点：  

   ```bash
   terminal-input
   ```

   这样可以确保 `terminal-input` 正常运行并接收/发送数据。


### 4. 详细文档

更多的详细文档在[documents](documents/README.md)子目录下。

