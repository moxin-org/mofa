

# GOSIM Pedia - AI-Powered Speaker Encyclopedia System

![Dataflow Architecture](gosim-pedia-dataflow-graph.html)

GOSIM Pedia is a distributed agent system that automatically generates comprehensive speaker profiles by aggregating and synthesizing information from multiple sources.

## Key Features

- **Multi-source Intelligence Fusion**:
  - Web search (Serper API)
  - Deep research (Firecrawl)
  - Vector database retrieval (ChromaDB)
- **Structured Output Generation**:
  - Chronological career timeline
  - Academic publications
  - Media appearances
  - Awards and achievements
- **Modular Agent Architecture**:
  - Independent components with clear interfaces
  - Parallel query execution
  - Schema-driven data validation

## System Architecture

### Core Components

| Component              | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| `gosim-pedia-agent`    | Orchestrates the workflow and generates final profiles                      |
| `serper-search-agent`  | Performs web searches using Google Serper API                               |
| `gosim-rag-agent`      | Retrieves relevant information from vector database                         |
| `firecrawl-agent`      | Conducts deep web research with configurable depth and analysis             |
| `dora-openai-server`   | Provides LLM capabilities for information synthesis                         |

### Data Flow

```mermaid
flowchart TB
  classDef agent fill:#e1f5fe,stroke:#039be5;
  classDef server fill:#e8f5e9,stroke:#43a047;
  
  dora-openai-server["dora-openai-server\n(LLM Service)"]:::server
  gosim-pedia-agent["gosim-pedia-agent\n(Orchestrator)"]:::agent
  
  gosim-pedia-agent -->|speaker_query| serper-search-agent:::agent
  gosim-pedia-agent -->|speaker_query| gosim-rag-agent:::agent
  gosim-pedia-agent -->|speaker_query| firecrawl-agent:::agent
  
  serper-search-agent -->|serper_result| gosim-pedia-agent
  gosim-rag-agent -->|rag_result| gosim-pedia-agent
  firecrawl-agent -->|firecrawl_result| gosim-pedia-agent
  
  gosim-pedia-agent -->|speaker_summary| dora-openai-server
```

## Getting Started

### Prerequisites

- Python 3.10+
- Dora framework
- API keys for:
  - Serper (web search)
  - Firecrawl (deep research)
  - OpenAI (LLM services)



1. Configure environment variables:
   ```bash
   cp .env.example .env.secret
   # Edit with your API keys
   ```

### Running the System

1. Start the Dora runtime:
   ```bash
   dora up
   ```

2. Build and start the dataflow:
   ```bash
   dora build gosim-pedia-dataflow.yml
   dora start gosim-pedia-dataflow.yml
   ```



