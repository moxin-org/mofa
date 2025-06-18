# memory_chat_assistant

A Dora node providing a memory-augmented chat assistant using OpenAI and mem0, compliant with the mofa-agent protocol. Easily integrates LLM responses with user-specific memory retrieval for enhanced, contextualized answers in your dataflow pipelines.

## Features
- Memory-augmented language model answering
- Secure API integration with OpenAI and mem0
- YAML-configurable agent behavior

## Getting Started

### Installation
Install via cargo:
```bash
pip install -e .
```

## Basic Usage

Create a YAML config (e.g., `demo.yml`):

```yaml
nodes:
  - id: memory_chat_assistant
    build: pip install -e memory_chat_assistant
    path: memory_chat_assistant
    inputs:
      user_input: input/user_input
    outputs:
      - assistant_response
    env:
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      MEM0_API_KEY: ${MEM0_API_KEY}
      MOFA_AGENT_CONFIG: configs/agent.yml
```

Run the demo:

```bash
dora build demo.yml
dora start demo.yml
```


## Integration with Other Nodes

To connect with your existing node:

```yaml
- id: user_input_node
  build: pip install -e your-input-node
  path: your-input-node
  outputs:
    - user_input

- id: memory_chat_assistant
  build: pip install -e memory_chat_assistant
  path: memory_chat_assistant
  inputs:
    user_input: user_input_node/user_input
  outputs:
    - assistant_response
```

Your point source must output:

* Topic: `user_input`
* Data: string (user question or prompt)
* Metadata:

  ```json
  {
    "type": "string",
    "required": true,
    "description": "User's message for the chat assistant."
  }
  ```

## Node Reference

### Input Topics

| Topic        | Type   | Description                      |
| ------------| ------ | -------------------------------- |
| user_input  | string | Message/question from the user    |

### Output Topics

| Topic             | Type   | Description                         |
| ----------------- | ------ | ----------------------------------- |
| assistant_response| string | Model's contextualized response     |


## License

Released under the MIT License.
