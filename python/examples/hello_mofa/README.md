# Hello MoFA

[English](README.md) | [简体中文](README_cn.md)

This project demonstrates the most basic intelligent agent design pattern implemented in MoFA. Without writing any code, you can construct a MoFA LLM Agent using MoFA's `agent-hub` and `node-hub`.

```yaml
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

## 1. Overview

LLM (Large Language Model) serves as the simplest type of intelligent agent. Its design pattern includes:

- Customized prompts for large language models
- Inference by large language models

## 2. Use Cases

This agent is useful when you need to customize prompts for a large language model.

## 3. Configuration

The basic configuration involves modifying the template configuration file `agent-hub/llm/llm_agent.yml` to utilize different LLMs.

```yaml
MODEL:
  # MODEL_API_KEY:
  # MODEL_NAME: deepseek-ai/DeepSeek-V2-Chat
  # MODEL_MAX_TOKENS: 2048
  # MODEL_API_URL: https://api.siliconflow.cn/v1/chat/completions
  MODEL_API_KEY:
  MODEL_NAME: gpt-4o-mini
  MODEL_MAX_TOKENS: 2048
```

If you plan to use OpenAI's LLM and have already configured the `OPENAPI_API_KEY` in the `.env` file, you do not need to configure `MODEL_API_KEY` here.

| File                      | Description                                                  |
| ------------------------- | ------------------------------------------------------------ |
| `hello_mofa_dataflow.yml` | Update the path for `build: pip install -e ../../node-hub/terminal-input` based on the directory (absolute paths are allowed). |
| `hello_mofa_dataflow.yml` | Update the path for `build: pip install -e ../../agent-hub/llm` based on the directory (absolute paths are allowed). |

------

## 4. Running the Agent

### Run with Dora-RS Command-Line Tool:

1. Install the MoFA project package.

2. Execute the following command:

   ```shell
   dora up && dora build hello_mofa_dataflow.yml && dora start hello_mofa_dataflow.yml
   ```

3. Open another terminal window and run:

   ```shell
   terminal-input
   ```

   Input tasks to interact with the agent.