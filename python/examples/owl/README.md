# Owl 智能代理

一个用于深度查询和信息处理的模块化AI代理框架。

## 功能特性
- owl项目进行开发
- 由于不同的模型对应不同的功能,当前只拿deepseek来作为案例

## 安装指南

1. 安装依赖(mac)：
```bash
brew install node

# Install Playwright MCP Service
npm install -g @executeautomation/playwright-mcp-server
npx playwright install-deps
```

## 配置说明

环境变量配置（在`.env.secret`中设置）：
```env
# API密钥和敏感配置项
DEEPSEEK_API_KEY='sk'
DEEPSEEK_API_BASE_URL="https://api.deepseek.com/v1"

```

## 使用说明

### 启动代理

1. 构建并启动数据流：
```bash
dora build owl_dataflow.yml && dora start owl_dataflow.yml
```

### 数据流配置 (`owl_dataflow.yml`)

数据流配置文件定义了节点及其连接关系：

```yaml
nodes:
  - id: terminal-input
    build: pip install -e ../../node-hub/terminal-input
    path: dynamic
    outputs:
      - data
    inputs:
      owl_agent_result: owl-agent/owl_agent_result
  
  - id: owl-agent
    build: pip install -e ../../agent-hub/owl-agent
    path: owl-agent
    outputs:
      - owl_agent_result
    inputs:
      user_query: terminal-input/data
    env:
      IS_DATAFLOW_END: true
      WRITE_LOG: true
```

