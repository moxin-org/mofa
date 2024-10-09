# 在本地运行开源大语言模型

参赛选手可以选择在自己的设备上通过 Moly 运行开源大语言模型，并以此为基础构建 LLM agent。

Moly 是一个使用 Rust 实现的在本地运行 LLM 的客户端工具，已支持多个开源模型，并且可以提供与 OpenAI 完全兼容的 API。

1. 前往 Moly 官网，根据自己的系统下载对应的软件包：https://www.moxin.app/
2. 浏览 model card，并且下载对应模型
3. 选择 Chat with Model，就可以与当前模型进行交互

同时，

通过 Moly 运行的开源大语言模型有着和 OpenAI API 完全兼容的 API server，接下来你就可以用熟悉的工具构建 LLM Agent

参考资料：
* [常用的 API Reference](https://llamaedge.com/docs/user-guide/api-reference)
* [OpenAI python library](https://llamaedge.com/docs/user-guide/openai-api/intro#the-openai-python-library)
