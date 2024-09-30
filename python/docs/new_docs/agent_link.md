
# Mae-Agent-Link
Mae-Agent-Link可以将两个agent-dataflow中的node做连接.例如`source-a`流程中的某个`node`的某个输出作为`source-b`流程中某个`node`的输入,从而构建出一个自定义的更强大的Agen-Dataflow

### 1,安装mae
如果你已经在环境中使用pip install -e . 安装好了整个程序,那么你可以直接使用 `mae-agent --help` 来查看帮助信息. 如果你不清楚怎么安装,那么查看文档 
[install_mae.md](install_mae.md)

### 2，详细案例
我们希望结合Web_search与Reasoner进行连接,让Reasoner去挑选出他认为Web-Search中`more_question_agent`输出多个答案中最适合的一个答案。

使用下面的命令
```bash
mofa-agent-link --upstream-dataflow-yml /Users/chenzi/project/zcbc/Moxin-App-Engine/mofa/mofa/agent_link/agent_template/web_search/web_search_dataflow.yml --downstream-dataflow-yml /Users/chenzi/project/zcbc/Moxin-App-Engine/mofa/mofa/agent_link/agent_template/reasoner/reasoner_dataflow.yml --dependencies "{ \"target_node_id\": \"reasoner_agent\", \"target_node_inputs\": [{\"output_node_id\": \"more_question_agent\", \"output_params_name\": \"more_question_results\"}]}" --output-directory  /Users/chenzi/project/zcbc/Moxin-App-Engine/mofa/examples/generate  --search-directory /Users/chenzi/project/zcbc/Moxin-App-Engine/mofa/mofa/agent_link/agent_template
```
然后直接运行生成的任务即可



### 3. 编写 Agent-Link 的实现流程

1. **编写 `agent-dataflow`**: 按照规则编写好 `agent-dataflow`，并将所有文件放置在 `Moxin-App-Engine/mae/mae/agent_link/agent_template` 文件夹中。编写完成后，先在当前节点进行测试。

2. **配置 CLI 参数**: 根据命令行界面 (CLI) 的要求，填写对应的参数，特别是 `dependencies` 参数。这个参数定义了 `downstream-dataflow` 中某个节点的输入如何依赖于 `upstream-dataflow` 中某个节点的输出。

3. **复制文件**: 程序会根据提供的参数，将 `agent-dataflow` 文件夹中的 `configs` 和 `scripts` 复制到指定的输出目录下。

4. **生成新数据流配置**: 程序会根据 `dependencies` 参数的设置，处理两个 `dora-dataflow` 中的 YAML 配置文件，并生成一个由这两个数据流组合而成的新 YAML 配置文件。

5. **修改节点脚本**: 程序会根据 `dependencies` 参数，修改依赖节点对应的 Python 文件，在文件中动态添加条件判断和 `agent`函数的输入参数。

   


### 4. 编写 Agent-Link 实现的难点
**合并数据流的复杂性**: Agent-Link 的实现需要将两个 `Dora-Dataflow` 合并为一个新的数据流。这意味着合并后的节点输入输出，以及相关文件，都需要进行动态调整。
   - **动态生成节点和数据流**: 需要根据 `upstream-dataflow` 和 `downstream-dataflow` 中节点的输入输出及依赖关系，动态生成新的节点，并更新对应的 `Dora-dataflow.yml` 文件中的节点定义和输入输出。
   - **动态修改节点脚本**: 根据节点的依赖关系，动态生成新的 `node.py` 文件中的条件判断，并修改 `agent_inputs` 参数，以确保合并后的数据流能够正确处理输入输出。
   - **动态添加任务**: 在 `node.py` 中，需要动态将任务添加到 `dspy-agent` 的运行函数参数中。在此过程中，程序需要自动判断该参数是否已经存在，若存在则跳过添加，若不存在则进行添加。





### 5. 现在还存在的问题
1. **节点重复问题**: 如果多个 `agent-dataflow` 中存在相同的 `node` 节点，合并后的节点可能会重复，导致运行失败。
2. **合并限制**: 当前版本仅支持两个 `agent-dataflow` 的合并，暂不支持多个 `agent-dataflow` 的合并。
3. **dependencies参数复杂**: dependencies参数设置较为复杂.需要对当前的`agent-dataflow`较为了解才能写得出
4. 当前仅支持`source-a`的某个node的单个参数作为`source-b`某个node的输入






### 6,cli命令说明

#### 命令格式
```bash
mofa-agent-link --main-dataflow-yml /Users/chenzi/project/zcbc/Moxin-App-Engine/mofa/mofa/agent_link/agent_template/web_search/web_search_dataflow.yml --additional-dataflow-yml /Users/chenzi/project/zcbc/Moxin-App-Engine/mofa/mofa/agent_link/agent_template/reasoner/reasoner_dataflow.yml --dependencies "{ \"target_node_id\": \"reasoner_agent\", \"target_node_inputs\": [{\"output_node_id\": \"more_question_agent\", \"output_params_name\": \"more_question_results\"}]}"
```
或者
```bash
mofa-agent-link --upstream-dataflow-yml /Users/chenzi/project/zcbc/Moxin-App-Engine/mofa/mofa/agent_link/agent_template/web_search/web_search_dataflow.yml --downstream-dataflow-yml /Users/chenzi/project/zcbc/Moxin-App-Engine/mofa/mofa/agent_link/agent_template/reasoner/reasoner_dataflow.yml --dependencies "{ \"target_node_id\": \"reasoner_agent\", \"target_node_inputs\": [{\"output_node_id\": \"more_question_agent\", \"output_params_name\": \"more_question_results\"}]}" --output-directory  /Users/chenzi/project/zcbc/Moxin-App-Engine/mofa/examples/generate  --search-directory /Users/chenzi/project/zcbc/Moxin-App-Engine/mofa/mofa/agent_link/agent_template 
```

### 7，参数说明

#### `--upstream-dataflow-yml`  (我们现在称之为主数据流)
- **描述**：主要数据流 YAML 文件路径。此文件包含主数据流的节点和配置。
- **示例**：`--upstream-dataflow-yml /path/to/main_dataflow.yml`
- **必需**：是

#### `--downstream-dataflow-yml`  (我们现在称之为附加数据流)
- **描述**：附加数据流 YAML 文件路径。此文件包含需要合并到主数据流中的附加节点和配置。
- **示例**：`--downstream-dataflow-yml /path/to/additional_dataflow.yml`
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





