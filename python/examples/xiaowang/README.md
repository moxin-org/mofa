[English](README.md) | [中文](README_cn.md)

# xiaowang

A multi-level dynamic reflective agent based on MoFA - xiaowang

**Languages:**

- Python 3.10+
- Rust

------

## 1. Overview

**xiaowang** is a multi-level dynamic reflective agent. During execution, it dynamically determines the level of reflection and performs corresponding depth of reflection based on decisions from dynamic decision nodes. This mimics a human process of repeatedly prompting a large model when dissatisfied with its results to improve the richness, accuracy, and reliability of the model's outputs.

------

## 2. Use Cases

This method can increase the depth of thinking and improve the reliability of results for any large language model.

------

## 3. Configuration

Modify multiple `.yml` configuration files in `xiaowang_start/configs` to fine-tune and customize each node's prompts, APIs, keys, etc.

------

## 4. Running xiaowang

1. Install the MoFA project package and relevant dependencies.

2. Execute the following command:

   ```shell
   dora up && dora build xiaowang_dataflow.yml && dora start xiaowang_dataflow.yml
   ```

3. Open another terminal and run:

   ```shell
   xiaowang
   ```

   Enter tasks to initiate the agent's workflow.