const id = "quick-start.md";
						const collection = "docs";
						const slug = "quick-start";
						const body = "\n# 快速开始\n\n欢迎使用 MoFA！本指南将帮助你在 5 分钟内创建你的第一个 AI 代理。\n\n## 系统要求\n\n- Python 3.8 或更高版本\n- pip 包管理器\n- 至少 4GB 内存\n\n## 安装\n\n### 使用 pip 安装\n\n```bash\npip install mofa\n```\n\n### 从源码安装\n\n```bash\ngit clone https://github.com/moxin-org/mofa.git\ncd mofa\npip install -e .\n```\n\n## 创建第一个代理\n\n### 1. 导入必要的模块\n\n```python\nfrom mofa import Agent, Pipeline\nfrom mofa.messages import HumanMessage\n```\n\n### 2. 创建一个简单的问答代理\n\n```python\n# 创建代理\nagent = Agent(\n    name=\"qna-agent\",\n    model=\"gpt-3.5-turbo\",\n    system_prompt=\"你是一个友好的 AI 助手，请用中文回答问题。\"\n)\n\n# 创建管道\npipeline = Pipeline()\npipeline.add(agent)\n```\n\n### 3. 与代理对话\n\n```python\n# 发送消息\nmessage = HumanMessage(content=\"什么是 MoFA？\")\nresponse = pipeline.run(message)\n\nprint(response.content)\n```\n\n## 下一步\n\n恭喜！你已经成功创建了第一个 MoFA 代理。接下来你可以：\n\n- 了解[核心概念](/docs/concepts/agent)\n- 探索[更多示例](/examples)\n- 查看[API 文档](/docs/api)\n- 加入[社区讨论](https://discord.gg/mofa)\n\n## 常见问题\n\n### 安装失败怎么办？\n\n确保你的 Python 版本是 3.8 或更高：\n\n```bash\npython --version\n```\n\n### 如何设置 API 密钥？\n\nMoFA 支持环境变量配置：\n\n```bash\nexport OPENAI_API_KEY=\"your-api-key\"\n```\n\n或在代码中设置：\n\n```python\nagent = Agent(\n    name=\"my-agent\",\n    model=\"gpt-3.5-turbo\",\n    api_key=\"your-api-key\"\n)\n``` ";
						const data = {title:"快速开始",description:"5分钟内开始使用 MoFA 构建你的第一个 AI 应用"};
						const _internal = {
							type: 'content',
							filePath: "/Users/liyao/Code/mofa/mofa-website/src/content/docs/quick-start.md",
							rawData: "\ntitle: 快速开始\ndescription: 5分钟内开始使用 MoFA 构建你的第一个 AI 应用",
						};

export { _internal, body, collection, data, id, slug };
