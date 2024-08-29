# Self-Refine Agent Example

**语言**
- [English](README.md)

## Use Cases

### 1. [audio_summarize_by_crewai.yml](use_case%2Faudio_summarize_by_crewai.yml)
这个案例是使用whisper来识别mp3中的语音,把语音转换成文字,然后根据文字总结内容


### 2. [summarize_pdf_by_rag_dspy.yml](use_case%2Fsummarize_pdf_by_rag_dspy.yml)
1. 使用dspy、embedding和向量来实现RAG（Retrieval-Augmented Generation）的功能。
2. 将PDF内容向量化，并存储向量化后的内容。
3. 分析用户任务，提取任务中的关键词和内容，使用RAG查询。
4. LLM结合RAG生成的结果完成任务答案。




### 3. [phrase_spelling_error_by_dspy.yml](use_case%2Fphrase_spelling_error_by_dspy.yml)
1. 使用Crewai的工具实现RAG功能。


## 启动

**切换不同的use_case**:
~~~
在[reasoning_loader.py](reasoning_loader.py)中修改第17行
params = read_yaml('use_case/summarize_pdf_by_crewai_rag.yml')
~~~


**如果你需要运行这个案例，请先安装mae，然后运行下面的命令**：
~~~
dora up && dora start  self_refine_dataflow.yml --attach
~~~

**如果你需要对配置进行修改,请查看[README_zh.md](..%2F..%2F..%2Fdocs%2FREADME_zh.md)**
