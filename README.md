# **MoFA**

[English](README.md) | [简体中文](README_cn.md)

## What

MoFA: **M**odular **F**ramework for **A**gent

MoFA is a software framework for building AI agents through a composition-based approach. Using MoFA, AI agents can be constructed via templates and combined in layers to form more powerful Super Agents.

## WHY

Building AI agents with MoFA offers:

1. **Modularity**: Modular agent templates and agent services; simple configurations with straightforward interfaces between modules.

2. **Clarity**:  A "LEGO brick"-style logic for assembling complex systems.

3. **Composition**: Agentic Application gain greater capabilities and expand functionalities with put composible agents together.

4. **Simplicity**: Constructing complex agents becomes a zero-code process.

5. **High Performance**: Agents operate in the high-performance, low-latency distributed AI and robotics computation environment of DORA-RS, outperforming Python-based environments.

6. **Diversity**: MoFA's agent composition combines capabilities organically, creating more powerful and comprehensive composite agents.

7. Towards AIOS

   : Designed with inspiration from Unix Philosophy and methodology:

   - AIOS Core: MoFA provides services like task planning, memory, actions, and Retrieval-Augmented Generation (RAG).
   - Utility and Applications: Common and foundational functionalities via agent templates.
   - Shell: An environment for running agents and automating their processes.

8. **Enabling Edge AI**: Together with the MoXin project for local model inference and the MoLy project for user interfaces, MoFA agents make AI applications more open and democratic.

## Features

#### Feature 1: Nesting Design Patterns of AI Agents

AI agents are intelligent software applications. Similar to the design patterns in object-oriented programming, there are various design patterns for AI agents, include but not limited to  :

- **LLM Inference**: Using large language models (LLMs) to inference is the most simplistic design pattern.
- **Customized Prompt**: tailoring system prompts for  agents.
- **Reflection Pattern**: Agents capable of self-review and improvement.
- **Actor Pattern**: Agents with the ability to use external tools and resources, like generating code or searching the web.
- **ReAct Pattern**: Combining reflection and tool usage to improve output quality.
- **Multi-Agent Collaboration**: Agents taking on specialized roles and collaborating to complete complex tasks

More design patterns can be easily added into MoFA as technology advances.   Agent Application developers can create their own design patterns and can be reused by in the community. 

#### Feature 2: Agent Kernal Services

Similar to an operating system providing services to software, MoFA provides core services to agents, including memory, planning, knowledge base, RAG, and action capabilities.

However, MoFA treat Kernel Services as Agents too, which makes them open to the the 3rd party developers. MoFA users can pick the kernal service agents that best fit their needs.  

#### Feature 3: Composition

Composition is the process of assembling elements into new entities without changing the original components. This modularity allows AI developers to build and recombine agents to create new functionalities.

#### Feature 4: Dataflow-Driven Approach

MoFA employs a dataflow-driven method instead of a workflow-driven one. By focusing on data dependencies rather than business rules, it simplifies and enhances modularity.

## How

MoFA currently supports agent development using the Dora-RS framework. For details, please refer to  the [python](python) directory's [README.md](python/README.md).



## GOSIM China 2024 Super Agent Hackathon

The MoFA project is one of the agent programming frameworks for the GOSIM 2024 China Conference Super Agent Hackathon. 

- Documentation for participants is available here[>>>](Hackathon/documents/README.md).

- Gosim China 2024 Super Agent Hackathon Website [>>>](https://gosim.gitcode.com/hackathon/)
- Weave your agent with MoFA，An introductory presentation of MoFA @ GOSIM China 2024 [YouTube](https://www.youtube.com/watch?v=FhL3orAVO6U)
