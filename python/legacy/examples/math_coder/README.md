[English](README.md) | [Simplified Chinese](README_cn.md)

# Math Coder

------

## 1. Overview

The Math Coder agent processes user task inputs, analyzes them via the reasoner-agent, and generates code to execute and solve math-related problems.
The design pattern combines: **Code Generation + Code Execution**.

**Process Description:**

- **Reasoner-Agent**: Receives task keywords and provides concise answers based on the task.

------

## 2. Configuration

### Configuration Overview

The configuration files are located in the `configs` directory, and `.py` files contain the actual agent code. Configuration files define the behavior, parameters, and model prompts for each agent.

### Configuration Steps

#### 3. Modify Configurations

Edit the `.yml` configuration files in the `configs` directory according to specific requirements.
You can customize model parameters but it is recommended to avoid changing the prompts.

------

## 4. Running the Agent

### Run Using Dora-RS Command Line

1. Install the MoFA project package.

2. Execute the following commands to start the agent workflow:

   ```shell
   dora up && dora build reasoner_dataflow.yml && dora start reasoner_dataflow.yml --attach
   ```

3. Open another terminal, run `terminal-input`, and input the corresponding task to initiate the Agent Fight workflow.