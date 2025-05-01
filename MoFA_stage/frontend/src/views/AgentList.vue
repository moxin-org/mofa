<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">Agent 列表</h1>
      <div class="page-actions">
        <el-button type="primary" @click="handleCreateAgent">
          <el-icon><Plus /></el-icon>
          创建 Agent
        </el-button>
      </div>
    </div>

    <!-- 加载中状态 -->
    <el-card v-if="isLoading" class="loading-container">
      <el-skeleton :rows="5" animated />
    </el-card>

    <!-- 空状态 -->
    <el-empty v-else-if="filteredAgents.length === 0" description="没有找到 Agent">
      <el-button type="primary" @click="handleCreateAgent">创建第一个 Agent</el-button>
    </el-empty>

    <!-- Agent 卡片列表 -->
    <div v-else class="agent-cards">
      <el-card v-for="agent in filteredAgents" :key="agent" class="agent-card">
        <template #header>
          <div class="agent-card-header">
            <h3 class="agent-card-title">{{ agent }}</h3>
            <div class="agent-status" v-if="isAgentRunning(agent)">
              <el-tag type="success" size="small">运行中</el-tag>
            </div>
          </div>
        </template>

        <div class="agent-card-body">
          <p class="agent-description">{{ agentDescription(agent) || '无描述信息' }}</p>
        </div>

        <div class="agent-card-footer">
          <el-button-group>
            <el-tooltip content="复制" placement="top">
              <el-button size="small" @click="handleCopyAgent(agent)">
                <el-icon><CopyDocument /></el-icon>
              </el-button>
            </el-tooltip>
            <el-tooltip content="编辑" placement="top">
              <el-button size="small" @click="handleEditAgent(agent)">
                <el-icon><Edit /></el-icon>
              </el-button>
            </el-tooltip>
            <el-tooltip content="查看日志" placement="top">
              <el-button size="small" type="info" @click="fetchAgentLogs(agent)">
                <el-icon><Document /></el-icon>
              </el-button>
            </el-tooltip>
            <el-tooltip content="运行" placement="top" v-if="!isAgentRunning(agent)">
              <el-button size="small" type="success" @click="handleRunAgent(agent)">
                <el-icon><VideoPlay /></el-icon>
              </el-button>
            </el-tooltip>
            <el-tooltip content="停止" placement="top" v-else>
              <el-button size="small" type="danger" @click="handleStopAgent(agent)">
                <el-icon><VideoPause /></el-icon>
              </el-button>
            </el-tooltip>
            <el-tooltip content="删除" placement="top">
              <el-button size="small" type="danger" @click="handleDeleteAgent(agent)">
                <el-icon><Delete /></el-icon>
              </el-button>
            </el-tooltip>
          </el-button-group>
        </div>
      </el-card>
    </div>

    <!-- 复制 Agent 对话框 -->
    <el-dialog v-model="copyDialogVisible" title="复制 Agent" width="30%">
      <el-form :model="copyForm" label-width="80px">
        <el-form-item label="源 Agent">
          <el-input v-model="copyForm.source" disabled />
        </el-form-item>
        <el-form-item label="新 Agent">
          <el-input v-model="copyForm.target" placeholder="请输入新 Agent 名称" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="copyDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmCopyAgent" :loading="isCopying">
            确认复制
          </el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- Agent 日志抽屉 -->
    <el-drawer
      v-model="logDrawerVisible"
      :title="`${selectedAgentName} 运行日志`"
      direction="rtl"
      size="50%">
      <div class="log-container">
        <div v-if="parsedLogs.length > 0" class="structured-logs">
          <!-- 日志过滤和搜索 -->
          <div class="log-controls">
            <el-input
              v-model="logSearchText"
              placeholder="搜索日志内容"
              clearable
              prefix-icon="el-icon-search"
              @input="filterLogs"
              class="log-search"
            ></el-input>
            <el-select 
              v-model="logTypeFilter" 
              placeholder="日志类型" 
              clearable 
              @change="filterLogs"
              class="log-type-filter"
            >
              <el-option label="全部" value=""></el-option>
              <el-option label="Dora Daemon" value="Dora Daemon"></el-option>
              <el-option label="运行实例" value="运行实例"></el-option>
              <el-option label="其他日志" value="其他"></el-option>
            </el-select>
            <el-button type="primary" size="small" @click="expandAllLogs" class="log-expand-btn">
              {{ allExpanded ? '全部折叠' : '全部展开' }}
            </el-button>
          </div>

          <!-- 日志条目数量显示 -->
          <div class="log-stats">
            <span>共 {{ parsedLogs.length }} 个日志条目</span>
            <span v-if="filteredLogs.length !== parsedLogs.length">，当前显示 {{ filteredLogs.length }} 个</span>
          </div>

          <!-- 日志内容 -->
          <el-collapse v-model="activeLogSections">
            <el-collapse-item 
              v-for="(section, index) in filteredLogs" 
              :key="index" 
              :name="index"
              class="log-item"
            >
              <template #title>
                <div class="log-section-title">
                  <span>{{ section.title }}</span>
                  <span class="log-time" v-if="section.time">{{ section.time }}</span>
                </div>
              </template>
              <pre class="log-content" v-html="highlightSearchText(section.content)"></pre>
            </el-collapse-item>
          </el-collapse>

          <!-- 无匹配结果提示 -->
          <div v-if="filteredLogs.length === 0" class="no-logs-message">
            没有找到匹配的日志条目
          </div>
        </div>
        <pre v-else class="agent-logs">{{ currentAgentLogs }}</pre>
      </div>
      <template #footer>
        <div class="log-footer">
          <el-button @click="logDrawerVisible = false">关闭</el-button>
          <el-button type="primary" @click="fetchAgentLogs(selectedAgentName)">刷新日志</el-button>
        </div>
      </template>
    </el-drawer>
  </div>
</template>

<script>
import { ref, computed, onMounted, inject, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAgentStore } from '../store/agent'
import { Plus, Search, Edit, Delete, CopyDocument, VideoPlay, VideoPause, Document, View } from '@element-plus/icons-vue'
import { ElMessageBox, ElMessage, ElDrawer } from 'element-plus'

export default {
  name: 'AgentList',
  components: {
    Plus,
    Search,
    Edit,
    Delete,
    CopyDocument,
    VideoPlay,
    VideoPause,
    Document,
    View
  },
  setup() {
    const router = useRouter()
    const agentStore = useAgentStore()
    
    // 从全局上下文中获取搜索查询
    const globalSearchQuery = inject('searchQuery', ref(''))
    const searchQuery = ref('')
    
    // 同步全局搜索查询到本地搜索查询
    watch(globalSearchQuery, (newVal) => {
      searchQuery.value = newVal
    })
    
    // 日志查看相关变量
    const logDrawerVisible = ref(false)
    const currentAgentLogs = ref('')
    const parsedLogs = ref([])
    const filteredLogs = ref([])
    const activeLogSections = ref([0]) // 默认展开第一个日志部分
    const logSearchText = ref('')
    const logTypeFilter = ref('')
    const allExpanded = ref(false)
    const selectedAgentName = ref('')
    const copyDialogVisible = ref(false)
    const copyForm = ref({
      source: '',
      target: ''
    })
    const isCopying = ref(false)
    
    const isLoading = computed(() => agentStore.isLoading)
    const error = computed(() => agentStore.error)
    
    const filteredAgents = computed(() => {
      const query = searchQuery.value.trim().toLowerCase()
      if (!query) return agentStore.agents
      
      return agentStore.agents.filter(agent => 
        agent.toLowerCase().includes(query)
      )
    })
    
    // 解析日志内容，将其分为不同的部分
    const parseLogContent = (logContent) => {
      if (!logContent || typeof logContent !== 'string') {
        return []
      }

      // 使用正则表达式匹配日志部分的标题行
      const sectionRegex = /===\s+([^=]+)\s+===/g
      const sections = []
      let match
      let lastIndex = 0
      let sectionIndex = 0

      // 查找所有日志部分
      while ((match = sectionRegex.exec(logContent)) !== null) {
        const title = match[1].trim()
        const startIndex = match.index
        
        // 如果不是第一个部分，添加前一个部分的内容
        if (sectionIndex > 0) {
          const prevSection = sections[sectionIndex - 1]
          prevSection.content = logContent.substring(lastIndex, startIndex).trim()
        }
        
        // 提取时间信息（如果存在）
        let timeMatch = null
        if (title.includes('运行实例')) {
          // 尝试从内容中提取时间信息
          const contentAfterTitle = logContent.substring(startIndex + match[0].length)
          timeMatch = contentAfterTitle.match(/\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}/)
        }
        
        // 确定日志类型
        let type = '其他'
        if (title.includes('Dora Daemon')) {
          type = 'Dora Daemon'
        } else if (title.includes('运行实例')) {
          type = '运行实例'
        }
        
        sections.push({
          title: title,
          time: timeMatch ? timeMatch[0] : null,
          content: '',
          type: type
        })
        
        lastIndex = startIndex + match[0].length
        sectionIndex++
      }
      
      // 添加最后一个部分的内容
      if (sections.length > 0) {
        const lastSection = sections[sections.length - 1]
        lastSection.content = logContent.substring(lastIndex).trim()
      } else {
        // 如果没有找到任何部分，将整个日志作为一个部分
        sections.push({
          title: '日志内容',
          time: null,
          content: logContent,
          type: '其他'
        })
      }
      
      return sections
    }
    
    // 过滤日志
    const filterLogs = () => {
      if (!logSearchText.value && !logTypeFilter.value) {
        // 如果没有搜索条件，显示所有日志
        filteredLogs.value = parsedLogs.value
      } else {
        filteredLogs.value = parsedLogs.value.filter(log => {
          // 类型过滤
          const typeMatch = !logTypeFilter.value || log.type === logTypeFilter.value
          
          // 搜索文本过滤
          const searchMatch = !logSearchText.value || 
            log.content.toLowerCase().includes(logSearchText.value.toLowerCase()) ||
            log.title.toLowerCase().includes(logSearchText.value.toLowerCase())
            
          return typeMatch && searchMatch
        })
      }
    }
    
    // 高亮搜索文本
    const highlightSearchText = (content) => {
      if (!logSearchText.value || !content) return content
      
      // 转义特殊字符，避免正则表达式错误
      const escapedSearchText = logSearchText.value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
      const regex = new RegExp(escapedSearchText, 'gi')
      
      return content.replace(regex, match => `<span class="highlight">${match}</span>`)
    }
    
    // 展开/折叠所有日志
    const expandAllLogs = () => {
      if (allExpanded.value) {
        // 全部折叠
        activeLogSections.value = []
      } else {
        // 全部展开
        activeLogSections.value = filteredLogs.value.map((_, index) => index)
      }
      allExpanded.value = !allExpanded.value
    }

    // 获取Agent日志
    const fetchAgentLogs = async (agentName) => {
      selectedAgentName.value = agentName
      try {
        // 这里应该想服务器发起请求获取日志
        const response = await agentStore.fetchAgentLogs(agentName)
        if (response && response.success) {
          currentAgentLogs.value = response.logs || '暂无日志'
          // 解析日志内容
          parsedLogs.value = parseLogContent(response.logs)
          filteredLogs.value = parsedLogs.value
          // 默认展开第一个部分
          activeLogSections.value = parsedLogs.value.length > 0 ? [0] : []
          // 重置过滤条件
          logSearchText.value = ''
          logTypeFilter.value = ''
        } else {
          currentAgentLogs.value = '获取日志失败'
          parsedLogs.value = []
          filteredLogs.value = []
        }
      } catch (error) {
        currentAgentLogs.value = `错误: ${error.message || error}`
        parsedLogs.value = []
        filteredLogs.value = []
      }
      logDrawerVisible.value = true
    }
    
    const isAgentRunning = (agentName) => {
      return agentStore.isAgentRunning(agentName)
    }
    
    const agentDescription = (agentName) => {
      // 这里可以从详情中获取描述，但需要预先加载
      return `${agentName} Agent`
    }
    
    const fetchAgents = async () => {
      await agentStore.fetchAgents()
    }
    
    const handleCreateAgent = () => {
      router.push('/agents/create')
    }
    
    const handleEditAgent = (agentName) => {
      router.push(`/agents/${agentName}/edit`)
    }
    
    const handleCopyAgent = (agentName) => {
      copyForm.value.source = agentName
      copyForm.value.target = `${agentName}_copy`
      copyDialogVisible.value = true
    }
    
    const confirmCopyAgent = async () => {
      if (!copyForm.value.target) {
        ElMessage.warning('请输入新 Agent 名称')
        return
      }
      
      isCopying.value = true
      const result = await agentStore.copyAgent(copyForm.value.source, copyForm.value.target)
      isCopying.value = false
      
      if (result) {
        ElMessage.success(`成功复制 Agent: ${copyForm.value.source} → ${copyForm.value.target}`)
        copyDialogVisible.value = false
      } else {
        ElMessage.error(`复制 Agent 失败: ${error.value}`)
      }
    }
    
    const handleDeleteAgent = (agentName) => {
      ElMessageBox.confirm(
        `确定要删除 Agent "${agentName}" 吗？此操作不可恢复！`,
        '确认删除',
        {
          confirmButtonText: '删除',
          cancelButtonText: '取消',
          type: 'warning'
        }
      )
        .then(async () => {
          const result = await agentStore.deleteAgent(agentName)
          if (result) {
            ElMessage.success(`成功删除 Agent: ${agentName}`)
          } else {
            ElMessage.error(`删除 Agent 失败: ${error.value}`)
          }
        })
        .catch(() => {
          // 用户取消操作
        })
    }
    
    const handleRunAgent = async (agentName) => {
      const result = await agentStore.runAgent(agentName)
      if (result.success) {
        ElMessage.success(`Agent ${agentName} 已启动`)
        // 自动打开日志查看
        setTimeout(() => fetchAgentLogs(agentName), 500)
      } else {
        ElMessage.error(`启动 Agent 失败: ${result.error}`)
      }
    }
    
    const handleStopAgent = async (agentName) => {
      const result = await agentStore.stopAgent(agentName)
      if (result.success) {
        ElMessage.success(`Agent ${agentName} 已停止`)
      } else {
        ElMessage.error(`停止 Agent 失败: ${result.error}`)
      }
    }
    
    onMounted(() => {
      fetchAgents()
    })
    
    return {
      searchQuery,
      isLoading,
      filteredAgents,
      copyDialogVisible,
      copyForm,
      isCopying,
      isAgentRunning,
      agentDescription,
      handleCreateAgent,
      handleEditAgent,
      handleCopyAgent,
      confirmCopyAgent,
      handleDeleteAgent,
      handleRunAgent,
      handleStopAgent,
      // 日志相关
      logDrawerVisible,
      currentAgentLogs,
      parsedLogs,
      filteredLogs,
      activeLogSections,
      logSearchText,
      logTypeFilter,
      allExpanded,
      filterLogs,
      highlightSearchText,
      expandAllLogs,
      selectedAgentName,
      fetchAgentLogs
    }
  }
}
</script>

<style scoped>
.page-container {
  padding: 20px;
}

.page-header {
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  margin: 0;
}

.page-actions {
  display: flex;
  gap: 16px;
}

.log-container {
  height: 100%;
  padding: 10px;
  border-radius: 4px;
  overflow-y: auto;
}

.agent-logs {
  white-space: pre-wrap;
  font-family: monospace;
  background-color: #1e1e1e;
  color: #d4d4d4;
  padding: 1rem;
  border-radius: 4px;
  overflow: auto;
  height: 100%;
  margin: 0;
  line-height: 1.5;
}

.structured-logs {
  height: 100%;
  overflow: auto;
}

.log-controls {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
  align-items: center;
}

.log-search {
  flex: 1;
}

.log-type-filter {
  width: 150px;
}

.log-stats {
  margin-bottom: 10px;
  font-size: 0.9em;
  color: #606266;
}

.no-logs-message {
  padding: 20px;
  text-align: center;
  color: #909399;
  font-style: italic;
}

.highlight {
  background-color: #ffd04b;
  color: #000;
  padding: 0 2px;
  border-radius: 2px;
}

.log-item {
  margin-bottom: 5px;
}

.log-section-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.log-time {
  font-size: 0.85em;
  color: #8a8a8a;
  margin-left: 10px;
}

.log-content {
  white-space: pre-wrap;
  font-family: monospace;
  background-color: #1e1e1e;
  color: #d4d4d4;
  padding: 1rem;
  border-radius: 4px;
  overflow: auto;
  margin: 0;
  line-height: 1.5;
}

[data-theme="light"] .log-container {
  background-color: #f5f5f5;
}

[data-theme="light"] .agent-logs {
  color: #333;
}

.log-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 16px;
}

.agent-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.agent-card {
  height: 100%;
}

.agent-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.agent-card-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-overflow: ellipsis;
}

.agent-card-body {
  min-height: 80px;
}

.agent-description {
  margin-top: 8px;
  color: var(--text-color-secondary);
  /* 显示最多3行，超出则省略 */
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.agent-card-footer {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

.agent-status {
  margin-left: 8px;
}

.loading-container {
  padding: 40px;
}
</style>
