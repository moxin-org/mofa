/**
 * Agent 相关的 API 服务
 */
import axios from 'axios'

const API_URL = '/api'

export default {
  /**
   * 获取所有 agents 列表
   */
  getAllAgents() {
    return axios.get(`${API_URL}/agents/`)
  },

  /**
   * 获取指定 agent 的详细信息
   */
  getAgentDetails(agentName) {
    return axios.get(`${API_URL}/agents/${agentName}`)
  },

  /**
   * 创建新的 agent
   */
  createAgent(agentData) {
    return axios.post(`${API_URL}/agents/`, agentData)
  },

  /**
   * 从已有 agent 复制创建新 agent
   */
  copyAgent(sourceAgent, targetAgent) {
    return axios.post(`${API_URL}/agents/copy`, {
      source: sourceAgent,
      target: targetAgent
    })
  },

  /**
   * 删除指定 agent
   */
  deleteAgent(agentName) {
    return axios.delete(`${API_URL}/agents/${agentName}`)
  },

  /**
   * 运行指定 agent
   */
  runAgent(agentName, timeout = 5) {
    return axios.post(`${API_URL}/agents/${agentName}/run`, { timeout })
  },

  /**
   * 停止正在运行的 agent
   */
  stopAgent(processId) {
    return axios.post(`${API_URL}/agents/stop/${processId}`)
  },

  /**
   * 获取 agent 运行日志
   */
  fetchAgentLogs(agentName) {
    return axios.get(`${API_URL}/agents/${agentName}/logs`)
  },

  /**
   * 获取 agent 的所有文件
   */
  getAgentFiles(agentName) {
    return axios.get(`${API_URL}/agents/${agentName}/files`)
  },

  /**
   * 获取文件内容
   */
  getFileContent(agentName, filePath) {
    return axios.get(`${API_URL}/agents/${agentName}/files/${filePath}`)
  },

  /**
   * 更新文件内容
   */
  updateFileContent(agentName, filePath, content) {
    return axios.put(`${API_URL}/agents/${agentName}/files/${filePath}`, { content })
  }
}
