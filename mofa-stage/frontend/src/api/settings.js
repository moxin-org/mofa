/**
 * 设置相关的 API 服务
 */
import axios from 'axios'

const API_URL = '/api'

export default {
  /**
   * 获取所有设置
   */
  getSettings() {
    return axios.get(`${API_URL}/settings/`)
  },

  /**
   * 更新设置
   */
  updateSettings(settings) {
    return axios.put(`${API_URL}/settings/`, settings)
  },

  /**
   * 重置设置为默认值
   */
  resetSettings() {
    return axios.post(`${API_URL}/settings/reset`)
  }
}
