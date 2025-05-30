# kling-agent-image

MoFA框架中的AI图像生成智能体，使用Kling AI API根据关键帧描述生成高质量图像。

## 功能特性

- 基于Kling AI的图像生成
- 支持关键帧描述到图像的转换
- 可配置的图像参数（尺寸比例、负面提示等）
- 自动图像保存和管理
- 与MoFA数据流无缝集成

## 安装

使用相对路径安装：

```bash
cd python/agent-hub/kling-agent-image
pip install -e .
```

## 基本使用

### 环境配置

配置以下环境变量：

```bash
# Kling API配置
ACCESSKEY_API=your_access_key
ACCESSKEY_SECRET=your_access_secret
KLING_API_BASE_URL=https://api.klingai.com
KLING_TOKEN_EXPIRATION=1800
KLING_API_TIMEOUT=60
KLING_API_MAX_RETRIES=3
```

### 数据流集成

在MoFA数据流配置中使用：

```yaml
nodes:
  - id: kling-agent-image
    build: pip install -e ../../agent-hub/kling-agent-image
    path: kling-agent-image
    outputs:
      - kling_result
    inputs:
      query: keyframe-agent/keyframe_result
    env:
      WRITE_LOG: true
```

### 使用示例

该agent接收关键帧描述并生成对应的图像：

```python
# 输入：关键帧描述文件
# 输出：生成的图像文件路径
```

## API参考

### 输入
- `query`: 关键帧描述结果路径

### 输出
- `kling_result`: 生成的图像文件路径

### 环境变量
- `ACCESSKEY_API`: Kling API访问密钥
- `ACCESSKEY_SECRET`: Kling API密钥
- `KLING_API_BASE_URL`: Kling API基础URL
- `KLING_TOKEN_EXPIRATION`: Token过期时间（秒）
- `KLING_API_TIMEOUT`: API请求超时时间（秒）
- `KLING_API_MAX_RETRIES`: 最大重试次数

## 项目结构

```
kling-agent-image/
├── README.md              # 项目文档
├── pyproject.toml         # Python包配置
├── agent/
│   ├── main.py            # 主要代码
│   └── klingimage/        # Kling图像API模块
│       ├── api.py         # API客户端
│       └── utils.py       # 工具函数
└── tests/
    └── test_main.py       # 测试代码
```

## 开发

运行测试：
```bash
python -m pytest tests/
```

## 许可证

MIT License
