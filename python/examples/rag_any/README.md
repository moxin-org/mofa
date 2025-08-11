# RAG-Anything 知识库问答系统

基于 Qdrant 向量数据库和 Ollama 的交互式 RAG 知识库问答系统。

## 🚀 快速开始

### 1. 启动 Qdrant 数据库

```bash
# 启动 Qdrant 向量数据库
docker-compose -f docker-compose.qdrant.yml up -d

# 检查服务状态
docker ps | grep qdrant
```

### 2. 安装依赖

```bash
pip install qdrant-client httpx
```

### 3. 运行交互式问答系统

```bash
python qdrant_rag_interactive.py
```

## ✨ 功能特性

### 🔍 智能搜索
- 基于词汇表的文档向量化
- 余弦相似度语义搜索
- 自动文档分块和索引

### 🤖 AI 问答
- 集成 Ollama 模型进行回答生成
- RAG (检索增强生成) 架构
- 显示完整的推理过程

### 💬 交互式体验
- 持续对话模式
- 实时显示搜索结果
- 完整的 RAG 上下文展示

## 🎯 使用示例

### 启动后的交互界面

```
🚀 交互式 Qdrant RAG 知识库问答系统
==================================================
✅ 使用现有集合 'knowledge_base' (394 个文档)
📖 加载词汇表 (1000 个词)

🎉 欢迎使用交互式 RAG 问答系统！
💡 提示:
   - 直接输入问题进行查询
   - 输入 'quit' 或 'exit' 退出
   - 输入 'stats' 查看系统状态
   - 输入 'help' 查看帮助

🗣️  请输入问题: Python 编程有什么优势？
```

### 完整的 RAG 结果展示

```
================================================================================
🎯 RAG 问答结果
================================================================================
❓ 问题: Python 编程有什么优势？

🤖 回答:
基于参考文档，Python 编程具有以下主要优势：

1. **简洁易学**: Python 语法简洁明了，适合初学者快速上手
2. **功能强大**: 广泛应用于数据科学、机器学习、Web开发等领域
3. **丰富生态**: 拥有大量第三方库和框架支持
4. **跨平台**: 支持多种操作系统
5. **高效开发**: 能够快速实现原型和完整应用

📚 参考文档 (3 个结果):
   1. Python基础.md (相似度: 0.756)
      预览: Python 是一种高级编程语言，具有简洁的语法和强大的功能...
   2. 数据科学入门.md (相似度: 0.642) 
      预览: 在数据科学领域，Python 被广泛使用，主要库包括 pandas, numpy...
   3. Web开发指南.md (相似度: 0.523)
      预览: Python 的 Flask 和 Django 框架为 Web 开发提供了便利...

📝 RAG 上下文 (前200字符):
   【参考文档1】
   文件: Python基础.md
   内容: Python 是一种高级编程语言，具有简洁的语法和强大的功能。它被广泛应用于各个领域...
================================================================================
```

## 🛠️ 配置选项

### 修改知识库路径

在 `qdrant_rag_interactive.py` 中修改：

```python
KNOWLEDGE_BASE_PATH = "/your/knowledge/base/path"
```

### 修改 Ollama 配置

```python
rag = InteractiveRAG(
    KNOWLEDGE_BASE_PATH,
    ollama_host="10.100.1.115:11434",
    ollama_model="gpt-oss:20b"  # 修改为你的模型
)
```

## 📊 系统架构

```
用户问题 → 文档搜索 → 上下文构建 → AI生成回答 → 结果展示
    ↓         ↓          ↓         ↓        ↓
  词汇表   → Qdrant    → RAG      → Ollama  → 完整输出
  向量化     向量搜索     提示词      模型     + 来源文档
```

## 🔧 故障排除

### Qdrant 连接问题
```bash
# 检查容器状态
docker ps | grep qdrant

# 重启服务
docker-compose -f docker-compose.qdrant.yml restart

# 查看日志
docker logs qdrant-vector-db
```

### Ollama 连接问题
1. 确认远程机器 IP 和端口
2. 检查模型名称: `ollama list`
3. 测试连接: `curl http://10.100.1.115:11434/api/tags`

### 索引问题
```bash
# 清除旧索引重新开始
rm -rf rag_storage/
python qdrant_rag_interactive.py
```

## 📝 支持的文档类型

- ✅ Markdown (.md)
- ✅ 文本文件 (.txt) 
- ✅ Python 代码 (.py)
- ✅ JSON 配置 (.json)

## 🎉 使用技巧

1. **精准提问**: 使用具体的技术关键词
2. **查看来源**: 注意参考文档的相似度分数
3. **系统状态**: 使用 'stats' 命令检查索引状态
4. **上下文理解**: RAG 上下文显示了 AI 的推理依据

## 🔄 更新索引

当知识库内容更新时：
1. 删除 `rag_storage/` 目录
2. 重新运行程序自动重建索引

---

**享受你的智能知识库问答体验！** 🎯