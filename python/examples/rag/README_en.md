# RAG Process Example in MoFA

## 1. Functionality

In MoFA, the **RAG (Retrieval-Augmented Generation)** agent is responsible for providing more accurate and relevant responses by combining retrieval and generation models. The design pattern of the RAG agent includes **File Upload and Encoding + Vector Retrieval + Context Generation + Intelligent Response**. This process ensures that the agent can utilize external documents and contextual information to generate high-quality, content-specific answers, thereby enhancing the user interaction experience.

## 2. Use Cases

The RAG agent is suitable for tasks that require information retrieval and generation by integrating external knowledge bases or documents. It ensures that in multi-turn conversations or complex tasks, the agent can reference relevant external materials to generate more detailed and accurate responses. Common applications include:

- **Knowledge Q&A**: Providing accurate answers by retrieving relevant documents, suitable for education, training, and other fields.
- **Content Generation**: Creating customized content based on specific documents or materials, such as reports and article writing.
- **Technical Support**: Retrieving technical documents or manuals to offer detailed solutions and operational guidance.
- **Legal Consultation**: Referencing legal literature and cases to generate compliant and evidence-based legal advice.

## 3. Configuration Method

### Configuration Overview

The configuration files for the RAG agent are located in the `configs` directory. The `.yml` files define various parameters of the RAG process, including model settings, storage paths, and related operations. Node configurations are defined within the configuration files and are responsible for executing specific tasks and data flow.

### Configuration Steps

#### 1. Modify the Configuration File

Edit the `configs/rag_retrieval.yml` file according to your specific needs. You can customize RAG-related parameters such as model name, API keys, file paths, etc. Ensure that all necessary paths and key information are correctly configured to allow the agent to operate smoothly.

#### 2. Example Configuration File

Below is an example configuration file for the RAG process:

```yaml
RAG:
  RAG_ENABLE: true
  MODULE_PATH: null  # If you have a custom module path, uncomment and set the path
  COLLECTION_NAME: mofa
  IS_UPLOAD_FILE: true
  CHROMA_PATH: ./data/output/chroma_store
  FILES_PATH:
    - /Users/chenzi/project/zcbc/mofa/python/examples/rag/data/input/2410.02742v1.pdf
  ENCODING: utf-8
  CHUNK_SIZE: 256
  RAG_SEARCH_NUM: 6
  RAG_MODEL_NAME: netease-youdao/bce-embedding-base_v1
  RAG_MODEL_API_URL: https://api.siliconflow.cn/v1
  RAG_MODEL_API_KEY: sk-

MODEL:
  MODEL_API_KEY: sk-XXXXXXXXXXXXXXXXXXXXXXXX  # Replace with your API key
  MODEL_NAME: Qwen/Qwen2.5-72B-Instruct  # Replace with your model name
  MODEL_API_URL: https://api.siliconflow.cn/v1/chat/completions
```

### Configuration Details

#### `RAG_ENABLE`

- **RAG_ENABLE**: Enables or disables the RAG functionality. Set to `true` to enable RAG.

#### `MODULE_PATH`

- **MODULE_PATH**: The path to a custom module. If using the default module, keep it as `null`.

#### `COLLECTION_NAME`

- **COLLECTION_NAME**: The name of the vector storage collection, set to `"mofa"`.

#### `IS_UPLOAD_FILE`

- **IS_UPLOAD_FILE**: Determines whether file upload functionality is enabled. Set to `true` to allow file uploads.

#### `CHROMA_PATH`

- **CHROMA_PATH**: The path to the vector storage database, set to `"./data/output/chroma_store"`.

#### `FILES_PATH`

- **FILES_PATH**: A list of file paths to be uploaded and processed. For example:
  ```yaml
  FILES_PATH:
    - /path/to/your/document1.pdf
    - /path/to/your/document2.pdf
  ```

#### `ENCODING`

- **ENCODING**: The file encoding format, typically set to `"utf-8"`.

#### `CHUNK_SIZE`

- **CHUNK_SIZE**: The size of document chunks, set to `256` to ensure effective vector retrieval.

#### `RAG_SEARCH_NUM`

- **RAG_SEARCH_NUM**: The number of relevant documents returned per retrieval, set to `6`.

#### `RAG_MODEL_NAME`

- **RAG_MODEL_NAME**: The name of the model used for embedding, for example, `"netease-youdao/bce-embedding-base_v1"`.

#### `RAG_MODEL_API_URL`

- **RAG_MODEL_API_URL**: The API URL of the RAG model, for example, `"https://api.siliconflow.cn/v1"`.

#### `RAG_MODEL_API_KEY`

- **RAG_MODEL_API_KEY**: The API key for the RAG model. Please replace it with your actual key, for example, `"   "`.

#### `MODEL` (Generation Model Configuration)

- **MODEL_API_KEY**: Your generation model API key. Please replace it with your actual key, for example, `"sk-XXXXXXXXXXXXXXXXXXXXXXXX"`.
- **MODEL_NAME**: The name of the generation model, for example, `"Qwen/Qwen2.5-72B-Instruct"`.
- **MODEL_API_URL**: The API URL of the generation model, for example, `"https://api.siliconflow.cn/v1/chat/completions"`.

### Node Configuration

The node configuration for the RAG agent is as follows:

```yaml
nodes:
  - id: terminal-input
    build: pip install -e ../../node-hub/terminal-input
    path: dynamic
    outputs:
      - data
    inputs:
      context_rag: rag-retrieval/context_rag
      reasoner_response: reasoner-agent/reasoner_response

  - id: rag-retrieval
    operator:
      python: ./scripts/rag_retrieval.py
      inputs:
        task: terminal-input/data
      outputs:
        - context_rag

  - id: reasoner-agent
    operator:
      python: scripts/reasoner_agent.py
      inputs:
        task: terminal-input/data
        context_rag: rag-retrieval/context_rag
      outputs:
        - reasoner_response
```

#### Node Descriptions

- **terminal-input**: Responsible for receiving user input tasks and passing the data to downstream nodes.
- **rag-retrieval**: Executes the RAG retrieval task, retrieving relevant context from the vector storage based on the user's input task.
- **reasoner-agent**: Generates intelligent responses based on the retrieved context and the user's task.

## 4. Running the Agent

### Using Dora-rs Command Line

1. **Start the RAG Agent Process**

   Execute the following command to start the RAG agent process:

   ```bash
   dora up && dora build rag_dataflow.yml && dora start rag_dataflow.yml --attach
   ```

2. **Initialize Task Input**

   Open another terminal window and run `terminal-input`, then enter the corresponding task to initiate the RAG process.

   ```bash
   terminal-input
   Enter your task: Provide key information recording and retrieval about machine learning
   ```

