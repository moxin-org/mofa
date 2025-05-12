# WordDefinitionAgent

A Mofa-based agent that queries a dictionary API to retrieve the definition of a given word.

## Features
- Accepts a word as input and returns its definition.
- Handles API errors gracefully and provides meaningful error messages.

## Input/Output Specifications
### Input
- `word` (string): The word to be queried in the dictionary.

### Output
- `definition_result` (string): The definition of the queried word in the format `"word: definition"`.
- `error` (string): An error message if the query fails.

## Workflow
```mermaid
graph TD
    A[Start] --> B[Receive word parameter]
    B --> C[Query dictionary API]
    C --> D{API response OK?}
    D -->|Yes| E[Extract definition]
    D -->|No| F[Return "未找到释义"]
    E --> G[Format output]
    G --> H[Send definition_result]
    F --> H
    C --> I[Error occurred]
    I --> J[Send error message]
```

## Code Structure
- **Input Handling**: The agent receives the `word` parameter using `agent.receive_parameter`.
- **Core Logic**: Queries the dictionary API and processes the response to extract the definition.
- **Output Delivery**: Sends the result or error message using `agent.send_output`.

## Error Handling
- Catches exceptions during API queries and sends an error message with details.

## Example Usage
```python
agent = MofaAgent(agent_name='WordDefinitionAgent')
agent.receive_parameter('word', 'example')
agent.run()
```

## Dependencies
- `requests` library for API queries.
- Mofa framework for agent functionality.