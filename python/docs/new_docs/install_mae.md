
## 1. Mae项目安装

### 1.1 安装项目
- 克隆此项目切换到指定分支:

```sh
git clone <repository-url> && git checkout <branch-name> 
```
**Example**:

```sh
git clone git@github.com:moxin-org/Moxin-App-Engine.git && cd Moxin-App-Engine/mofa && git checkout feature/mofa
```

- 切换到Python 3.10环境：
  - 如果出现环境版本不匹配，请使用conda重新安装此环境：
  ```sh
  conda create -n py310 python=3.10.12 -y
  ```

### 1.2 项目环境部署

- 安装mae项目：
```sh
pip3 install -r requirements.txt && pip3 install -e .

```
安装完毕之后你可以使用`mae --help`查看Cli帮助信息

## 2. Rust环境安装
请你访问下面的页面,根据你的系统安装Rust环境：
```sh
https://www.rust-lang.org/tools/install
```

然后安装dora-rs的包：
```sh
cargo install dora-cli --locked
```


