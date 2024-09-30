# 迈向AIOS （Toward AIOS）

本节简要地描述一下，MoFA的设计思想和我们创建MoFA更进一步的原因。

## 组合AI的远景和AIOS的原则

MoFA希望创造组合AI (Composition AI)：

- 以模块化的结构，组合的逻辑，让广大的AI开发者的聪明才智能够被承载，积累和壮大，让涓涓细流，汇成大海。
- 通过组合相对小规模的大语言模型、外部工具和编程技术，能够在特定领域任务上达到或超过大规模商用大语言模型的性能，三个臭裨将，胜过一个诸葛亮。

MoFA的设计思想借鉴了核心思想是Keep it Simple的Unix哲学, 特别是Eric Raymond's Unix Rules （详见《Unix编程艺术》一书）。

![Image](https://mmbiz.qpic.cn/mmbiz_png/ibqbukt6PTv7GgGOVgGIQgKB7nIRZrSOfowv1KjYcNGOxyPrap0GeMpYoEfVoLgkx5HgT0DQ7ibzdbZps7iagzjaw/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

MoFA所特别突出体现的几个Unix法则是：

1. 模块化（Modularity）：模块化的智能体模版，模块化的智能体服务，简单的模块配置，简单的模块间接口。
2. 更清晰（Clarity）：“乐高积木”式的组合逻辑搭建复杂系统。
3. 可组合（Composition）：智能体连接服务以获得更强的能力，智能体连接智能体以获得更多的功能。
4. 更简单（Simplicity）：复杂智能体的构建是将各模块进行组合的零代码过程。
5. 更多样化（Diversity）：MoFA的智能体组合将成员将智能体能力有机地结合在一起，形成功能更加强大和完善的组合智能体。
6. 可扩展（Extensibility)：简单而开放的架构和组织使得Everything can be an agent。各种能力可以通过agent的形式加入MoFA，并被组合，灵活使用，成为系统新的能力。

## 迈向AIOS

*MoFA*项目与*[Moxin](https://github.com/moxin-org/moxin)*, *Moly*, *[Dora-RS](https://github.com/dora-rs/dora)*, *[XLang](https://github.com/xlang-foundation/xlang)* 等开源项目一起，虽然各司其职，但它们的共同的使命是迈向AIOS，实现组合AI，使AI更加的全民化，并在边缘落地，让AI应用更加的繁荣。



![Image](https://mmbiz.qpic.cn/mmbiz_png/ibqbukt6PTv7GgGOVgGIQgKB7nIRZrSOfIpjjnmdDEAflmia8o28WK1FIzXS67UBRe2Qvg1aAJCf0by1romJXDsA/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

**持模心（Moxin)，施模法（MoFA)，展模力（Moly)。**Moxin，MoFA和Moly是我们Composition AI的三件套。从MoFA的角度看，Moxin为MoFA Agents提供大语言模型的管理和推理服务，特别是开源的大模型在本地（区别于云端）的服务；而Moly应用则为MoFA Agents提供一个类似ChatGPT的强大用户界面，同时支持本地部署。

智能体数据流运行在DORA-RS和XLang Executor高性能低延迟的分布式AI计算环境，性能远超基于Python的计算环境。

![Image](https://mmbiz.qpic.cn/mmbiz_png/ibqbukt6PTv7GgGOVgGIQgKB7nIRZrSOfGnKKv0vib6pajwIR3gl2oibicmcf6cdFdOicxfia1CWGJAu3liad97p0Diaiag/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

DoRA-RS不但提供了一个机器人应用的数据流框架，更是MoFA的多进程运行环境。XLang Executor则提供了一个分布式、多线程运行环境。DoRA-RS和XLang Executor提供了一个分布式的本地化的组合计算底座。