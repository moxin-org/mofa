# Memory Process Example in MoFA

## 1. Functionality

The **Memory** agent in MoFA manages and retrieves contextual memory to assist users in maintaining consistency and relevance during interactions. Its design pattern includes: **Context Retrieval + Reasoning Response + Memory Recording**. This process ensures that the agent can utilize previous conversations and task information to provide more accurate and relevant answers.

## 2. Use Cases

This agent is suitable for tasks requiring the maintenance of long-term or short-term memory, ensuring that in multi-turn conversations or complex tasks, the agent can reference prior information to generate better responses. Common applications include:

- **Customer Support**: Remembering customer needs and issues across multiple interactions to provide continuous and personalized service.
- **Project Management**: Tracking and recording project progress, task assignments, and related information to aid in decision-making and report generation.
- **Personal Assistant**: Retaining user preferences, schedules, and interaction history to offer customized suggestions and reminders.
- **Research Assistance**: Recording and retrieving relevant research information during scientific processes to aid in literature reviews and data analysis.

## 3. Configuration Method

### Configuration Overview

Configuration files are located in the `configs` directory. The `.yml` files define the behavior, parameters, and model settings for each agent. The Python scripts implement the actual tasks of each agent.

| **File**                     | **Purpose**                                     |
| ---------------------------- | ----------------------------------------------- |
| `configs/memory_config.yml`  | Configures parameters for the Memory process, including model and storage settings. |
| `memory_retrieval.py`        | Executes the context retrieval task.            |
| `reasoner_agent.py`          | Generates intelligent responses based on context. |
| `memory_record.py`           | Records key interaction information into the memory store. |

### Configuration Steps

#### 1. Modify the Configuration File

Edit the `configs/memory_config.yml` file according to your specific needs. You can customize the model parameters and storage paths, but it is recommended not to alter the prompts.

#### 2. Configuration File Example

Below is an example configuration file for the Memory process:

```yaml
config:
  version: "v1.1"
  
  llm:
    provider: openai
    config:
      model: "Qwen/Qwen2.5-32B-Instruct"  # Replace with your model name
      max_tokens: 1500

  vector_store:
    provider: chroma
    config:
      collection_name: "memory_collection"
      path: "./db"

  embedder:
    provider: openai
    config:
      model: "BAAI/bge-large-zh-v1.5"

model:
  model_api_key: "sk-XXXXXXXXXXXXXXXXXXXXXXXX"  # Replace with your API key
  model_api_url: "https://api.siliconflow.cn/v1/"  # Replace with your API URL

user_id: "mofa"
```

### Configuration Details

#### `version`

- **version**: The version of the configuration file, currently set to `v1.1`.

#### `llm` (Large Language Model Configuration)

- **provider**: The language model provider, here it is `openai`.
- **config**: Configuration related to the language model.
  - **model**: The name of the model, e.g., `"Qwen/Qwen2.5-32B-Instruct"`.
  - **max_tokens**: The maximum number of tokens the model can generate, set to `1500`.

#### `vector_store` (Vector Store Configuration)

- **provider**: The vector store provider, here it is `chroma`.
- **config**: Configuration related to the vector store.
  - **collection_name**: The name of the vector collection, set to `"memory_collection"`.
  - **path**: The path to the database file, set to `"./db"`.

#### `embedder` (Embedding Model Configuration)

- **provider**: The embedding model provider, here it is `openai`.
- **config**: Configuration related to the embedding model.
  - **model**: The name of the embedding model, e.g., `"BAAI/bge-large-zh-v1.5"`.

#### `model` (Model API Configuration)

- **model_api_key**: Your model API key, replace with your actual API key, e.g., `"sk-XXXXXXXXXXXXXXXXXXXXXXXX"`.
- **model_api_url**: The URL of the model API, replace with your actual API URL, e.g., `"https://api.siliconflow.cn/v1/"`.

#### `user_id`

- **user_id**: User identifier, set to `"mofa"`. Used to identify and manage different user requests and data.

## 4. Running the Agent

### Using Dora-rs Command Line

1. **Install MoFA Project Dependencies**

   Ensure that you have installed all necessary dependencies for the MoFA project. This typically involves setting up a Python environment and installing required packages.

2. **Start the Agent Process**

   Execute the following command to start the Memory agent process:

   ```bash
   dora up && dora build memory_dataflow.yml && dora start memory_dataflow.yml --attach
   ```

3. **Initiate Task Input**

   Open another terminal window and run `terminal-input`, then input the corresponding task to start the Memory process.

   ```bash
   terminal-input
   Enter your task: Record and retrieve key information about machine learning
   ```
