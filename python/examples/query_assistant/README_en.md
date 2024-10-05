# Query Assistant Example in MoFA

**Language**: English

## 1. Functionality Description

The **Query Assistant** is a simple question-and-answer agent designed to provide direct answers based on user-inputted questions. Its design pattern is: **Receive Question + Query + Return Answer**.

## 2. Use Cases

The Query Assistant is suitable for scenarios that require simple and quick responses to user questions. Common application scenarios include:

- **Providing Quick Knowledge Queries and Answers**: Offering users fast access to informational queries and responses.
- **Handling Simple FAQ Systems**: Managing frequently asked questions with straightforward answers.
- **Providing Instant Answers Based on User Input**: Delivering immediate responses tailored to the user's specific questions.

## 3. Configuration Method

The Query Assistant template implements a question-and-answer agent through simple configurations. Below are the detailed configuration steps and explanations.

### Configuration Overview

Configuration files are located in the `query_assistant` directory. The `.yml` files define the data flow for the agent. The configuration file specifies the agent's workflow, including how to receive questions and generate answers.

| **File**                       | **Purpose**                                                                  |
| ------------------------------ | ---------------------------------------------------------------------------- |
| `query_assistant_dataflow.yml` | Configures the data flow for the Q&A task, including how to receive user questions and query corresponding answers. |

## 4. Running the Agent

### Running with Dora-rs Command Line

1. **Install MoFA Project Packages**

   Ensure that you have installed all necessary packages for the MoFA project. This typically involves setting up a Python environment and installing the required packages.

2. **Execute the Following Command to Start the Agent Process**

   ```bash
   dora up && dora build query_assistant_dataflow.yml && dora start query_assistant_dataflow.yml --attach
   ```

3. **Initialize Task Input**

   Open another terminal window, run `terminal-input`, and then input the corresponding task to start the Query Assistant process.

   ```bash
   terminal-input
   Enter your task: Record and retrieve key information about machine learning
   ```

---

