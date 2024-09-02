# Agent Configuration Documentation

## 1. DSPy-Agent Design Pattern
We use Python and the DSPy library to design Agents.

### DSPy-Agent Advantages
- **Customizable Prompt Framework**: Easily customize prompts without spending extensive time on prompt engineering and optimization. Simply fill in the requirements within the framework.
- **Modular Functionality**: Supports custom modules, allowing you to encapsulate required functions into different modules and call them via Python for various functionalities.
- **Self-Trained Optimizers**: DSPy supports self-trained `Optimizers`, enabling the LLM to understand requirements more efficiently and generate more accurate results that meet specific needs.

### DSPy-Agent Configuration Instructions
We use the `Co-Star` prompt architecture. You can define prompts freely in the Config according to different tags in the prompt framework.

**Note**:
- You can freely delete unnecessary tags, but the Role and Task tags must be retained.
- If RAG participation is not required, you can delete all RAG configurations.
- If `MODULE_PATH` is provided, `RAG_MODEL_NAME` must be null.

```yml
AGENT:
  ROLE:  # AGENT name required   
  BACKSTORY:  # Background information of the AGENT  
  OBJECTIVE: # Clarify the main goal of the task  
  SPECIFICS:  # List the specific requirements of the task   
  ACTIONS: # List the specific steps to be executed  
  RESULTS:  # Describe the expected results or outcomes  
  EXAMPLE:  # Example of the task  
  TASK:  # Task to be performed
RAG:
  MODULE_PATH: null # If there is no local embedding model, you can pass null
  RAG_MODEL_NAME: text-embedding-3-small # OpenAI's embedding model name
  PG_CONNECTION: postgresql+psycopg://langchain:langchain@localhost:6024/langchain  # Configuration path in Pg-Vector
  COLLECTION_NAME: paper # Collection name in Vector, use the default value
  IS_UPLOAD_FILE: true # Whether to upload files to the Vector. Pass true if uploading, otherwise pass false
  FILES_PATH:  # Path of the files to be uploaded
    - ./data/input/moa_llm.pdf
  ENCODING: utf-8  # File encoding format
  CHUNK_SIZE: 256 # Size of the text chunks, recommended default value is 256
  RAG_SEARCH_NUM: 4 # The larger the number, the more results retrieved through RAG, and the more data the LLM receives. Be careful not to exceed the LLM's maximum token limit

MODEL:
  MODEL_API_KEY:
  MODEL_NAME: gpt-3.5-turbo
  MODEL_MAX_TOKENS: 2048

ENV:
  PROXY_URL: http://192.168.31.50:10890
  AGENT_TYPE: reasoner
```
**If you need the configuration for Ollama, please refer to the following content.**:
```yml
MODEL:
  MODEL_API_KEY: ollama
  MODEL_NAME: qwen:14b
  MODEL_MAX_TOKENS: 2048
  MODEL_API_URL: http://192.168.0.75:11434
```


## 2. CrewAI-Agent Design Pattern
We use Python and the CrewAI library to design Agents.

### CrewAI-Agent Advantages
- **Seamless Collaboration**: Achieve seamless collaboration between multiple intelligent agents through modular design and simplicity principles.
- **Flexible Integration**: CrewAI can integrate with tools like LangChain, providing users with great flexibility. We can also customize different functions, allowing CrewAI to automatically call and implement them according to task requirements.

### CrewAI-Agent Configuration Instructions
**Note**:
- Specify the configuration parameters of the tools used in the `tasks/description` or in the `agents/backstory`.
- You can define multiple agents in `agents` and set multiple tasks in `tasks`, but each task can only be assigned to one agent.

```yml
agents:
  - name: rag_agent  # Define the agent name
    role: 'The RAG agent serves as an intelligent assistant, retrieving information from a vector database and generating contextually appropriate responses. It uses advanced natural language processing and efficient data retrieval.'  # Define the role and responsibilities of the agent
    goal: 'The agent combines retrieval and generation to meet user needs, ensuring responses are accurate and relevant.'  # Define the goal of the agent
    backstory: |  # Provide the background information of the agent. You can also place your prompt here.
      #### Objective:
    
      #### Specifics:
   
      #### Tasks:
    
      #### Actions:
    
      #### Results:
    verbose: true  # Whether to output detailed information (default value, do not modify unless debugging)
    allow_delegation: false  # Whether to allow task delegation (default value, do not modify unless debugging)
    tools:  # List of tools that the agent can use
      - delete_vector_collection_with_tool
      - upload_files_to_vector_with_tool
      - search_vector_with_tool

tasks:
  - description: |  # Describe the specific content of the task
      module_path: '/mnt/d/models/embeddings/bce-embedding-base_v1'
      collection_name: 'mae'
      is_upload_file: True
      multi_process: False
      pg_connection: 'postgresql+psycopg://mae:MLbDGKC7d7IPBN@124.156.214.116:6024/mae_db'
      files_path: ['./data/input/moa_llm.pdf']
     
      The task is: Summarize the content of the paper "Mixture-of-Agents Enhances Large Language Model Capabilities," specifying the author, date, key points, and achievements of the paper.
    expected_output: 'details'  # Expected output format
    agent: rag_agent  # Specify the agent responsible for executing the task
    max_inter: 1  # Maximum number of interactions
    human_input: false  # Whether human input is required

model:
  model_api_key:  # Model API key
    Description: Model API key
  model_name: gpt-3.5-turbo  # Model name
  model_max_tokens: 2048  # Maximum token count for the model
  module_api_url: null  # Module API URL

other:
  proxy_url: http://192.168.0.75:10809  # Proxy URL for network requests. Configure proxy if located in China

env:
  SERPER_API_KEY:     # SERPER API key
  AGENTOPS_API_KEY: 6805b2d1-50f8-4b7c-b88b-cff2b1c6ef27  # AGENTOPS API key

crewai_config:
  memory: false  # Whether to enable memory
```

**Language**: 
- [简体中文](Agent_Config_zh.md)