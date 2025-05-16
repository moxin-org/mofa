# Euterpe Agent for MoFA

> AI 视频生成代理 - 将 euterpe-creator 无缝集成到 MoFA 框架

这个代理将 euterpe-creator 包集成到 MoFA 框架中，使用户能够通过简单的 JSON 参数传递生成高质量的 AI 视频，包含关键帧插值和可选的 AI 生成音乐。

## 功能特点

- **参数化视频生成**：通过 JSON 参数控制视频生成的各个方面
- **关键帧到视频**：从文本提示生成关键帧图像，并智能插值为流畅视频
- **AI 音乐生成**：可选择生成匹配视频内容的背景音乐
- **灵活配置**：支持多种视频格式、分辨率和宽高比
- **MoFA 集成**：作为 MoFA 数据流的一部分使用
- **提示增强**：可选的 Dify AI 提示增强功能

## 快速开始

### 安装

```bash
# 安装 euterpe-creator 包（如果尚未安装）
cd c:\Users\nbdhc\PycharmProject\2025\mofa\euterpe
uv pip install -e .

# 安装 Euterpe Agent
cd c:\Users\nbdhc\PycharmProject\2025\mofa\python\agent-hub\euterpe-agent
uv pip install -e .
```

### 配置环境变量

创建 `.env.secret` 文件并添加以下环境变量：

```plaintext
# 必需的 API 密钥
KLING_API_KEY=your_kling_api_key
BEATOVEN_API_KEY=your_beatoven_api_key

# 可选的 Dify 相关配置
DIFY_API_KEY=your_dify_api_key
DIFY_API_BASE=your_dify_base_url
DIFY_APP_ID=your_dify_app_id
```

### 启动数据流

```bash
cd c:\Users\nbdhc\PycharmProject\2025\mofa\python\agent-hub\euterpe-agent
dora up
dora build euterpe_dataflow.yml
dora start euterpe_dataflow.yml
```

### 发送请求

打开一个新的终端窗口，运行 terminal-input 并输入 JSON 参数：

```bash
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
    }
  ],
  "music": {
    "prompt": "Relaxing calm ocean sounds with soft piano melody",
    "duration": 15.0
  },
  "output_dir": "./euterpe_output",
  "aspect_ratio": "16:9",
  "image_model": "kling-v1-5",
  "use_dify": false,
  "fps": 30,
  "resolution": 720
}
```

## 详细文档

- [完整使用文档](DOCUMENTATION.md) - 详细的安装、配置和使用说明
- [技术实现文档](TECHNICAL.md) - 技术设计和实现细节
- [使用示例集合](EXAMPLES.md) - 各种场景的详细示例

## 必要环境变量

- `KLING_API_KEY`: 用于 Kling 图像生成的 API 密钥
- `BEATOVEN_API_KEY`: 用于 Beatoven 音乐生成的 API 密钥（如果使用音乐功能）

## 可选环境变量（用于 Dify 增强功能）

- `DIFY_API_KEY`: Dify API 密钥
- `DIFY_API_BASE`: Dify API 基础 URL
- `DIFY_APP_ID`: Dify 应用 ID

## 项目状态

当前版本: 0.1.0

## 许可证

MIT License
