# 模法1: AI智能体可嵌套的设计模式（The Nesting Design Patterns of AI Agents） 

AI智能体就是有智能特点的计算机软件。随着大语言模型和应用的迅速发展，如面向对象编程有多种设计模式一般，基于LLM的AI智能体的设计也有多种模式。常用的模式包括但不限于：

- 大语言模型推理模式(LLM Inference)：大语言模型本身就是最简单的智能体，根据用户的提示，LLM就可以通过推理给出智能化的响应。
- 提示定制模式（Customized Prompt）：通过对大语言模型的系统提示进行定制化所形成的智能体。
- 反思模式（Reflection）：让Agent 能够审视和修正自己的输出的模式。
- 工具使用模式(Actor)：这种模式赋予 Agent 使用外部工具和资源的能力,如生成代码、调用 API、搜索网页等。
- 多智能体协作模式：这种模式涉及多个 Agent 扮演不同的专家角色,协同完成任务。通过团队合作,多个 Agent 可以共同解决复杂问题。

![Image](https://mmbiz.qpic.cn/mmbiz_png/ibqbukt6PTv7GgGOVgGIQgKB7nIRZrSOfbsyEsWDNphZOVeJlt7Rm0m4N4acgtAcAU1AVFwJJmyR3IficL2xjpTQ/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

图：MoFA认为：智能体有多种不同的设计模式。就好像elusive套娃，复杂的智能体，往往嵌套简单的智能体。

一般而言，复杂的智能体设计模式可以通过嵌套在比较简单的设计模式的智能体上构成。所以，在MoFA中，我们提供了一些实现基础的（简单的）智能体设计模式的智能体模版。使用这些模版，应用开发者能够构建原子智能体，并与其它的智能体进行组合，形成功能完善，符合复杂需求的超级智能体。