# Euterpe Agent 技术实现文档

## 1. 架构概述

Euterpe Agent 是连接 MoFA 框架和 euterpe-creator 包的桥梁，通过数据流机制实现 AI 视频生成功能。该 agent 采用了以下分层架构：

```
+------------------+
|   MoFA 框架      |
+------------------+
        ↓
+------------------+
|  Euterpe Agent   |  → 解析参数、协调处理流程、返回结果
+------------------+
        ↓
+------------------+
|  euterpe-creator |  → 视频生成核心库
+------------------+
        ↓
+------------------+
| AI 服务 (API)    |  → Kling, Beatoven, Dify 等
+------------------+
```

## 2. 代码结构说明

```
euterpe-agent/
├── euterpe_agent/
│   ├── __init__.py              # 包初始化
│   ├── main.py                  # 主要逻辑实现
│   └── configs/
│       └── agent.yml            # Agent 配置文件
├── tests/                       # 测试代码目录
├── pyproject.toml               # 项目依赖配置
├── README.md                    # 基本说明
├── DOCUMENTATION.md             # 使用文档
├── TECHNICAL.md                 # 技术文档（本文件）
└── euterpe_dataflow.yml         # 数据流配置
```

## 3. 核心模块实现

### 3.1 参数解析模块

`main.py` 中实现了 JSON 参数解析逻辑，将输入的 JSON 转换为 euterpe-creator 支持的模型对象：

```python
# JSON 字符串解析为字典
if isinstance(params, str):
    try:
        params = json.loads(params)
    except json.JSONDecodeError:
        agent.logger.error(f"Failed to parse JSON parameters: {params}")
        agent.send_output(
            agent_output_name='euterpe_result',
            agent_result={"error": "Invalid JSON parameters"}
        )
        return

# 字典转换为 Pydantic 模型
keyframes = []
for kf in params['keyframes']:
    keyframe = Keyframe(
        frame_id=kf.get('frame_id'),
        timestamp=kf.get('timestamp', 0.0),
        prompt=kf.get('prompt', ''),
        negative_prompt=kf.get('negative_prompt'),
        image_path=kf.get('image_path'),
    )
    keyframes.append(keyframe)
```

### 3.2 配置处理模块

负责处理环境变量和配置对象的创建：

```python
# 创建 EuterpeConfig 对象
config = EuterpeConfig(
    output_dir=output_dir,
    kling_api_key=os.environ.get('KLING_API_KEY'),
    beatoven_api_key=os.environ.get('BEATOVEN_API_KEY'),
)
```

### 3.3 视频生成模块

封装了 euterpe-creator 的 `generate_video` 函数调用：

```python
# 创建 VideoGenerationRequest 对象
request = VideoGenerationRequest(
    keyframes=keyframes,
    music_params=music_params,
    aspect_ratio=aspect_ratio,
    image_model=image_model,
    dify_enhancement_params=dify_params,
    fps=params.get('fps', 30),
    resolution=params.get('resolution', 720),
)

# 调用 euterpe-creator 生成视频
result = generate_video(request, config)
```

### 3.4 结果处理模块

将 euterpe-creator 的结果转换为标准的输出格式：

```python
# 创建响应对象
response = {
    "success": result.success,
    "message": result.message,
    "video_path": str(result.video_path) if result.video_path else None,
    "image_paths": [str(p) for p in result.image_paths],
    "music_path": str(result.music_path) if result.music_path else None,
}

# 发送结果
agent.send_output(
    agent_output_name='euterpe_result',
    agent_result=json.dumps(response)
)
```

## 4. 数据流交互

### 4.1 输入端点

从 terminal-input 节点接收 JSON 字符串：

```yaml
inputs:
  params: terminal-input/data
```

参数 `params` 接受序列化的 JSON 数据，包含所有视频生成所需的配置信息。

### 4.2 输出端点

将处理结果发送回 terminal-input 节点：

```yaml
outputs: euterpe_result
```

输出 `euterpe_result` 包含 JSON 格式的处理结果信息。

### 4.3 完整数据流

```
terminal-input --[JSON参数]--> euterpe-agent --[JSON结果]--> terminal-input
```

## 5. 关键技术点与实现细节

### 5.1 异常处理

采用全局 try-except 机制捕获所有可能的异常：

```python
try:
    # 处理逻辑...
except Exception as e:
    agent.logger.error(f"Error in Euterpe agent: {str(e)}")
    agent.send_output(
        agent_output_name='euterpe_result',
        agent_result=json.dumps({
            "success": False,
            "error": str(e)
        })
    )
```

### 5.2 环境变量处理

通过 `agent.yml` 配置文件声明所需的环境变量：

```yaml
options:
  use_environment_variables: true
  environment_variables:
    - KLING_API_KEY
    - BEATOVEN_API_KEY
    - DIFY_API_KEY
    - DIFY_API_BASE
    - DIFY_APP_ID
```

### 5.3 参数验证

对必需的参数进行验证，确保处理前数据完整：

```python
# Keyframes are required
if 'keyframes' not in params:
    agent.logger.error("No keyframes provided in parameters")
    agent.send_output(
        agent_output_name='euterpe_result',
        agent_result={"error": "No keyframes provided"}
    )
    return
```

### 5.4 枚举值处理

处理枚举类型参数，确保使用有效的值：

```python
# Determine aspect ratio
aspect_ratio = AspectRatio.LANDSCAPE
if 'aspect_ratio' in params:
    aspect_ratio_str = params['aspect_ratio']
    if aspect_ratio_str in [ar.value for ar in AspectRatio]:
        aspect_ratio = AspectRatio(aspect_ratio_str)
```

## 6. 与底层库的交互

### 6.1 euterpe-creator API 调用

Euterpe Agent 主要通过 `generate_video` 函数与 euterpe-creator 包交互：

```python
from euterpe import generate_video, VideoGenerationRequest, EuterpeConfig

# ...

result = generate_video(request, config)
```

这个函数封装了以下处理步骤：
1. 图像生成（通过 Kling API）
2. 音乐生成（通过 Beatoven API，如果配置了）
3. 视频插值和组装（通过 FFmpeg）
4. 音视频合成（通过 FFmpeg）

### 6.2 MoFA 框架交互

通过 `@run_agent` 装饰器和 `MofaAgent` 类与 MoFA 框架交互：

```python
from mofa.agent_build.base.base_agent import MofaAgent, run_agent

@run_agent
def run(agent: MofaAgent):
    # 处理逻辑...

def main():
    agent = MofaAgent(agent_name='euterpe-agent')
    run(agent=agent)
```

## 7. 性能考量

### 7.1 处理大型视频的优化

对于生成长时间视频，需要注意以下几点：

1. 内存使用：图像生成和视频处理可能会占用大量内存
2. 处理时间：每个关键帧的生成大约需要 5-10 秒
3. API 限制：第三方 API 可能有并发和速率限制

### 7.2 可能的优化方向

1. 增加异步处理：使用 `asyncio` 并行处理不同的关键帧
2. 实现缓存机制：缓存已生成的图像和音乐
3. 添加进度报告：实时报告处理进度
4. 支持断点续传：允许在失败时从中断点继续

```python
# 异步处理示例（伪代码）
async def generate_all_keyframes(keyframes, config):
    tasks = []
    for keyframe in keyframes:
        task = asyncio.create_task(generate_keyframe(keyframe, config))
        tasks.append(task)
    return await asyncio.gather(*tasks)
```

## 8. 测试策略

### 8.1 单元测试

为 Euterpe Agent 的各个组件编写单元测试，确保每个组件正常工作：

```python
# tests/test_parameter_parsing.py
def test_parse_keyframes():
    params = {
        "keyframes": [
            {"timestamp": 0.0, "prompt": "Test prompt"}
        ]
    }
    keyframes = parse_keyframes(params)
    assert len(keyframes) == 1
    assert keyframes[0].timestamp == 0.0
    assert keyframes[0].prompt == "Test prompt"
```

### 8.2 集成测试

测试 Euterpe Agent 与 MoFA 框架和 euterpe-creator 的集成：

```python
# tests/test_integration.py
def test_agent_workflow(mocker):
    # 模拟 MoFA 代理和参数
    mock_agent = mocker.MagicMock()
    mock_agent.receive_parameter.return_value = json.dumps({
        "keyframes": [{"timestamp": 0.0, "prompt": "Test"}]
    })
    
    # 模拟 euterpe-creator
    mocker.patch("euterpe.generate_video", return_value=mock_result)
    
    # 运行代理
    run(mock_agent)
    
    # 验证结果
    mock_agent.send_output.assert_called_once()
    called_args = mock_agent.send_output.call_args[1]
    assert called_args["agent_output_name"] == "euterpe_result"
    result = json.loads(called_args["agent_result"])
    assert result["success"] is True
```

### 8.3 端到端测试

使用 Dora 运行时执行实际的数据流测试：

1. 启动数据流
2. 发送测试用例 JSON
3. 验证输出结果和生成的文件

## 9. 扩展与定制

### 9.1 添加新功能

扩展 Euterpe Agent 以支持更多功能的模板：

```python
# 扩展参数解析以支持新功能
if 'new_feature' in params:
    new_feature_config = process_new_feature_params(params['new_feature'])
    # 处理新功能...
```

### 9.2 自定义处理流程

通过扩展 `run` 函数来定制处理流程：

```python
@run_agent
def run(agent: MofaAgent):
    # 原有流程...
    
    # 自定义前处理
    custom_preprocessing(params)
    
    # 调用 euterpe-creator
    result = generate_video(request, config)
    
    # 自定义后处理
    enhanced_result = custom_postprocessing(result)
    
    # 发送结果
    agent.send_output(
        agent_output_name='euterpe_result',
        agent_result=json.dumps(enhanced_result)
    )
```

## 10. 部署建议

### 10.1 资源要求

- **CPU**：建议 4核以上，多核可加速视频处理
- **内存**：至少 8GB，推荐 16GB 以上
- **存储**：SSD 存储加快文件读写
- **网络**：稳定的网络连接，用于访问外部 API

### 10.2 Docker 部署

提供 Dockerfile 示例，用于创建包含所有依赖的容器：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 安装 euterpe-creator 和 euterpe-agent
COPY . .
RUN pip install -e ./euterpe && pip install -e ./agent-hub/euterpe-agent

# 设置环境变量
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["dora", "start", "euterpe_dataflow.yml"]
```

## 11. 贡献指南

### 11.1 代码风格

- 遵循 PEP 8 代码规范
- 使用 Black 和 Ruff 进行代码格式化和检查
- 为所有函数和类添加文档字符串

### 11.2 提交流程

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 11.3 安全最佳实践

- 不在代码中硬编码 API 密钥
- 使用 `.env.secret` 文件存储敏感数据
- 确保 `.env.secret` 在 `.gitignore` 中
- 定期更新依赖以修复安全漏洞
