# MoFA for Dora-RS

在这个分支里，我们介绍建立在Dora-RS上的MoFA框架。

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

~~~
MODEL:
  MODEL_API_KEY:  
  MODEL_NAME: gpt-4o-mini
  MODEL_MAX_TOKENS: 2048
~~~

当然你也可以配置成为Ollama模型，或Moxin提供的本地开源大模型：

使用**Ollama**示例:

~~~
MODEL:
  MODEL_API_KEY: ollama
  MODEL_NAME: qwen:14b
  MODEL_MAX_TOKENS: 2048
  MODEL_API_URL: http://192.168.0.1:11434
~~~



### 3. 启动

在命令端启用MOFA智能体

### 4. 详细文档

更多的详细文档在[documents](documents/README.md)子目录下。

