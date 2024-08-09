# Agent的Config配置说明




## 1. DSPy-Agent 配置

```yml
AGENT:
  ROLE:  # AGENT名称 必传   
  BACKSTORY:  # AGENT的背景信息  
  OBJECTIVE: # 明确任务的主要目标  
  SPECIFICS:  # 列出任务的具体要求   
  ACTIONS: # 列出需要执行的具体步骤。  
  RESULTS:  # 描述预期的结果或成果  
  EXAMPLE:  # 任务的案例  
  TASK:  # 需要运行的任务
RAG:
  MODULE_PATH: null # 如果没有本地的embedding模型, 可以传递null
  RAG_MODEL_NAME: text-embedding-3-small # Openai的embedding模型名称
  PG_CONNECTION: postgresql+psycopg://langchain:langchain@localhost:6024/langchain  # Pg-Vector中的配置路径 
  COLLECTION_NAME: paper # Vector中的集合名称，使用默认值即可
  IS_UPLOAD_FILE: true # 是否需要将文件上传到Vector中，如果上传则传递true，否则传递false
  FILES_PATH:  # 需要上传的文件地址
    - ./data/input/moa_llm.pdf
  ENCODING: utf-8  # 文件编码格式 
  CHUNK_SIZE: 256 # 分割的文本大小，建议默认值256
  RAG_SEARCH_NUM: 4 # 数值越大，通过RAG查询的结果越多，相应的LLM接收的数据也越多，注意不要超过LLM最大的token数量

MODEL:
  MODEL_API_KEY:
  MODEL_NAME: gpt-3.5-turbo
  MODEL_MAX_TOKENS: 2048

ENV:
  PROXY_URL: http://192.168.31.50:10890
  AGENT_TYPE: reasoner
```

**如果你需要Ollama的配置,请参考以下内容**:
```yml
MODEL:
  MODEL_API_KEY: ollama
  MODEL_NAME: qwen:14b
  MODEL_MAX_TOKENS: 2048
  MODEL_API_URL: http://192.168.0.75:11434
```

## 2. CrewAI-Agent配置
我们使用 Python + CrewAI 库来设计 Agent。

```yml
agents:
  - name: rag_agent  # 定义代理名称
    role: 'RAG代理作为智能助手，从向量数据库中检索信息并生成上下文相关的响应。使用先进的自然语言处理和高效的数据检索。'  # 定义代理的角色和职责
    goal: '代理结合检索和生成，以满足用户需求，确保响应准确且相关。'  # 定义代理的目标
    backstory: |  # 提供代理的背景信息。也可以在此处放置Prompt。
      #### 目标:
    
      #### 具体要求:
   
      #### 任务:
    
      #### 行动:
    
      #### 结果:
    verbose: true  # 是否输出详细信息（默认值，不修改除非调试）
    allow_delegation: false  # 是否允许委派任务（默认值，不修改除非调试）
    tools:  # 代理可以使用的工具列表
      - delete_vector_collection_with_tool
      - upload_files_to_vector_with_tool
      - search_vector_with_tool

tasks:
  - description: |  # 描述任务的具体内容
      module_path: '/mnt/d/models/embeddings/bce-embedding-base_v1'
      collection_name: 'mae'
      is_upload_file: True
      multi_process: False
      pg_connection: 'postgresql+psycopg://mae:MLbDGKC7d7IPBN@124.156.214.116:6024/mae_db'
      files_path: ['./data/input/moa_llm.pdf']
     
      以下是任务: 总结论文《Mixture-of-Agents Enhances Large Language Model Capabilities》的内容，具体说明作者、日期、关键点和论文的成就。
    expected_output: 'details'  # 预期输出格式
    agent: rag_agent  # 指定负责执行任务的代理
    max_inter: 1  # 最大交互次数
    human_input: false  # 是否需要人类输入

model:
  model_api_key:  # 模型API密钥
    Description: 模型API密钥
  model_name: gpt-3.5-turbo  # 模型名称
  model_max_tokens: 2048  # 模型的最大token数
  module_api_url: null  # 模块API URL

other:
  proxy_url: http://192.168.0.75:10809  # 网络请求的代理URL，如果在中国需要配置代理

env:
  SERPER_API_KEY:     # SERPER API密钥
  AGENTOPS_API_KEY: 6805b2d1-50f8-4b7c-b88b-cff2b1c6ef27  # AGENTOPS API密钥

crewai_config:
  memory: false  # 是否启用记忆功能
```


