
# **MoFA**

*With MoXin in the heart, Play **MoFa** magic, Show Moly to the world.*

## What is MoFa?

**MoFa** stands for **Mo**xin **F**ramework for **A**gent Composition.

MoFa is a software framework that builds AI agents through composition. With MoFa, AI agents can be created using templates, combined in a stackable manner to form more powerful "super agents."

## Why MoFa?

Using MoFa to build agents has several key benefits:

1. **Modularity**: Modular agent templates and services, with simple configuration and easy-to-use interfaces between modules.
2. **Clarity**: Build complex systems using a "LEGO-like" combination of logical blocks.
3. **Composability**: Agents can connect to services for enhanced capabilities or to other agents for expanded functionality.
4. **Simplicity**: Constructing complex agents is a zero-code process of combining different modules.
5. **High Performance**: Agent data streams run in a high-performance, low-latency distributed AI and robotics environment called **DORA-RS**, outperforming Python-based computational environments.
6. **Diversity**: MoFa’s composable agents integrate various agent capabilities into powerful, complete super agents.
7. **Towards AI Operating Systems (AIOS)**: Inspired by Unix Philosophy, MoFa provides core services for planning, memory, actions, and Retrieval-Augmented Generation (RAG), building the foundation of an AI operating system.
8. **Enable Edge AI**: With MoFa, alongside MoXin (local large model inference) and MoLy (user interface for AI models and agents), the deployment of local AI agents becomes more open and democratic.


## Features

### MoFa Design Patterns for AI Agents

AI agents can follow various design patterns, such as:

- **LLM Inference**: The simplest agent, leveraging a large language model to generate responses based on user prompts.
- **Customized Prompting**: Creating agents by customizing system prompts for language models.
- **Reflection**: Agents that review and adjust their outputs.
- **Actor (Tool Use)**: Agents capable of using external tools, generating code, calling APIs, and performing web searches.
- **ReAct**: Combining reflection and tool use to improve output quality.
- **Multi-Agent Collaboration**: Multiple agents working together to solve complex tasks as a team.

MoFa allows you to combine these simple patterns into more complex "super agents" using modular templates.

### Agent Kernel Services

Similar to how traditional operating systems provide core services to applications, MoFa provides memory, planning, RAG, and action services to agents, allowing users to tailor these capabilities to their needs.

### Agent Composition

Composition in MoFa allows agents to be combined like LEGO blocks, creating powerful and complex agents without modifying the individual components. This modular approach ensures reversibility and scalability.

### Dataflow Driven Design

MoFa uses a dataflow-driven approach, emphasizing the movement of data between tasks rather than complex workflows. This simplifies managing and debugging agents.


