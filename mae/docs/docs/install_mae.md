
## 1. Mae项目安装

### 1.1 项目环境部署
建议使用`Dockerfile`来部署当前环境，我们已经在`Dockerfile`中安装了`Rust`和`Python`。
```sh
docker build -t mae_env:v1 .
```

### 1.2 安装项目

- 克隆此项目：
```sh
git clone <repository-url>
```
- 切换到Python 3.10环境：
  - 如果出现环境版本不匹配，请使用conda重新安装此环境：
  ```sh
  conda create -n py310 python=3.10.12 -y
  ```
- 安装mae项目：
```sh
pip3 install -r requirements.txt && pip3 install -e .
```

## 2. Rust环境安装
根据你的系统安装Rust环境：
```sh
https://www.rust-lang.org/tools/install
```

然后安装dora-rs的包：
```sh
cargo install dora-cli --locked
```


