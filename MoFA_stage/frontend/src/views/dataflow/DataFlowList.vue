<template>
  <div class="dataflow-list-container">
    <div class="header">
      <h1>数据流编排</h1>
      <el-button type="primary" @click="createNewDataFlow">创建新数据流</el-button>
    </div>

    <el-card class="description-card">
      <div class="description">
        <p>数据流编排允许您将多个Agent连接在一起，形成一个数据处理流水线。一个Agent的输出可以作为另一个Agent的输入，实现复杂的数据处理和任务编排。</p>
      </div>
    </el-card>

    <div class="dataflow-list">
      <el-empty v-if="dataFlows.length === 0" description="暂无数据流，点击上方按钮创建" />
      
      <el-row :gutter="20" v-else>
        <el-col :span="8" v-for="flow in dataFlows" :key="flow.flow_id">
          <el-card class="dataflow-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <h3>{{ flow.name }}</h3>
                <div class="actions">
                  <el-button type="primary" size="small" @click="editDataFlow(flow)">编辑</el-button>
                  <el-button type="success" size="small" @click="runDataFlow(flow)">运行</el-button>
                  <el-dropdown trigger="click" @command="handleCommand($event, flow)">
                    <el-button type="info" size="small" icon="el-icon-more"></el-button>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item command="duplicate">复制</el-dropdown-item>
                        <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </div>
              </div>
            </template>
            <div class="card-content">
              <p class="description">{{ flow.description || '无描述' }}</p>
              <div class="stats">
                <div class="stat-item">
                  <span class="label">节点数:</span>
                  <span class="value">{{ flow.nodes.length }}</span>
                </div>
                <div class="stat-item">
                  <span class="label">连接数:</span>
                  <span class="value">{{ flow.connections.length }}</span>
                </div>
                <div class="stat-item">
                  <span class="label">状态:</span>
                  <el-tag :type="getStatusType(flow.status)">{{ flow.status }}</el-tag>
                </div>
              </div>
              <div class="last-updated">
                <span>最后更新: {{ formatDate(flow.updated_at) }}</span>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 创建/编辑数据流对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEditing ? '编辑数据流' : '创建新数据流'"
      width="30%"
    >
      <el-form :model="formData" label-width="80px">
        <el-form-item label="名称">
          <el-input v-model="formData.name" placeholder="请输入数据流名称"></el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="formData.description"
            type="textarea"
            placeholder="请输入数据流描述"
          ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveDataFlow">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 确认删除对话框 -->
    <el-dialog
      v-model="deleteDialogVisible"
      title="确认删除"
      width="30%"
    >
      <span>确定要删除数据流 "{{ selectedFlow?.name }}" 吗？此操作不可恢复。</span>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="deleteDialogVisible = false">取消</el-button>
          <el-button type="danger" @click="confirmDelete">确定删除</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import dataflowApi from '@/api/dataflow'

export default {
  name: 'DataFlowList',
  setup() {
    const router = useRouter()
    const dataFlows = ref([])
    const dialogVisible = ref(false)
    const deleteDialogVisible = ref(false)
    const isEditing = ref(false)
    const selectedFlow = ref(null)
    const formData = ref({
      name: '',
      description: ''
    })

    // 获取所有数据流
    const fetchDataFlows = async () => {
      try {
        const response = await dataflowApi.getAllDataFlows()
        if (response.data.success) {
          dataFlows.value = response.data.flows
        } else {
          ElMessage.error(response.data.message || '获取数据流列表失败')
        }
      } catch (error) {
        console.error('Error fetching dataflows:', error)
        ElMessage.error('获取数据流列表失败')
      }
    }

    // 创建新数据流
    const createNewDataFlow = () => {
      isEditing.value = false
      formData.value = {
        name: '',
        description: ''
      }
      dialogVisible.value = true
    }

    // 编辑数据流
    const editDataFlow = (flow) => {
      isEditing.value = true
      selectedFlow.value = flow
      formData.value = {
        name: flow.name,
        description: flow.description
      }
      dialogVisible.value = true
    }

    // 保存数据流
    const saveDataFlow = async () => {
      try {
        if (!formData.value.name) {
          ElMessage.warning('请输入数据流名称')
          return
        }

        let response
        if (isEditing.value) {
          response = await dataflowApi.updateDataFlow(selectedFlow.value.flow_id, formData.value)
        } else {
          response = await dataflowApi.createDataFlow(formData.value)
        }

        if (response.data.success) {
          ElMessage.success(isEditing.value ? '数据流更新成功' : '数据流创建成功')
          dialogVisible.value = false
          await fetchDataFlows()
          
          // 如果是新创建的，跳转到编辑页面
          if (!isEditing.value) {
            router.push(`/dataflows/${response.data.flow.flow_id}/edit`)
          }
        } else {
          ElMessage.error(response.data.message || (isEditing.value ? '更新数据流失败' : '创建数据流失败'))
        }
      } catch (error) {
        console.error('Error saving dataflow:', error)
        ElMessage.error(isEditing.value ? '更新数据流失败' : '创建数据流失败')
      }
    }

    // 运行数据流
    const runDataFlow = async (flow) => {
      try {
        const response = await dataflowApi.runDataFlow(flow.flow_id)
        if (response.data.success) {
          ElMessage.success('数据流已开始运行')
          await fetchDataFlows()
        } else {
          ElMessage.error(response.data.message || '运行数据流失败')
        }
      } catch (error) {
        console.error('Error running dataflow:', error)
        ElMessage.error('运行数据流失败')
      }
    }

    // 处理下拉菜单命令
    const handleCommand = (command, flow) => {
      if (command === 'duplicate') {
        duplicateDataFlow(flow)
      } else if (command === 'delete') {
        selectedFlow.value = flow
        deleteDialogVisible.value = true
      }
    }

    // 复制数据流
    const duplicateDataFlow = async (flow) => {
      try {
        const newFlow = {
          name: `${flow.name} (复制)`,
          description: flow.description,
          nodes: flow.nodes,
          connections: flow.connections
        }
        
        const response = await dataflowApi.createDataFlow(newFlow)
        if (response.data.success) {
          ElMessage.success('数据流复制成功')
          await fetchDataFlows()
        } else {
          ElMessage.error(response.data.message || '复制数据流失败')
        }
      } catch (error) {
        console.error('Error duplicating dataflow:', error)
        ElMessage.error('复制数据流失败')
      }
    }

    // 确认删除
    const confirmDelete = async () => {
      try {
        const response = await dataflowApi.deleteDataFlow(selectedFlow.value.flow_id)
        if (response.data.success) {
          ElMessage.success('数据流删除成功')
          deleteDialogVisible.value = false
          await fetchDataFlows()
        } else {
          ElMessage.error(response.data.message || '删除数据流失败')
        }
      } catch (error) {
        console.error('Error deleting dataflow:', error)
        ElMessage.error('删除数据流失败')
      }
    }

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '未知'
      const date = new Date(dateString)
      return date.toLocaleString()
    }

    // 获取状态类型
    const getStatusType = (status) => {
      const statusMap = {
        'idle': 'info',
        'running': 'warning',
        'completed': 'success',
        'failed': 'danger',
        'stopped': 'info'
      }
      return statusMap[status] || 'info'
    }

    onMounted(() => {
      fetchDataFlows()
    })

    return {
      dataFlows,
      dialogVisible,
      deleteDialogVisible,
      isEditing,
      selectedFlow,
      formData,
      createNewDataFlow,
      editDataFlow,
      saveDataFlow,
      runDataFlow,
      handleCommand,
      confirmDelete,
      formatDate,
      getStatusType
    }
  }
}
</script>

<style scoped>
.dataflow-list-container {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.description-card {
  margin-bottom: 20px;
}

.description {
  line-height: 1.6;
}

.dataflow-list {
  margin-top: 20px;
}

.dataflow-card {
  margin-bottom: 20px;
  transition: all 0.3s;
}

.dataflow-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 16px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.actions {
  display: flex;
  gap: 5px;
}

.card-content {
  padding: 10px 0;
}

.description {
  margin-bottom: 15px;
  color: #666;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.stats {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 10px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.label {
  color: #909399;
}

.value {
  font-weight: bold;
}

.last-updated {
  font-size: 12px;
  color: #909399;
  text-align: right;
}
</style>
