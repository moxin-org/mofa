# xMind -- AgentFlow Framework

**xMind** is a modular framework built with XLang, designed to implement Large Language Model (LLM) Memory, Planning, and Agent-flow capabilities. This project allows developers to seamlessly integrate advanced AI features like context retention, decision-making, and dynamic dataflows into their applications.

## Features

- **LLM Memory**: Retain and utilize context across sessions to enhance interaction and decision-making.
- **Planning**: Implement sophisticated planning mechanisms that allow LLMs to make informed decisions based on historical data and projected outcomes.
- **Agent-flow Management**: Orchestrate complex Agent-flows to streamline processing and enhance the performance of AI-driven applications.
- **Modular Design**: Easily extend and customize the framework to fit your specific needs.  

[AgentFlow Graph](./AgentFlow.md)

## Getting Started

### Prerequisites

- [XLang](https://github.com/xlang-foundation/xlang) Please clone XLang into the xMind/ThirdParty folder and ensure the folder is named xlang.

### Build the Framework

Clone the repository:

```bash
git clone https://github.com/xlang-foundation/xMind.git
cd xMind
mkdir build
cd build
cmake ..
make

```

## Terms and Concepts

1. **Blueprint**: A YAML-based structure used to define various elements such as variables, prompts, actions, and more.

2. **Variable**: 
   - **Scope**: Variables are global within the same file and do not require a prefix. 
   - **Cross-File Access**: When accessing a variable from another file, a prefix must be used, e.g., `file1.var1`.

3. **Node**: 
   - Represents a component in AgentFlow, using a graph-based approach to connect various nodes.

4. **Function**:
   - A node within AgentFlow that serves as an inline translate node. It supports only one input and one output.

5. **Action**:
   - A buffered node in AgentFlow that processes input through a separate thread (in XLang) or a process (in Python).
   - **Use Case**: Actions are typically used to connect to external environments such as REST APIs, file access, or UIs.

6. **Agent**:
   - A specialized node within AgentFlow that performs LLM (Large Language Model) inference. 
   - **Core Node**: It serves as the core of AgentFlow, buffering inputs and combining them with prompts from various sources before making an inference request to an LLM.

7. **LlmPool**:
   - Managed by xMind, this concept involves handling LLM requests in a pool, based on factors like HTTP request status and LLM key usage time limits.
8. **Session Memory**: 
   - Session Persistence: Each chat completion is maintained within a session, ensuring continuity across interactions.
   - Session Identifiers: Externally, each session is identified by a globally unique identifier (GUID). Internally, sessions are tracked using an integer that loops for efficient resource management.
   - Node Data Handling: The first item in each node’s input and output data is the internal session ID. This approach allows a single graph instance to serve multiple chat instances, optimizing resource usage.
   - Session Memory: Sessions maintain a history of interactions as session memory. When making requests, this history is automatically bound as part of the prompt, ensuring context is preserved.
   - LLM Output Integration: All outputs from the language model (LLM) are fed back into the session memory, continuously enriching the session’s context.
### Running the Framework
  [Start Guide](./Start.md)

### CLI - xmcli
  [CLI](./xmcli.md)
