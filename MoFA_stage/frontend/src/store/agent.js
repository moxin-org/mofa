/**
 * Agent 状态管理
 */
import { defineStore } from 'pinia'
import agentApi from '../api/agent'

export const useAgentStore = defineStore('agent', {
  state: () => ({
    hubAgents: [],
    exampleAgents: [],
    currentAgent: null,
    currentAgentFiles: [],
    currentFile: null,
    isLoading: false,
    error: null,
    runningAgents: {}, // 保存正在运行的 agent 进程 ID
    agentLogs: {}, // 保存每个agent的日志
    processOutputs: {}, // 保存进程输出
  }),
  
  getters: {
    // 获取所有agents（合并hub和example）
    allAgents: (state) => {
      return [...state.hubAgents, ...state.exampleAgents]
    },
    
    getAgentByName: (state) => (name) => {
      // 在两个列表中查找agent
      return state.hubAgents.includes(name) || state.exampleAgents.includes(name) ? name : undefined
    },
    
    isAgentRunning: (state) => (agentName) => {
      return !!state.runningAgents[agentName]
    }
  },
  
  actions: {
    async fetchAgents() {
      this.isLoading = true
      this.error = null
      try {
        const response = await agentApi.getAllAgents()
        if (response.data && response.data.success) {
          this.hubAgents = response.data.hub_agents || []
          this.exampleAgents = response.data.example_agents || []
        } else {
          throw new Error('Failed to fetch agents')
        }
      } catch (error) {
        this.error = error.message || 'Failed to fetch agents'
        console.error(error)
      } finally {
        this.isLoading = false
      }
    },
    
    async fetchAgentDetails(agentName) {
      this.isLoading = true
      this.error = null
      try {
        const response = await agentApi.getAgentDetails(agentName)
        if (response.data && response.data.success) {
          this.currentAgent = response.data.agent
          return response.data.agent
        } else {
          throw new Error(`Failed to fetch details for agent: ${agentName}`)
        }
      } catch (error) {
        this.error = error.message || `Failed to fetch details for agent: ${agentName}`
        console.error(error)
        return null
      } finally {
        this.isLoading = false
      }
    },
    
    async fetchAgentFiles(agentName) {
      this.isLoading = true
      this.error = null
      try {
        const response = await agentApi.getAgentFiles(agentName)
        if (response.data && response.data.success) {
          this.currentAgentFiles = response.data.files
          return response.data.files
        } else {
          throw new Error(`Failed to fetch files for agent: ${agentName}`)
        }
      } catch (error) {
        this.error = error.message || `Failed to fetch files for agent: ${agentName}`
        console.error(error)
        return []
      } finally {
        this.isLoading = false
      }
    },
    
    async fetchFileContent(agentName, filePath) {
      this.isLoading = true
      this.error = null
      try {
        const response = await agentApi.getFileContent(agentName, filePath)
        if (response.data && response.data.success) {
          this.currentFile = {
            path: filePath,
            content: response.data.content,
            type: response.data.type
          }
          return this.currentFile
        } else {
          throw new Error(`Failed to fetch file content: ${filePath}`)
        }
      } catch (error) {
        this.error = error.message || `Failed to fetch file content: ${filePath}`
        console.error(error)
        return null
      } finally {
        this.isLoading = false
      }
    },
    
    async saveFileContent(agentName, filePath, content) {
      this.isLoading = true
      this.error = null
      try {
        const response = await agentApi.updateFileContent(agentName, filePath, content)
        if (response.data && response.data.success) {
          // 更新当前文件
          if (this.currentFile && this.currentFile.path === filePath) {
            this.currentFile.content = content
          }
          return true
        } else {
          throw new Error(`Failed to save file: ${filePath}`)
        }
      } catch (error) {
        this.error = error.message || `Failed to save file: ${filePath}`
        console.error(error)
        return false
      } finally {
        this.isLoading = false
      }
    },
    
    async createAgent(agentData) {
      this.isLoading = true
      this.error = null
      try {
        const response = await agentApi.createAgent(agentData)
        if (response.data && response.data.success) {
          await this.fetchAgents()
          return true
        } else {
          throw new Error(`Failed to create agent: ${agentData.name}`)
        }
      } catch (error) {
        this.error = error.message || `Failed to create agent: ${agentData.name}`
        console.error(error)
        return false
      } finally {
        this.isLoading = false
      }
    },
    
    /**
     * 复制 Agent
     * @param {string} sourceAgent - 源 Agent 名称
     * @param {string} targetAgent - 目标 Agent 名称
     * @param {string} [agentType=null] - Agent 类型，'agent-hub' 或 'examples'，如果为 null 则自动检测
     * @returns {Promise<boolean>} - 操作是否成功
     */
    async copyAgent(sourceAgent, targetAgent, agentType = null) {
      this.isLoading = true
      this.error = null
      try {
        const response = await agentApi.copyAgent(sourceAgent, targetAgent, agentType)
        if (response.data && response.data.success) {
          await this.fetchAgents()
          return true
        } else {
          throw new Error(`Failed to copy agent from ${sourceAgent} to ${targetAgent}`)
        }
      } catch (error) {
        this.error = error.message || `Failed to copy agent from ${sourceAgent} to ${targetAgent}`
        console.error(error)
        return false
      } finally {
        this.isLoading = false
      }
    },
    
    async deleteAgent(agentName) {
      this.isLoading = true
      this.error = null
      try {
        const response = await agentApi.deleteAgent(agentName)
        if (response.data && response.data.success) {
          // 从两个列表中都尝试移除
          this.hubAgents = this.hubAgents.filter(agent => agent !== agentName)
          this.exampleAgents = this.exampleAgents.filter(agent => agent !== agentName)
          
          if (this.currentAgent && this.currentAgent.name === agentName) {
            this.currentAgent = null
            this.currentAgentFiles = []
            this.currentFile = null
          }
          return true
        } else {
          throw new Error(`Failed to delete agent: ${agentName}`)
        }
      } catch (error) {
        this.error = error.message || `Failed to delete agent: ${agentName}`
        console.error(error)
        return false
      } finally {
        this.isLoading = false
      }
    },
    
    async runAgent(agentName) {
      this.isLoading = true
      this.error = null
      try {
        const response = await agentApi.runAgent(agentName)
        if (response.data && response.data.success) {
          const processId = response.data.process_id
          this.runningAgents[agentName] = processId
          return { success: true, processId }
        } else {
          throw new Error(`Failed to run agent: ${agentName}`)
        }
      } catch (error) {
        this.error = error.message || `Failed to run agent: ${agentName}`
        console.error(error)
        return { success: false, error: this.error }
      } finally {
        this.isLoading = false
      }
    },
    
    async stopAgent(agentName) {
      try {
        if (!this.runningAgents[agentName]) {
          return { success: false, error: 'Agent is not running' }
        }
        
        const processId = this.runningAgents[agentName]
        const response = await agentApi.stopAgent(processId)
        
        if (response.data && response.data.success) {
          delete this.runningAgents[agentName]
          return { success: true }
        } else {
          return { success: false, error: response.data.error || 'Failed to stop agent' }
        }
      } catch (error) {
        console.error('Error stopping agent:', error)
        return { success: false, error: error.message || 'Failed to stop agent' }
      }
    },
    
    /**
     * 获取Agent运行日志
     */
    async fetchAgentLogs(agentName) {
      try {
        const response = await agentApi.fetchAgentLogs(agentName)
        
        if (response.data && response.data.success) {
          // 将日志保存到状态中
          this.agentLogs[agentName] = response.data.logs
          return {
            success: true,
            logs: response.data.logs
          }
        } else {
          return {
            success: false, 
            error: response.data.error || '获取日志失败',
            logs: '无法获取日志'
          }
        }
      } catch (error) {
        console.error('Error fetching agent logs:', error)
        return {
          success: false,
          error: error.message || '获取日志失败',
          logs: `错误: ${error.message || error}`
        }
      }
    },
    
    /**
     * 获取正在运行的进程的输出
     * @param {string} agentName - Agent 名称
     * @returns {Promise<Object>} - 包含进程输出的对象
     */
    async fetchProcessOutput(agentName) {
      try {
        const response = await agentApi.fetchProcessOutput(agentName)
        
        if (response.data && response.data.success) {
          // 将输出保存到状态中
          this.processOutputs[agentName] = response.data
          return {
            success: true,
            ...response.data
          }
        } else {
          return {
            success: false, 
            error: response.data.message || '获取进程输出失败',
            is_running: false,
            new_output: [],
            all_output: []
          }
        }
      } catch (error) {
        console.error('Error fetching process output:', error)
        return {
          success: false,
          error: error.message || '获取进程输出失败',
          is_running: false,
          new_output: [],
          all_output: []
        }
      }
    }
  }
})
