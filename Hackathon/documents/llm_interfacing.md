# LLM Interfacing Configuration Guide

This guide provides detailed instructions for configuring Large Language Models (LLMs) using two distinct configurations: **Dspy** and **Crewai**. The configurations are categorized under **Cloud APIs** and **Local Services**. All configurations are managed via YAML files.


## Cloud APIs

### OpenAI

#### Dspy Configuration

Configure OpenAI for Dspy by setting the following parameters in your YAML configuration file:

```yaml
MODEL_API_KEY: your_openai_api_key
MODEL_NAME: gpt-4o
MODEL_MAX_TOKENS: 4096
```

- **MODEL_API_KEY**: *(String)* Your OpenAI API key.
- **MODEL_NAME**: *(String)* Specifies the model version (e.g., `gpt-4o`).
- **MODEL_MAX_TOKENS**: *(Integer)* Maximum number of tokens for the model (e.g., `4096`).

#### Crewai Configuration

Configure OpenAI for Crewai by setting the following parameters in your YAML configuration file:

```yaml
model_api_key: your_openai_api_key
model_name: gpt-4o-mini
model_max_tokens: 2048
module_api_url: null  # Optional: Specify if using a custom module API
```

- **model_api_key**: *(String)* Your OpenAI API key.
- **model_name**: *(String)* Specifies the model version (e.g., `gpt-4o-mini`).
- **model_max_tokens**: *(Integer)* Maximum number of tokens for the model (e.g., `2048`).
- **module_api_url**: *(String | null)* URL for a custom module API if applicable. Set to `null` if not used.

---


## Local Services

### Moxin

#### Dspy Configuration

*Configuration details for Moxin using Dspy are currently unavailable.



#### Crewai Configuration

*Configuration details for Moxin using Crewai are currently unavailable.




### Ollama

#### Dspy Configuration

Configure Ollama for Dspy by setting the following parameters in your YAML configuration file. Note that these settings are currently commented out and should be uncommented when in use.

```yaml
# MODEL_API_KEY: ollama
# MODEL_NAME: qwen:32b
# MODEL_MAX_TOKENS: 2048
# MODEL_API_URL: http://192.168.0.75:11434
```

#### Crewai Configuration

Configure Ollama for Crewai by setting the following parameters in your YAML configuration file:

```yaml
model_api_key: "ollama"
model_name: qwen:7b
model_max_tokens: 2048
module_api_url: "http://192.168.0.75:11434/v1"
```

---

### AnythingLLM

#### Dspy Configuration

*Waiting for LLm service to test*


#### Crewai Configuration

Configure AnythingLLM for Crewai by setting the following parameters in your YAML configuration file. These settings are currently commented out and should be uncommented and filled in as needed.

```yaml
# model_api_key: your_anythingllm_api_key
# model_name: your_model_name
# model_max_tokens: 2048
# module_api_url: your_module_api_url
```






