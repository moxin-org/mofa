#!/bin/bash
# RAG 系统清理脚本

echo "🧹 清理 RAG 系统..."

# 停止 Qdrant 容器
echo "🛑 停止 Qdrant 服务..."
docker-compose -f docker-compose.qdrant.yml down

# 清理数据
echo "🗑️  清理本地数据..."
rm -rf rag_storage/
rm -rf qdrant_storage/

# 清理 Docker 卷（可选）
echo "🔄 清理 Docker 卷..."
docker volume prune -f

echo "✅ 清理完成！"
echo "💡 如需重新开始，请运行: python demo_rag.py"