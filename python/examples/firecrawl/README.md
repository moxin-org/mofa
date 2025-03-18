

## 概述

本数据流用于通过 Firecrawl 抓取网页内容，并将结果返回给用户。数据流包含两个节点：

1. **terminal-input**: 终端输入节点，用于接收用户输入的 URL
2. **firecrawl-agent**: 网页抓取节点，使用 Firecrawl 抓取指定 URL 的内容

## 快速开始

### 1. 环境准备

确保已安装以下依赖：
- Python 3.10+
- Firecrawl Python SDK
- Dora 运行时

### 2. 配置 API 密钥

在项目根目录创建 `.env.secret` 文件，并添加 Firecrawl API 密钥：

```plaintext
FC_API_KEY=your_firecrawl_api_key
```

### 3. 启动数据流

```bash
# 构建数据流
dora build firecrawl_dataflow.yml

# 启动数据流并附加到终端
dora start firecrawl_dataflow.yml --attach
```

### 4. 使用说明

1. 启动数据流后，在终端输入要抓取的 URL
2. 数据流将返回抓取结果，包含以下内容：
   - markdown 格式的内容
   - 网页元数据
   - 原始 HTML

### 5. 示例

```bash
> https://example.com
{
  "markdown": "# Example Domain\n\nThis domain is for use in illustrative examples...",
  "metadata": {
    "title": "Example Domain",
    "url": "https://example.com",
    "statusCode": 200
  },
  "html": "<!doctype html>\n<html>\n<head>...</html>"
}
```

## 配置说明

### 数据流配置 firecrawl_dataflow.yml

```yaml
nodes:
  - id: terminal-input
    build: pip install -e ../../node-hub/terminal-input
    path: dynamic
    outputs: data
    inputs:
      firecrawl_agent_result: firecrawl-agent/firecrawl_agent_result

  - id: firecrawl-agent
    build: pip install -e ../../agent-hub/firecrawl-agent
    path: firecrawl-agent
    outputs: firecrawl_agent_result
    inputs:
      url: terminal-input/data
    env:
      IS_DATAFLOW_END: true
      WRITE_LOG: true
```

### 环境变量

- `IS_DATAFLOW_END`: 设置为 true 表示这是数据流的最后一个节点
- `WRITE_LOG`: 设置为 true 启用日志记录

## 常见
