<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">{{ $t('agent.list') }}</h1>
      <div class="search-container">
        <el-input
          v-model="searchQuery"
          placeholder="Search for Agents/Dataflows..."
          clearable
          @input="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
      <div class="page-actions">
        <el-button type="primary" @click="handleCreateAgent">
          <el-icon><Plus /></el-icon>
          {{ $t('agent.create') }}
        </el-button>
      </div>
    </div>

    <!-- Loading state -->
    <el-card v-if="isLoading" class="loading-container">
      <el-skeleton :rows="5" animated />
    </el-card>
    
    <!-- Tabs for different agent categories -->
    <div v-else>
      <el-tabs v-model="activeTab" class="agent-tabs">
        <!-- Agent Hub Tab -->
        <el-tab-pane :label="'Agent Hub (' + filteredHubAgents.length + ')'" name="hub">
          <!-- Empty state for hub agents -->
          <el-empty v-if="filteredHubAgents.length === 0" :description="$t('agent.noAgentsFound')">
            <el-button type="primary" @click="handleCreateAgent">{{ $t('agent.createFirst') }}</el-button>
          </el-empty>
          
          <!-- Hub Agent card list -->
          <div v-else class="agent-cards">
            <el-card v-for="agent in filteredHubAgents" :key="agent" class="agent-card">
        <template #header>
          <div class="agent-card-header">
            <h3 class="agent-card-title">{{ agent }}</h3>
            <div class="agent-status" v-if="isAgentRunning(agent)">
              <el-tag type="success" size="small">{{ $t('agent.running') }}</el-tag>
            </div>
          </div>
        </template>

        <div class="agent-card-body">
          <p class="agent-description">{{ agentDescription(agent) || $t('agent.noDescription') }}</p>
        </div>

        <div class="agent-card-footer">
          <el-button-group>
            <el-tooltip :content="$t('common.copy')" placement="top">
              <el-button size="small" @click="handleCopyAgent(agent)">
                <el-icon><CopyDocument /></el-icon>
              </el-button>
            </el-tooltip>
            <el-tooltip :content="$t('common.edit')" placement="top">
              <el-button size="small" @click="handleEditAgent(agent)">
                <el-icon><Edit /></el-icon>
              </el-button>
            </el-tooltip>
            <el-tooltip :content="$t('agent.viewLogs')" placement="top">
              <el-button size="small" type="info" @click="fetchAgentLogs(agent)">
                <el-icon><Document /></el-icon>
              </el-button>
            </el-tooltip>
            <!-- <el-tooltip :content="$t('agent.run')" placement="top" v-if="!isAgentRunning(agent)" :hide-after="0">
              <el-button size="small" type="success" @click="handleRunAgent(agent)">
                <el-icon><VideoPlay /></el-icon>
              </el-button>
            </el-tooltip>
            <el-tooltip :content="$t('agent.stop')" placement="top" v-else :hide-after="0">
              <el-button size="small" type="danger" @click="handleStopAgent(agent)">
                <el-icon><VideoPause /></el-icon>
              </el-button>
            </el-tooltip> -->
            <el-tooltip :content="$t('common.delete')" placement="top">
              <el-button size="small" type="danger" @click="handleDeleteAgent(agent)">
                <el-icon><Delete /></el-icon>
              </el-button>
            </el-tooltip>
          </el-button-group>
        </div>
            </el-card>
          </div>
        </el-tab-pane>
        
        <!-- Examples Tab -->
        <el-tab-pane :label="'Dataflows (' + filteredExampleAgents.length + ')'" name="examples">
          <!-- Empty state for example agents -->
          <el-empty v-if="filteredExampleAgents.length === 0" :description="$t('agent.noExamplesFound') || 'No example agents found'">
          </el-empty>
          
          <!-- Example Agent card list -->
          <div v-else class="agent-cards">
            <el-card v-for="agent in filteredExampleAgents" :key="agent" class="agent-card">
              <template #header>
                <div class="agent-card-header">
                  <h3 class="agent-card-title">{{ agent }}</h3>
                  <div class="agent-status" v-if="isAgentRunning(agent)">
                    <el-tag type="success" size="small">{{ $t('agent.running') }}</el-tag>
                  </div>
                </div>
              </template>

              <div class="agent-card-body">
                <p class="agent-description">{{ agentDescription(agent) || $t('agent.noDescription') }}</p>
              </div>

              <div class="agent-card-footer">
                <el-button-group>
                  <el-tooltip :content="$t('common.copy')" placement="top">
                    <el-button size="small" @click="handleCopyAgent(agent)">
                      <el-icon><CopyDocument /></el-icon>
                    </el-button>
                  </el-tooltip>
                  <el-tooltip :content="$t('common.edit')" placement="top">
                    <el-button size="small" @click="handleEditAgent(agent)">
                      <el-icon><Edit /></el-icon>
                    </el-button>
                  </el-tooltip>
                  <el-tooltip :content="$t('agent.viewLogs')" placement="top" :hide-after="0">
                    <el-button size="small" type="info" @click="fetchAgentLogs(agent)">
                      <el-icon><Document /></el-icon>
                    </el-button>
                  </el-tooltip>
                  <!-- <el-tooltip :content="$t('agent.run')" placement="top" v-if="!isAgentRunning(agent)" :hide-after="0">
                    <el-button size="small" type="success" @click="handleRunAgent(agent)">
                      <el-icon><VideoPlay /></el-icon>
                    </el-button>
                  </el-tooltip>
                  <el-tooltip :content="$t('agent.stop')" placement="top" v-else>
                    <el-button size="small" type="danger" @click="handleStopAgent(agent)">
                      <el-icon><VideoPause /></el-icon>
                    </el-button>
                  </el-tooltip> -->
                  <el-tooltip :content="$t('common.delete')" placement="top">
                    <el-button size="small" type="danger" @click="handleDeleteAgent(agent)">
                      <el-icon><Delete /></el-icon>
                    </el-button>
                  </el-tooltip>
                </el-button-group>
              </div>
            </el-card>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- Copy Agent Dialog -->
    <el-dialog v-model="copyDialogVisible" :title="$t('agent.copyAgent')" width="40%">
      <el-form :model="copyForm" label-width="120px">
        <el-form-item :label="$t('agent.sourceAgent')">
          <el-input v-model="copyForm.source" disabled />
        </el-form-item>
        <el-form-item :label="$t('agent.newAgent')">
          <el-input v-model="copyForm.target" :placeholder="$t('agent.enterNewAgentName')" />
        </el-form-item>
        <el-form-item :label="$t('settings.agentType')">
          <el-radio-group v-model="copyForm.agentType">
            <el-radio label="auto">{{ $t('agent.autoDetect') }}</el-radio>
            <el-radio label="agent-hub">{{ $t('settings.agentHubDir') }}</el-radio>
            <el-radio label="examples">{{ $t('settings.examplesDir') }}</el-radio>
          </el-radio-group>
          <div class="form-help">{{ $t('agent.agentTypeHelp') }}</div>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="copyDialogVisible = false">{{ $t('common.cancel') }}</el-button>
          <el-button type="primary" @click="confirmCopyAgent" :loading="isCopying">
            {{ $t('agent.confirmCopy') }}
          </el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- Agent Log Drawer -->
    <el-drawer
      v-model="logDrawerVisible"
      :title="`${selectedAgentName} ${$t('agent.runningLogs')}`"
      direction="rtl"
      size="50%">
      <div class="log-container">
        <div class="log-controls">
          <el-input v-model="logSearchText" placeholder="搜索日志..." clearable class="log-search">
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          <el-select v-model="logTypeFilter" placeholder="日志类型" clearable class="log-type-filter">
            <el-option label="所有" value="all" />
            <el-option label="INFO" value="INFO" />
            <el-option label="DEBUG" value="DEBUG" />
            <el-option label="WARNING" value="WARNING" />
            <el-option label="ERROR" value="ERROR" />
          </el-select>
          <el-button @click="expandAllLogs" type="primary" plain>
            {{ allExpanded ? '折叠全部' : '展开全部' }}
          </el-button>
        </div>
        
        <div class="log-stats" v-if="filteredLogs.length > 0">
          显示 {{ filteredLogs.length }} 条日志
        </div>
        
        <div class="structured-logs" v-if="parsedLogs.length > 0">
          <el-collapse v-model="activeLogSections">
            <el-collapse-item v-for="(section, index) in filteredLogs" :key="index" :name="index.toString()">
              <template #title>
                <div class="log-section-title">
                  <span v-html="highlightSearchText(section.title)"></span>
                  <span class="log-time">{{ section.time }}</span>
                </div>
              </template>
              <pre class="log-content" v-html="highlightSearchText(section.content)"></pre>
            </el-collapse-item>
          </el-collapse>
        </div>
        
        <div v-else-if="currentAgentLogs" class="agent-logs">
          <pre>{{ currentAgentLogs }}</pre>
        </div>
        
        <div v-else class="no-logs-message">
          {{ $t('agent.noLogs') }}
        </div>
        
        <div class="log-footer">
          <el-button @click="logDrawerVisible = false">{{ $t('common.close') }}</el-button>
          <el-button type="primary" @click="fetchAgentLogs(selectedAgentName)">刷新日志</el-button>
        </div>
      </div>
    </el-drawer>
    
    <!-- Process Output Dialog -->
    <el-dialog 
      v-model="processOutputDialogVisible" 
      :title="$t('agent.processOutput') + ' - ' + selectedAgentName" 
      width="80%" 
      :before-close="handleCloseProcessDialog"
      fullscreen
      destroy-on-close
    >
      <div class="process-output-container">
        <el-tabs v-model="terminalTab">
          <el-tab-pane label="进程输出" name="output">
            <div class="process-output-header">
              <div class="process-info" v-if="processOutput">
                <el-tag :type="processOutput.is_running ? 'success' : 'info'">
                  {{ processOutput.is_running ? '运行中' : '已停止' }}
                </el-tag>
                <span class="process-elapsed-time" v-if="processOutput.elapsed_time">
                  运行时间: {{ formatElapsedTime(processOutput.elapsed_time) }}
                </span>
              </div>
              <div class="process-controls">
                <el-button type="primary" size="small" @click="refreshProcessOutput" :loading="refreshingOutput">
                  <el-icon><Refresh /></el-icon> 刷新
                </el-button>
                <el-button type="primary" size="small" @click="toggleAutoRefresh">
                  {{ autoRefresh ? '停止自动刷新' : '自动刷新' }}
                </el-button>
                <el-button type="danger" size="small" @click="handleStopAgent(selectedAgentName)">
                  <el-icon><VideoPause /></el-icon> 停止运行
                </el-button>
              </div>
            </div>
            
            <div class="process-output-content">
              <pre v-if="processOutput && processOutput.all_output && processOutput.all_output.length > 0" class="process-output-text">
{{ processOutput.all_output.join('\n') }}</pre>
              <div v-else class="no-output-message">
                {{ $t('agent.noOutput') }}
              </div>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="SSH 终端" name="ssh">
            <ssh-terminal 
              :title="`${selectedAgentName} SSH 终端`" 
              :auto-connect="true" 
              :agent-path="getAgentPath(selectedAgentName)" 
            />
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted, inject, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAgentStore } from '../store/agent'
import { Search, Plus, Edit, Document, VideoPlay, VideoPause, Delete, CopyDocument, Refresh, Close, View } from '@element-plus/icons-vue'
import { ElMessageBox, ElMessage, ElDrawer } from 'element-plus'
import { useI18n } from 'vue-i18n'
import SshTerminal from '../components/SshTerminal.vue'

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
    View,
    Refresh,
    Close,
    SshTerminal
  },
  setup() {
    const router = useRouter()
    const agentStore = useAgentStore()
    const { t } = useI18n()
    
    // 本地搜索查询
    const searchQuery = ref('')
    
    // 日志相关
    const logDrawerVisible = ref(false)
    const currentAgentLogs = ref('')
    const parsedLogs = ref([])
    const filteredLogs = ref([])
    const activeLogSections = ref([])
    const logSearchText = ref('')
    const logTypeFilter = ref('')
    const allExpanded = ref(false)
    const selectedAgentName = ref('')
    
    // 进程输出相关
    const processOutputDialogVisible = ref(false)
    const processOutput = ref(null)
    const refreshingOutput = ref(false)
    const autoRefresh = ref(false)
    const autoRefreshInterval = ref(null)
    const terminalTab = ref('ssh')  // 默认显示 SSH 终端页面
    const copyDialogVisible = ref(false)
    const copyForm = ref({
      source: '',
      target: '',
      agentType: 'auto' // 'auto', 'agent-hub' 或 'examples'
    })
    const isCopying = ref(false)
    
    const isLoading = computed(() => agentStore.isLoading)
    const error = computed(() => agentStore.error)
    
    const activeTab = ref('hub') // 默认显示hub标签页
    
    // 过滤hub代理列表
    const filteredHubAgents = computed(() => {
      if (!searchQuery.value) {
        return agentStore.hubAgents
      }
      const query = searchQuery.value.toLowerCase()
      return agentStore.hubAgents.filter(agent => 
        agent.toLowerCase().includes(query)
      )
    })
    
    // 过滤example代理列表
    const filteredExampleAgents = computed(() => {
      if (!searchQuery.value) {
        return agentStore.exampleAgents
      }
      const query = searchQuery.value.toLowerCase()
      return agentStore.exampleAgents.filter(agent => 
        agent.toLowerCase().includes(query)
      )
    })
    
    // 兼容原有代码，合并所有过滤后的代理
    const filteredAgents = computed(() => {
      return [...filteredHubAgents.value, ...filteredExampleAgents.value]
    })
  
    // 处理搜索
    const handleSearch = () => {
      // 搜索逻辑已经在 filteredAgents 计算属性中处理
    }
    
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
        activeLogSections.value = filteredLogs.value.map((_, index) => index.toString())
      }
      allExpanded.value = !allExpanded.value
    }
    
    // 获取进程输出
    const fetchProcessOutput = async (agentName) => {
      selectedAgentName.value = agentName
      refreshingOutput.value = true
      
      try {
        const result = await agentStore.fetchProcessOutput(agentName)
        
        if (result.success) {
          processOutput.value = result
          processOutputDialogVisible.value = true
          
          // 如果进程已经结束，停止自动刷新
          if (!result.is_running && autoRefresh.value) {
            toggleAutoRefresh()
          }
        } else {
          ElMessage.warning(`Failed to get process output: ${result.error}`)
        }
      } catch (error) {
        console.error('Error fetching process output:', error)
        ElMessage.error(`Failed to get process output: ${error.message || error}`)
      } finally {
        refreshingOutput.value = false
      }
    }
    
    // 刷新进程输出
    const refreshProcessOutput = () => {
      if (selectedAgentName.value) {
        fetchProcessOutput(selectedAgentName.value)
      }
    }
    
    // 处理关闭进程输出对话框
    const handleCloseProcessDialog = () => {
      processOutputDialogVisible.value = false
      
      // 如果自动刷新已开启，停止自动刷新
      if (autoRefresh.value) {
        toggleAutoRefresh()
      }
    }
    
    // 切换自动刷新
    const toggleAutoRefresh = () => {
      autoRefresh.value = !autoRefresh.value
      
      if (autoRefresh.value) {
        // 启动自动刷新
        autoRefreshInterval.value = setInterval(() => {
          refreshProcessOutput()
        }, 2000) // 每2秒刷新一次
      } else {
        // 停止自动刷新
        if (autoRefreshInterval.value) {
          clearInterval(autoRefreshInterval.value)
          autoRefreshInterval.value = null
        }
      }
    }
    
    // 格式化运行时间
    const formatElapsedTime = (seconds) => {
      const minutes = Math.floor(seconds / 60)
      const remainingSeconds = Math.floor(seconds % 60)
      
      if (minutes > 0) {
        return `${minutes}分${remainingSeconds}秒`
      } else {
        return `${remainingSeconds}秒`
      }
    }
    
    // 获取 Agent 路径
    const getAgentPath = (agentName) => {
      // 检查是否是 example 类型的 Agent
      const isExample = agentStore.exampleAgents.includes(agentName)
      
      if (isExample) {
        return `/mnt/c/Users/ufop/Desktop/code/mofa_second_stage/mofa/python/examples/${agentName}`
      } else {
        return `/mnt/c/Users/ufop/Desktop/code/mofa_second_stage/mofa/python/agent-hub/${agentName}`
      }
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
        ElMessage.warning('Please enter a new Agent name')
        return
      }
      
      isCopying.value = true
      // 如果选择了 'auto'，则传递 null 作为 agentType
      const agentType = copyForm.value.agentType === 'auto' ? null : copyForm.value.agentType
      const result = await agentStore.copyAgent(copyForm.value.source, copyForm.value.target, agentType)
      isCopying.value = false
      
      if (result) {
        copyDialogVisible.value = false
        ElMessage.success(`Agent copied successfully: ${copyForm.value.source} → ${copyForm.value.target}`)
      } else {
        ElMessage.error(`Failed to copy Agent: ${error.value}`)
      }
    }
    
    const handleDeleteAgent = (agentName) => {
      ElMessageBox.confirm(
        t('agent.deleteConfirm', { name: agentName }),
        t('agent.delete'),
        {
          confirmButtonText: t('common.delete'),
          cancelButtonText: t('common.cancel'),
          type: 'warning'
        }
      )
        .then(async () => {
          const result = await agentStore.deleteAgent(agentName)
          if (result) {
            ElMessage.success(t('agent.deleteSuccess', { name: agentName }))
          } else {
            ElMessage.error(t('agent.deleteError', { error: error.value }))
          }
        })
        .catch(() => {
          // 用户取消操作
        })
    }
    
    const handleRunAgent = async (agentName) => {
      const result = await agentStore.runAgent(agentName)
      if (result.success) {
        ElMessage.success(`Agent ${agentName} started successfully`)
        
        // 检查是否是 example 类型的 Agent
        const isExample = agentStore.exampleAgents.includes(agentName)
        
        if (isExample) {
          // 如果是 example 类型，直接打开 SSH 终端对话框
          selectedAgentName.value = agentName
          processOutputDialogVisible.value = true
          terminalTab.value = 'ssh'  // 默认显示 SSH 终端页面
          
          // 同时获取进程输出，以便在另一个标签页显示
          setTimeout(() => fetchProcessOutput(agentName), 500)
        } else {
          // 如果是 agent-hub 类型，打开日志查看
          setTimeout(() => fetchAgentLogs(agentName), 500)
        }
      } else {
        ElMessage.error(`Failed to start Agent: ${result.error}`)
      }
    }
    
    const handleStopAgent = async (agentName) => {
      const result = await agentStore.stopAgent(agentName)
      if (result.success) {
        ElMessage.success(`Agent ${agentName} stopped successfully`)
      } else {
        ElMessage.error(`Failed to stop Agent: ${result.error}`)
      }
    }
    
    onMounted(() => {
      fetchAgents()
    })
    
    return {
      searchQuery,
      isLoading,
      activeTab,
      filteredHubAgents,
      filteredExampleAgents,
      filteredAgents,
      handleSearch,
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
      fetchAgentLogs,
      // 进程输出相关
      processOutputDialogVisible,
      processOutput,
      refreshingOutput,
      autoRefresh,
      fetchProcessOutput,
      refreshProcessOutput,
      toggleAutoRefresh,
      formatElapsedTime,
      handleCloseProcessDialog,
      terminalTab,
      getAgentPath
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
  gap: 16px;
}

.search-container {
  flex: 1;
  max-width: 400px;
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

.agent-tabs {
  margin-bottom: 20px;
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

/* 进程输出样式 */
.process-output-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 10px;
}

.process-output-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.process-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.process-elapsed-time {
  font-size: 0.9em;
  color: #606266;
}

.process-controls {
  display: flex;
  gap: 10px;
}

.process-output-content {
  flex: 1;
  overflow: auto;
  background-color: #1e1e1e;
  border-radius: 4px;
  padding: 10px;
}

.process-output-text {
  white-space: pre-wrap;
  font-family: monospace;
  color: #d4d4d4;
  margin: 0;
  line-height: 1.5;
}

.no-output-message {
  padding: 20px;
  text-align: center;
  color: #909399;
  font-style: italic;
}

[data-theme="light"] .process-output-content {
  background-color: #f5f5f5;
}

[data-theme="light"] .process-output-text {
  color: #333;
}
</style>
