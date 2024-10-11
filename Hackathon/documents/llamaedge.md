# 基于 LlamaEdge 和 Gaia 的大语言模型


基于 LlamaEdge 和 Gaia，我们运行了以下模型，API endpoint 与 Model name 如下，供大家自由选择使用。

| Llama-3-Groq 8b | Fine-tuned for tool call | 
| -------- | -------- |
| API endpoint | http://llamatool.llm.secondstate.info/v1 |
| Model name for chat | llamatool |

| Llama-3.2-3b | Latest model from Meta | 
| -------- | -------- |
| API endpoint | http://llama3.2.llm.secondstate.info/v1 |
| Model name for chat | llama-3.2-3b |

| functionary-small-v3.1 | A model that supports tool use | 
| -------- | -------- |
| API endpoint | http://whisper.llm.secondstate.info/v1 |

| Embedding model| Convert text to embeddings | 
| -------- | -------- |
| API endpoint | http://embedding.llm.secondstate.info/v1 |
| Model name for embedding | llama-3.2-3b |


上述所有的 API endpoint 都与 OpenAI API 完全兼容。可以参考以下文档来开发你的 LLM Agent

* [OpenAI python 和 OpenAI Node 库](https://docs.gaianet.ai/user-guide/apps/intro)
* [API Reference](https://docs.gaianet.ai/user-guide/api-reference)
