Here is the updated document translated into English:

---

# Self-Refine Template Implementation in MoFA

**Language**: English

## 1. Function Overview

The Self-Refine agent is a self-iterative improvement model based on feedback, optimization, and evaluation. This model consists of four agent modules: generation, feedback, refinement, and evaluation. The design pattern is: **Feedback + Optimization + Evaluation + Iteration**.

## 2. Use Cases

The Self-Refine agent is suitable for complex tasks that require multiple rounds of feedback and optimization. Common use cases include:

- Creating an agent that can continuously improve generated content based on system or user feedback.
- Designing a system capable of self-iterative improvements through an internal feedback mechanism.

## 3. Configuration Method

The Self-Refine template enables the creation of an agent that performs self-feedback and optimization by modifying its configuration files. Below are the detailed configuration steps and instructions.

### Configuration Details

Configuration files are located in the `configs` directory, and the `.py` files are the actual agent code to be run. The configuration files specify the behavior of each agent, model parameters, prompts, etc.

| **File**                        | **Function**                                                           |
| ------------------------------- | ----------------------------------------------------------------------- |
| `configs/evaluation_agent.yml`   | Configures evaluation parameters, including evaluation criteria and success conditions. |
| `configs/feedback_agent.yml`     | Configures the feedback mechanism, defining the logic and content of feedback. |
| `configs/refinement_agent.yml`   | Configures the optimization logic, defining refinement rounds and strategies. |
| `configs/writer_agent.yml`       | Configures the prompts and model parameters for initial content generation. |
| `evaluation_agent.py`            | Actual evaluation agent, assessing whether the `refinement_agent`'s output meets expectations. |
| `feedback_agent.py`              | Actual feedback agent, generating feedback for the initial output and providing suggestions for improvement. |
| `refinement_agent.py`            | Actual refinement agent, refining the output based on feedback from the `feedback_agent`. |
| `writer_agent.py`                | Actual writer agent, responsible for generating the initial content based on the task. |

### Configuration Steps

#### 1. Template Copy

Copy the `self_refine` subdirectory containing the Self-Refine template to your working directory.

#### 2. Agent Naming

You can rename the files based on your project requirements. For example:
- `self_refine_dataflow.yml` can be renamed to `my_project_dataflow.yml`.
- `configs/writer_agent.yml` can be renamed to `configs/my_writer_agent.yml`.

#### 3. Modify Configuration

Edit the `.yml` configuration files located in the `configs` directory according to your specific needs. For example:
- **`writer_agent.yml`**: Customize the prompts to define the logic for generating initial content.
- **`refinement_agent.yml`**: Adjust refinement parameters, such as feedback rounds and optimization strategies.
- **`feedback_agent.yml`**: Define the logic and conditions for generating feedback.
- **`evaluation_agent.yml`**: Set evaluation criteria and success conditions.

#### 4. Update Python File Paths

Ensure that the `yaml_file_path` variable in each `.py` file points to the correct configuration file. For example:
```python
yaml_file_path = "configs/self_refine_agent.yml"
```

### Method Two: Using MoFA IDE

This method is to be determined (TBD).

## 4. Running the Agent

### Method One: Running via Dora-rs Command Line

1. Install the MoFA project package.
2. Execute the following commands to start the agent workflow:
   ```bash
   dora up && dora build self_refine_dataflow.yml && dora start self_refine_dataflow.yml
   ```
3. Open another terminal, run `terminal-input`, and then enter the appropriate task to start the self-refine process.

### Method Two: Running in the MoFA Environment

This method is to be determined (TBD).

---
