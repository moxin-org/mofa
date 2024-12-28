# 如何在比赛中使用 GitCode-NoteBook 运行案例和提交代码

本指南旨在帮助参赛者，特别是新手，了解如何在比赛中使用 GitCode-NoteBook 环境运行案例代码并提交项目.

## 目录

1. [MoFA GitCode 容器](#1-mofa-gitcode-容器)
2. [注册 SiliconFlow](#2-注册-siliconflow)
3. [创建 NoteBook 环境](#3-创建-notebook-环境)
    - [3.1 登录 GitCode 并创建 NoteBook 环境](#31-登录-gitcode并创建-notebook-环境)
4. [比赛代码的创建和运行](#4-比赛代码的创建和运行)
    - [4.1 克隆项目代码](#41-克隆项目代码)
    - [4.2 更新代码环境](#42-更新代码环境)
    - [4.3 运行示例代码](#43-运行示例代码)
5. [创建和提交代码](#5-创建和提交代码)
    - [5.1 配置 Git 访问令牌和用户信息](#51-配置-git-访问令牌和用户信息)
    - [5.2 创建案例](#52-创建案例)
    - [5.3 确保提交案例的结构](#53-确保提交案例的结构)
    - [5.4 提交代码](#54-提交代码)
        - [5.4.1 提交代码到远程仓库](#541-提交代码到远程仓库)
        - [5.4.2 提交 Pull Request（PR）](#542-提交-pull-requestpr)
    - [5.5 提交案例流程总结](#55-提交案例流程总结)
6. [常见问题及解决方法](#6-常见问题及解决方法)
7. [附录](#7-附录)

---

## 1. MoFA GitCode 容器

选择使用 **MoFA 框架** 的参赛选手，可以使用 GitCode 提供的容器进行编程。

为方便参赛者进行项目开发，在比赛前（**10 月 12 日**），您可以登录 GitCode，从用户中心进入“我的 Notebook”申请容器。您可以根据自身需求自定义容器配置，镜像版本为 **GOSIMxxx**。我们的技术支持团队将竭诚为您服务，您可以在选手群中咨询容器申请的相关问题，技术支持人员会及时解答。

为便于交流，我们特设了组委会专用微信号（**代码君**），该微信号将汇集所有参赛选手和支持人员。在群里，您可以发布共性问题，组委会会统一解答；如有个性化问题，我们将会在微信中拉您和相关支持人员组成小群进行一对一解答。

请注意，GitCode 容器将于 **10 月 17 日晚上 9 点** 统一关闭，请合理安排您的使用时间，以确保项目的顺利进行。

比赛项目地址：[https://gitcode.com/moxin-org/mofa](https://gitcode.com/moxin-org/mofa)

---

## 2. 注册 SiliconFlow

请前往 [SiliconFlow 注册页面](../siliconflow_llms.md) 注册账户，以获取 LLM 密钥。

---

## 3. 创建 NoteBook 环境

### 3.1 登录 GitCode 并创建 NoteBook 环境

1. **登录 GitCode**：

    - 打开浏览器，访问 [GitCode 官网](https://gitcode.com/)。
    - 点击页面右上角的 **头像**，然后选择 **NoteBook**。

    ![登录 GitCode](attachment/gitcode-login.png)

2. **创建 NoteBook 环境**：

    - 在 NoteBook 页面，点击 **创建** 按钮。
    - 根据组委会提供的 **镜像名称** 和 **版本号**，选择合适的开发环境。默认请选择 `gosim_py310_self_notebook` 作为镜像环境，计算类型为 `CPU`。
    - 配置所需的 **硬件资源**（如 CPU 核数、内存大小）：请选择 `16核心/32GB内存` 进行开发。
    - 点击 **创建**，等待环境初始化完成。

    ![创建 NoteBook 环境](attachment/create_notebook.png)

3. **进入 NoteBook 环境**：

    - 创建完成后，您将在 NoteBook 环境列表中看到新创建的环境。
    - 点击相应的 NoteBook，进入工作界面。

    ![进入 Jupyter Notebook](attachment/jupyter_notebook.png)

---

## 4. 比赛代码的创建和运行

### 4.1 克隆项目代码

1. **Fork 比赛项目**：

    - 登录 GitCode，访问比赛官方的项目仓库：[https://gitcode.com/moxin-org/mofa](https://gitcode.com/moxin-org/mofa)。
    - 点击 **Fork** 按钮，将官方仓库复制到您的个人或团队仓库中。

    ![Fork 项目](attachment/fork_project.png)

2. **克隆仓库到本地环境**：

    - 在您 Fork 的仓库页面，点击 **Clone** 按钮。
    - 在弹出的窗口中，选择 `HTTPS` 选项，复制 **克隆到本地** 的 URL。例如：

    ```bash
    git clone https://gitcode.com/您的用户名/mofa.git
    ```

    - 在 NoteBook 的终端中，运行上述命令。运行成功后，当前目录下会创建一个名为 `mofa` 的文件夹。

### 4.2 更新代码环境

1. **进入项目目录**：

    ```bash
    cd mofa/python
    ```

2. **更新依赖包**：

    ```bash
    pip3 install -e .
    ```

    > **说明**：该命令会根据 `setup.py` 文件安装项目的依赖包。

### 4.3 运行示例代码

1. **运行示例**：

    - 在`mofa/python/examples`项目目录下，有一些示例代码供参考。您可以尝试运行这些示例，确保环境配置正确。

2. **验证环境**：

    - 确认示例代码运行无误，表示环境已正确配置，可以开始进行开发。

---

## 5. 创建和提交代码

### 5.1 配置 Git 访问令牌和用户信息

1. **创建访问令牌**：

    - 在 GitCode 右上角，点击 **头像**，选择 **个人设置**。
    - 进入 **安全设置**，找到 **访问令牌** 选项，点击 **新建访问令牌**。
    - 设置令牌的描述（例如：“比赛提交令牌”）和到期时间，然后点击 **创建访问令牌**。
    - **复制生成的访问令牌**，并妥善保存，稍后提交代码时需要使用。

2. **配置 Git 用户信息**：

    ```bash
    git config --global user.name "您的姓名"
    git config --global user.email "您的邮箱地址"
    ```

    > **提示**：确保用户名和邮箱与您的 GitCode 账户信息一致。

### 5.2 创建案例

1. **创建案例目录**：

    ```bash
    cd mofa/Hackathon/projects
    mkdir 您的团队名称
    cd 您的团队名称
    ```

2. **编写代码**：

    - 在您的团队目录下，编写或修改代码，确保代码结构清晰。

3. **完善 README.md 文件**：

    ```bash
    vim README.md
    ```

    - 简要说明您的案例内容和功能。

### 5.3 确保提交案例的结构

1. **案例结构要求**：

    - 提交的案例结构应与 `examples` 目录下的原有案例结构一致，包含以下内容：

        - `configs/*.yml`：配置文件，定义配置的结构。
        - `scripts/*.py`：包含 `dora-node` 和操作符的脚本文件。
        - `案例名称_dataflow.yml`：`dora-dataflow` 的文件。
        - `README.md`：说明案例内容及逻辑。
        - `案例_dataflow-graph.html`：使用 Dora Graph 生成的 dataflow 展示结构。
        - `README_en.md`：案例流程说明的英文版本。
        - `agent_response.json`：用于保存您的 agent 的任务和结果，内容结构为：

            ```json
            {
                "task": "你的名称是什么？",
                "agent_response": "我的名字是xxx"
            }
            ```

    - **提交注意事项**：

        - 您的 API 密钥在`git push `之前必须删除。请您详细检查上传的文件中不包含任何密钥信息，例如：
        - 由 `dora/python/log` 生成的临时文件。
        - 您不能修改任何非examples 目录之外的源码.如果您觉得仓库中的代码存在问题，请联系组委会进行处理。如果您修改了非examples的代码,我们会拒绝合并您的pr.
        - 如果您的案例中安装了一些其他的包,请你将这些依赖包添加到`requirements.txt`.
        - 如果您的案例需要安装一些其他的依赖才能运行,请您在`README.md` 中进行说明,包括安装运行等流程
### 5.4 提交代码

#### 5.4.1 提交代码到远程仓库

1. **添加更改**：

    ```bash
    git add .
    ```

2. **提交更改并添加提交信息**：

    ```bash
    git commit -m "添加 [个人/团队名称] 的案例"
    ```

3. **设置远程仓库的 URL（包含访问令牌）**：

    ```bash
    git remote set-url origin https://您的用户名:您的访问令牌@gitcode.com/您的用户名/mofa.git
    ```

    > **示例**：

    ```bash
    git remote set-url origin https://johnDoe:abcdef123456@gitcode.com/johnDoe/mofa.git
    ```

4. **推送代码到远程仓库**：

    ```bash
    git push origin main
    ```

    > **注意**：

    - 将 `您的用户名`、`您的访问令牌` 和 `mofa` 替换为实际信息。
    - 如果默认分支不是 `main`，请使用相应的分支名称（例如 `master`）。

#### 5.4.2 提交 Pull Request（PR）

1. **提交 PR**：

    - 在您 Fork 的仓库页面，点击 **New Pull Request** 按钮。

2. **填写 PR 信息**：

    - 在 PR 描述中，详细说明您提交的内容，包括：

        - **提交的内容**：添加或修改了哪些文件和功能。
        - **逻辑说明**：代码实现的逻辑和工作方式。
        - **修改原因**：如果修改了现有代码，说明原因和解决的问题。

    - 确认无误后，点击 **Create Pull Request** 提交 PR。

    > **示例描述**：

    ```
    ### 提交内容
    - 添加了 `configs/sample_config.yml` 配置文件。
    - 编写了 `scripts/sample_script.py` 脚本，实现数据处理功能。

    ### 逻辑说明
    - `sample_script.py` 读取配置文件中的参数，处理输入数据并生成输出结果。

    ### 修改原因
    - 修正了原有脚本中的数据读取错误，确保数据处理的准确性。
    ```

    - 提交 PR 后，您的修改将被官方仓库审查，审核通过后会合并到主项目中。

### 5.5 提交案例流程总结

1. **确保案例结构正确**：

    - 在提交代码之前，确保您的案例符合要求的目录结构和文件规范。

2. **提交代码到远程仓库**：

    - 按照上述步骤，将代码提交并推送到您的 GitCode 仓库。

3. **提交 Pull Request（PR）**：

    - 在您 Fork 的仓库页面，点击 **New Pull Request** 按钮，提交您的修改。

---

## 6. 常见问题及解决方法

### 6.1 无法登录 GitCode

- **解决方法**：

    - 确认网络连接正常。
    - 检查用户名和密码是否正确。
    - 如果忘记密码，可以通过 **找回密码** 功能重置。

### 6.2 访问令牌丢失或泄露

- **解决方法**：

    - 如果访问令牌丢失，请重新创建新的访问令牌。
    - 确保令牌保存在安全的地方，避免泄露。

### 6.3 克隆仓库失败

- **解决方法**：

    - 确认仓库 URL 是否正确。
    - 检查是否配置了正确的访问令牌。
    - 确认网络连接正常。

### 6.4 提交代码遇到冲突

- **解决方法**：

    - 拉取最新的远程仓库代码：

    ```bash
    git pull origin main
    ```

    - 解决代码冲突后，重新提交代码。

### 6.5 更多问题

- **解决方法**：

    - 请参阅 [常见问题解答 (FAQ)](../frequently_asked_questions_(faq).md)。

---

## 7. 附录

- **Git 基础知识**：

    - 如果您对 Git 不熟悉，建议先学习一些基础知识，如 [Git 官方文档](https://git-scm.com/doc)。

- **GitCode 帮助中心**：

    - 更多关于 GitCode 的使用，可以参考 [GitCode 帮助中心](https://gitcode.net/help)。


