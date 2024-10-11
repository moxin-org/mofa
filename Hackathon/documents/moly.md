# 在本地运行开源大语言模型

参赛选手可以选择在自己的设备上通过 Moly 运行开源大语言模型，并以此为基础构建 LLM agent。

Moly 是一个使用 Rust 实现的在本地运行 LLM 的客户端工具，已支持多个开源模型，并且可以提供与 OpenAI 完全兼容的 API。

## 1. 安装 Moly
下载适合你设备的安装包。建议下载最新的预发布版本，因为我们正在快速发展。

https://github.com/moxin-org/moly/releases/tag/v0.1.0-20241011

## 2. 启动 Moly
我们需要在固定的 API 服务器端口 8080 上启动 Moly。如果我们不指定端口，Moly 的默认行为是在你的电脑上找到一个空闲端口。

在 MacOS 上，可以在终端窗口执行以下操作：
```
xattr -dr com.apple.quarantine /Applications/Moly.app
export MOLY_API_SERVER_ADDR=localhost:8080
open -a Moly
```
在 Linux 或者 Windows 上，请执行以下操作：

```
export MOLY_API_SERVER_ADDR=localhost:8080
moly
```
如果你使用的是 Windows 机器，在首先找到安装的 moly.exe 程序的路径。假设路径为 C:\Users\demo\AppData\Local\Moly\moly.exe。然后在 PowerShell 窗口中执行以下操作

```
$Env:MOLY_API_SERVER_ADDR="localhost:8080"
C:\Users\demo\AppData\Local\Moly\moly.exe
```

## 3. 启动模型
在 Moly UI 中下载一个模型（例如 Llama-3.1-8b-instruct），然后向它提问（例如：“你是谁？”）。确保你在聊天中收到回复。

接下来，你可以通过运行以下命令测试本地 API 服务器：

```
curl http://localhost:8080/v1/models
```
你应该能看到一个包含两个模型的响应——一个聊天 LLM 和一个 embedding 模型。

```
{
  "object":"list",
  "data":[
    {
      "id":"moly-chat",
      "created":1727908219,
      "object":"model",
      "owned_by":"Not specified"
    },
    {
      "id":"moly-embedding",
      "created":1727908219,
      "object":"model",
      "owned_by":"Not specified"
    }
  ]
 }
```
你还可以通过 API 发送聊天请求。

```
curl -X POST http://localhost:8080/v1/chat/completions \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"messages":[{"role":"system", "content": "You are a helpful assistant."}, {"role":"user", "content": "What are the most important accomplishments of Albert Einstein?"}]}'
```


回复可能如下所示：

```
{"id":"chatcmpl-79f6c045-5d46-4416-a355-c9032c9918ae","object":"chat.completion","created":1727908319,"model":"moly-chat","choices":[{"index":0,"message":{"content":"Albert Einstein (1879-1955) was a renowned German-born physicist who is widely regarded as one of the most influential scientists of the 20th century. He made significant contributions to our understanding of space, time, matter, and energy, which revolutionized the field of physics and had a profound impact on the development of modern science. Here are some of his most important accomplishments:\n\n1. **Theory of Relativity (1905 and 1915)**: Einstein's special theory of relativity posits that time and space are relative and can be affected by gravity, and that the laws of physics are the same for all observers in uniform motion.\n2. **The Photoelectric Effect**: Einstein's work on the photoelectric effect led to a fundamental understanding of light and its interaction with matter. He showed that light is composed of particles (now called photons) rather than a continuous wave, and demonstrated the quantization of energy.\n3. **Brownian Motion**: Einstein provided a mathematical explanation for Brownian motion, showing that the random movements of particles suspended in a fluid are due to collisions with surrounding molecules, rather than inertia.\n4. **Einstein's Field Equation (1905)**: He introduced the concept of a unified field theory, where gravity, electromagnetism, and the strong and weak nuclear forces are all described by a single mathematical equation, known as the Einstein field equations.\n5. **Mass-Energy Equivalence**: Einstein's famous equation E=mc² shows that mass (m) and energy (E) are interchangeable, with a small percentage of mass being converted into energy during acceleration or deceleration.\n6. **Gravitational Redshift**: He demonstrated that time dilation occurs in strong gravitational fields, leading to a redshift of light emitted from celestial objects, such as white dwarfs and black holes.\n7. **Quantum Mechanics**: Einstein's work on the photoelectric effect laid the foundation for quantum mechanics, a fundamental theory of the behavior of matter and energy at the atomic and subatomic level.\n8. **The Special Theory of Relativity**: This theory revolutionized our understanding of space, time, and gravity by introducing the concept of spacetime as a unified, four-dimensional fabric.\n9. **Photons and Quantum Mechanics**: Einstein's work on photons led to the development of quantum mechanics and the famous equation for the photoelectric effect.\n10. **Moseley's Law**: In 1913, he used the energy levels of atoms to predict the frequencies of spectral lines in noble gases, which laid the foundation for spectroscopy.\n\nThese accomplishments cemented Einstein's reputation as a master physicist and one of the most influential scientists in history, with a lasting impact on our understanding of the universe.","role":"assistant"},"finish_reason":"stop","logprobs":null}],"usage":{"prompt_tokens":31,"completion_tokens":553,"total_tokens":584}}
```
这一步是为了确保模型已加载并启动。

## Moly 的 endpoint

如果你的 Moly 指定端口是 8080， Moly 的大模型 API server endpoint 如下所示：

```
| Env var  | Value |
| ------------- | ------------- |
| CHAT_MODEL_BASE_URL  | http://localhost:8080/v1  |
| CHAT_MODEL_NAME  | moly-chat  |
| CHAT_API_KEY  |  ANYTHING  |
| EMBEDDING_MODEL_BASE_URL  | http://localhost:8080/v1  |
| EMBEDDING_MODEL_NAME  | moly-embedding  |
| EMBEDDING_API_KEY  | ANYTHING  |
```


通过 Moly 运行的开源大语言模型有着和 OpenAI API 完全兼容的 API server，接下来你就可以用熟悉的工具构建 LLM Agent

参考资料：
* [常用的 API Reference](https://llamaedge.com/docs/user-guide/api-reference)
* [OpenAI python library](https://llamaedge.com/docs/user-guide/openai-api/intro#the-openai-python-library)
