
# Browser Use Connector Agent

A MOFA agent that connects browser automation tasks with OpenAI's GPT models for intelligent web interaction.

## Features

- **Browser Automation Integration**: Connects with browser automation tools
- **OpenAI GPT Integration**: Uses `ChatOpenAI` from langchain for LLM processing
- **Asynchronous Processing**: Built with `asyncio` for efficient task handling
- **MOFA Agent Framework**: Implements `MofaAgent` base class
- **Environment Configuration**: Supports `.env.secret` for sensitive configuration

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/moxin-org/mofa.git
   cd mofa/python/agent-hub/browser-use-connector
   ```


2. Set up environment variables in `.env.secret`:
   ```bash
   echo "LLM_API_KEY=your_openai_api_key" > .env.secret
   echo "LLM_BASE_URL=your_openai_base_url" >> .env.secret
   echo "LLM_MODEL_NAME=gpt-4o" >> .env.secret
   ```

## Configuration

Agent behavior is configured through environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_API_KEY` | OpenAI API key | - |
| `LLM_MODEL_NAME` | Model to use | `gpt-4o` |

## API Reference

### `run(agent: MofaAgent)`
Main agent entry point that:
1. Receives user question via `agent.receive_parameter()`
2. Executes browser automation
3. Returns results via `agent.send_output()`

### `run_browser_use(question: str) -> AgentResult`
Async function that handles browser automation:
- Creates `Agent` instance with configured LLM
- Executes task and returns final result

## Usage

### As a Python Module
```python
from browser_use_connector import main
import asyncio

async def execute_question(question: str):
    # Initialize and run agent
    agent = MofaAgent(agent_name='browser-use-connector')
    agent.receive_parameter('question', question)
    await run(agent)
    return agent.get_output('agent_result')
```

### CLI Usage
```bash
uv pip install -e .
python -m browser_use_connector --question "Your browser query"
```

## Project Structure

```
browser-use-connector/
├── browser_use_connector/
│   ├── __init__.py        # Package initialization
│   ├── main.py            # Core agent implementation
│   ├── configs/           # Configuration directory
│   └── .env.secret        # Environment variables
├── pyproject.toml         # Project metadata
└── README.md              # Documentation
```

## Dependencies

Core dependencies:
- Python 3.10+
- `mofa` framework
- `langchain-openai`
- `python-dotenv`

## Development Guidelines

1. All browser interactions should be implemented in the `Agent` class
2. Maintain clear separation between browser logic and LLM processing
3. Use environment variables for all sensitive configuration
4. Follow MOFA agent interface standards

## Example Use Case

```python
from browser_use_connector import main

result = asyncio.run(execute_question(
    "Search for latest AI news and summarize top 3 articles"
))
print(result)
```

## License

MIT License - See [LICENSE](https://github.com/moxin-org/mofa/blob/main/LICENSE) for details.
```

