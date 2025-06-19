/**
 * VS Code Web API
 */

const API_BASE_URL = '/api/vscode'

export default {
  /**
   * 启动 VS Code Web 服务器
   * @param {string} agentName - Agent 名称
   * @param {number} port - 可选端口号
   * @returns {Promise} API 响应
   */
  async startVSCode(agentName, port = null) {
    const response = await fetch(`${API_BASE_URL}/start/${agentName}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ port })
    })
    return response.json()
  },

  /**
   * 停止 VS Code Web 服务器
   * @returns {Promise} API 响应
   */
  async stopVSCode() {
    const response = await fetch(`${API_BASE_URL}/stop`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    return response.json()
  },

  /**
   * 获取 VS Code Web 状态
   * @returns {Promise} API 响应
   */
  async getVSCodeStatus() {
    const response = await fetch(`${API_BASE_URL}/status`)
    return response.json()
  },

  /**
   * 安装 code-server
   * @returns {Promise} API 响应
   */
  async installVSCode() {
    const response = await fetch(`${API_BASE_URL}/install`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    return response.json()
  },

  /**
   * 为指定 agent 安装推荐扩展
   * @param {string} agentName - Agent 名称
   * @returns {Promise} API 响应
   */
  async installExtensions(agentName) {
    const response = await fetch(`${API_BASE_URL}/install-extensions/${agentName}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    return response.json()
  },

  /**
   * 更新指定 agent 的 VS Code 配置
   * @param {string} agentName - Agent 名称
   * @returns {Promise} API 响应
   */
  async updateConfig(agentName) {
    const response = await fetch(`${API_BASE_URL}/config/${agentName}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    return response.json()
  }
} 