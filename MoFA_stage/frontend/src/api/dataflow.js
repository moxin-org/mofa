/**
 * 数据流相关的 API 服务
 */
import axios from 'axios'

const API_URL = '/api'

export default {
  /**
   * 获取所有数据流列表
   */
  getAllDataFlows() {
    return axios.get(`${API_URL}/dataflows/`)
  },

  /**
   * 获取指定数据流的详细信息
   */
  getDataFlowDetails(flowId) {
    return axios.get(`${API_URL}/dataflows/${flowId}`)
  },

  /**
   * 创建新的数据流
   */
  createDataFlow(flowData) {
    return axios.post(`${API_URL}/dataflows/`, flowData)
  },

  /**
   * 更新数据流
   */
  updateDataFlow(flowId, flowData) {
    return axios.put(`${API_URL}/dataflows/${flowId}`, flowData)
  },

  /**
   * 删除指定数据流
   */
  deleteDataFlow(flowId) {
    return axios.delete(`${API_URL}/dataflows/${flowId}`)
  },

  /**
   * 添加节点到数据流
   */
  addNode(flowId, nodeData) {
    return axios.post(`${API_URL}/dataflows/${flowId}/nodes`, nodeData)
  },

  /**
   * 从数据流中移除节点
   */
  removeNode(flowId, nodeId) {
    return axios.delete(`${API_URL}/dataflows/${flowId}/nodes/${nodeId}`)
  },

  /**
   * 添加连接到数据流
   */
  addConnection(flowId, connectionData) {
    return axios.post(`${API_URL}/dataflows/${flowId}/connections`, connectionData)
  },

  /**
   * 从数据流中移除连接
   */
  removeConnection(flowId, connectionId) {
    return axios.delete(`${API_URL}/dataflows/${flowId}/connections/${connectionId}`)
  },

  /**
   * 运行数据流
   */
  runDataFlow(flowId) {
    return axios.post(`${API_URL}/dataflows/${flowId}/run`)
  },

  /**
   * 停止数据流
   */
  stopDataFlow(flowId) {
    return axios.post(`${API_URL}/dataflows/${flowId}/stop`)
  },

  /**
   * 获取数据流状态
   */
  getDataFlowStatus(flowId) {
    return axios.get(`${API_URL}/dataflows/${flowId}/status`)
  }
}
