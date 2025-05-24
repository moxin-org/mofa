# Music AI Agent

Music AI Agent是一个基于MoFA框架的音乐生成代理，它使用Beatoven.ai API来根据文本提示生成音乐。

## 一、项目结构

```
music_ai/
├── README.md          # 项目说明文档
├── pyproject.toml     # Python包依赖配置
├── euterpe/           # Euterpe库 - 音乐和视频生成核心库
│   ├── src/           # 源代码目录
│   │   └── music_generator.py  # 音乐生成模块
│   ├── tests/         # 测试目录
│   ├── examples/      # 示例代码
│   └── build/         # 构建输出目录
├── music_ai/          # 主代码目录
│   └── main.py        # 代理主要实现代码
└── tests/             # 测试目录
    └── test_main.py   # 功能测试代码
```

## 二、功能特点

- 根据文本提示生成背景音乐
- 支持自定义音乐时长、格式和输出路径
- 集成了Beatoven.ai API进行高质量音乐生成
- 作为MoFA代理运行，可以与其他代理协作
- 支持通过环境变量文件(.env)配置参数

## 三、使用方法

## 3.1 环境变量配置

创建一个.env文件，包含以下配置项：

```
BEATOVEN_API_KEY=your_api_key_here
BEATOVEN_API_URL=https://api.beatoven.ai/v2
MUSIC-PROMOT=你的音乐生成提示文本
MUSIC_OUTPUT=输出音乐文件的路径
MUSIC_GENRE=音乐风格（可选）
MUSIC_TEMPO=音乐节奏（可选）
BEATOVEN_DEFAULT_DURATION=180.0
BEATOVEN_DEFAULT_FORMAT=mp3
BEATOVEN_REQUEST_TIMEOUT=30
BEATOVEN_DOWNLOAD_TIMEOUT=60
BEATOVEN_POLLING_INTERVAL=5
ASPECT_RATIO=LANDSCAPE
```

### 3.2 作为MoFA代理运行

**3.2.1 在agent-hub/music_ai目录下新建终端输入**

```bash
dora up
dora build music_ai.yml
dora start music_ai.yml
```

**3.2.2 另起一个终端输入**

```
terminal-input
输入.env.music文件的绝对地址
```

### 四、API集成

代理接收参数格式为.env文件的路径，返回JSON格式的结果，包含：

- success: 处理是否成功
- music_params: 生成音乐使用的参数
- aspect_ratio: 视频比例设置
- music_output_path: 生成的音乐文件路径
- message: 处理结果消息

## 五、开发说明

该项目使用Euterpe作为核心库，Euterpe集成了图像和音乐生成功能，可以生成视频内容。该代理主要使用Euterpe的音乐生成功能。

## 六、许可证

MIT License
