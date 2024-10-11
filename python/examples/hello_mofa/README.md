# Hello MoFA  

MoFA中最基本的智能体设计模式的实现. 不需要编写任何代码，通过利用MoFA `agent-hub` 和`node-hub`构造一个MoFA LLM Agent。

```
nodes:
  - id: terminal-input
    build: pip install -e ../../node-hub/terminal-input
    path: dynamic
    outputs:
      - data
    inputs:
      reasoner_results: llm/llm_results

  - id: llm
    build: pip install -e ../../agent-hub/llm
    path: llm
    inputs:
      task: terminal-input/data
    outputs:
      - llm_results
```

## 1. 功能说明

LLM可以说是最简单的智能体。它的设计模式是：定制的大语言模型提示 + 大语言模型推理。

## 2. 使用场景

在智能体想定制大语言模型的提示时使用。

## 3. 配置方法

基本的配置原理就是通过更改`agent-hub/llm/llm_agent.yml`模版里的配置信息来调用不同的LLM。

```   
MODEL:
  # MODEL_API_KEY:
  # MODEL_NAME: deepseek-ai/DeepSeek-V2-Chat
  # MODEL_MAX_TOKENS: 2048
  # MODEL_API_URL: https://api.siliconflow.cn/v1/chat/completions
  MODEL_API_KEY:
  MODEL_NAME: gpt-4o-mini
  MODEL_MAX_TOKENS: 2048
```  

如果您想利用OpenAI的LLM， 并且已经在`.env`文件中配置了`OPENAPI_API_KEY`, 那不需要配置这里的`MODEL_API_KEY`. 
   

   | 文件                            | 说明                                                         |
   | ------------------------------- | ------------------------------------------------------------ |
   | `hello_mofa_dataflow.yml`       | 根据当前目录，需要更改`build: pip install -e ../../node-hub/terminal-input`的路径(可以在mofa/node-hub/terminal-input中找到. 可以填写绝对路径) |
   | `hello_mofa_dataflow.yml`       | 根据当前目录，需要更改`build: pip install -e ../../agent-hub/llm`的路径(可以在mofa/agent-hub/llm中找到. 可以填写绝对路径)
   


## 4. 运行Agent

### 在Dora-rs命令端里运行：

1. 安装MoFA项目包
2. `dora up && dora build  hello_mofa_dataflow.yml && dora start hello_mofa_dataflow.yml`
3. 启动另外一个命令端,在另外一个命令端运行 `terminal-input`.然后输入任务即可

