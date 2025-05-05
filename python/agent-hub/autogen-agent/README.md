
# Autogen Agent

An advanced AI agent specialized in analyzing and synthesizing information using OpenAI's GPT models, built on the MOFA framework.

## Features

- **OpenAI GPT-4o Integration**: Uses the latest GPT-4o model via `OpenAIChatCompletionClient`
- **Asynchronous Processing**: Built with `asyncio` for efficient task handling
- **MOFA Agent Framework**: Implements `MofaAgent` base class for standardized agent behavior
- **Markdown Output**: Returns well-formatted responses in Markdown
- **Configuration Support**: YAML-based agent configuration

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/moxin-org/mofa.git
   cd mofa/python/agent-hub/autogen-agent
   ```


2. Set up environment variables:
   ```bash
   echo "LLM_API_KEY=your_openai_api_key" > autogen_agent/.env
   ```

## Configuration

Agent behavior is configured in `autogen_agent/configs/agent.yml`:

```yaml
agent:
  prompt:
    role: You are an advanced AI agent specializing in analyzing and synthesizing information...
    backstory: Developed to assist users in making sense of pre-collected data...
    answer: Optimize the output to be in Markdown format...
```

## API Reference

### `autogen_agent(task: str) -> str`
Main async function that processes queries using GPT-4o.

Parameters:
- `task`: The query string to process

Returns:
- Formatted Markdown response

Example:
```python
from autogen_agent import autogen_agent

result = await autogen_agent("Explain quantum computing")
```

### `run(agent: MofaAgent)`
MOFA agent entry point that handles:
- Environment setup
- Task execution
- Result output

## Development

### Project Structure

```
autogen-agent/
├── autogen_agent/
│   ├── __init__.py        # Package initialization
│   ├── main.py            # Core agent implementation
│   ├── configs/
│   │   └── agent.yml      # Agent configuration
│   └── .env               # Environment variables
├── pyproject.toml         # Project metadata
└── README.md              # Documentation
```

### Dependencies

Core dependencies (managed by UV):
- Python 3.10+
- `autogen-agentchat`
- `autogen-ext[openai]`
- `mofa` framework

## Examples

### Basic Usage
```python
from autogen_agent import autogen_agent
import asyncio

async def main():
    response = await autogen_agent("Explain AI in simple terms")
    print(response)

asyncio.run(main())
```


