# Self-Refine 模版实现	

**语言**: 中文

## 1. 功能说明

Self-Refine智能体是一种基于反馈、优化和评估的自我迭代改进模式。该模式由四个智能体模块组成：生成、反馈、优化和评估。其设计模式为：**反馈 + 优化 + 评估 + 迭代**。

## 2. 使用场景

Self-Refine智能体适用于需要多轮反馈和优化的复杂任务。常见的应用场景包括：

- 创建一个可以根据系统或用户反馈不断优化生成内容的智能体。
- 设计一个能够通过内部反馈机制进行自我迭代改进的系统。

## 3. 配置方法

Self-Refine模版通过更改配置信息来实现一个能够进行自我反馈和优化的智能体。以下是详细的配置步骤和说明。


### 配置说明

配置文件位于`configs`目录下，`.py`文件为实际运行的智能体代码。配置文件指定了各个Agent的行为、模型参数、提示等。

| **文件**                        | **作用**                                                                 |
| ------------------------------- | ------------------------------------------------------------------------ |
| `configs/evaluation_agent.yml`   | 配置评估阶段的参数，包括评估标准和成功条件。                             |
| `configs/feedback_agent.yml`     | 配置反馈机制，定义反馈的逻辑和内容。                                     |
| `configs/refinement_agent.yml`   | 配置优化逻辑，定义优化轮次和策略。                                       |
| `configs/writer_agent.yml`       | 配置生成初步内容的提示词和模型参数，定义生成逻辑。                        |
| `evaluation_agent.py`            | 实际评估智能体，评估`refinement_agent`生成的结果是否符合预期。           |
| `feedback_agent.py`              | 实际反馈智能体，生成对初步结果的反馈，并提供改进建议。                   |
| `refinement_agent.py`            | 实际优化智能体，根据`feedback_agent`的反馈对结果进行优化。               |
| `writer_agent.py`                | 实际生成智能体，负责根据任务生成初步内容。                               |

### 配置步骤

#### 1. 模版拷贝

将包含Self-Refine模版的`self_refine`子目录拷贝到您的工作目录中。

#### 2. 智能体命名

您可以根据需求重命名相关文件。例如：
- `self_refine_dataflow.yml` 可以重命名为`my_project_dataflow.yml`。
- `configs/writer_agent.yml` 可以重命名为`configs/my_writer_agent.yml`。

#### 3. 修改配置

根据具体需求，编辑`configs`目录下的`.yml`配置文件。例如：
- **`writer_agent.yml`**：自定义提示词，用于定义初步生成内容的逻辑。
- **`refinement_agent.yml`**：调整优化参数，如反馈轮次和优化策略。
- **`feedback_agent.yml`**：定义反馈生成的逻辑和条件。
- **`evaluation_agent.yml`**：设置评估标准和成功条件。

#### 4. 更新Python文件路径

在每个`.py`文件中，确保引用的`yaml_file_path`变量路径指向正确的配置文件。例如：
```python
yaml_file_path = "configs/self_refine_agent.yml"
```

### 方法二：使用MoFA IDE

此方法待定（TBD）。

## 4. 运行智能体

### 方法一：使用Dora-rs命令行运行

1. 安装MoFA项目包。
2. 执行以下命令以启动智能体流程：
   ```bash
   dora up && dora build self_refine_dataflow.yml && dora start self_refine_dataflow.yml
   ```
3. 启动另一个终端，运行`terminal-input`，然后输入相应任务以启动self-refine流程。

### 方法二：在MoFA运行环境中运行

此方法待定（TBD）。

---

