

## 1. pyproject.toml 标准模板

```toml
[tool.poetry]
name        = "<package_name>"          # • 包名，与项目/Agent 名称一致
version     = "<version>"               # • 版本号，格式如 "0.1.0"
description = "<简短描述>"               # • 一句话概述包功能
authors     = [                         # • 作者&联系方式列表
  "<Your Name> <you@example.com>",
]
packages = [                            # • 指定要打包的模块目录
  { include = "<module_dir_name>" }
]

[tool.poetry.dependencies]
python         = ">=3.10" # • Python 版本约束，如 ">=3.10"

[tool.poetry.scripts]
<command_name> = "<module_dir_name>.main:main"  
# • 定义可执行脚本入口：命令名映射到模块内 callabale

[build-system]
requires      = ["poetry-core>=<x.y.z>"]      # • 构建时依赖
build-backend = "poetry.core.masonry.api"     # • Poetry 构建后端

```

**说明**：

* `<package_name>` 与模块目录 `<module_dir_name>` 应一致。
* `scripts` 部分根据项目是否需要命令行工具再启用。

---

## 2. README.md 标准模板

````markdown
# <项目名称>

> <一句话概述项目功能，突出价值和场景>

---

## Features / 功能亮点
- <核心功能 1>
- <核心功能 2>
- <核心功能 3>

---

## Installation / 安装
```bash
pip install -e .
````

> 使用可编辑模式安装，方便二次开发和调试。

---

## Usage / 使用示例

1. 创建配置文件（如 `config.yml`）：

   ```yaml
   # 示例配置
   nodes:
     - id: <node_id>
       build: pip install -e .
       path: <module_dir_name>
       inputs:
         <input_topic>: <其他节点>/输出主题
       outputs:
         - <output_topic1>
         - <output_topic2>
   ```
2. 启动节点：

   ```bash
   dora build demo.yml
   dora start demo.yml
   ```




---

## Integration with Other Nodes案例 / 链接其他的Node案例
To connect with your existing node ...

---

## API Reference / 接口文档
### Input Topics
| Topic         | Type            | Description                     |
|---------------|-----------------|---------------------------------|
| `<topic1>`    | `<类型>`        | `<功能描述>`                     |

### Output Topics
| Topic         | Type            | Description                     |
|---------------|-----------------|---------------------------------|
| `<topic2>`    | `<类型>`        | `<功能描述>`                     |

---

## Contributing / 贡献指南
1. Fork 本仓库
2. 创建分支 `feature/xxx`
3. 提交 PR，描述改动和测试方法

---

## License / 许可证
Released under the MIT License.



