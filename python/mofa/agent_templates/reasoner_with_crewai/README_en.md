Here is the optimized and translated version of the content:

---

# Reasoner Template

The most basic implementation of the agent design pattern in MoFA.

**Language**

## 1. Functionality Overview

The Reasoner is perhaps the simplest type of agent. Its design pattern consists of a customized large language model (LLM) prompt + reasoning from the LLM. Currently, the Reasoner is implemented using the `CrewAI` framework.

## 2. Use Cases

The Reasoner is used when you want to customize the prompt of a large language model.
For example:

- Create an agent that chats with users in the tone of "Einstein."
- Develop an agent that breaks down a question into five smaller questions.

## 3. Configuration Method

The basic principle of configuration is to generate a customized agent by modifying the configuration information in the Reasoner template.

### Method 1: Using a Text Editor to Modify the MoFA Configuration File

1. Template Copy: Copy the subdirectory containing the agent template (Reasoner) to your specified directory (e.g., `hello_world`). The directory will contain two folders and three files:

   | File                                         | Description                                                   |
   |----------------------------------------------|---------------------------------------------------------------|
   | `reasoner_dataflow.yml`                      | Dora data flow configuration file                             |
   | `configs/reasoner_agent_with_crewai.yml`     | MoFA configuration file, including LLM-related and prompt customization parameters. |
   | `scripts/reasoner_agent.py`                  | Python operator tool for the functionality the agent needs to perform |

2. Agent Renaming: You can rename your agent. For instance, if you want your agent to be called "Hello World," you can rename the files as follows:

   | File                         | Description                            |
   | ---------------------------- | -------------------------------------- |
   | `reasoner_dataflow.yml`       | `hello_world_dataflow.yml`             |
   | `configs/reasoner_agent.yml`  | `configs/hello_world_agent.yml`        |
   | `scripts/reasoner_agent.py`   | No need to rename                      |

3. Modify Configuration

   | File                              | Description |
   | --------------------------------- | ----------------------------------------------------------------------------------- |
   | `hello_world_dataflow.yml`        | Modify the path for `build: pip install -e ../../../node-hub/terminal-input` to match your directory structure (absolute path can be used). |
   | `configs/hello_world_agent.yml`   | Customize prompts and LLM parameters as needed, including RAG.                      |
   | `scripts/reasoner_agent.py`       | Update the `yaml_file_path` variable to point to the correct path of the `yml` file in the config. |

4. CrewAI-Agent Configuration

```yml
agents:
  - name: rag_agent  # Define the agent name
    role: ''  # Define the agent's role and responsibilities
    goal: ''  # Define the agent's goal
    backstory: |  # Provide background information for the agent. You can also place the prompt here.
      #### Goals:
    
      #### Specific Requirements:
   
      #### Tasks:
    
      #### Actions:
    
      #### Results:
    verbose: true  # Enable detailed output (leave as default unless debugging)
    allow_delegation: false  # Allow task delegation (leave as default unless necessary)
    tools:  # List of tools the agent can use; leave empty if not applicable
      - delete_vector_collection_with_tool

tasks:
  - description: null  # Task description; if the tool needs specific parameters, add them here or in the backstory
    expected_output: 'details'  # Expected output format
    agent: rag_agent  # Assign the task to the agent
    max_inter: 1  # Maximum number of interactions
    human_input: false  # Whether human input is required

model:
  model_api_key:  # Model API key
  model_name: gpt-3.5-turbo  # Model name
  model_max_tokens: 2048  # Maximum token limit
  module_api_url: null  # Module API URL

other:
  proxy_url: null  # Proxy URL for network requests (configure this if operating in China)

env:
  SERPER_API_KEY:  # SERPER API key

crewai_config:
  memory: false  # Enable memory functionality or not
```

### Method 2: MoFA IDE

(TBD)

## 4. Running the Agent

### Method 1: Running in Dora-rs Command:

1. Install the MoFA project package.
2. Run `dora up && dora build reasoner_dataflow.yml && dora start reasoner_dataflow.yml`.
3. Open another terminal and run `terminal-input`, then input the desired task.

### Method 2: Running in the MoFA Environment:

(TBD)

--- 

Let me know if you need further adjustments!