# Tool Agent Example in MoFA

**语言**: 中文

## 1. 功能说明

Tool Agent是一个带简单计算器的智能体，旨在根据用户输入的简单算术问题通过辅助计算器提供答案。其设计模式为：**接收问题 + 查询/计算 + 返回答案**。

## 2. 使用场景

Tool Agent 适用于需要简单快速响应用户问题的场景。常见的应用场景包括：

- 这主要是一个示例， 展示如何添加额外的Python functions 来作为LLM的辅助功能。
- 为用户提供快速的知识性查询和回答。
- 处理简单的FAQ问答系统。
- 提供基于用户输入问题的即时答案。
- 提供简单的计算器功能。

## 3. 配置方法

Tool Agent 模板通过简单的配置来实现一个问答智能体。以下是详细的配置步骤和说明。

### 配置说明

配置文件位于`tools_agent`目录下，`.yml`文件为定义该智能体的数据流文件。配置文件指定了智能体的工作流，包括如何接收问题并生成答案。

| **文件**                               | **作用**                                                                 |
| -------------------------------------- | ------------------------------------------------------------------------ |
| `tools_agent_dataflow.yml`             | 配置问答任务的数据流，包括如何接收用户问题并查询对应答案。                         |

### Tool 配置说明

支持的Python 工具导入, 参见`scripts\tools_agent.py`文件：

```
from calculator.tool import calculator, calculator_2, newton_calculator

# Define a dictionary to map function names to actual callables
available_functions = {
    'calculator': calculator,
    'calculator_2': calculator_2,
    'newton_calculator': newton_calculator,
}
```

具体的Python 工具实现，参见`scripts\calculator\tool.py`文件。

关于添加工具到LLM的查询中， 参见`configs\tools_agent.yml`文件：
```
Tool:
  TOOL_NAME: Calculator
  TOOL_FUNC: calculator
  TOOL_DESCRIPTION: A calculator is a device that performs arithmetic operations on numbers. The simplest calculators can do only addition, subtraction, multiplication, and division. More sophisticated calculators can handle exponential operations, roots, logarithms, trigonometric functions, and hyperbolic functions. Some calculators have the ability to store numbers in memory and retrieve them for later use. The calculator is a useful tool for performing mathematical calculations quickly and accurately.
```
在这个例子中， 我们提供了三个不同的计算器，上面的`TOOL_FUNC` 可以替换成`calculator`, `calculator_2` 或`newton_calculator`. 

## 4. 运行智能体

### 使用Dora-rs命令行运行

1. 安装MoFA项目包。
2. 执行以下命令以启动智能体流程：
   ```bash
   dora up && dora build tool_agent_dataflow.yml && dora start tool_agent_dataflow.yml --attach
   ```
3. 启动另一个终端，运行`terminal-input`，然后输入相应任务以启动Tool Agent流程。 
   例如： What is 2^3 +3 -(2-3)?

