
# Letta Agent

Letta Agent is a dynamic AI agent for processing tasks, managing memory, and interacting with the user. It integrates with a dataflow system and interacts with a large language model (LLM) to generate responses based on the provided tasks. This agent supports ta***REMOVED***based execution, memory storage, and integration with external systems like `Dora` for dynamic dataflows.

## Requirements

- Python 3.10+


1. **Environment Variables**:

   * `LLM_API_KEY`: The API key for your LLM provider (such as OpenAI).
   * `LLM_MODEL_NAME`: The name of the model you're using (e.g., `gpt-4o`).
   * `LLM_EMBEDDER_MODEL_NAME`: The name of the embedding model for document retrieval.
   * `TASK`: The default task to execute (optional).
   * `IS_DATAFLOW_END`: A flag to indicate if the dataflow has ended.

2. **Configuration Files**:

   * `config.yml`: Configuration file containing agent-specific settings.
   * `.env.secret`: The file that contains secret environment variables (e.g., API keys, model configurations).

3. **Memory Configuration**:

   * The agent uses an internal memory system to store and retrieve past interactions. The memory can be customized with the persona for the agent and human.

4. **Dynamic Node Integration**:

   * The agent can be integrated into a dynamic dataflow system using the `Node` class from the `dora` library. The agent will listen for tasks, process them, and return results.
