# Agent Fight

## 1. Overview
This tool is designed to compare and evaluate the results of two agents and/or LLMs. AgentFight is powered by LLM itself, to score both agent/llm's results, across various dimensions.

## 2. Use Cases
Evaluate and compare the performance of two different agent/llms, in terms of the quality of their results.

## 3. Configuration
AgentFight utilize llm to be the judge. The judge rules are written with prompt. 

To modify the `Prompt`, i.e. the judge rules, and other settings, please update the `content_evaluation_agent.yml` file, located in the `content-evaluation` directory under `agent-hub`.

## 4. Running AgentFight

### Method 1: Using Dora-rs Commands

1. Install the MoFA project package.
2. Run the following commands:
   ```bash
   dora up && dora build agent_fight_dataflow.yml && dora start reasoner_dataflow.yml
3. Open another terminal and run multiple-terminal-input. Enter the following three parameters:
   - **primary_data**: The result of the first agent/llm (provide an absolute path to a Markdown file).
   - **second_data**: The result of the second agent/llm (provide an absolute path to a Markdown file).
   - **source_task**: The task that generated the agent/llm results. We assume that the same task was assigned to two agent/llms. "primary_data" and "second_data" are the results generated, respectively, by the two different agent/llm, with the same "source_task".
