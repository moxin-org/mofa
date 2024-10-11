
---

# 对象检测智能体

## 1. 功能说明

该对象检测智能体用于根据用户上传图片，进行对象检测，显示检测结果。

## 2. 使用场景

## 3. 配置方法
在 `object_detection_dataflow.yml`配置文件中, 请确保 `terminal-input` 指向正确的 MoFA `node-hub/terminal-input` 目录. 
```
- id: terminal-input
    build: pip install -e ../../../node-hub/terminal-input
    path: dynamic
    outputs:
      - data
    inputs:
```

## 4. 运行智能体

使用Dora-rs命令行运行

1. 安装MoFA项目包。
2. 执行以下命令以启动智能体流程：
   ```bash
   dora up && dora build object_detection_dataflow.yml && dora start object_detection_dataflow.yml --attach
   ```
3. 启动另一个终端，运行`terminal-input`，然后输入图片路径名即可启动流程。

