# Euterpe Agent 使用文档

## 概述

Euterpe Agent 是一个基于 MoFA 框架的组件，它将 euterpe-creator 包集成到 MoFA 数据流中，实现通过简单的 JSON 参数传递就能生成 AI 关键帧视频。该 agent 封装了 euterpe-creator 的复杂性，让用户能够以简单的方式创建高质量的视频内容，并与其他 MoFA 组件无缝集成。

## 架构图

```
+-----------------+      +-------------------+      +-------------------+
| 终端输入        |----->| Euterpe Agent     |----->| 视频输出          |
| (JSON 参数)     |      | (视频生成处理)    |      | (路径和状态信息)  |
+-----------------+      +-------------------+      +-------------------+
                                   |
                                   v
                          +-------------------+
                          | 文件系统          |
                          | (保存视频、图像)  |
                          +-------------------+
```

## 安装说明

### 前提条件

- Python 3.8+
- 安装了 MoFA 框架
- 安装了 Dora 运行时

### 安装步骤

1. 安装 euterpe-creator 包（如果尚未安装）：

```powershell
cd c:\Users\nbdhc\PycharmProject\2025\mofa\euterpe
uv pip install -e .
```

2. 安装 Euterpe Agent：

```powershell
cd c:\Users\nbdhc\PycharmProject\2025\mofa\python\agent-hub\euterpe-agent
uv pip install -e .
```

### 配置环境变量

创建 `.env.secret` 文件并添加以下环境变量：

```plaintext
# 必需的 API 密钥
KLING_API_KEY=your_kling_api_key
BEATOVEN_API_KEY=your_beatoven_api_key

# 可选的 Dify 相关配置（如果使用 Dify 增强功能）
DIFY_API_KEY=your_dify_api_key
DIFY_API_BASE=your_dify_base_url
DIFY_APP_ID=your_dify_app_id
```

## 基本使用

### 启动数据流

```powershell
cd c:\Users\nbdhc\PycharmProject\2025\mofa\python\agent-hub\euterpe-agent
dora up
dora build euterpe_dataflow.yml
dora start euterpe_dataflow.yml
```

### 发送请求

打开一个新的终端窗口，运行 terminal-input 并输入 JSON 参数：

```powershell
terminal-input
```

然后粘贴类似下面的 JSON 参数：

```json
{
  "keyframes": [
    {
      "frame_id": "frame1",
      "timestamp": 0.0,
      "prompt": "A beautiful beach at sunrise, golden light, waves gently touching the shore"
    },
    {
      "frame_id": "frame2",
      "timestamp": 5.0,
      "prompt": "Beach at midday, bright blue sky, clear water, white sand"
    },
    {
      "frame_id": "frame3",
      "timestamp": 10.0,
      "prompt": "Beach at sunset, dramatic colors, red and orange sky"
    }
  ],
  "music": {
    "prompt": "Relaxing calm ocean sounds with soft piano melody",
    "duration": 15.0
  },
  "output_dir": "./euterpe_output",
  "aspect_ratio": "16:9",
  "image_model": "kling-v1-5",
  "fps": 30,
  "resolution": 720
}
```

## 参数详解

### 输入参数

Euterpe Agent 接受一个名为 `params` 的 JSON 格式参数，包含以下字段：

#### 1. 必需字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `keyframes` | 数组 | 包含视频关键帧信息的数组 |

#### 2. 可选字段

| 字段名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `music` | 对象 | 无 | 音乐生成相关参数 |
| `output_dir` | 字符串 | `./euterpe_output` | 输出文件夹路径 |
| `aspect_ratio` | 字符串 | `16:9` | 视频宽高比，可选：`1:1`, `9:16`, `16:9`, `21:9`, `2.39:1` |
| `image_model` | 字符串 | `kling-v1-5` | 图像生成模型，可选：`kling-v1`, `kling-v1-5`, `kling-v2` |
| `use_dify` | 布尔值 | `false` | 是否使用 Dify 增强提示 |
| `dify` | 对象 | 无 | Dify 增强相关配置 |
| `fps` | 整数 | 30 | 视频帧率 |
| `resolution` | 整数 | 720 | 视频分辨率 |

#### 3. keyframes 数组中的对象结构

每个关键帧对象包含以下字段：

| 字段名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| `frame_id` | 字符串 | 否 | 关键帧 ID，用于标识 |
| `timestamp` | 浮点数 | 是 | 关键帧时间点（秒） |
| `prompt` | 字符串 | 是 | 图像生成提示词 |
| `negative_prompt` | 字符串 | 否 | 负面提示词，用于排除不需要的元素 |
| `image_path` | 字符串 | 否 | 预先存在的图像路径，如果提供则跳过图像生成 |

#### 4. music 对象结构

音乐参数对象包含以下字段：

| 字段名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| `prompt` | 字符串 | 是 | 音乐生成提示词 |
| `duration` | 浮点数 | 否 | 音乐时长（秒），默认为 180.0 |
| `genre` | 字符串 | 否 | 音乐风格/流派 |
| `tempo` | 整数 | 否 | 音乐节奏（BPM） |
| `format` | 字符串 | 否 | 音频格式，默认为 `mp3` |

#### 5. dify 对象结构

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `api_key` | 字符串 | Dify API 密钥 |
| `api_base_url` | 字符串 | Dify API 基础 URL |
| `application_id` | 字符串 | Dify 应用 ID |

### 输出参数

Euterpe Agent 返回一个名为 `euterpe_result` 的 JSON 字符串，包含以下字段：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `success` | 布尔值 | 是否成功生成视频 |
| `message` | 字符串 | 处理结果消息或错误信息 |
| `video_path` | 字符串 | 生成的视频文件路径 |
| `image_paths` | 数组 | 生成的关键帧图像路径数组 |
| `music_path` | 字符串 | 生成的音乐文件路径 |
| `error` | 字符串 | 如果出现错误，则提供错误详情 |

## 高级使用场景

### 1. 与其他 Agent 集成

Euterpe Agent 可以轻松与其他 MoFA 代理组合使用，例如：

- 结合 LLM Agent 自动生成关键帧描述和音乐提示
- 结合 Text-to-Speech Agent 为视频添加旁白
- 结合 Video Analysis Agent 对生成的视频进行内容分析

示例数据流配置：

```yaml
nodes:
  - id: terminal-input
    build: pip install -e ../../node-hub/terminal-input
    path: dynamic
    outputs: data
    inputs:
      agent_response: llm-agent/llm_result

  - id: llm-agent
    build: pip install -e ../../agent-hub/llm-agent
    path: llm-agent
    outputs: llm_result
    inputs:
      query: terminal-input/data
    
  - id: euterpe-agent
    build: pip install -e ../../agent-hub/euterpe-agent
    path: euterpe-agent
    outputs: euterpe_result
    inputs:
      params: llm-agent/llm_result
    env:
      IS_DATAFLOW_END: true
      WRITE_LOG: true
```

### 2. 批量处理多个视频

通过传递包含多组参数的 JSON 数组，可以实现批量处理：

```json
[
  {
    "keyframes": [...],
    "music": {...},
    "output_dir": "./euterpe_output/video1"
  },
  {
    "keyframes": [...],
    "music": {...},
    "output_dir": "./euterpe_output/video2"
  }
]
```

### 3. 使用自定义图像

如果您已经有现成的图像想用作关键帧，可以通过 `image_path` 参数指定：

```json
{
  "keyframes": [
    {
      "timestamp": 0.0,
      "image_path": "./my_images/frame1.jpg"
    },
    {
      "timestamp": 5.0,
      "prompt": "A futuristic city with flying cars"
    }
  ]
}
```

## 故障排除

### 常见错误及解决方案

| 错误信息 | 可能原因 | 解决方案 |
|---------|---------|---------|
| `No keyframes provided` | 输入 JSON 中没有包含 keyframes 数组或为空 | 确保提供至少一个关键帧描述 |
| `Invalid JSON parameters` | 输入的参数不是有效的 JSON 格式 | 检查 JSON 语法，确保没有缺少逗号、引号等 |
| `Error in Euterpe agent: No module named 'euterpe'` | euterpe-creator 包未安装或未正确安装 | 确保已安装 euterpe-creator 包 |
| `API key not found` | 未设置必要的 API 密钥环境变量 | 在 .env.secret 文件中设置必要的 API 密钥 |

### 日志查看

Euterpe Agent 的日志存储在以下位置：

```
c:\Users\nbdhc\PycharmProject\2025\mofa\python\logs\log_euterpe-agent.txt
```

可通过检查日志文件获取详细的错误信息和处理过程。

## 性能优化建议

1. **减少关键帧数量**：每个关键帧需要单独生成图像，减少关键帧数量可加快处理速度
2. **使用更低的分辨率**：对于原型设计和测试，可使用较低的分辨率（如 480p）
3. **预生成图像**：如果有多个视频共享相同的场景，可以预先生成图像并通过 `image_path` 复用
4. **优化音乐生成**：如不需要自定义音乐，可以使用预先生成的音频文件

## 示例场景

### 1. 产品演示视频

```json
{
  "keyframes": [
    {
      "timestamp": 0.0,
      "prompt": "A sleek modern smartphone on a white background, professional product photography"
    },
    {
      "timestamp": 3.0,
      "prompt": "Close up of smartphone screen showing a colorful app interface"
    },
    {
      "timestamp": 6.0,
      "prompt": "Person holding smartphone, using the app with one hand"
    }
  ],
  "music": {
    "prompt": "Upbeat corporate technology music, professional and modern",
    "duration": 10.0
  },
  "aspect_ratio": "16:9",
  "resolution": 1080
}
```

### 2. 风景旅行视频

```json
{
  "keyframes": [
    {
      "timestamp": 0.0,
      "prompt": "Aerial view of mountains with snow caps and green valleys, cinematic"
    },
    {
      "timestamp": 5.0,
      "prompt": "Mountain lake with crystal clear water reflecting the surroundings, wide angle"
    },
    {
      "timestamp": 10.0,
      "prompt": "Forest path with sunlight streaming through trees, atmospheric"
    },
    {
      "timestamp": 15.0,
      "prompt": "Sunset over mountain range, orange and purple sky, cinematic wide shot"
    }
  ],
  "music": {
    "prompt": "Inspiring orchestral music with piano and soft strings, emotional journey",
    "duration": 20.0
  },
  "aspect_ratio": "21:9",
  "resolution": 1080,
  "fps": 30
}
```

### 3. 抽象艺术视频

```json
{
  "keyframes": [
    {
      "timestamp": 0.0,
      "prompt": "Abstract fluid art, vibrant blue and purple colors swirling together",
      "negative_prompt": "realistic, photographic, human, face"
    },
    {
      "timestamp": 4.0,
      "prompt": "Abstract geometric patterns, bold red and yellow shapes on black background",
      "negative_prompt": "realistic, photographic, human, face"
    },
    {
      "timestamp": 8.0,
      "prompt": "Abstract digital art with fractal patterns, green and gold colors",
      "negative_prompt": "realistic, photographic, human, face"
    }
  ],
  "music": {
    "prompt": "Ambient electronic music with subtle beats, experimental and abstract",
    "duration": 12.0,
    "tempo": 90
  },
  "aspect_ratio": "1:1",
  "image_model": "kling-v2"
}
```

## 技术原理简介

Euterpe Agent 基于以下技术栈构建：

1. **MoFA 框架**：提供 agent 架构和数据流管理
2. **euterpe-creator**：核心视频生成库，处理图像生成、音乐生成和视频组装
3. **Kling API**：用于图像生成的 AI 服务
4. **Beatoven API**：用于音乐生成的 AI 服务
5. **Dify**（可选）：用于增强提示词的 AI 服务

生成流程如下：

1. 接收 JSON 参数并解析
2. 根据关键帧描述生成图像
3. 根据音乐描述生成音频（如果提供）
4. 将图像插值合成为视频
5. 将音频与视频合成
6. 返回生成的文件路径和状态信息

## 后续开发计划

1. **实时进度反馈**：添加进度报告功能，实时更新处理状态
2. **Web 界面**：开发一个简单的 Web UI 用于参数配置和预览
3. **模型扩展**：支持更多的图像和音乐生成模型
4. **批处理优化**：优化批量处理性能
5. **视频编辑功能**：添加简单的视频编辑功能，如添加文字、叠加效果等

## 许可证

Euterpe Agent 使用 MIT 许可证发布。

## 联系方式

如有问题或建议，请联系项目维护者。
