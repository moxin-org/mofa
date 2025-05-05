
# MCP Server Agent

A MOFA agent that provides MCP (Multi-Channel Processing) server capabilities for tool and resource management.

## Features

- **Tool Registration**: Register and expose Python functions as MCP tools
- **Resource Management**: Manage and serve resources through MCP protocol
- **SSE Support**: Server-Sent Events for real-time communication
- **MOFA Integration**: Built on MOFA agent framework

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/moxin-org/mofa.git
   cd mofa/python/agent-hub/mcp-server
   ```


### Example Client Usage
```python
from mcp_server.client import run
import asyncio

asyncio.run(run())
```

### Available Commands
- List tools: `await session.list_tools()`
- Call tool: `await session.call_tool("add", arguments={"a": 4, "b": 5})`
- List resources: `await session.list_resources()`
- Read resource: `await session.read_resource("resource://some_static_resource")`

## API Reference

### Server Functions
```python
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b
```

### Client Methods
- `initialize()`: Initialize session
- `list_tools()`: List available tools
- `call_tool()`: Execute registered tool
- `list_resources()`: List available resources
- `read_resource()`: Access resource content

## Project Structure
```
mcp-server/
├── mcp_server/
│   ├── __init__.py
│   ├── main.py        # Server implementation
│   ├── client.py      # Client implementation
│   └── configs/       # Configuration files
├── pyproject.toml
└── README.md
```

## Dependencies
- Python 3.8+
- `mcp` package
- `pyarrow` (>=5.0.0)

## License
MIT License
