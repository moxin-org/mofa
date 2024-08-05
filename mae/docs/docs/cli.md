

# Mae-cli合并多个流程的说明



### 安装mae
如果你已经在环境中使用pip install -e . 安装好了整个程序,那么你可以直接使用 `mae-agent --help` 来查看帮助信息. 如果你不清楚怎么安装,那么查看文档 
[install_mae.md](install_mae.md)


### 参数说明

#### 命令格式
```bash
python3 cli.py --main-dataflow-yml /Users/chenzi/project/zcbc/Moxin-App-Engine/mae/mae/agent_link/agent_template/web_search/web_search_dataflow.yml --additional-dataflow-yml /Users/chenzi/project/zcbc/Moxin-App-Engine/mae/mae/agent_link/agent_template/reasoner/reasoner_dataflow.yml --dependencies "{ \"target_node_id\": \"reasoner_agent\", \"target_node_inputs\": [{\"output_node_id\": \"more_question_agent\", \"output_params_name\": \"more_question_results\"}]}"
```
或者
```bash
mae-agent --main-dataflow-yml /Users/chenzi/project/zcbc/Moxin-App-Engine/mae/mae/agent_link/agent_template/web_search/web_search_dataflow.yml --additional-dataflow-yml /Users/chenzi/project/zcbc/Moxin-App-Engine/mae/mae/agent_link/agent_template/reasoner/reasoner_dataflow.yml --dependencies "{ \"target_node_id\": \"reasoner_agent\", \"target_node_inputs\": [{\"output_node_id\": \"more_question_agent\", \"output_params_name\": \"more_question_results\"}]}"
```

### 参数说明

#### `--main-dataflow-yml`  (我们现在称之为主数据流)
- **描述**：主要数据流 YAML 文件路径。此文件包含主数据流的节点和配置。
- **示例**：`--main-dataflow-yml /path/to/main_dataflow.yml`
- **必需**：是

#### `--additional-dataflow-yml`  (我们现在称之为附加数据流)
- **描述**：附加数据流 YAML 文件路径。此文件包含需要合并到主数据流中的附加节点和配置。
- **示例**：`--additional-dataflow-yml /path/to/additional_dataflow.yml`
- **必需**：是

#### `--dependencies`
- **描述**：依赖关系 JSON 字符串。此参数定义了主数据流和附加数据流之间的依赖关系，指定了附加数据流中的某个节点的输出如何依赖于主数据流中某个节点的输出值。
- **格式说明**：
  ```json
  {
    "target_node_id": "string",
    "target_node_inputs": [
      {
        "output_node_id": "string",
        "output_params_name": "string"
      }
    ]
  }
  ```
  - `target_node_id`：附加数据流中的目标节点ID。
  - `target_node_inputs`：包含一个或多个对象，定义了目标节点的输入依赖于主数据流中哪个节点的输出。
    - `output_node_id`：主数据流中的输出节点ID。
    - `output_params_name`：输出节点中的参数名称。

- **示例**：
  ```bash
  --dependencies '{"target_node_id": "reasoner_agent", "target_node_inputs": [{"output_node_id": "more_question_agent", "output_params_name": "more_question_results"}]}'
  ```
- **必需**：是

#### `--output-directory`
- **描述**：输出目录路径。合并后的数据流配置文件将保存到此目录中。默认值为当前工作目录的上一级目录的 `examples/generate` 目录。
- **示例**：`--output-directory /path/to/output_directory`
- **必需**：否
- **默认值**：`<当前工作目录>/../examples/generate`

#### `--search-directory`
- **描述**：搜索目录路径。此目录用于查找数据流模板。默认值为当前工作目录的 `agent_link/agent_template` 目录。
- **示例**：`--search-directory /path/to/search_directory`
- **必需**：否
- **默认值**：`<当前工作目录>/agent_link/agent_template`

### 依赖关系示例说明
假设你有两个数据流文件：

1. `web_search_dataflow.yml` (主数据流)：
   ```yaml
   nodes:
     - id: web_search_task
       path: dynamic
       inputs:
         direction: dora/timer/secs/1
       outputs:
         - task
     - id: web_search_agent
       operator:
         python: ./scripts/web_search_agent.py
         inputs:
           web_search_task: web_search_task/task
         outputs:
           - web_search_results
           - web_search_resource
           - web_search_aggregate_output
     - id: more_question_agent
       operator:
         python: ./scripts/more_question_agent.py
         inputs:
           web_search_aggregate_output: web_search_agent/web_search_aggregate_output
         outputs:
           - more_question_results
           - web_search_aggregate_output
     - id: web_search_output
       operator:
         python: ./scripts/web_search_output.py
         inputs:
           web_search_aggregate_output: more_question_agent/web_search_aggregate_output
         outputs:
           - web_search_output
           - web_search_results
           - web_search_resource
           - more_question_results
           - web_search_task
   ```

2. `reasoner_dataflow.yml` (附加数据流)：
   ```yaml
   nodes:
     - id: reasoner_task_input
       path: dynamic
       inputs:
         direction: dora/timer/secs/1
       outputs:
         - reasoner_task
     - id: reasoner_agent
       operator:
         python: ./scripts/reasoner_agent.py
         inputs:
           reasoner_task: reasoner_task_input/reasoner_task
         outputs:
           - reasoner_result
     - id: reasoner_output
       operator:
         python: ./scripts/reasoner_output.py
         inputs:
           reasoner_result: reasoner_agent/reasoner_result
         outputs:
           - reasoner_output
   ```

你希望 `reasoner_agent` 节点依赖于 `more_question_agent` 节点的 `more_question_results` 输出。你可以使用如下的依赖关系 JSON 字符串：

```bash
--dependencies '{"target_node_id": "reasoner_agent", "target_node_inputs": [{"output_node_id": "more_question_agent", "output_params_name": "more_question_results"}]}'
```

此命令将合并 `reasoner_dataflow.yml` 中的 `reasoner_agent` 节点，使其输入依赖于 `web_search_dataflow.yml` 中的 `more_question_agent` 节点的 `more_question_results` 输出。


