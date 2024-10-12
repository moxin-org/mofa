# 一些补充模型

有一些专用模型无法通过 SiliconFlow 服务访问。我们启动了几个额外的 OpenAI 兼容的 API 服务器，使用 [Gaia](https://github.com/GaiaNet-AI/gaianet-node) 轻量级 LLM 运行时，这些模型运行在 [OpenBayes](https://openbayes.com/) 和华为的 [Ascend GPU](https://ascend.github.io/docs/sources/ascend/quick_install.html) 提供的 GPU 机器上运行。

### Llama-3-Groq LLM

此 LLM 针对工具调用从 Llama 3 8b 进行了微调。您可以使用 [由 OpenAI 定义](https://platform.openai.com/docs/guides/function-calling) 的 `tools` JSON 字段将可用工具传递给 LLM，并使用对话中的 `tool` 角色发送工具调用结果。

|  Key | Value |
| ------------- | ------------- |
| API endpoint  | `https://gosim-llama-3-groq-8b.gaianet.network/v1`  |
| Model name  | `llama-tool`  |
| API key | `GAIA` |
| API docs | [/chat/completions](https://platform.openai.com/docs/api-reference/chat/create) |

请求示例:

```
curl -X POST https://gosim-llama-3-groq-8b.gaianet.network/v1/chat/completions \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"messages":[{"role":"user","content":"What is the weather like in San Francisco in Celsius?"}],"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather in a given location","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and state, e.g. San Francisco, CA"},"unit":{"type":"string","enum":["celsius","fahrenheit"],"description":"The temperature unit to use. Infer this from the users location."}},"required":["location","unit"]}}},{"type":"function","function":{"name":"predict_weather","description":"Predict the weather in 24 hours","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and state, e.g. San Francisco, CA"},"unit":{"type":"string","enum":["celsius","fahrenheit"],"description":"The temperature unit to use. Infer this from the users location."}},"required":["location","unit"]}}}],"tool_choice":"auto","stream":false}'
```

LLM 的回应:

```
{"id":"chatcmpl-efa60d0a-9427-4f21-ba4e-1b5353bdc41c","object":"chat.completion","created":1728724972,"model":"llama","choices":[{"index":0,"message":{"content":"<tool_call>\n{\"id\": 0, \"name\": \"get_current_weather\", \"arguments\": {\"location\": \"San Francisco, CA\", \"unit\": \"celsius\"}}\n</tool_call>","tool_calls":[{"id":"call_abc123","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\":\"San Francisco, CA\",\"unit\":\"celsius\"}"}}],"role":"assistant"},"finish_reason":"tool_calls","logprobs":null}],"usage":{"prompt_tokens":404,"completion_tokens":38,"total_tokens":442}}
```

### The functionary LLM

这个模型也是微调的Llama 3，以支持 [tool calls](https://platform.openai.com/docs/guides/function-calling).

|  Key | Value |
| ------------- | ------------- |
| API endpoint  | `https://gosim-functionary-31-small.gaianet.network/v1`  |
| Model name  | `functionary`  |
| API key | `GAIA` |
| API docs | [/chat/completions](https://platform.openai.com/docs/api-reference/chat/create) |

请求示例:

```
curl -X POST https://gosim-functionary-31-small.gaianet.network/v1/chat/completions \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"messages":[{"role":"user","content":"What is the weather like in San Francisco in Celsius?"}],"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather in a given location","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and state, e.g. San Francisco, CA"},"unit":{"type":"string","enum":["celsius","fahrenheit"],"description":"The temperature unit to use. Infer this from the users location."}},"required":["location","unit"]}}},{"type":"function","function":{"name":"predict_weather","description":"Predict the weather in 24 hours","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and state, e.g. San Francisco, CA"},"unit":{"type":"string","enum":["celsius","fahrenheit"],"description":"The temperature unit to use. Infer this from the users location."}},"required":["location","unit"]}}}],"tool_choice":"auto","stream":false}'
```

LLM 回复:

```
{"id":"chatcmpl-fdbf5180-b9cb-4eb5-b6f2-0252541962eb","object":"chat.completion","created":1728726580,"model":"functionary","choices":[{"index":0,"message":{"content":"<function=get_current_weather>{\"location\": \"San Francisco, CA\", \"unit\": \"celsius\"}</function>","tool_calls":[{"id":"call_abc123","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"San Francisco, CA\", \"unit\": \"celsius\"}"}}],"role":"assistant"},"finish_reason":"tool_calls","logprobs":null}],"usage":{"prompt_tokens":410,"completion_tokens":25,"total_tokens":435}}
```

### nomic embed 模型

在许多 Agent 和 RAG 应用程序中，你需要将自然语言或代码转换为数字向量，以便我们执行语义搜索。为此，你需要一个“embedding”模型。Gaia 节点提供了一个名为 “nomic-embed-v1.5”的高性能嵌入模型。它也可以通过 OpenAI 兼容 API 获得。

|  Key | Value |
| ------------- | ------------- |
| API endpoint  | `https://gosim-nomic-embed.gaianet.network/v1`  |
| Model name  | `nomic-embed`  |
| API key | `GAIA` |
| API docs | [/embeddings](https://platform.openai.com/docs/api-reference/embeddings/create) |


### Llama 3.2 系列模型

我们支持全上下文长度（128k 个 token）的 Llama 3.2 小模型。它们允许你试验 [针对使用小型语言模型进行知识提取优化](https://x.com/juntao/status/1828474514801328637) 的应用程序。

Llama 3.2 1B (很小很快)

|  Key | Value |
| ------------- | ------------- |
| API endpoint  | `https://gosim-llama-32-1b.gaianet.network/v1`  |
| Model name  | `llama-32-1b`  |
| API key | `GAIA` |
| API docs | [/chat/completions](https://platform.openai.com/docs/api-reference/chat/create) |
| Web chat | [Link](https://gosim-llama-32-1b.gaianet.network/chatbot-ui/index.html) |

Llama 3.2 3B (小且快)

|  Key | Value |
| ------------- | ------------- |
| API endpoint  | `https://gosim-llama-32-3b.gaianet.network/v1`  |
| Model name  | `llama-32-3b`  |
| API key | `GAIA` |
| API docs | [/chat/completions](https://platform.openai.com/docs/api-reference/chat/create) |
| Web chat | [Link](https://gosim-llama-32-3b.gaianet.network/chatbot-ui/index.html) |
