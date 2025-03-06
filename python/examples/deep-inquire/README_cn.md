# Deep-Inquire 研究代理系统

基于Dora框架的多节点研究分析系统，集成OpenAI流式API服务

## 系统架构图
```mermaid
graph LR
    Client[客户端] -->|HTTP请求| Server[[dora-openai-server]]
    Server -->|用户查询| Agent[[deep-inquire-agent]]
    Agent -->|研究结果| Server
    Server -->|流式响应| Client
```

## 节点功能说明

### 1. dora-openai-server 节点
- **路径**: `../../node-hub/openai-server-stream`
- **功能**:
  - 提供兼容OpenAI API规范的HTTP端点
  - 处理客户端流式请求/响应
  - 转发用户查询到研究代理
  - 实时回传代理生成的研究片段
- **输入输出**:
  ```yaml
  inputs: deep-inquire-agent/deep_inquire_result
  outputs: v3/chat/completions
  ```

### 2. deep-inquire-agent 节点 
- **路径**: `../../agent-hub/deep-inquire`
- **功能**:
  - 执行多阶段研究分析：
    1. 智能网络搜索（Serper API）
    2. 上下文提取与可信度评估
    3. 矛盾检测与综合生成
  - 生成实时研究片段和最终报告
- **输入输出**:
  ```yaml
  inputs: dora-openai-server/v3/chat/completions
  outputs: deep_inquire_result
  ```

## 环境配置

1. 配置密钥文件
```bash
# .env.secret 已包含：
LLM_API_KEY=
LLM_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
LLM_MODEL_NAME=deepseek-v3-241226
SERPER_API_KEY=
```



## 启动流程

```bash
# 在 python/examples/deep-inquire/ 目录下执行

# 清理环境
dora destroy

# 启动Dora服务
dora up

# 构建数据流节点
dora build deep-inquire-dataflow.yml

# 启动并监控数据流
dora start deep-inquire-dataflow.yml --attach
```

## 测试方法

### 使用测试客户端
```bash
python moly_client_stream.py
```

### 示例请求/响应
```python
# 请求示例
user_input = '大语言模型安全防护最新研究'

# 响应片段示例
{
  "type": "thinking",
  "content": "正在分析来自arXiv的3篇论文...",
  "articles": [
    {
      "title": "LLM对抗训练新方法",
      "url": "https://arxiv.org/abs/2405.12345",
      "relevance": 0.95
    }
  ]
}
```

