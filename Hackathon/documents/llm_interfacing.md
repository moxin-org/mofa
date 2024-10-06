# LLM 接口配置指南

本指南提供了使用两种不同配置（Dspy 和 Crewai）来配置大型语言模型（LLM）的详细说明。这些配置分为云 API 和本地服务两类。所有配置均通过 YAML 文件进行管理。

## 云 API
### OpenAI
#### Dspy 配置
通过在您的 YAML 配置文件中设置以下参数，来为 Dspy 配置 OpenAI：

```MODEL_API_KEY```: your_openai_api_key
```MODEL_NAME```: ```gpt-4o```
```MODEL_MAX_TOKENS````: ```4096```

**参数说明：**

```MODEL_API_KEY```: （字符串）您的 OpenAI API 密钥。
```MODEL_NAME```: （字符串）指定模型版本（例如 ```gpt-4o```）。
```MODEL_MAX_TOKENS```: （整数）模型的最大 ```token``` 数量（例如 4096）。
#### Crewai 配置
通过在您的 YAML 配置文件中设置以下参数，来为 Crewai 配置 OpenAI：

```model_api_key```: your_openai_api_key
```model_name```: ```gpt-4o-mini```
```model_max_tokens```: ```2048```
```module_api_url```: ```null``` # 可选：若使用自定义模块 API，则指定此项
**参数说明：**

```model_api_key```: （字符串）您的 OpenAI API 密钥。
```model_name```: （字符串）指定模型版本（例如 ```gpt-4o-mini```）。
```model_max_tokens```: （整数）模型的最大 token 数量（例如 ```2048```）。
```module_api_url```: （字符串 | ```null```）如果适用，自定义模块 API 的 URL。若不使用，则设置为 ```null```。
## 本地服务

### Ollama
#### Dspy 配置
通过在您的 YAML 配置文件中设置以下参数，来为 Dspy 配置 Ollama。请注意，这些设置目前被注释掉，在使用时应取消注释。

yaml配置
复制代码
```MODEL_API_KEY```: ```ollama```
```MODEL_NAME```: ```qwen:32b```
```MODEL_MAX_TOKENS```: ```2048```
```MODEL_API_URL```: ```http://192.168.0.75:11434```

#### Crewai 配置
通过在您的 YAML 配置文件中设置以下参数，来为 Crewai 配置 Ollama：

```model_api_key```: ```"ollama"```
```model_name: qwen:```7b```
```model_max_tokens```: ```2048```
```module_api_url```: ```"http://192.168.0.75:11434/v1"```

### AnythingLLM
#### Dspy 配置
等待 LLM 服务测试。

#### Crewai 配置
通过在您的 YAML 配置文件中设置以下参数，来为 Crewai 配置 AnythingLLM。这些设置目前被注释掉，在需要时应取消注释并填写。

yaml
复制代码
```model_api_key```: your_anythingllm_api_key
```model_name```: your_model_name
```model_max_tokens```: ```2048```
```module_api_url```: your_module_api_url





