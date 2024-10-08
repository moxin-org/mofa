# 常见问题与解决方案（Q&A）

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
       MODEL_API_KEY: sk-XXXXXXXXXXXXXXXXXXXXXXXX  # 替换为您的 API 密钥
       MODEL_NAME: Qwen/Qwen2.5-72B-Instruct  # 更换为支持更高 Token 的模型
       MODEL_API_URL: https://api.siliconflow.cn/v1/chat/completions
     ```

3. **重新运行代理**：

   ```bash
   dora up && dora build rag_dataflow.yml && dora start rag_dataflow.yml --attach
   ```

---

## 问题 3: 如何为 `run_dspy_or_crewai_agent` 函数添加 prompt 参数或其他代理结果？

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




