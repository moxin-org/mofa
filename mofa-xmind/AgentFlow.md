---

**AgentFlow** is a robust and dynamic data graph framework designed to manage multiple chat sessions efficiently within a single graph instance. It consists of interconnected nodes and edges, where each node can represent a function, action, or agent. These nodes are linked through input and output interfaces known as pins.

### Key Features:

- **Session Memory**: Each chat session within AgentFlow maintains its own session memory, preserving the history of interactions. This memory automatically binds to each request as part of the prompt, ensuring continuity and context across interactions. All outputs from the language model (LLM) are fed back into this session memory, continuously enriching the session's context.

- **Data Structure**: The data flowing through each pin is organized into four key components: session ID, status, output index, and the actual data encapsulated as `X::Value`. This structured approach ensures consistent and efficient data management across the graph.

- **Node Operations**: Nodes can operate within their own threads or processes, offering flexibility in execution. Function nodes, however, execute inline within the context of their associated action or agent nodes, ensuring seamless integration within the designated workflow.

- **Agent Integration**: Agents in AgentFlow are directly bound to LLM requests, effectively acting as the brain of the framework. They drive the logic, decision-making, and context management across the entire graph, leveraging the session memory to maintain continuity.

- **Flexible Pin Connections**: Each input pin can accept multiple connections from output pins, allowing for complex and flexible data routing between nodes.

- **Multi-Session Support**: AgentFlow is specifically designed to support multiple chat sessions simultaneously within a single graph instance. This design optimizes resource usage, enabling scalable and efficient management of multiple conversations.

By combining session memory with a flexible, multi-threaded architecture, AgentFlow offers a powerful solution for managing complex workflows in environments that require persistent context and high scalability.
