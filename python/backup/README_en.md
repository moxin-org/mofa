# Project Installation and Startup Guide

**Language**
- [中文](README_en.md)

## Table of Contents

1. [Installing the Mae Project](#1-installing-the-mae-project)
   1. [Setting Up the Project Environment](#11-setting-up-the-project-environment)
   2. [Installing the Project](#12-installing-the-project)
2. [Installing the Rust Environment](#2-installing-the-rust-environment)
3. [Project Structure Explanation](#3-project-structure-explanation)
   1. [Main Project Directory `mae/`](#main-project-directory-mae)
      - [Module `apps/`](#module-apps)
      - [Module `kernel/`](#module-kernel)
      - [Module `run/`](#module-run)
      - [Module `utils/`](#module-utils)
   2. [Directory `tests/`](#directory-tests)
   3. [Root Directory Files](#root-directory-files)
4. [Starting the Example Project](#4-starting-the-example-project)
   1. [Example Project Structure Explanation](#41-example-project-structure-explanation)
   2. [Configuration Instructions](#42-configuration-instructions)
      - [Rag-Agent Configuration Instructions](#421-rag-agent-configuration-instructions)
      - [Crewai Configuration Instructions](#422-crewai-configuration-instructions)
5. [Startup Considerations](#5-startup-considerations)
6. [Frequently Asked Questions (FAQ)](#6-frequently-asked-questions-faq)

## 1. Installing the Mae Project

### 1.1 Setting Up the Project Environment
It is recommended to use the `Dockerfile` to set up the current environment. The `Dockerfile` already includes the installation of `Rust` and `Python`.
```sh
docker build -t mae_env:v1 .
```

### 1.2 Installing the Project

- Clone the project:
```sh
git clone <repository-url>
```
- Switch to the Python 3.10 environment:
  - If there is a version mismatch, use conda to create a new environment:
  ```sh
  conda create -n py310 python=3.10.12 -y
  ```
- Install the Mae project:
```sh
pip3 install -r requirements.txt && pip3 install -e .
```

## 2. Installing the Rust Environment
Install Rust based on your system:
```sh
https://www.rust-lang.org/tools/install
```

Then, install the `dora-rs` package:
```sh
cargo install dora-cli --locked
```

## 3. Project Structure Explanation

### Main Project Directory `mae/`
Contains all applications and kernel code.

#### Module `apps/`
Contains multiple Agent application modules, each with specific functionality.

#### Module `kernel/`
Core functionality modules of the app, including submodules for memory, planning, retrieval, tools, and utilities.
- **`memory/`**: Handles memory-related functionalities.
- **`planning/`**: Handles planning-related functionalities.
- **`rag/`**: Handles retrieval-augmented generation (RAG) functionalities.
- **`tools/`**: Contains various tool modules for the Agent.
- **`utils/`**: Utility modules providing various auxiliary functions.

#### Module `run/`
Handles runtime modules, including scripts needed for running the project.
- **`run.py`**: Main script for running the project.

#### Module `utils/`
General utility modules for the project.

### Directory `tests/`
Contains test files and configurations to ensure the correctness of the project's functionality.

### Root Directory Files
- **`.dockerignore`**: Specifies files and directories to ignore when building the Docker image.
- **`.gitignore`**: Specifies files and directories to ignore in version control.
- **`CONTRIBUTING.rst`**: Guidelines for contributing to the project.
- **`Dockerfile`**: Configuration file for building the project's Docker image.
- **`HISTORY.rst`**: Records updates and changes to the project.
- **`MANIFEST.in`**: Specifies files to include when packaging the project.
- **`README.md`**: Main project description and usage guide.
- **`README.rst`**: reStructuredText version of the main project description.
- **`requirements.txt`**: Lists all Python dependencies for the project.
- **`setup.cfg`**: Configuration file for packaging and metadata.
- **`setup.py`**: Script for installing and packaging the project.

## 4. Starting the Example Project

### 4.1 Example Project Structure Explanation
```plaintext
agents
└── reasoner  # agent name
    ├── README.md  
    ├── data  # Data storage directory
    │   └── input  # Input data
    │       └── moa_llm.pdf 
    ├── listener.py  # Listens for results in the dora process
    ├── out  # Output of the dora process
    │   ├── 019073e3-febd-7538-8ece-1ac71284ac4c
    │   └── 019073e6-71e7-7d81-87d3-d0726c9ceee5
    │       ├── log_agents.txt
    │       ├── log_listener.txt
    │       └── log_loader.txt
    ├── reasoner_dataflow.yml  # Dora process configuration file
    ├── reasoning_agent.py  # Agent logic
    ├── reasoning_loader.py  # Loads agent configuration files
    ├── result  # Output directory for use case results
    └── use_case  # Use case configuration files
        ├── phrase_spelling_error_by_dspy.yml  # Spelling error example
        ├── snake_game_build_by_dspy.yml  # Snake game example
        └── summarize_pdf_by_rag.yml  # Paper summary using RAG
```

### 4.2 Configuration Instructions
[Agent Configuration Instructions](../docs/config/Agent_Config_en.md)

## 5. Startup Considerations

1. Start the dataflow process:
```sh
dora up
```

2. If you need to switch between different use cases, modify line 17 in [reasoning_loader.py](../examples/agents/reasoner/reasoning_loader.py) to the use case you want to run:
```python
params = read_yaml('use_case/summarize_pdf_by_rag.yml')  # Change this to the desired YAML file path and name
```

3. Define the API key for your model in each use case, as it is required (recommended to use gpt-3.5-turbo).

4. How to use Rag-UseCase?
- Rag use cases end with `Rag`, for example `summarize_pdf_by_rag.yml`.
- Since the Rag Vector database uses Postgres-Vector, you must run a local Vector database (based on Docker):
```sh
docker run --name pgvector-container -e POSTGRES_USER=langchain -e POSTGRES_PASSWORD=langchain -e POSTGRES_DB=langchain -p 6024:5432 -d pgvector/pgvector:pg16
```
- If you don't have Docker, you can use our public test Pg-Vector account and password. (Note: This account may be disabled for security reasons. Check the database connection before using it.)
```sh
postgresql+psycopg://mofa:MLbDGKC7d7IPBN@124.156.214.116:6024/mae_db
```
- Rag currently only supports `Txt` and `Pdf` file formats.

5. Run the Dora process:
```sh
dora start reasoner_dataflow.yml --attach
```

## 6. Frequently Asked Questions (FAQ)

**Q: What should I do if I encounter version compatibility issues while running the project?**
A: Ensure your environment is Python 3.10 or higher. If there is a version incompatibility, use conda to create a Python 3.10 environment.

**Q: How do I switch between different use cases?**
A: Modify line 17 in the `reasoning_loader.py` file to point to the use case configuration file you want to run.

**Q: What is the connection information for the Postgres-Vector database?**
A: If using a locally run Docker database, the connection information is:
```sh
postgresql+psycopg://langchain:langchain@localhost:6024/langchain
```
If using the public test Pg-Vector database, the connection information is:
```sh
postgresql+psycopg://mofa:MLbDGKC7d7IPBN@124.156.214.116:6024/mae_db
```

**Q: Why is my Rag-UseCase not returning the expected results?**
A: Check if your embedding model configuration is correct and ensure your Postgres-Vector database is running properly.

We hope this guide is helpful. If you have any questions, please feel free to contact us.