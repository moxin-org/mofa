# 在比赛中如何使用GitCode-NoteBook来运行案例和提交代码

## 1，创建NoteBook环境
### 1.1 登陆GitCode创建NoteBook环境
1. 登陆GitCode，点击右上角头像，选择NoteBook，点击创建，即可看到如下图所示的NoteBook环境，点击进入即可看到如下图所示的NoteBook环境。
![gitcode-login.png](attachment/gitcode-login.png)
2. 根据组委会给的镜像以及镜像版本，选择以及硬件资源，创建NoteBook环境。
![create_netobook.png](attachment/create_netobook.png)
3. 创建完成后进入页面，即可看到如下图所示的NoteBook环境。
![netobook.png](attachment/netobook.png)


## 2，比赛代码创建和运行
TODO: 待完善


## 3，创建和提交代码 
1. Fork 项目，创建仓库到队长或个人的仓库
![img.png](img.png)
2. 在NetoBook中将仓库clone到本地
1. 在GitCode的右上角点击头像 -> 个人设置 -> 安全设置 -> 访问令牌 -> 点击 "新建访问令牌". 请你设置你的到期时间，并复制token，保存好，后面需要用到。
2. 设置你的Git的'name'以及'email'. 如果你不清楚你的账号名字以及邮箱，请点击 右上角点击头像 -> [用户资料,电子邮箱],即可看到自己的账号名字以及邮箱。
~~~
git config user.name "name"
git config user.email  "email"
~~~
3. 创建案例
将你写的代码提交到 entries/[个人/团队名称]下,然后写好你的 `README.md`和 git commit 的提交信息
4. 提交案例
~~~
cd entries
git add . 
git commit -m "提交案例"
https://username:token@gitcode.com/chenzi00103/test-mofatest-mofa.git

https://chenzi00103:@gitcode.com/chenzi00103/test-mofatest-mofa.git
~~~


以下是优化后的文档，目的是让读者更清晰、流畅地了解如何在比赛中使用 GitCode-NoteBook 运行案例和提交代码。

---

# 在比赛中如何使用 GitCode-NoteBook 运行案例和提交代码

## 1. 创建 NoteBook 环境

### 1.1 登录 GitCode 并创建 NoteBook 环境

1. **登录 GitCode**：进入 [GitCode 官网](https://gitcode.net/)，点击右上角的头像，选择 **NoteBook**。
   
2. **创建 NoteBook 环境**：
   - 点击 **创建** 按钮，选择组委会提供的镜像及版本号，根据比赛需求配置硬件资源。
   - 创建成功后，将看到如下图所示的 NoteBook 环境界面。点击进入即可。
   
   ![gitcode-login.png](attachment/gitcode-login.png)

3. **配置 NoteBook 环境**：
   - 根据组委会提供的指导，设置开发环境的镜像和资源配置，如 CPU 和内存大小。
   
   ![create_netobook.png](attachment/create_netobook.png)

4. **进入 NoteBook 环境**：
   - 创建完成后，进入 NoteBook 界面，查看如下所示的工作环境。
   
   ![netobook.png](attachment/netobook.png)

## 2. 比赛代码创建和运行

**TODO: 待完善** 

该部分将涵盖如何在 NoteBook 中创建和运行比赛代码的详细步骤。

## 3. 创建和提交代码

### 3.1 Fork 项目并创建仓库

1. **Fork 项目**：
   - 登录 GitCode，找到比赛项目，点击 **Fork**，将项目复制到个人或队长的仓库中。

   ![img.png](img.png)

2. **克隆仓库到 NoteBook 本地**：
   - 进入 NoteBook 环境，打开终端，将 Fork 后的仓库克隆到本地：
   
   ```bash
   git clone https://gitcode.com/username/project.git
   ```

### 3.2 配置 Git 访问令牌和用户信息

1. **创建访问令牌**：
   - 在 GitCode 的右上角点击头像，选择 **个人设置 -> 安全设置 -> 访问令牌**，点击 **新建访问令牌**。
   - 设置到期时间，并生成令牌，复制保存该令牌，后续将用于认证。

2. **配置 Git 用户信息**：
   - 设置 Git 的用户名和邮箱：

   ```bash
   git config --global user.name "your_name"
   git config --global user.email "your_email"
   ```

   - 如果不确定账号信息，可以在 GitCode 右上角点击头像，选择 **用户资料** 查看用户名和邮箱。

### 3.3 创建案例并提交代码

1. **创建案例**：
   - 将编写的代码提交到 `entries/[个人或团队名称]` 目录下，确保代码结构清晰，并编写 `README.md` 文件说明案例内容。
   
   - 在提交代码前，请确保已更新所有文件并准备提交：

   ```bash
   cd hackathon
   git add .
   git commit -m "添加 [个人或团队名称] 的案例"
   ```

2. **提交代码到远程仓库**：
   - 使用以下命令提交代码到远程仓库，替换 `username` 和 `project` 为实际的用户名和项目名，`token` 为之前生成的访问令牌：

   ```bash
   git remote set-url origin https://username:token@gitcode.com/username/project.git
   git push origin main
   ```

   - 如果令牌已经包含在 URL 中：

   ```bash
   git push https://username:token@gitcode.com/username/project.git
   ```

### 3.4 提交案例流程总结

1. **Fork 比赛项目** 到个人或团队的仓库。
2. **克隆仓库** 到 NoteBook 本地环境。
3. **配置 Git 用户信息和访问令牌**。
4. **编写案例代码** 并提交到指定的文件夹 `hackathon/[个人/团队名称]`。
5. **提交代码** 到远程仓库。

---

