## 1，如何运行mae-server
1. 安装mae的项目. 可以去查看此文档 [install_mae](install_mae.md)
2. 安装rust相关的环境(安装文档与上面相同)
3. 找到`/mae/server/server.py`这个文件，运行它，会自动的生成一个后端的api服务
4. 运行前端代码
    - 找到`https://github.com/ROLFFFX/MAE`项目
    - 安装node.js环境
    - `cd mae-frontend`
    - `npm install`
    - `npm run dev`
5. 运行后端代码,进入到`/Moxin-App-Engine/mae/mae/server`使用 `python server.py`运行后台程序

## 2，API 接口功能
1. **获取 Agent 列表**: 通过调用 `agent_list` 接口，获取 `/Moxin-App-Engine/mae/mae/agent_link/agent_template` 目录下的所有 agent。
2. **获取 Agent 节点**: 使用 `agent_dataflow` 接口，提取指定 `agent-dataflow` 中的所有节点，每个节点都是一个独立的小型 agent。
3. **获取节点配置**: 通过 `agent_node_config` 接口，检索每个节点的具体配置参数。
4. **修改节点配置**: 调用 `upload_agent_node_config` 接口，调整节点的具体参数，如 `prompt` 等内容。
5. **运行Agent**: 使用 `run_agent` 接口，输入 agent 的名称，系统将自动生成并运行配置好的 agent。
6. **上传文件**: 使用 `upload_files` 接口，上传文件到指定目录.





