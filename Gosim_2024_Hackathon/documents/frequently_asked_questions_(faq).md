[# 常见问题与解决方案（Q&A）

## 问题 1: 运行 Agent 时出现 `Exited with code 1` 错误

### 描述

在尝试运行  Agent 时，系统返回以下错误信息，导致进程以代码 1 退出。

### 错误信息

```
File "/env/miniconda3/envs/py310/lib/python3.10/site-packages/dspy/teleprompt/finetune.py", line 28, in <module>
      os.makedirs(training_data_directory)
    File "/env/miniconda3/envs/py310/lib/python3.10/os.py", line 225, in makedirs
      mkdir(name, mode)

  FileExistsError: [Errno 17] File exists: 'local_cache/compiler'

Location:
    binaries/runtime/src/operator/python.rs:28:9
```

### 解决方案

1. **删除现有的 `local_cache/compiler` 文件夹**：
   
   - 导航到当前工作目录。
   - 删除 `local_cache/compiler` 文件夹。

2. **重新运行代理**：

   - 确保删除操作成功后，重新执行之前的运行命令。

### 操作步骤

```bash
# 删除 local_cache/compiler 文件夹
rm -rf local_cache/compiler

# 重新运行  代理
dora up && dora build dataflow.yml && dora start dataflow.yml --attach
```

---

## 问题 2: `reasoner-agent` 运行时出现 `RuntimeError: 404 page not found` 错误

### 描述

在运行 `reasoner-agent` 时，系统返回 404 错误，导致进程以代码 1 退出。

### 错误信息

```
File "/project/zcbc/mofa/python/examples/rag/scripts/reasoner_agent.py", line 31, in on_event
      agent_result = run_dspy_or_crewai_agent(agent_config=inputs)
    File "/project/zcbc/mofa/python/mofa/run/run_agent.py", line 165, in run_dspy_or_crewai_agent
      raise RuntimeError(str(e))

  RuntimeError: 404 page not found
```

### 解决方案

1. **确认 `siliconflow` 账户是否完成实名验证**：

   - 未完成实名验证的账户可能无法使用部分模型。
   - 登录您的 `siliconflow` 账户，检查实名验证状态，并完成相关验证。

2. **检查模型的 Token 限制**：

   - 确认所使用模型的最大 Token 数量是否被超出。
   - 如果超过限制，请更换为支持更高 Token 数量的模型。

### 操作步骤

1. **检查实名验证**：

   - 访问 [siliconflow 官方网站](https://siliconflow.cn)。
   - 登录您的账户，导航到账户设置，确认是否已完成实名验证。

2. **更换模型**（如果 Token 超出限制）：

   - 打开 `configs/rag_retrieval.yml` 文件。
   - 修改 `MODEL_NAME` 为支持更高 Token 数量的模型，例如：
   
     ```yaml
     MODEL:
       MODEL_API_KEY: ***REMOVED***XXXXXXXXXXXXXXXXXXXXXXXX  # 替换为您的 API 密钥
       MODEL_NAME: Qwen/Qwen2.5-72B-Instruct  # 更换为支持更高 Token 的模型
       MODEL_API_URL: https://api.siliconflow.cn/v1/chat/completions
     ```

3. **重新运行代理**：

   ```bash
   dora up && dora build rag_dataflow.yml && dora start rag_dataflow.yml --attach
   ```

---

## 问题 3: 如何为 Agent (也就是agent的核心函数 `run_dspy_or_crewai_agent`) 函数添加 prompt 参数或其他代理结果？

### 描述

在使用 MoFA 自带的运行代理函数 `run_dspy_or_crewai_agent` 时，需求需要添加自定义的 prompt 参数或整合其他代理结果。

### 解决方案

您可以通过修改代码段，向 `inputs['input_fields']` 中添加自定义的 prompt 参数或其他代理结果。以下是具体操作步骤：

### 修改代码示例

```python
yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='reasoner_agent.yml')
inputs = load_agent_config(yaml_file_path)
inputs["task"] = self.task
inputs['input_fields'] = {"memory_data": self.context_memory}

# 添加自定义的 prompt 参数或其他代理结果
inputs['input_fields']['prompt'] = "Your custom prompt here"
inputs['input_fields']['additional_result'] = "Additional agent result"

agent_result = run_dspy_or_crewai_agent(agent_config=inputs)
```

### 详细步骤

1. **添加自定义参数**：

   ```python
   inputs['input_fields']['prompt'] = "Your custom prompt here"
   inputs['input_fields']['additional_result'] = "Additional agent result"
   ```


## 问题 4: 如何对`Dora-Node`中的代码进行debug.
1. 首先当你使用 `dora up`的时候，会在当前生成一个`out`的临时目录，里面包含了当前运行流程中的节点的运行日志。
2. 你可以在代码中使用print,print的内容会在`out`中输出。你可以在里面进行查看。
3. 你可以将日志拿出来，然后单独创建一个文件。进行测试



## 问题 5: 如何使用dora-dataflow使用node的agent的数据传输

**5.1 如何在dataflow.yml中定义好节点之间的依赖关系?**

**在 `dataflow.yml` 中，节点之间的依赖关系是通过定义每个节点的 `inputs` 和 `outputs` 来建立的。**

### 如何定义节点的依赖关系？

- **节点标识符 (`id`)：** 每个节点都有一个唯一的 `id`，用于标识和引用该节点。
- **输出 (`outputs`)：** 节点处理后生成的数据，可供其他节点使用。
- **输入 (`inputs`)：** 节点需要的数据，通常来自其他节点的输出。

**通过在一个节点的 `inputs` 中引用另一个节点的 `outputs`，就建立了节点之间的依赖关系。**

### 示例解析

```yaml
nodes:

  - id: terminal-input
    outputs:
      - data
    inputs:
      reasoner_results: reasoner-agent/reasoner_results

  - id: reasoner-agent
    operator:
      python: scripts/reasoner_agent.py
    inputs:
      task: terminal-input/data
    outputs:
      - reasoner_results
```

#### 1. `terminal-input` 节点

- **输出 (`outputs`)：**
  - `data`：用户输入的数据。
- **输入 (`inputs`)：**
  - `reasoner_results`：来自 `reasoner-agent` 节点的 `reasoner_results` 输出。

#### 2. `reasoner-agent` 节点

- **输入 (`inputs`)：**
  - `task`：来自 `terminal-input` 节点的 `data` 输出。
- **输出 (`outputs`)：**
  - `reasoner_results`：智能体处理后的结果。

### 建立依赖关系的方法

- **格式：**

  ```yaml
  inputs:
    本节点的输入参数名: 上游节点ID/上游节点的输出参数名
  ```

- **示例：**

  - 在 `reasoner-agent` 节点中：

    ```yaml
    inputs:
      task: terminal-input/data
    ```

    **含义：** `reasoner-agent` 节点的输入 `task`，来自于 `terminal-input` 节点的输出 `data`。

  - 在 `terminal-input` 节点中：

    ```yaml
    inputs:
      reasoner_results: reasoner-agent/reasoner_results
    ```

    **含义：** `terminal-input` 节点的输入 `reasoner_results`，来自于 `reasoner-agent` 节点的输出 `reasoner_results`。

### 核心要点

- **节点的 `id` 必须唯一**，用于标识节点和建立引用。
- **通过 `inputs` 和 `outputs` 定义数据流动**：
  - 节点的输入 `inputs` 引用其他节点的输出 `outputs`，建立依赖关系。
- **数据传递方向明确**：
  - 数据从上游节点的输出流向下游节点的输入。


**5.2 如何在对应的python中定义好节点之间的依赖关系?**

### 1. 定义 Operator 类

首先，定义一个 `Operator` 类，用于在数据流中处理节点的操作。

```python
class Operator:
    def on_event(self, dora_event, send_output) -> DoraStatus:
        # 事件处理逻辑
        return DoraStatus.CONTINUE
```

- **解释**：`Operator` 类包含一个方法 `on_event`，用于处理收到的事件。
- **返回值**：`DoraStatus.CONTINUE` 表示继续监听后续事件。

---

### 2. 检查事件类型和输入 ID

在 `on_event` 方法中，首先检查事件类型是否为 `"INPUT"`，并验证事件的 ID 是否在需要处理的输入列表中。

```python
def on_event(self, dora_event, send_output) -> DoraStatus:
    if dora_event["type"] == "INPUT":
        agent_inputs = ['data', 'task']
        if dora_event["id"] in agent_inputs:
            # 处理输入事件
            return DoraStatus.CONTINUE
```

- **解释**：
  - 仅当事件类型为 `"INPUT"` 时才处理。
  - `agent_inputs` 列表包含需要处理的输入事件的 ID，例如 `'data'` 或 `'task'`。
  - 如果事件的 ID 在 `agent_inputs` 中，表示这是一个需要处理的任务。

---

### 3. 提取任务并加载配置

提取用户的任务输入，并加载智能体的配置文件 `reasoner_agent.yml`。

```python
if dora_event["id"] in agent_inputs:
    task = dora_event["value"][0].as_py()
    to_do_something
```


### 3. 发送处理结果到数据流

使用 `send_output` 函数，将智能体的结果发送回数据流，输出 ID 为 `'reasoner_results'`。

```python
send_output(
    "reasoner_results",
    pa.array([
        create_agent_output(
            step_name='keyword_results',
            output_data=agent_result,
            dataflow_status=os.getenv('IS_DATAFLOW_END', True)
        )
    ]),
    dora_event['metadata']
)
print('reasoner_results:', agent_result)
```

- **解释**：
  - `send_output` 函数发送输出，指定输出 ID 为 `'reasoner_results'`。
  - `create_agent_output` 函数创建输出数据，包括步骤名称、输出数据和数据流状态。
  - 打印结果，便于实时查看。

---

### 7. 返回继续状态

最后，返回 `DoraStatus.CONTINUE`，表示继续监听并处理后续的事件。

```python
return DoraStatus.CONTINUE
```


**总结：**

- **定义 Operator 类**：用于处理数据流中的事件。
- **处理输入事件**：检查事件类型和 ID，提取任务内容。
- **发送输出**：将结果发送回数据流，供其他节点使用。
- **继续监听**：返回继续状态，等待下一个事件。


## 问题 5: 运行`terminal-input`之后，报错：
~~~
RuntimeError: Could not setup node from node id. Make sure to have a running dataflow with this dynamic node.

Caused by:
  failed to get node config from daemon: multiple dataflows contains dynamic node id terminal-input. Please only have one running dataflow with the specified node id if you want to use dynamic node.
~~~

**你可以使用下面的命令后，重新运行 `dora up && dora build  dataflow.yml && dora start dataflow.yml`/`terminal-input`**:
~~~
dora destroy && dora up
~~~
 