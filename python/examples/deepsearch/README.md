
# DeepSearch Dataflow Deployment and Feature Guide

## Table of Contents

* [DeepSearch Dataflow Deployment and Feature Guide](#deepsearch-dataflow-deployment-and-feature-guide)

  * [Table of Contents](#table-of-contents)
  * [1. Project Overview and Core Features](#1-project-overview-and-core-features)

    * [DeepSearch Intelligent Research Agent System](#deepsearch-intelligent-research-agent-system)
  * [2. Environment Preparation and MoFA Framework Installation](#2-environment-preparation-and-mofa-framework-installation)
  * [3. Environment Variable Configuration (API Keys)](#3-environment-variable-configuration-api-keys)

    * [Step 1: Copy the `.env.example` File](#step-1-copy-the-envexample-file)
    * [Step 2: Fill in Your Keys](#step-2-fill-in-your-keys)
  * [4. `openai-server-stream` Node Description](#4-openai-server-stream-node-description)
  * [5. Building and Starting the DeepSearch Dataflow](#5-building-and-starting-the-deepsearch-dataflow)

    * [Step 1: Enter the Example Directory](#step-1-enter-the-example-directory)
    * [Step 2: Build the Dataflow Nodes](#step-2-build-the-dataflow-nodes)
    * [Step 3: Start the Dataflow](#step-3-start-the-dataflow)
  * [6. Interactive Testing and Sample Output](#6-interactive-testing-and-sample-output)

    * [Launching the Python Test Client](#launching-the-python-test-client)

      * [Sample Output](#sample-output)
  * [7. FAQs and Cross-Platform Compatibility](#7-faqs-and-cross-platform-compatibility)

    * [Cross-Platform Compatibility Notes](#cross-platform-compatibility-notes)
  * [8. References and Further Reading](#8-references-and-further-reading)

---

## 1. Project Overview and Core Features

### DeepSearch Intelligent Research Agent System

DeepSearch is an end-to-end streaming research agent built on the [MoFA](../../README.md) intelligent-agent development framework. Its key highlights include:

* **Multi-Stage Reasoning with Chunked Streaming Output**: For each user query, the system automatically performs “Retrieval → Article Processing → Multi-Stage Reasoning → Content Generation → Comprehensive Report,” outputting each stage in real time as chunks, which can be displayed incrementally on the front end.
* **Intelligent Web Retrieval with Credibility Assessment**: Integrates the SERPER API to fetch high-quality web resources, de-duplicate, rank, extract context, and evaluate credibility.
* **Multi-Round Content Generation and Synthesis**: Uses multiple rounds of LLM calls—first thinking, then summarizing, then generating content—to finally synthesize a complete report.
* **Extensible Streaming Dataflow Architecture**: All nodes can be independently extended and reused, supporting enterprise-level knowledge retrieval, intelligence analysis, and other scenarios.

For detailed dataflow and stage descriptions, please refer to the [DeepSearch Agent Design Document](../../agent-hub/deep-search/README.md).

---

## 2. Environment Preparation and MoFA Framework Installation

Please follow the instructions in the [MoFA main project documentation](../../README.md) to install Python, Rust, Dora CLI, and the MoFA framework.

* **Linux/macOS**: Recommended terminal: bash or zsh
* **Windows**: Recommended shell: PowerShell or WSL (Windows Subsystem for Linux)

> **Note**: Your local environment must have Python 3.10+, Rust 1.70+, and Dora CLI 0.3.9+.

---

## 3. Environment Variable Configuration (API Keys)

### Step 1: Copy the `.env.example` File

In the `python/examples/deepsearch/` directory, run:

```bash
# Linux/macOS
cp .env.example .env.secret

# Windows (PowerShell)
copy .env.example .env.secret
```

### Step 2: Fill in Your Keys

* **LLM\_API\_KEY**: Obtain from [OpenAI](https://platform.openai.com/account/api-keys) or other platforms like DeepSeek/Volcano Ark
* **SERPER\_API\_KEY**: Register and get it from [Serper.dev](https://serper.dev/)

Edit the `.env.secret` file and add:

```ini
LLM_API_KEY=your-llm-api-key
LLM_BASE_URL=https://api.openai.com/v1   # or another compatible API endpoint
LLM_MODEL_NAME=gpt-3.5-turbo             # or another model name
SERPER_API_KEY=your-serper-api-key
```

> **Security Tip**: The `.env.secret` file is listed in `.gitignore`. Do not commit it to your repository.

---

## 4. `openai-server-stream` Node Description

The integrated `openai-server-stream` node is built with FastAPI and Dora. It features:

* **Full Compatibility with OpenAI’s ChatCompletions Streaming API**, allowing seamless integration with the official OpenAI SDK.
* **Automatic Request Forwarding to Dora Dataflow**, streaming agent-generated content back in real time.

For detailed API reference and usage, see the [openai-server-stream documentation](../../node-hub/openai-server-stream/README.md).

---

## 5. Building and Starting the DeepSearch Dataflow

### Step 1: Enter the Example Directory

```bash
cd python/examples/deepsearch
```

### Step 2: Build the Dataflow Nodes

```bash
dora build deepsearch-dataflow.yml
```

* Installs all node dependencies automatically
* Validates the YAML configuration

### Step 3: Start the Dataflow

```bash
dora start deepsearch-dataflow.yml
```

* Once started, the system listens on port 8000 locally for client requests

---

## 6. Interactive Testing and Sample Output

### Launching the Python Test Client

Ensure your Dataflow is running. In a new terminal, run:

```bash
python moly_client_stream.py
```

* You can modify the `user_input` variable inside `moly_client_stream.py` to test any research topic.
* Supports streaming output; the terminal displays multi-stage reasoning and the final report in real time.

#### Sample Output

```json
{
  "type": "thinking",
  "content": "Analyzing 3 papers from arXiv...",
  "articles": [
    {"title": "A New Method for Adversarial Training of LLMs", "url": "https://arxiv.org/abs/2405.12345", "relevance": 0.95}
  ],
  "metadata": {"stage": "Context Extraction"},
  "id": "0-1"
}
```

---

## 7. FAQs and Cross-Platform Compatibility

| Issue                        | Possible Cause                       | Solution                                               |
| ---------------------------- | ------------------------------------ | ------------------------------------------------------ |
| Port in Use                  | Port 8000 is occupied                | Change Dataflow config or free up the port             |
| API Key Error                | Key not set or invalid               | Check your `.env.secret` file and verify the keys      |
| Cannot Access External Sites | Network restrictions                 | Configure a proxy or start Dora with `proxychains4`    |
| Dependency Installation Fail | Python/Rust environment issue        | Verify Python/Rust versions and reinstall dependencies |
| No Logs Appearing            | Dataflow not running or node failure | Check Dora logs to ensure all nodes are up and running |

### Cross-Platform Compatibility Notes

* **Linux/macOS**: All commands work directly in bash/zsh.
* **Windows**: Use PowerShell or WSL; replace commands like `cp` with `copy` where needed.

---

## 8. References and Further Reading

* [MoFA Main Project Documentation (Installation & Principles)](../README.md)
* [DeepSearch Agent Design](../../agent-hub/deep-search/README.md)
* [openai-server-stream Node Documentation](../../node-hub/openai-server-stream/README.md)
* [Serper.dev Official Documentation](https://serper.dev/)
* [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
* [Dora Runtime Official Documentation](https://dora-rs.ai/)

---

For further technical support, please contact the MoFA team or open an issue on the repository.
