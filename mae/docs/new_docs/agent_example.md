### 4.1 Example项结构说明
```plaintext
agents
└── reasoner  # agent 名称
    ├── README.md  
    ├── data  # 数据存放地址
    │   └── input  # 输入数据
    │       └── moa_llm.pdf 
    ├── listener.py  # 负责监听dora流程中的结果
    ├── out # dora 流程输出
    │   ├── 019073e3-febd-7538-8ece-1ac71284ac4c
    │   └── 019073e6-71e7-7d81-87d3-d0726c9ceee5
    │       ├── log_agents.txt
    │       ├── log_listener.txt
    │       └── log_loader.txt
    ├── reasoner_dataflow.yml # dora 流程配置文件
    ├── reasoning_agent.py # agent 逻辑
    ├── reasoning_loader.py  # 加载agent 配置文件
    ├── result  # use_case输出结果保存地址
    └── use_case  # use_case配置文件
        ├── phrase_spelling_error_by_dspy.yml  # 语法错误案例
        ├── snake_game_build_by_dspy.yml  # 贪吃蛇案例
        └── summarize_pdf_by_rag.yml # 论文rag提取总结
```

# 1, Reasoner Agent
[README_zh.md](..%2F..%2Fexamples%2Fagents%2Freasoner%2FREADME_zh.md)

# 2. Self Refine Agent
[README_zh.md](..%2F..%2Fexamples%2Fagents%2Freasoner%2FREADME_zh.md)


# 3, Search SuperAgent
[README_zh.md](..%2F..%2Fexamples%2Fagents%2Fsuper_agent%2Fweb_search%2FREADME_zh.md)

# 4, arXiv Research SuperAgent
[README_zh.md](..%2F..%2Fexamples%2Fagents%2Fsuper_agent%2Fpaper%2FREADME_zh.md)
