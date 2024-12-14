# MoFA for Dora-RS

[English](README.md) | [简体中文](README_cn.md)

This guide explains how to install, deploy, and start the MoFA framework built on [Dora-RS](https://github.com/dora-rs/dora).

## Getting Started

### 1. Installation

1. **Clone the project and switch to the specified branch:**

```sh
git clone <repository-url> && git checkout <branch-name>
```

**Example**:

```sh
git clone git@github.com:moxin-org/mofa.git && cd mofa
```

2. **Use Python 3.10 or later:**

- If there's a version mismatch, reinstall the environment using conda. For example:

```sh
conda create -n py310 python=3.10.12 -y
```

3. **Set up the project environment:**

- Install the required dependencies:

```
cd python && pip3 install -r requirements.txt && pip3 install -e .
```

Once installed, you can use the command `mofa --help` to view CLI help information.

4. **Install Rust and Dora-RS:**

Since the Dora-RS computing framework is built using Rust, visit the following page to install Rust for your operating system:

https://www.rust-lang.org/tools/install

Then, install Dora-CLI:

```sh
cargo install dora-cli --locked
```

### 2. Configuration

In the `examples` directory, we provide some available agent examples. Before use, you need to configure the `.yml` files in the `configs` directory of the agent. If the `node` was installed via pip, locate the node's name in the `agent-hub` and modify the `.yml` file accordingly.

**Example of configuring the LLM inference API:**

Using **OpenAI** API:

```yaml
MODEL:
  MODEL_API_KEY:
  MODEL_NAME: gpt-4o-mini
  MODEL_MAX_TOKENS: 2048
```

You can also configure it to use the Ollama model or the local open-source model provided by Moxin:

**Example using Ollama:**

```yaml
MODEL:
  MODEL_API_KEY: ollama
  MODEL_NAME: qwen:14b
  MODEL_MAX_TOKENS: 2048
  MODEL_API_URL: http://192.168.0.1:11434
```

### 3. Starting the Framework

------

Example: Starting the `hello_world` Agent in the `examples` directory:

1. **Navigate to the directory:**

   Open the terminal, switch to the `hello_world` directory, and execute the following command:

   ```sh
   cd /mofa/python/examples/hello_world
   ```

2. **Build the Dataflow file:**

   Open a new terminal window in the current directory and execute the following command to prepare and build the Dataflow:

   ```sh
   dora up && dora build dataflow.yml
   ```

   Here, `dataflow.yml` is the configuration file describing the Agent's execution flow.

3. **Start the Dataflow process:**

   In the same terminal, start the Dataflow process:

   ```sh
   dora start dataflow.yml
   ```

4. **Handle dynamic nodes:**

   If `dataflow.yml` specifies a node's `path` as `dynamic` (e.g., `path: dynamic`), you need to run that dynamic node in a separate terminal.
   **Example:** The node `terminal-input` is a dynamic node in the following configuration:

   ```yaml
   nodes:
     - id: terminal-input
       build: pip install -e ../../node-hub/terminal-input
       path: dynamic
       outputs:
         - data
       inputs:
         agent_response: agent/agent_response
   ```

   For the above node, open a new terminal and run the following command to start the dynamic node:

   ```sh
   terminal-input
   ```

   This ensures `terminal-input` runs properly and sends/receives data as required.

### 4. Detailed Documentation

More detailed documentation is available in the [documents](documents/README.md) subdirectory.
