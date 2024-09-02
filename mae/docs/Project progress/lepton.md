### 流程文档

#### 概述
此文档描述了 `search_with_lepton.py` 脚本的整体流程。脚本通过调用多种搜索引擎，结合 Lepton AI 模型生成高质量的回答，并通过流式响应返回结果。

#### 1. 导入库与初始化
- **导入库**: `import requests`, `import leptonai`, `from fastapi import HTTPException` 等。
- **定义常量**: 搜索引擎端点，引用计数，默认查询，停止词等。

#### 2. 定义搜索函数
- **Bing 搜索**: `def search_with_bing(query: str, subscription_key: str)`
- **Google 搜索**: `def search_with_google(query: str, subscription_key: str, cx: str)`
- **Serper 搜索**: `def search_with_serper(query: str, subscription_key: str)`
- **SearchAPI 搜索**: `def search_with_searchapi(query: str, subscription_key: str)`

#### 3. RAG 类
- **类定义**: `class RAG(Photon)`
- **本地客户端**: `def local_client(self)`
- **初始化**: `def init(self)`
  - 设置后端（Bing、Google、Serper、SearchAPI、Lepton）
  - 设置模型
  - 初始化键值存储（KV）
- **生成相关问题**: `def get_related_questions(self, query, contexts)`

#### 4. 查询处理与响应
- **查询处理**: `def query_function(self, query: str, search_uuid: str, generate_related_questions: Optional[bool] = True)`
  - **接收查询**: 从用户获取查询和 UUID。
  - **执行搜索**: 调用相应的搜索函数获取上下文（例如 `self.search_function(query)`）。
  - **构建系统提示**: 使用 `_rag_query_text` 模板构建系统提示。
  - **调用 Lepton AI 模型**: 使用 `client.chat.completions.create` 生成答案。
  - **流式传输结果**: 使用 `StreamingResponse` 返回生成的答案，并将结果上传到 KV 存储。
- **流式传输响应**: `def stream_and_upload_to_kv(self, contexts, llm_response, related_questions_future, search_uuid)`

### 运行流程

1. **初始化配置**: 使用 `init` 设置搜索引擎、模型、KV 等。
2. **接收查询**: 用户通过 API 提交查询到 `query_function`。
3. **执行搜索**: 调用搜索函数（如 `search_with_bing`、`search_with_google`）获取上下文。
4. **生成答案**: 使用 Lepton AI 模型（`local_client`）生成答案和相关问题。
5. **返回结果**: 使用 `stream_and_upload_to_kv` 以流式响应方式返回结果，并将结果存储在 KV 中。





### 代码分析

#### 功能概述
该函数处理 POST 请求，对查询执行搜索并返回响应结果。如果提供的 `search_uuid` 已在 KV 中存在，则直接返回存储的结果；否则，执行新的搜索，生成答案，并将结果存储在 KV 中。

#### 流程步骤

1. **检查 `search_uuid`**：
   - 如果 `search_uuid` 存在，尝试从 KV 中获取结果。
   - 如果找到结果，使用 `StreamingResponse` 返回存储的结果。
   - 如果未找到结果或出现错误，记录日志，并继续执行新的查询。

   ```python
   if search_uuid:
       try:
           result = self.kv.get(search_uuid)
           def str_to_generator(result: str) -> Generator[str, None, None]:
               yield result
           return StreamingResponse(str_to_generator(result))
       except KeyError:
           logger.info(f"Key {search_uuid} not found, will generate again.")
       except Exception as e:
           logger.error(f"KV error: {e}\n{traceback.format_exc()}, will generate again.")
   else:
       raise HTTPException(status_code=400, detail="search_uuid must be provided.")
   ```

2. **选择后端处理**：
   - 如果后端是 Lepton，调用 `leptonsearch_client.query` 方法获取结果并返回。

   ```python
   if self.backend == "LEPTON":
       result = self.leptonsearch_client.query(
           query=query,
           search_uuid=search_uuid,
           generate_related_questions=generate_related_questions,
       )
       return StreamingResponse(content=result, media_type="text/html")
   ```

3. **执行搜索查询**：
   - 调用相应的搜索函数（如 Bing、Google）获取上下文内容。

   ```python
   query = query or _default_query
   query = re.sub(r"\[/?INST\]", "", query)
   contexts = self.search_function(query)
   ```

4. **构建系统提示**：
   - 使用 `_rag_query_text` 模板构建系统提示，包含查询上下文内容。

   ```python
   system_prompt = _rag_query_text.format(
       context="\n\n".join(
           [f"[[citation:{i+1}]] {c['snippet']}" for i, c in enumerate(contexts)]
       )
   )
   ```

5. **调用 Lepton AI 模型生成答案**：
   - 使用 `client.chat.completions.create` 方法调用 Lepton AI 模型生成答案。

   ```python
   client = self.local_client()
   llm_response = client.chat.completions.create(
       model=self.model,
       messages=[
           {"role": "system", "content": system_prompt},
           {"role": "user", "content": query},
       ],
       max_tokens=1024,
       stop=stop_words,
       stream=True,
       temperature=0.9,
   )
   ```

6. **生成相关问题（可选）**：
   - 如果需要生成相关问题，异步执行 `get_related_questions` 方法。

   ```python
   if self.should_do_related_questions and generate_related_questions:
       related_questions_future = self.executor.submit(
           self.get_related_questions, query, contexts
       )
   else:
       related_questions_future = None
   ```

7. **流式传输结果并存储**：
   - 使用 `stream_and_upload_to_kv` 方法将上下文、生成的答案和相关问题流式传输并存储到 KV 中。

   ```python
   return StreamingResponse(
       self.stream_and_upload_to_kv(
           contexts, llm_response, related_questions_future, search_uuid
       ),
       media_type="text/html",
   )
   ```
### 当前问题: 
1. 是否需要使用lepton的kv存储?如果使用,那么需要我们注册和登陆



### 总结

1. **检查 `search_uuid`**：尝试从 KV 中获取结果，若存在则返回结果，否则继续处理。
2. **选择后端处理**：若后端为 Lepton，则调用 `leptonsearch_client.query` 获取结果并返回。
3. **执行搜索查询**：调用搜索函数（如 Bing 或 Google）获取上下文内容。
4. **构建系统提示**：使用模板构建包含上下文的系统提示。
5. **调用 Lepton AI 模型**：生成答案。
6. **生成相关问题（可选）**：异步生成相关问题。
7. **流式传输结果并存储**：将上下文、答案和相关问题流式传输并存储到 KV 中。
