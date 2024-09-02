
# Set Up


## Table of Contents

1. [Mae Project Installation](#mae-project-installation)
   1. [Environment Setup](#environment-setup)
   2. [Install the Project](#install-the-project)
2. [Rust Environment Installation](#rust-environment-installation)
3. [Project Structure](#project-structure)
   1. [Main Directory `mae`](#main-directory-mae)
      - [Module `apps`](#module-apps)
      - [Module `kernel`](#module-kernel)
      - [Module `run`](#module-run)
      - [Module `utils`](#module-utils)
   2. [Directory `tests`](#directory-tests)
   3. [Root Directory Files](#root-directory-files)
4. [Example Project Startup](#example-project-startup)
   1. [Example Project Structure](#example-project-structure)
   2. [Configuration Description](#configuration-description)
      - [Rag-Agent Configuration](#rag-agent-configuration)
      - [Crewai Configuration](#crewai-configuration)
5. [Startup Notes](#startup-notes)
6. [Frequently Asked Questions (FAQ)](#frequently-asked-questions-faq)

## Mae Project Installation

### Environment Setup

It is recommended to use the `Dockerfile` to set up the environment. We have already installed `Rust` and `Python` in the `Dockerfile`.

```sh
docker build -t mae_env:v1 .
```

### Install the Project

- Clone the project:

```sh
git clone <repository-url>
```

- Switch to Python 3.10 environment:
  - If there is a version mismatch, use conda to create the environment:

```sh
conda create -n py310 python=3.10.12 -y
```

- Install the mae project:

```sh
pip3 install -r requirements.txt && pip3 install -e .
```

## Rust Environment Installation

Install the Rust environment according to your system:

```sh
https://www.rust-lang.org/tools/install
```

Then install the dora-rs package:

```sh
cargo install dora-cli --locked
```

## Project Structure

### Main Directory `mae`

Contains all application and kernel code.

#### Module `apps`

Contains multiple Agent application modules, each module has a specific function.

#### Module `kernel`

Core function modules of the app, including memory, planning, retrieval, tools, and utility sub-modules.

- **`memory/`**: Responsible for memory-related functions.
- **`planning/`**: Responsible for planning-related functions.
- **`rag/`**: Responsible for Retrieval-Augmented Generation (RAG) related functions.
- **`tools/`**: Contains various tools for the Agent.
- **`utils/`**: Utility module, providing various auxiliary functions.

#### Module `run`

Responsible for running modules, including scripts required at runtime.

- **`run.py`**: Main script for running the project.

#### Module `utils`

General utility module for the project.

### Directory `tests`

Contains test files and configurations to ensure the correct functionality of the project.

### Root Directory Files

- **`.dockerignore`**: Docker ignore file, defines which files and directories are ignored when building Docker images.
- **`.gitignore`**: Git ignore file, defines which files and directories are ignored in version control.
- **`CONTRIBUTING.rst`**: Project contribution guide, instructs how to contribute to the project.
- **`Dockerfile`**: Docker configuration file for building the project Docker image.
- **`HISTORY.rst`**: Project history file, records project updates and changes.
- **`MANIFEST.in`**: Defines which files are included when packaging the project.
- **`README.md`**: Main project description file, provides an overview and usage guide.
- **`README.rst`**: reStructuredText version of the main project description file.
- **`requirements.txt`**: Python dependencies file, lists all Python packages required by the project.
- **`setup.cfg`**: Project configuration file, includes packaging and metadata information.
- **`setup.py`**: Project installation script for installing and packaging the project.

## Example Project Startup

### Example Project Structure

```text
agents
└── reasoner  # Agent name
    ├── README.md  
    ├── data  # Data storage directory
    │   └── input  # Input data
    │       └── moa_llm.pdf 
    ├── listener.py  # Responsible for listening to the results in the dora flow
    ├── out # dora flow output
    ├── reasoner_dataflow.yml # dora flow configuration file
    ├── reasoning_agent.py # Agent logic
    ├── reasoning_loader.py  # Load agent configuration file
    ├── result  # Use case output save directory
    └── use_case  # Use case configuration file
        ├── phrase_spelling_error_by_dspy.yml  # Spelling error example
        ├── snake_game_build_by_dspy.yml  # Snake game example
        └── summarize_pdf_by_rag.yml # Paper RAG extraction summary
```

### Task Configuration Description

#### Rag-Agent Task Configuration

```text
agents:
  - name: rag_agent  # Define the name of the agent.
    role: 'The RAG agent serves as an intelligent assistant, retrieving information from a vector database and generating contextually appropriate responses. It uses advanced natural language processing and efficient data retrieval.'  # Define the role and responsibilities of the agent.
    goal: 'The agent combines retrieval and generation to meet user needs, ensuring responses are accurate and relevant.'  # Define the goal of the agent.
    backstory: |  # Provide the background information of the agent. You can also put your prompt in here.
      #### Objective:
    
      #### Specifics:
   
      #### Tasks:
    
      #### Actions:
    
      #### Results:
    verbose: true  # Whether to output detailed information. (Default value, do not modify unless debugging)
    allow_delegation: false  # Whether to allow delegation. (Default value, do not modify unless debugging)
    tools:  # List of tools that the agent can use.
      - delete_vector_collection_with_tool
      - upload_files_to_vector_with_tool
      - search_vector_with_tool

tasks:
  - description: |  # Describe the specific content of the task.
      module_path: '/mnt/d/models/embeddings/bce-embedding-base_v1'
      collection_name: 'mae'
      is_upload_file: True
      multi_process: False
      pg_connection: 'postgresql+psycopg://mae:MLbDGKC7d7IPBN@124.156.214.116:6024/mae_db'
      files_path: ['./data/input/moa_llm.pdf']
     
      Below is the task: Summarize the content of the paper "Mixture-of-Agents Enhances Large Language Model Capabilities," and specify the author, date, key points, and the achievements of the paper.
    expected_output: 'details'  # Expected output.
    agent: rag_agent  # Specify the agent responsible for executing the task.
    max_inter: 1  # Maximum number of interactions.
    human_input: false  # Whether human input is required.

model:
  model_api_key:  # Model API key.
    Description: Model API key.
  model_name: gpt-3.5-turbo  # Model name.
  model_max_tokens: 2048  # Maximum token number of the model.
  module_api_url: null  # Module API URL.

other:
  proxy_url: http://192.168.0.75:10809  # Proxy URL for network requests. Configure proxy if located in China.

env:
  SERPER_API_KEY:     # SERPER API key.
  AGENTOPS_API_KEY: 6805b2d1-50f8-4b7c-b88b-cff2b1c6ef27  # AGENTOPS API key.

crewai_config:
  memory: false  # Whether to enable memory.

```

#### Crewai Task Configuration

```text
agents:
  - name: rag_agent  # Define the name of the agent.
    role: 'The RAG agent serves as an intelligent assistant, retrieving information from a vector database and generating contextually appropriate responses. It uses advanced natural language processing and efficient data retrieval.'  # Define the role and responsibilities of the agent.
    goal: 'The agent combines retrieval and generation to meet user needs, ensuring responses are accurate and relevant.'  # Define the goal of the agent.
    backstory: |  # Provide the background information of the agent. You can also put your prompt in here.
      #### Objective:
    
      #### Specifics:
   
      #### Tasks:
    
      #### Actions:
    
      #### Results:
    verbose: true  # Whether to output detailed information. (Default value, do not modify unless debugging)
    allow_delegation: false  # Whether to allow delegation. (Default value, do not modify unless debugging)
    tools:  # List of tools that the agent can use.
      - delete_vector_collection_with_tool
      - upload_files_to_vector_with_tool
      - search_vector_with_tool

tasks:
  - description: |  # Describe the specific content of the task.
      module_path: '/mnt/d/models/embeddings/bce-embedding-base_v1'
      collection_name: 'mae'
      is_upload_file: True
      multi_process: False
      pg_connection: 'postgresql+psycopg://mae:MLbDGKC7d7IPBN@124.156.214.116:6024/mae_db'
      files_path: ['./data/input/moa_llm.pdf']
     
      Below is the task: Summarize the content of the paper "Mixture-of-Agents Enhances Large Language Model Capabilities," and specify the author, date, key points, and the achievements of the paper.
    expected_output: 'details'  # Expected output.
    agent: rag_agent  # Specify the agent responsible for executing the task.
    max_inter: 1  # Maximum number of interactions.
    human_input: false  # Whether human input is required.

model:
  model_api_key:  # Model API key.
    Description: Model API key.
  model_name: gpt-3.5-turbo  # Model name.
  model_max_tokens: 2048  # Maximum token number of the model.
  module_api_url: null  # Module API URL.

other:
  proxy_url: http://192.168.0.75:10809  # Proxy URL for network requests. Configure proxy if located in China.

env:
  SERPER_API_KEY:     # SERPER API key.
  AGENTOPS_API_KEY: 6805b2d1-50f8-4b7c-b88b-cff2b1c6ef27  # AGENTOPS API key.

crewai_config:
  memory: false  # Whether to enable memory.


```
**Note**: In Crewai, you can define multiple agents and tasks, but each task must have one responsible agent. It does not support multiple agents for one task.


## Startup Notes

1. Start the dataflow process:

```sh
dora up
```

2. If you need to switch to a different use case, go to `reasoning_loader.py` and modify line 17 to the use case you want to run:

```python
params = read_yaml('use_case/summarize_pdf_by_rag.yml')  # Modify the yml file path and name
```

3. In each use case, you need to define the API key for your model; otherwise, it will not work (recommend using gpt-3.5-turbo).

4. How to use Rag-UseCase?

   The Rag use case ends with Rag, for example, `summarize_pdf_by_rag.yml`.

   Since our Rag Vector database uses Postgres-Vector, we must run a Vector database locally (based on Docker).

```sh
docker run --name pgvector-container -e POSTGRES_USER=langchain -e POSTGRES_PASSWORD=langchain -e POSTGRES_DB=langchain -p 6024:5432 -d pgvector/pgvector:pg16
```

   If you do not have Docker, you can use our public test Pg-Vector account and password. (Note, this account and password may be destroyed for security reasons. Please try connecting to this database to ensure it is available before using).

```sh
postgresql+psycopg://mae:MLbDGKC7d7IPBN@124.156.214.116:6024/mae_db
```

   We can use either OpenAI or local embedding models. If you need a local embedding model, download it from Huggingface and point to the local path in the configuration.

   Rag currently only supports `Txt` and `Pdf` file formats.

5. Run the Dora process:

```sh
dora start reasoner_dataflow.yml --attach
```

## Frequently Asked Questions (FAQ)

**Q: What should I do if I encounter version incompatibility issues while running the project?**

A: Ensure your environment is Python 3.10 or above. If there is a version incompatibility, use conda to create a Python 3.10 environment.

**Q: How do I switch to a different use case?**

A: Modify line 17 in the `reasoning_loader.py` file to point to the use case configuration file you want to run.

**Q: What are the connection details for the Postgres-Vector database?**

A: If using a locally run Docker database, the connection details are:

```sh
postgresql+psycopg://langchain:langchain@localhost:6024/langchain
```

   If using the public test Pg-Vector database, the connection details are:

```sh
postgresql+psycopg://mae:MLbDGKC7d7IPBN@124.156.214.116:6024/mae_db
```

**Q: Why is my Rag-UseCase not returning the expected results?**

A: Check that your embedding model configuration is correct and ensure your Postgres-Vector database is running properly.
```

