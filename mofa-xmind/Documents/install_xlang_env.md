# 在不同的系统下安装xlang + xMind环境

本指南将引导您下载并编译 **xMind** 项目，适用于不同操作系统（macOS、Ubuntu 和 Windows）。请按照以下步骤操作，以确保顺利完成安装和编译过程。

## 目录

1. [下载项目](#1-下载项目)
2. [安装必要的依赖](#2-安装必要的依赖)
   - [macOS 系统](#macos-系统)
   - [Ubuntu 系统](#ubuntu-系统)
   - [Windows 系统](#windows-系统)
3. [编译项目](#3-编译项目)
   - [macOS 和 Ubuntu 系统](#macos-和-ubuntu-系统)
   - [Windows 系统](#windows-系统)
4. [停止当前服务](#4-停止当前服务)
   - [macOS 和 Ubuntu](#macos-和-ubuntu)
   - [Windows](#windows)
5. [相关网址](#5-相关网址)
6. [Q&A](#6-qa)

---

## 1. 下载项目

首先，克隆 **xMind** 仓库及其依赖项目 **mofa** 和 **xlang**：

```bash
# 创建项目目录
mkdir -p /project && cd /project

# 返回项目根目录并克隆 xMind 仓库
cd /project
git clone https://github.com/xlang-foundation/xMind.git
cd xMind/ThirdParty

# 克隆 xlang 仓库
git clone https://github.com/xlang-foundation/xlang.git
cd xlang
git checkout Jit

# 返回 xMind 根目录并创建构建目录
cd /project/xMind
mkdir -p out
```

---

## 2. 安装必要的依赖

根据您的操作系统，按照以下步骤安装编译 **xMind** 所需的依赖。

### macOS 系统

1. **安装 Homebrew（如果尚未安装）**

   Homebrew 是 macOS 上的包管理器，可以通过以下命令安装：

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **安装必要的依赖**

   ```bash
   brew install ossp-uuid
   brew install openssl
   brew install jpeg-turbo  # 可选，用于图像模块
   brew install python3      # 可选，用于 Python 库集成
   pip3 install numpy
   ```

### Ubuntu 系统

1. **更新包列表并安装必要的依赖**

   ```bash
   sudo apt update
   sudo apt install -y git build-essential cmake uuid-dev libssl-dev python3-dev make python3-pip
   sudo apt install -y libcurl4-openssl-dev  # 安装 curl-devel 对应的包
   pip3 install numpy
   ```

### Windows 系统

1. **安装 Python**
   - 下载并安装 Python：[Python 下载](https://www.python.org/downloads/)
   - 确保在安装过程中勾选 **"Add Python to PATH"**，以便在命令提示符中直接访问 `python`。

2. **安装 CMake**
   - 下载并安装 CMake：[CMake 下载](https://cmake.org/download/)

3. **安装 Visual Studio**
   - 下载并安装 Visual Studio：[Visual Studio 下载](https://visualstudio.microsoft.com/zh-hans/downloads/)
   - 在安装过程中选择 **"自定义安装"**，确保选择 **"C++ 桌面开发"** 工作负载。

4. **配置 Python 环境（如果遇到 Python 启动问题，请参考以下 Q&A）**

---

## 3. 编译项目

根据您的操作系统，按照以下步骤编译 **xMind** 项目。

### macOS 和 Ubuntu 系统

1. **导航到构建目录并编译项目**

   ```bash
   cd /project/xMind/out
   cmake .. -DOPENSSL_ROOT_DIR=$(brew --prefix openssl)  # macOS 使用 Homebrew 安装的 OpenSSL 路径
   make -j$(nproc)
   ```

   > **注意**：在 Ubuntu 上，CMake 通常能自动找到 OpenSSL。如果有问题，可以手动指定 OpenSSL 路径：

   ```bash
   cmake .. -DOPENSSL_ROOT_DIR=/usr/lib/ssl
   ```

### Windows 系统

1. **打开 Visual Studio 并配置项目**

   - 使用 Visual Studio 打开 **xMind** 目录。
   - 点击 **"xMind.exe"**。
   - 选择 **"生成"** -> **"重新生成"**。

   > **提示**：确保在 Visual Studio 中选择正确的解决方案配置（如 Release 或 Debug）。
![vscode_build.png](attachment/vscode_build.png)
---

## 4. 停止当前服务

在进行编译或运行项目之前，可能需要停止当前正在运行的服务。

### macOS 和 Ubuntu

1. **查看运行服务**

   ```bash
   lsof -i :9902
   ```

2. **停止服务**

   根据上一步输出的 PID（进程ID），执行以下命令：

   ```bash
   kill -9 <PID>
   ```

### Windows

- 直接关闭服务器服务窗口即可，或在任务管理器中结束相关进程。

---

## 5. 相关网址

- **模型网址**: [SiliconFlow](https://cloud.siliconflow.cn/)
- **项目网址**: [xlang-foundation GitHub](https://github.com/xlang-foundation)

---

## 6. Q&A

### 在 Windows 下正常添加 Python 到编译环境中

安装 **xlang** 时，如果在 Windows 上尝试使用 `python` 命令时，系统跳转到 Microsoft Store 或其他页面，请按照以下步骤修改设置：

1. **打开系统设置**

   - 按下 `Win + I` 键打开 **设置**。

2. **导航到应用执行别名**

   - 点击 **"应用"**。
   - 在 **"应用"** 页面中，选择 **"应用和功能"**。
   - 滚动并点击 **"更多设置"** -> **"应用执行别名"**。

3. **关闭 Python 应用别名**

   - 在 **"应用执行别名"** 页面，找到带有 `Python` 的条目。
   - 将这些条目的开关关闭，以确保 `python` 命令指向正确的 Python 安装路径。

   ![关闭 Python 应用别名](https://i.imgur.com/your-image-link.png)  <!-- 替换为实际图片链接 -->

4. **验证 Python 命令**

   - 打开命令提示符 (`cmd`) 或 PowerShell，输入以下命令：

     ```bash
     python --version
     ```

   - 应该显示已安装的 Python 版本，而不会跳转到 Microsoft Store。

---

## 更新后的步骤总结

为了确保顺利下载和编译 **xMind** 项目，请按照以下顺序操作：

1. **下载项目**：克隆 **mofa** 和 **xMind** 仓库，并安装 Python 依赖。
2. **安装依赖**：根据您的操作系统，安装必要的构建工具和库。
3. **编译项目**：导航到构建目录，使用 CMake 和 make（或 Visual Studio）编译项目。
4. **停止服务**：在编译前确保相关服务已停止，避免端口冲突。
5. **参考相关网址**：获取更多资源和支持。
6. **解决常见问题**：按照 Q&A 部分的指导，解决在 Windows 上遇到的 Python 环境问题。

---

如果在执行上述步骤时遇到任何问题，请参阅 [xlang-foundation GitHub](https://github.com/xlang-foundation) 或 [SiliconFlow](https://cloud.siliconflow.cn/) 获取更多帮助和支持。