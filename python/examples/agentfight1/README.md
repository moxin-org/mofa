# Agent Fight case

[English](README.md) | [简体中文](README_cn.md)

## 1. Function description

The agent fights two agents with different large models to answer the task questions through the input of the user task. The judge agent generates evaluation criteria according to the tasks input by the user, and scores and evaluates the answers of the two answer agents.
Its design mode is: ** Task extraction + task response + generate scoring criteria + result evaluation **.

** Process Description: **

answer_agent_1: Take the task keywords and give a brief answer around the task.

answer_agent_2: Take the task keywords and give a brief answer around the task.

judge_agent: Generates evaluation criteria, receives answer1 and 2 results, evaluates and feeds back to the terminal.


2. Configuration method

### Configuration description

The configuration file is in the configs directory, and the.py file is the agent code that actually runs. The configuration file specifies the behavior, parameters, and model hints of each Agent.

### Configuration steps


#### 3. Modify the configuration

Edit the.yml configuration file in the configs directory according to your requirements.
You can customize and modify the model parameters in it. It is recommended not to modify and prompt words.


## 4. Run the agent

Run with the Dora-rs command line

1. Install the MoFA project package.
2. Run the following command to start the agent process:
   ```bash
   dora up && dora build fight_dataflow.yml && dora start fight_dataflow.yml --attach
   ```
3. Start another terminal, run 'terminal-input', and enter the corresponding task to start the Agent Fight flow.