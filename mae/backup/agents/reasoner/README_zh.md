# Reasoner Example

**语言**
- [English](README.md)

## Use Cases

### 1. [snake_game_build_by_dspy.yml](use_case%2Fsnake_game_build_by_dspy.yml)
这个案例是一个编程任务，要求使用Python编写一个经典的贪吃蛇游戏。

### 2. [phrase_spelling_error_by_dspy.yml](use_case%2Fphrase_spelling_error_by_dspy.yml)
这个案例是一个语句错误检测任务，考察大模型是否能够理解语句的含义，并给出正确的语句。

### 3. [summarize_pdf_by_rag_dspy.yml](use_case%2Fsummarize_pdf_by_rag_dspy.yml)
1. 使用dspy、embedding和向量来实现RAG（Retrieval-Augmented Generation）的功能。
2. 将PDF内容向量化，并存储向量化后的内容。
3. 分析用户任务，提取任务中的关键词和内容，使用RAG查询。
4. LLM结合RAG生成的结果完成任务答案。

### 4. [summarize_pdf_by_crewai_rag.yml](use_case%2Fsummarize_pdf_by_crewai_rag.yml)
1. 使用Crewai的工具实现RAG功能。
2. 在Agent的提示中定义RAG的逻辑（与`summarize_pdf_by_rag_dspy.yml`的查询逻辑一致）。
3. Crewai会自动调用不同工具，实现提示中定义好的逻辑。

## 启动

**切换不同的use_case**:
~~~
在[reasoning_loader.py](reasoning_loader.py)中修改第17行
params = read_yaml('use_case/summarize_pdf_by_crewai_rag.yml')
~~~


**如果你需要运行这个案例，请先安装mae，然后运行下面的命令**：
~~~
dora up && dora start  reasoner_dataflow.yml --attach
~~~

**如果你需要对配置进行修改,请查看[README_zh.md](..%2F..%2F..%2Fdocs%2FREADME_zh.md)**
