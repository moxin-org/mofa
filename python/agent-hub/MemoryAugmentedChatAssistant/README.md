# memory_augmented_chat

A Dora node that provides a memory-augmented, OpenAI GPT-based conversational assistant. User queries are answered using both retrieval-augmented generation from a persistent memory backend (mem0) and LLM completions. Intended for stateless operation, with per-user memory retrieval and adaptive persona.

## Features
- Memory augmentation with per-user retrieval from mem0 backend
- Stateless, easily-launched Dora node (parameter-only interface)
- Integrates OpenAI's GPT models for context-aware, personalized responses

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
  - id: chat-assistant
    build: pip install -e .
    path: memory_augmented_chat
    inputs:
      user_input: input/user_input
      user_id: input/user_id
    outputs:
      - assistant_response
```

Run the demo:

```bash
dora build demo.yml
dora start demo.yml
```

## Integration with Other Nodes

To connect with your existing node:

```yaml
nodes:
  - id: user_input_source
    build: pip install my-user-input-source
    path: my_user_input_source
    outputs:
      - user_input
      - user_id
  - id: chat-assistant
    build: pip install -e .
    path: memory_augmented_chat
    inputs:
      user_input: user_input_source/user_input
      user_id: user_input_source/user_id
    outputs:
      - assistant_response
```

Your point source must output:

* Topic: `user_input` and optionally `user_id`
* Data: User message as string (and optionally user id as string)
* Metadata:

  ```json
  {
    "dtype": "str",
    "desc": "user message (and user id, if present) as UTF-8 string"
  }
  ```

## API Reference

### Input Topics

| Topic      | Type   | Description                  |
| ---------- | ------ | --------------------------- |
| user_input | str    | User's message/query string  |
| user_id    | str    | (Optional) Unique user ID    |

### Output Topics

| Topic              | Type   | Description                                   |
| ------------------ | ------ | --------------------------------------------- |
| assistant_response | str    | Generated assistant reply (or error message)  |

## License

Released under the MIT License.
