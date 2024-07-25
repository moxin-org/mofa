
## 方案一：在 `dataflow.yml` 中串联所有的 agents

### 目标
在 `dataflow.yml` 文件中定义所有的 agents 及其连接关系.


### 步骤

1. **定义 Agent 模板**
2. **生成 Python 脚本**
3. **生成 Dora-YAML 数据流文件**
4. **加载和执行数据流**
5. **监控和调试**

### 注意
1. 我们希望每一个不同类型的Agent(例如 Self-Refine)等，对于客户而言，其实都是一个 agent,我们会提前生成它的dora模版
2. Agent与Agent之间的参数传递,我们希望使用类似于Dify/Airflow等这种方式,通过连接线把他们连接起来



### 实现

#### 1. 定义 agent 模板

定义每个 agent 的 Python 脚本模板，包括一个 decision agent。

##### agent_template.py
```python
import sys
import json

def agent(input_data):
    # 这里是 agent 的逻辑
    output_data = input_data + 1
    return output_data

if __name__ == "__main__":
    input_data = json.loads(sys.stdin.read())
    output_data = agent(input_data)
    print(json.dumps(output_data))
```

##### decision_agent_template.py
```python
import sys
import json

def decision_agent(input_data):
    # 这里是 decision agent 的逻辑
    if input_data > 10:
        return {"rebuild": True}
    else:
        return {"rebuild": False}

if __name__ == "__main__":
    input_data = json.loads(sys.stdin.read())
    output_data = decision_agent(input_data)
    print(json.dumps(output_data))
```

#### 2. 生成 Python 脚本

编写一个 Python 脚本，根据模板动态生成多个 agent 的 Python 脚本。

##### generate_agents.py
```python
agent_template = """
import sys
import json

def agent(input_data):
    output_data = input_data + {increment}
    return output_data

if __name__ == "__main__":
    input_data = json.loads(sys.stdin.read())
    output_data = agent(input_data)
    print(json.dumps(output_data))
"""

decision_agent_template = """
import sys
import json

def decision_agent(input_data):
    if input_data > 10:
        return {"rebuild": True}
    else:
        return {"rebuild": False}

if __name__ == "__main__":
    input_data = json.loads(sys.stdin.read())
    output_data = decision_agent(input_data)
    print(json.dumps(output_data))
"""

def generate_agent_scripts(num_agents):
    for i in range(num_agents):
        script_content = agent_template.format(increment=i+1)
        with open(f'agent_{i+1}.py', 'w') as f:
            f.write(script_content)

    with open('decision_agent.py', 'w') as f:
        f.write(decision_agent_template)

generate_agent_scripts(3)
```

#### 3. 生成 YAML 数据流文件

编写一个 Python 脚本，根据生成的 agent 脚本动态生成 YAML 数据流文件。

##### generate_dataflow.py
```python
import yaml

def generate_dataflow(num_agents):
    nodes = [{'id': f'agent{i+1}', 'type': 'python', 'script': f'agent_{i+1}.py'} for i in range(num_agents)]
    connections = [{'from': f'agent{i}.output', 'to': f'agent{i+1}.input'} for i in range(1, num_agents)]
    nodes.append({'id': 'decision_agent', 'type': 'python', 'script': 'decision_agent.py'})
    connections.append({'from': f'agent{num_agents}.output', 'to': 'decision_agent.input'})

    dataflow = {'nodes': nodes, 'connections': connections}
    with open('dataflow.yml', 'w') as file:
        yaml.dump(dataflow, file)

generate_dataflow(3)
```

#### 4. 加载和执行数据流

使用 Dora-rs 提供的工具加载并执行生成的 YAML 数据流文件。

##### run_dataflow.py
```python
import dora
import json
import subprocess

def run_dataflow():
    dataflow = dora.load_dataflow('dataflow.yml')
    dora.run_dataflow(dataflow)
    result = subprocess.run(['dora', 'get', 'decision_agent.output'], capture_output=True, text=True)
    return json.loads(result.stdout)

decision_output = run_dataflow()
if decision_output.get('rebuild'):
    generate_dataflow(3)
    run_dataflow()
```

#### 5. 监控和调试

使用 Dora-rs 提供的命令行工具监控和调试数据流的执行情况。

```bash
dora logs
dora trace
dora metrics
```

### 不足和改进

1. **数据流的灵活性**：每次需要重新生成和加载 YAML 文件，增加了复杂性。
   - **改进**：可以在代码中动态调整数据流，而不是每次都生成新的 YAML 文件。

2. **参数传递的复杂性**：需要手动管理每个 agent 的输入输出连接。
   - **改进**：使用更高级的数据流管理工具或框架，自动处理连接和参数传递。

## 方案二：在代码中动态生成和调整数据流

### 目标
在代码中动态生成和调整数据流，提供更高的灵活性。

### 步骤

1. **定义 agent 模板**
2. **生成 Python 脚本**
3. **动态生成 YAML 数据流文件**
4. **加载和执行数据流**
5. **动态调整数据流**
6. **监控和调试**

### 实现

#### 1. 定义 agent 模板

定义每个 agent 的 Python 脚本模板，包括一个 decision agent。

##### agent_template.py
```python
import sys
import json

def agent(input_data):
    output_data = input_data + 1
    return output_data

if __name__ == "__main__":
    input_data = json.loads(sys.stdin.read())
    output_data = agent(input_data)
    print(json.dumps(output_data))
```

##### decision_agent_template.py
```python
import sys
import json

def decision_agent(input_data):
    if input_data > 10:
        return {"rebuild": True}
    else:
        return {"rebuild": False}

if __name__ == "__main__":
    input_data = json.loads(sys.stdin.read())
    output_data = decision_agent(input_data)
    print(json.dumps(output_data))
```

#### 2. 生成 Python 脚本

编写一个 Python 脚本，根据模板动态生成多个 agent 的 Python 脚本。

##### generate_agents.py
```python
agent_template = """
import sys
import json

def agent(input_data):
    output_data = input_data + {increment}
    return output_data

if __name__ == "__main__":
    input_data = json.loads(sys.stdin.read())
    output_data = agent(input_data)
    print(json.dumps(output_data))
"""

decision_agent_template = """
import sys
import json

def decision_agent(input_data):
    if input_data > 10:
        return {"rebuild": True}
    else:
        return {"rebuild": False}

if __name__ == "__main__":
    input_data = json.loads(sys.stdin.read())
    output_data = decision_agent(input_data)
    print(json.dumps(output_data))
"""

def generate_agent_scripts(num_agents):
    for i in range(num_agents):
        script_content = agent_template.format(increment=i+1)
        with open(f'agent_{i+1}.py', 'w') as f:
            f.write(script_content)

    with open('decision_agent.py', 'w') as f:
        f.write(decision_agent_template)

generate_agent_scripts(3)
```

#### 3. 动态生成 YAML 数据流文件

编写一个 Python 脚本，根据生成的 agent 脚本动态生成 YAML 数据流文件。

##### generate_dataflow.py
```python
import yaml

def generate_dataflow(num_agents):
    nodes = [{'id': f'agent{i+1}', 'type': 'python', 'script': f'agent_{i+1}.py'} for i in range(num_agents)]
    connections = [{'from': f'agent{i}.output', 'to': f'agent{i+1}.input'} for i in range(1, num_agents)]
    nodes.append({'id': 'decision_agent', 'type': 'python', 'script': 'decision_agent.py'})
    connections.append({'from': f'agent{num_agents}.output', 'to': 'decision_agent.input'})

    dataflow = {'nodes': nodes, 'connections': connections}
    with open('generated_dataflow.yaml', 'w') as file:
        yaml.dump(dataflow, file)

generate_dataflow(3)
```

#### 4. 加载和执行数据流

使用 Dora-rs 提供的工具加载并执行生成的 YAML 数据流文件。

##### run_dataflow.py
```python
import dora
import json
import subprocess

def run_dataflow():
    dataflow = dora.load_dataflow('generated_dataflow.yaml')
    dora.run_dataflow(dataflow)
    result = subprocess.run(['dora', 'get', 'decision_agent.output'], capture_output=True, text=True)
    return json.loads(result.stdout)

def main():
    generate_dataflow(3)
    decision_output = run_dataflow()
    while decision_output.get('rebuild'):
        generate_dataflow(3)
        decision_output = run_dataflow()

if __name__ == "__main__":
    main()
```

#### 5. 监控和调试

使用 Dora-rs 提供的命令行工具监控和调试数据流的执行情况。

```bash
dora logs
dora trace
dora metrics
```

### 不足和改进

1. **代码复杂性**：动态生成和调整数据流增加了代码的复杂性。
   - **改进**：封装生成和调整数据流的逻辑，减少重复代码。

2. **性能问题**：频繁生成和加载 YAML 文件可能会影响性能。
   - **改进**：优化生成和加载的过程，减少不必要的操作。

### 优化建议

1. **封装逻辑**：将生成和调整数据流的逻辑封装成函数或类，减少重复代码，提高可维护性。
2. **缓存机制**：引入缓存机制，避免频繁生成和加载相同的 YAML 文件，提高性能。
3. **日志和监控**：增加日志和监控，方便调试和性能分析。

