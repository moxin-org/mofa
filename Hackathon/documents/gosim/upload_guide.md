CheckList：
- 写一个讲清楚你的项目的README：
    - 你和你的团队, GitCode Repo等信息
    - 项目简介
    - 安装和运行说明
    - 说明你的创新点、突破点
    - 描述项目的技术难点和你的解决方案
    - 给至少三个运行案例支持创新点和突破点，给少量的解释。
- 拍一段3到5分钟录屏，演示你的Readme里的三个运行案例（以及ChatGPT的对比结果，如果你想说明你的智能体比ChatGPT强的话）
- 你的Code
- 拍几张你团队的照片 
- 将你的项目打包提交

### 1. 确保提交案例的结构

1. **案例结构要求**：

    - 提交的案例结构应与 `examples` 目录下的原有案例结构一致，包含以下内容：

        - `configs/*.yml`：配置文件，定义配置的结构。
        - `scripts/*.py`：包含 `dora-node` 和操作符的脚本文件。
        - `案例名称_dataflow.yml`：`dora-dataflow` 的文件。
        - `README.md`：如何编辑自己的 `README.md` 文件。示例参考：[sample_readme](sample_readme.md)
        - `案例_dataflow-graph.html`：使用 Dora Graph 生成的 dataflow 展示结构。
        - `agent_response.json`：用于保存您的 agent 的任务和结果，内容结构为：
        - `data/input/*` ：用来保存这个`Dora-Dataflow`需要的输入数据
        - `data/output/agent_response.json`：用来保存这个`Dora-Dataflow`的输出数据.要求格式如下.其中task代表你至少要执行的任务，response代表你的agent的输出结果
            ```json
           [
            {
                "task": "你是谁?",
                "response": "Hello World"
            },
            {
                "task": "你的名字是什么?",
                "response": "Hello World"
            }
          ]
          ```
        - `data/info/[team.jpg｜personal.jpg]` ： 个人或者团队照片
        - `data/info/[team.md｜personal.md]` ： 个人或者团队成员说明
        - `data/info/ExplanatoryVideo.mp4` : 
            - **分辨率：**1080p 或 2K。
            - **文件大小：**最大限制 150MB。
            - **时长：**3-5 分钟。
            - **录制工具：**使用腾讯会议或 OBS 进行视频录制。
            - **内容要求：**
              - 根据你的README来进行演讲
              - 需要在视频中运行你的项目.必须完整的看到你的项目从依赖安装启动以及运行结束的流程
    
2. **提交注意事项**：
  - **不要上传您的 API 密钥**。在 `git push` 之前，请仔细检查上传的文件中不包含任何密钥信息。
  - **不要修改非 examples 目录之外的源码**。如果您发现仓库中的代码存在问题，请联系组委会进行处理。若您修改了非 examples 的代码，我们会拒绝合并您的 PR。
  - 如果您的案例需要安装其他的包，请将这些依赖包添加到 `requirements.txt` 中。
  - 如果您的案例需要特殊的安装或运行步骤，请在 `README.md` 中详细说明，包括安装和运行的流程。

3. **项目打包发送给组委会**：
  - 参赛选手务必将自己的项目进行打包并且发送给组委会
    ~~~
    sudo apt update
    sudo apt install zip
    cd /examples 
    zip -r you_project.zip you_project/
    用户自行添加 `gitcode君`微信号 然后私聊将文件发给他。并且标注团队名/个人名称
    ~~~
