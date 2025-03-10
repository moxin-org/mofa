# **MoFA**

[English](README.md) | [简体中文](README_cn.md)

*持模心，施**模法**，展模力。*

*With MoXin in the heart, Play **MoFA** magic, Show Moly to the world.* 

<sub>注：Moxin 和 Moly 是MoFA的姊妹项目。</sub>

## What

MoFA: **M**odular **F**ramework for **A**gent 

MoFA是一个以组合（Composition)的方式构建AI智能体的软件框架。使用MoFA，AI智能体可以通过模版方式构建，堆叠的方式组合，形成更强大的超级智能体（Super Agent)。

## WHY

用MoFa构建智能体：

1. 模块化（Modularity）：模块化的智能体模版，模块化的智能体服务，简单的模块配置，简单的模块间接口。
2. 更清晰（Clarity）：“乐高积木”式的组合逻辑搭建复杂系统。
3. 可组合（Composition）：智能体连接服务以获得更强的能力，智能体连接智能体以获得更多的功能。
4. 更简单（Simplicity）：复杂智能体的构建是将各模块进行组合的零代码过程。
5. 更快（High Performance）：智能体数据流运行在DORA-RS高性能低延迟的分布式AI和机器人计算环境，性能远超基于Python的计算环境。
6. 更多样化（Diversity）：MoFa的智能体组合将成员将智能体能力有机地结合在一起，形成功能更加强大和完善的组合智能体。
7. 迈向AI操作系统（Towards AIOS）：参照Unix Philosophy和设计方法设计：大语言模型推理提供“AIOS”的核心算力，Dora-RS和XMind Executor提供“AIOS”底层多进程计算调度和环境，而MoFa则是
   - “AIOS”的Kernal Services，为智能体提供任务规划，记忆，行动和RAG等服务， 
   - “AIOS”的Utility and Applications：实现常用功能、基础功能的Agents和它们的模版，和
   - “AIOS”的Shell：运行智能体（即AI智能体）和通过PIPELINE等方式连接和组合智能体并使其自动化运行的环境。
8. 使能边缘AI（Enable Edge AI）：执模心（MoXin开源项目)、施模法（MoFa项目，即本项目）、展模力（MoLy项目）。与提供本地开源大模型推理能力的MoXin项目和大语言模型和智能体用户界面的MoLy项目一起，部署在本地MoFa智能体让AI的应用变得更加开放和民主化。

## Features

#### 模法1: AI智能体可嵌套的设计模式（The Nesting Design Patterns of AI Agents） 

AI智能体就是有智能特点的计算机软件。随着大语言模型和应用的迅速发展，如面向对象编程有多种设计模式一般，基于LLM的AI智能体的设计也有多种模式。常用的模式包括但不限于：

- 大语言模型推理模式(LLM Inference)：大语言模型本身就是最简单的智能体，根据用户的提示，LLM就可以通过推理给出智能化的响应。
- 提示定制模式（Customized Prompt）：通过对大语言模型的系统提示进行定制化所形成的智能体。

- 反思模式（Reflection）： 让Agent 能够审视和修正自己的输出的模式。
- 工具使用模式(Actor)：这种模式赋予 Agent 使用外部工具和资源的能力,如生成代码、调用 API、搜索网页等。
- ReAct模式：由反思和工具使用交替进行从而改进输出质量的模式。
- 多智能体协作模式：这种模式涉及多个 Agent 扮演不同的专家角色,协同完成任务。通过团队合作,多个 Agent 可以共同解决复杂问题。

一般而言，复杂的智能体设计模式可以通过嵌套在比较简单的设计模式的智能体上构成。所以，在MoFa中，我们提供了一些实现基础的（简单的）智能体设计模式的智能体模版。使用这些模版，应用开发者能够构建原子智能体，并与其它的智能体进行组合，形成功能完善，符合复杂需求的超级智能体。

#### 模法2：智能体核心服务 Agent Kernal Services

有如一个传统计算机操作系统为传统软件应用提供系统服务，MoFa为AI智能体提供智能体核心服务，包括记忆和存储(Memory), 任务规划(Planning)，知识库和RAG以及行动（Action）等。因此，根据用户不同的需求，这些核心服务可以一击提供给任何一个用户Agent。

#### 模法3: 智能体组合（Composition）

组合是将各元素拼接形成新事物的方法和过程，在组合的过程中，不涉及元素的实际结合或变化。组合是松耦合的，具有可逆行和可叠加的特性，比如乐高玩具，可以将形状不同的乐高积木通过组合的方式构建成各式各样的物体。这些物体还可以通过进一步的组合形成更加复杂的物体。组合的物体也可以通过拆解的过程，还原成各元素。

为了更好地理解组合，我们还可以对比一下事物形成的方法，比如：

复合（Compound)：化合是多种元素发生了变化和进行了实际的结合，形成一种新的物质的方法和过程。过程中，元素发生了变化，紧密耦合的（我中有你，你中有我），复合过程不具备可逆性和可叠加性。比如蛋糕烘焙，面粉、糖、奶油，鸡蛋等元素，经过一个烘焙的复合过程成为蛋糕。而用几个小蛋糕烘焙成更大蛋糕或将蛋糕中的糖，鸡蛋等元素分解还原出来，是非常困难的。

混合（Mix)：混合是将多种元素通过物理方式放在一起。虽然混合的过程也存在可逆性和可叠加性，但这种方法，各元素之间并没有发生联系，并没有产生新的事物，而是形成了元素的集合。比如：将苹果和橙子放到了一起，我们得到的是苹果和橙子的集合。

通过MoFA，基于组合的方法和过程，AI应用开发者可以构建AI智能体，也可以将现有的智能体进行创造性的组合，从而形成具有新功能或更加强大的智能体。因为MoFA，智能体的开发变得过程简单，模块化，逻辑清晰，可扩展，可重用。

#### 模法4: 数据流驱动（Dataflow Driven）

与基于工作流(Workflow)的方法不同，MoFA选择基于数据流（Dataflow)的方法。工作流的方法的重心在于对任务的流程和各操作步骤之间业务规则的抽象，而数据流的方法主要是确定任务之间的数据依赖性就可以了。

在各成员智能体之间搭建数据流是MoFA中组合的核心方法。MoFA并不特别关心复杂的业务规则和流程的编排。基本的业务规则在原子智能体模版里就获得了实现，而更复杂的业务规则是成员智能体内部维护，并不暴露在节点和节点之间的流程配置中。流程的编排并不强调管理业务之间顺序，而是数据流动的顺序。正是由于简单和不具“侵入”性的数据流驱动，保障了组合的可叠加和可逆性。在构建复杂应用的过程中，更具备可管理和可调试性。

在MoFA提供的智能体模版上定制用户智能体，一键获取任务规划、知识库、记忆和行动等核心能力，通过数据流将多个用数据流组合在一起提供更强大的功能。

## How

MoFA目前支持基于Dora-RS的智能体开发模式。

- 基于Dora-RS的开发模式，详见[python](python)目录[README.md](python/README.md)



## GOSIM China 2024 Super Agent Hackathon

MoFA项目是GOSIM 2024中国大会Super Agent黑客马拉松大赛的编程框架之一。

- 为参赛选手准备的文档在[这里>>>](Gosim_2024_Hackathon/documents/README.md).

- 比赛的情况和结果在[这里>>>](https://gosim.gitcode.com/hackathon/)
- 用MoFA编织你的人工智能应用程序，GOSIM China 2024 [YouTube](https://www.youtube.com/watch?v=FhL3orAVO6U)
