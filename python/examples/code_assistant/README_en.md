# Code Assistant Example in MoFA

**Language**: English
## 1. Functionality Description

The **Code Assistant** is a simple code aid tool designed to provide code based on user input requirements. Its design pattern is: **receive question + query corresponding part of the code + return code**.

## 2. Use Cases

The Code Assistant is suitable for scenarios where simple code writing is required. Common application scenarios include:

-   **Helping users find errors in code.**
-   **Assisting users in writing certain code.**

## 3. Configuration Method

The Code Assistant template achieves a Q&A agent through simple configuration. Here are the detailed configuration steps and instructions.

### Configuration Overview

Configuration files are located in the `configs` directory. The `.yml` files define the data flow for the agent. The configuration file specifies the agent's workflow, including how to receive questions and generate answers.
| **File**                       | **Purpose**                                                                  |
| ------------------------------ | ---------------------------------------------------------------------------- |
| `code_assistant_agent.yml` | Provides new code based on the user's question or code snippet.|
| `code_content_agent.yml` | Extracts key fragments from the code based on the user's question. |

## 4. Running the Agent

### Running with Dora-rs Command Line

1. **Install MoFA Project Packages**

Ensure that you have installed all necessary packages for the MoFA project. This typically involves setting up a Python environment and installing the required packages.

2. **Install Code-assistant Dependencies**
    ```bash
   pip install -r requirements.txt
   ```

3. **Execute the Following Command to Start the Agent Process**

    ```bash
    dora up && dora build code_assistant_dataflow.yml && dora start code_assistant_dataflow.yml --attach
    ```

4. **Initialize Task Input**
    Open another terminal window, run `terminal-input`, and then input the corresponding task to start the Query Assistant process.

   ```bash
   terminal-input
   Enter your task: Record and retrieve key information about machine learning
   ```

### Attention
As a demo, the content of the code must be in the code_assistant folder and be named as *.py.
And all *.py files in this folder will be considered by the content agent.
