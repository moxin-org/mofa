# llm_request_node

Dora node for querying OpenAI or compatible LLM APIs from within a pipeline, and sending LLM responses as outputs.

## Features
- Receives text queries as parameters from upstream Dora nodes
- Forwards queries to an LLM using OpenAI (or compatible) API
- Sends the LLM response back as output for downstream nodes

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
  - id: llm_request_node
    build: pip install -e .
    path: llm_request_node
    env:
      LLM_API_KEY: "sk-..."    # Set your OpenAI-compatible API key
    inputs:
      query: upstream_node/query
    outputs:
      - llm_response
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
  - id: upstream_node
    build: pip install your-upstream-node
    path: your-upstream-node
    outputs:
      - query

  - id: llm_request_node
    build: pip install -e .
    path: llm_request_node
    env:
      LLM_API_KEY: "sk-..."
    inputs:
      query: upstream_node/query
    outputs:
      - llm_response
```

Your point source must output:

* Topic: `query`
* Data: String (the prompt or question)
* Metadata:

  ```json
  {
    "dtype": "str",
    "description": "Text query for LLM"
  }
  ```

## API Reference

### Input Topics

| Topic | Type | Description |
|-------|------|-------------|
| query | str  | Text query to be sent to the LLM |

### Output Topics

| Topic        | Type | Description                  |
|--------------|------|------------------------------|
| llm_response | str  | LLM output (answer or error) |


## License

Released under the MIT License.
