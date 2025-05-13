0.克隆代码
```powershell
git clone https://github.com/betasecond/euterpe --recursive
cd euterpe
```

1.安装环境 (使用uv)
```powershell
uv venv

# windows
.\.venv\Scripts\activate
# linux
source ./.venv/bin/activate

# 安装开发版本
uv pip install -e .

# 或安装带开发依赖的版本
uv pip install -e ".[dev]"
```

> **注意**: BeatovenDemo 和 KlingDemo 库已经作为内部模块集成到 euterpe 包中，不再需要单独安装。
> 查看 [LOCAL_LIBS_INTEGRATION.md](./LOCAL_LIBS_INTEGRATION.md) 了解更多详情。
2.进入目录
```powershell
cd ../../workflow

```
3.运行
```powershell
python ../main.py --keyframes-file ./keyframes.txt --model-name kling-v1-5 --env-file ./.env --beatoven-env-file ./.env.beatoven --use-dify --music-prompt "一个优美的钢琴旋律，带有轻微的弦乐伴奏，适合深思和冥想" --music-filename piano_meditation
```