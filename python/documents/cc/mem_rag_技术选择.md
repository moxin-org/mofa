

## 一、LightRAG 对 LLM 的基本要求

根据 LightRAG 官方建议：

* **LLM 参数量**：建议至少 32B 参数级别模型；
* **上下文长度**：需支持至少 32 KB，推荐使用 64 KB 上下文窗口；
* **实体-关系抽取能力**：因 LightRAG 构建图谱检索，需要 LLM 能够从文档中生成实体与关系提示信息，例如高低层关键词提取、实体类型与关系三元组构建 ([知乎专栏][1], [GitHub][2], [GitHub][3])。

因此，LightRAG 对 LLM 的要求比传统 RAG 更高，尤其在抽取知识图谱时。

---

## 二、推荐 LLM 模型（适合边侧部署或轻端设备）

虽然官方建议使用 32B 参数模型，但我们可使用更轻量、可量化的版本以适配边侧部署：

* **Qwen‑32B-AWQ / QwQ‑32B**（通义千问系列）

  * 支持 Function Call，推理性能较强，部署在消费级显卡上（如 RTX 4090）可用 ([CSDN博客][4])。
  * 可量化为 INT4 或 AWQ 格式，显存占用约 18GB，适合本地部署。

* **MobileLLM 系列**（＜1B 参数）

  * 包括 125M、350M、600M、1.5B 等规模，采用 deep‑and‑thin 架构、SwiGLU 激活、Grouped‑query attention，性能与 LLaMA‑v2 7B 接近，可在边缘设备运行 ([CSDN博客][4], [GitHub][5])。
  * 若场景仅限对话对检索结果进行组织（不需生成复杂推理），可使用 MobileLLM 执行低参数量 LLM 与检索增强组合。

* **TinyLlama / Phi‑2 / Gemma**

  * Edge-SLM 框架已在 Android/Mobile 上实现 MiniRAG，使用 TinyLlama 和 Gemma 模型（1–3B 参数）支持 RAG 问答应用 ([deepsense.ai][6])。

---

## 三、Embedding 模型推荐与注意事项

* **主流多语言 Embedding 模型** 推荐使用：

  * `BAAI/bge-m3`
  * `text-embedding-3-large`
    LightRAG 强调：索引阶段必须固定 embedding 模型，并在查询阶段使用相同模型以确保一致性 ([GitHub][2])。

* **集成方式**：

  * 可使用如 Xinference 本地服务部署 embedding 模型（如 bge-m3）；
  * 可直接加载 HuggingFace 提供的 embedding 模型；均通过统一接口绑定 ([GitCode 博客][7])。

---

## 四、Reranker 模型配置建议

启用后置 Reranker（重排序）可显著提升检索结果质量：

* **推荐模型**：

  * `BAAI/bge-reranker-v2-m3`
  * Jina 社区提供的 reranker 服务模型
    使用 LightRAG 默认 `mix mode` 查询方式更佳，即先检索后 rerank ([GitHub][3])。

---

## 五、结合 Mem0 使用的总体技术栈建议

| 组件               | 模型 / 技术建议                          | 说明                                         |
| ---------------- |------------------------------------| ------------------------------------------ |
| **主 LLM**        | 32B模型,例如gpt-oss 20b/qwen3-32b      | 满足 LightRAG 抽取需求；可支持 Function Call，适用于边侧部署 |
| **Embedding 模型** | BAAI/bge‑m3（本地部署）                  | 索引和查询阶段一致，保障检索质量                           |
| **Reranker 模型**  | bge‑reranker‑v2‑m3 或 Jina Reranker | mix mode 查询逻辑下提升召回排序准确性                    |

---

## 六、汇报重点提炼

1. **LightRAG 对 LLM 要求较高**：推荐 32B 参数模型 + 64KB 上下文能力，特别在实体关系提取方面更强。
3. **Embedding 必须固定且高性能**：使用 bge-m3 等模型，document indexing 与 query 阶段一致。
4. **启用 Reranker 可提升召回质量**：推荐使用相应 reranker 模型配合 mix mode 查询。
5. **与 Mem0 协同使用**：LightRAG 检索结果和 Mem0 长期对话记忆协作给小模型提供更丰富上下文。

---

[1]: https://zhuanlan.zhihu.com/p/13261291813?utm_source=chatgpt.com "LightRAG技术框架解读 - 知乎"
[2]: https://github.com/yanfeng98/fork-LightRAG?utm_source=chatgpt.com "\"LightRAG: Simple and Fast Retrieval-Augmented Generation\""
[3]: https://github.com/HKUDS/LightRAG?utm_source=chatgpt.com "\"LightRAG: Simple and Fast Retrieval-Augmented Generation\""
[4]: https://blog.csdn.net/Androiddddd/article/details/146113384?utm_source=chatgpt.com "大模型LLM | QwQ-32B 测评和使用教程来了！ - CSDN博客"
[5]: https://github.com/facebookresearch/MobileLLM?utm_source=chatgpt.com "facebookresearch/MobileLLM - GitHub"
[6]: https://deepsense.ai/blog/implementing-small-language-models-slms-with-rag-on-embedded-devices-leading-to-cost-reduction-data-privacy-and-offline-use/?utm_source=chatgpt.com "Implementing Small Language Models (SLMs) with RAG on Embedded Devices ..."
[7]: https://blog.gitcode.com/90c328ba1f98710de293ae6bee9cfe28.html?utm_source=chatgpt.com "LightRAG项目中本地Embedding模型的集成与应用实践 ..."



### 模型参数量假设

为了进行精确计算，我们首先假设每个模型的参数量：

* **主 LLM**: `gpt-oss 20b` (200亿参数)
* **Embedding 模型**: `BAAI/bge-m3` (通常在10亿参数左右，我们以10亿参数计)
* **Reranker 模型**: `bge-reranker-v2-m3` 或 `Jina Reranker` (通常在10亿参数左右，以10亿参数计)


### 显存总需求汇总

下表清晰地展示了在不同量化方案下，所有模型**同时运行**所需的显存总需求。

| 模型组件           | 参数量    | FP16 (非量化) | INT8 (量化)  | INT4 (量化)  |
| :------------------- | :---------- | :------------ | :------------ |:-----------|
| **主 LLM** (`gpt-oss 20b`) | 20B         | 40 GB         | 20 GB         | 10 GB      |
| **Embedding** (bge-m3)    | ~1B         | ~2 GB         | ~1 GB         | ~0.5 GB    |
| **Reranker** (bge-reranker) | ~1B         | ~2 GB         | ~1 GB         | ~0.5 GB    |
| **总计显存需求** | **22B** | **~44 GB** | **~22 GB** | **~14 GB** |
| **推荐硬件显存** | -         | **48GB+** | **24GB+** | **16GB+**  |

* **总计显存需求**已包含KV Cache等额外显存开销。
* **推荐硬件显存**考虑了部署时需要略大于模型本身的显存空间。

### 总结与建议

根据显存估算，**gpt-oss 20b** 作为主 LLM 的配置，为边侧部署提供了非常大的灵活性。

* **INT8 量化**：总显存需求约 **22 GB**，这使得它可以在一张 **24GB 显卡**（如 RTX 4090）上轻松部署，是性能和成本的最佳平衡点。
* **INT4 量化**：总显存需求仅 **11 GB** 左右，这意味着它甚至可以在一些 **16GB 显卡**上运行，但需要注意验证量化后模型的精度是否满足业务要求。

------
# Rag / Mem0 Nodes的输入和输出参数的选择
rag-build 支持一个文件夹或者一个文件地址 作为输入参数，文件夹下的所有文件都会被读取并处理
rag-query 支持用户的一个查询,然后根据用户的输入作为查询条件，查询知识库，输出的是一个list[dict]的数据结构

mem0-query 支持用户的一个查询,然后根据用户的输入作为查询条件，查询memory，输出的是一个list[dict]的数据结构
mem0-add 把用户的输入和llm输出作为输入，然后添加到memory中，输出的是一个记忆状态


-------
# rag支持的文件格式 
下面是完整的技术报告，涵盖 **LightRAG** 和 **RAG‑Anything** 支持的文档类型，以便你用于技术汇报：

---

## 一、LightRAG 支持的文件结构与格式 📂

### ✅ 多模态格式支持（自 v1.1.2 起）

依据最新说明，LightRAG 支持通过 `textract` 和 RAG‑Anything 集成，实现以下格式的解析与检索 ([GitHub][1])：

* **PDF**
* **Office 文档**：包括 `.doc`, `.docx`, `.ppt`, `.pptx`, `.xls`, `.xlsx`
* **CSV**, **TXT**, **Markdown (.md)** 等纯文本格式
* **图像格式**：JPG/PNG 等嵌入文档中时可以通过 OCR/解析提取
* **其他结构化文本**：如 HTML、JSON、JSONL 等

### ✅ 文档解析与分块机制

* LightRAG 会根据文档类型智能应用不同解析器，实现内容切分、嵌入生成和实体关系抽取 ([GitHub][2], [GitHub][1], [53AI][3], [wiki.genexus.com][4], [每时AI][5])。
* Office 和 PDF 文档保留章节、标题、表格层级结构，无损抽取。
* 使用异步文档管理接口提交上传、状态监控和清理操作，支持批量和增量索引 ([开放深度][6])。

---

## 二、RAG‑Anything 支持的文件类型

RAG‑Anything 是对 LightRAG 的多模态扩展，能够端到端处理以下格式，并自动构建跨模态知识图谱 ([GitHub][2])：

* **PDF**
* **Office 文档**：DOC/DOCX、PPT/PPTX、XLS/XLSX
* **图像格式**：JPEG, PNG 等
* **表格**：内嵌 Excel 格式表格数据
* **数学公式**：支持 LaTeX 和图像中的公式识别
* **自然语言文本**：Markdown、TXT 等格式

### ✅ 多模态元素处理能力

* 系统通过 MinerU 框架，实现文本、图像、表格与公式并行解析与分类处理 ([GitHub][2], [每时AI][5], [GitHub][7])。
* 架构支持内容分解为：文本块、视觉块、表格块与公式块，并保留元素间语义上下文关系。
* 支持自动实体提取与跨模态关系映射至知识图谱，提升检索和回答场景准确性。

---

## 三、技术对比汇总表

| 框架 / 系统          | 支持格式类型                                              | 多模态处理能力与特点                             |
| ---------------- | --------------------------------------------------- | -------------------------------------- |
| **LightRAG**     | PDF、DOC/DOCX、PPT/PPTX、XLS/XLSX、TXT、CSV、Markdown、图像等 | 主要支持文本与表格；图像内容需 OCR 与手动内容注入；支持结构化分块与索引 |
| **RAG‑Anything** | 前者支持全部 + 图像、表格、数学公式等多模态格式                           | 原生支持跨模态解析；自动构建实体与关系图谱；模态感知检索与图谱融合检索策略  |

---
