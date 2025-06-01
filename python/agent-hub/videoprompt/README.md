# videoprompt

MoFA框架中的视频提示词生成智能体，基于关键帧信息生成优化的视频制作提示词。

## 功能特性

- 智能视频提示词生成
- 基于关键帧信息的内容优化
- 支持多种LLM API
- 可配置的提示词模板
- 与MoFA数据流无缝集成

## 安装

使用相对路径安装：

```bash
cd python/agent-hub/videoprompt
pip install -e .
```

## 基本使用

### 环境配置

配置以下环境变量：

```bash
# LLM API配置
LLM_API_KEY=your_api_key_here
LLM_API_BASE=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat
```

### 数据流集成

在MoFA数据流配置中使用：

```yaml
nodes:
  - id: videoprompt
    build: pip install -e ../../agent-hub/videoprompt
    path: videoprompt
    outputs:
      - videoprompt_result
    inputs:
      query: keyframe-agent/keyframe_result
    env:
      WRITE_LOG: true
```

### 使用示例

该agent接收关键帧结果并生成视频提示词：

```python
# 输入：关键帧描述结果
# 输出：优化的视频制作提示词
```

## API参考

### 输入
- `query`: 关键帧描述结果

### 输出
- `videoprompt_result`: 生成的视频提示词

### 环境变量
- `LLM_API_KEY`: LLM API密钥
- `LLM_API_BASE`: LLM API基础URL  
- `LLM_MODEL`: 使用的LLM模型名称

## 项目结构

```
videoprompt/
├── README.md              # 项目文档
├── pyproject.toml         # Python包配置
├── videoprompt/
│   └── agent/
│       └── main.py        # 主要代码
└── tests/
    └── test_main.py       # 测试代码
```

## 开发

运行测试：
```bash
python -m pytest tests/
```

## 安全注意事项

请确保将API密钥存储在环境变量中，不要在代码中硬编码。

## 许可证

MIT License
