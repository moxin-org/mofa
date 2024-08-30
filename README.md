# MOFA

## What

MOFA是一个以组合（Composition)的方式构建AI智能体的软件框架。使用MOFA，AI智能体可以通过模版方式构建，堆叠的方式组合，形成更强大的超级智能体（Super Agent)。

## WHY

用MOFA构建智能体：

1. 更简单：复杂智能体的构建是将模块进行组合的零代码过程。
2. 更清晰：“乐高积木”式的组合逻辑搭建复杂系统。比工作流更简单的模块之间的数据流定义。
3. 更快：智能体数据流运行在DORA-RS高性能低延迟的分布式AI和机器人计算环境，性能远超基于Python的计算环境。
4. 更强：MOFA的智能体组合将成员将智能体能力有机地结合在一起，形成功能更加强大和完善的组合智能体。
5. 使能边缘AI：执模心（Moxin开源项目)、施模法（Mofa项目）、展模力（Moly项目）。与提供本地开源大模型推理能力的Moxin项目和大语言模型和智能体用户界面的Moly项目一起，部署在本地Mofa智能体让AI的应用变得更加开放和民主化。 

## 开始（Getting started)

### 1. 安装

1. 克隆此项目切换到指定分支:

```sh
git clone <repository-url> && git checkout <branch-name> 
```

**示例**:

```sh
git clone git@github.com:moxin-org/Moxin-App-Engine.git && cd Moxin-App-Engine/mae && git checkout feature/mae
```

2. 使用Python 3.10或以上环境：

- 如果出现环境版本不匹配，请使用conda重新安装此环境。例如：

```sh
conda create -n py310 python=3.10.12 -y
```

3. 项目环境部署

- 安装环境的依赖：

```sh
pip3 install -r requirements.txt && pip3 install -e .

```

安装完毕之后，可以使用`mae --help`命令查看Cli帮助信息

4. Rust和Dora-RS安装

由于底层的Dora-RS计算框架基于Rust语言开发，请你访问下面的页面，根据你的操作系统安装Rust环境：

```sh
https://www.rust-lang.org/tools/install
```

安装 dora(v0.3.6-rc0)或以后的版本。安装步骤如下：

~~~
sudo rm $(which dora)
pip uninstall dora-rs

## dora binary
git clone https://github.com/dora-rs/dora.git
cd dora
cargo build --release -p dora-cli
PATH=$PATH:$(pwd)/target/release

## Python API
maturin develop -m apis/python/node/Cargo.toml

dora --help
~~~

### 2. 配置

在 `Moxin-App-Engine/mae/example` 这个目录下, 我们提供一些可用的智能体案例。在使用时，首先需要对智能体的configs目录下面的yml文件进行配置。 
如果`node`使用的是pip的方式进行安装的. 那么请你到`agent-hub`中找到对应的名称,并且修改里面的`yml`文件

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

#### 3.1 不同cmd命令

**获取当前可用Agent**:

~~~ /shell
mae agent-list
~~~

**运行Agent**:

~~~ /shell
mae run --agent-name reasoner
~~~

关闭Agent? 
输入exit/quit即可关闭

注意: 如果遇到Dora卡死的情况怎么办? 

**A:** :  建议在sudo命令下面使用 

~~~
pkill dora 
~~~

注意 它会删除所有的关于dora的进程 请谨慎使用

## Features

#### 模法1: AI智能体可嵌套的设计模式（The Nesting Design Patterns of AI Agents） 

AI智能体就是有智能特点的计算机软件。随着大语言模型和应用的迅速发展，如面向对象编程有多种设计模式一般，基于LLM的AI智能体的设计也有多种模式。常用的模式包括但不限于：

- 大语言模型推理模式(LLM Inference)：大语言模型本身就是最简单的智能体，根据用户的提示，LLM就可以通过推理给出智能化的响应。
- 提示定制模式（Customized Prompt）：通过对大语言模型的系统提示进行定制化所形成的智能体。

- 反思模式（Reflection）： 让Agent 能够审视和修正自己的输出的模式。
- 工具使用模式(Actor)：这种模式赋予 Agent 使用外部工具和资源的能力,如生成代码、调用 API、搜索网页等。
- ReAct模式：由反思和工具使用交替进行从而改进输出质量的模式。
- 多智能体协作模式：这种模式涉及多个 Agent 扮演不同的专家角色,协同完成任务。通过团队合作,多个 Agent 可以共同解决复杂问题。

一般而言，复杂的智能体设计模式可以通过嵌套在比较简单的设计模式的智能体上构成。所以，在MOFA中，我们提供了一些实现基础的（简单的）智能体设计模式的智能体模版。使用这些模版，应用开发者能够构建原子智能体，并与其它的智能体进行组合，形成功能完善，符合复杂需求的超级智能体。

#### 模法2：智能体核心服务 Agent Kernal Services

有如一个传统计算机操作系统为传统软件应用提供系统服务，MOFA为AI智能体提供智能体核心服务，包括记忆和存储(Memory), 任务规划(Planning)，知识库和RAG以及行动（Action）等。因此，根据用户不同的需求，这些核心服务可以一击提供给任何一个用户Agent。

#### 模法3: 智能体组合（Composition）

组合是将各元素拼接形成新事物的方法和过程，在组合的过程中，不涉及元素的实际结合或变化。组合是松耦合的，具有可逆行和可叠加的特性，比如乐高玩具，可以将形状不同的乐高积木通过组合的方式构建成各式各样的物体。这些物体还可以通过进一步的组合形成更加复杂的物体。组合的物体也可以通过拆解的过程，还原成各元素。

为了更好地理解组合，我们还可以对比一下事物形成的方法，比如：

复合（Compound)：化合是多种元素发生了变化和进行了实际的结合，形成一种新的物质的方法和过程。过程中，元素发生了变化，紧密耦合的（我中有你，你中有我），复合过程不具备可逆性和可叠加性。比如蛋糕烘焙，面粉、糖、奶油，鸡蛋等元素，经过一个烘焙的复合过程成为蛋糕。而用几个小蛋糕烘焙成更大蛋糕或将蛋糕中的糖，鸡蛋等元素分解还原出来，是非常困难的。

混合（Mix)：混合是将多种元素通过物理方式放在一起。虽然混合的过程也存在可逆星河可叠加性，但这种方法，各元素之间并没有发生联系，并没有产生新的事物，而是形成了元素的集合。比如：将苹果和橙子放到了一起，我们得到的是苹果和橙子的集合。

通过MOFA，基于组合的方法和过程，AI应用开发者可以构建AI智能体，也可以将现有的智能体进行创造性的组合，从而形成具有新功能或更加强大的智能体。因为MOFA，智能体的开发变得过程简单，模块化，逻辑清晰，可扩展，可重用。

#### 模法4: 数据流驱动（Dataflow Driven）

与基于工作流(Workflow)的方法不同，MOFA选择基于数据流（Dataflow)的方法。工作流的方法的重心在于对任务的流程和各操作步骤之间业务规则的抽象，而数据流的方法主要是确定任务之间的数据依赖性就可以了。

在各成员智能体之间搭建数据流是MOFA中组合的核心方法。MOFA并不特别关心复杂的业务规则和流程的编排。基本的业务规则在原子智能体模版里就获得了实现，而更复杂的业务规则是成员智能体内部维护，并不暴露在节点和节点之间的流程配置中。流程的编排并不强调管理业务之间顺序，而是数据流动的顺序。正是由于简单和不具“侵入”性的数据流驱动，保障了组合的可叠加和可逆性。在构建复杂应用的过程中，更具备可管理和可调试性。

在MOFA提供的智能体模版上定制用户智能体，一键获取任务规划、知识库、记忆和行动等核心能力，通过数据流将多个用数据流组合在一起提供更强大的功能。

## 示例

您可以在[examples](./examples)目录下测试MOFA的不同示例：

[simplicity.ai](examples/simplicity.ai): 一个由两个智能体组合而实现类似Perplexity.ai式用户体验的搜索案例。因为我们搜索的功能是通过简单调用Google Search API实现的，所以我们叫它simplicity。

[agent_fight](examples/agent_fight): 一个让大语言模型(GPT4o)做裁判，为完成同一任务的不同智能体所生成的报告进行评估，判定分数和胜负的智能体。

[arXiv_research](examples/arxiv_research)：一个通过搜索arXiv论文数据库，下载论文，总结论文并写出研究报告的，由多个智能体构成的组合智能体。