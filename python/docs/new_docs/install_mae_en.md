

## 1. Installing the MAE Project

### 1.1 Project Installation

- Clone the repository and switch to the specified branch:

```sh
git clone <repository-url> && git checkout <branch-name>
```

**Example**:

```sh
git clone git@github.com:moxin-org/Moxin-App-Engine.git && cd Moxin-App-Engine/mofa && git checkout feature/mofa
```

- Switch to the Python 3.10 environment:
  - If you encounter version mismatches, use conda to create the appropriate environment:
  ```sh
  conda create -n py310 python=3.10.12 -y
  ```

### 1.2 Project Environment Setup

- Install the MAE project dependencies:

```sh
pip3 install -r requirements.txt && pip3 install -e .

pip3 install uv && uv pip install -e . 
```

After installation, you can use `mae --help` to view the CLI help information.

## 2. Installing the Rust Environment

Visit the following page and follow the instructions to install the Rust environment for your system:

```sh
https://www.rust-lang.org/tools/install
```

Then, install the `dora-rs` package:

```sh
cargo install dora-cli --locked
```

---