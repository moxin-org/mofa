<template>
  <div class="dataflow-list-container">
    <div class="header">
      <h1>{{ $t('dataflow.title') }}</h1>
      <el-button type="primary" @click="createNewDataFlow">{{ $t('dataflow.createNew') }}</el-button>
    </div>

    <el-card class="description-card">
      <div class="description">
        <p>{{ $t('dataflow.description') }}</p>
      </div>
    </el-card>

    <div class="dataflow-list">
      <el-empty v-if="dataFlows.length === 0" :description="$t('dataflow.noDataflows')" />
      
      <el-row :gutter="20" v-else>
        <el-col :span="8" v-for="flow in dataFlows" :key="flow.flow_id">
          <el-card class="dataflow-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <h3>{{ flow.name }}</h3>
                <div class="actions">
                  <el-button type="primary" size="small" @click="editFlowVisually(flow)">{{ $t('dataflow.editFlow') }}</el-button>
                  <el-dropdown trigger="click" @command="handleCommand($event, flow)">
                    <el-button type="primary" size="small">{{ $t('common.edit') }} <i class="el-icon-arrow-down el-icon--right"></i></el-button>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item command="edit">{{ $t('dataflow.editInfo') }}</el-dropdown-item>
                        <el-dropdown-item command="run">{{ $t('agent.run') }}</el-dropdown-item>
                        <el-dropdown-item command="duplicate">{{ $t('dataflow.copy') }}</el-dropdown-item>
                        <el-dropdown-item command="delete" divided>{{ $t('common.delete') }}</el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </div>
              </div>
            </template>
            <div class="card-content">
              <p class="description">{{ flow.description || $t('dataflow.noDescription') }}</p>
              <div class="stats">
                <div class="stat-item">
                  <span class="label">{{ $t('dataflow.nodeCount') }}:</span>
                  <span class="value">{{ flow.nodes.length }}</span>
                </div>
                <div class="stat-item">
                  <span class="label">{{ $t('dataflow.connectionCount') }}:</span>
                  <span class="value">{{ flow.connections.length }}</span>
                </div>
                <div class="stat-item">
                  <span class="label">{{ $t('dataflow.status') }}:</span>
                  <el-tag :type="getStatusType(flow.status)">{{ flow.status }}</el-tag>
                </div>
              </div>
              <div class="last-updated">
                <span>{{ $t('dataflow.lastUpdated') }}: {{ formatDate(flow.updated_at) }}</span>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 创建/编辑数据流对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEditing ? $t('dataflow.editInfo') : $t('dataflow.createNew')"
      width="30%"
    >
      <el-form :model="formData" label-width="80px">
        <el-form-item :label="$t('dataflow.name')">
          <el-input v-model="formData.name" :placeholder="$t('dataflow.enterName')"></el-input>
        </el-form-item>
        <el-form-item :label="$t('dataflow.descriptionLabel')">
          <el-input
            v-model="formData.description"
            type="textarea"
            :placeholder="$t('dataflow.enterDescription')"
          ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">{{ $t('common.cancel') }}</el-button>
          <el-button type="primary" @click="saveDataFlow">{{ $t('common.confirm') }}</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 确认删除对话框 -->
    <el-dialog
      v-model="deleteDialogVisible"
      :title="$t('dataflow.confirmDelete')"
      width="30%"
    >
      <span>{{ $t('dataflow.deleteConfirm', { name: selectedFlow?.name }) }}</span>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="deleteDialogVisible = false">{{ $t('common.cancel') }}</el-button>
          <el-button type="danger" @click="confirmDelete">{{ $t('common.delete') }}</el-button>
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
          ElMessage.success($t('dataflow.runSuccess'))
          await fetchDataFlows()
        } else {
          ElMessage.error(response.data.message || $t('dataflow.runError'))
        }
      } catch (error) {
        console.error('Error running dataflow:', error)
        ElMessage.error($t('dataflow.runError'))
      }
    }

    // 编辑数据流可视化界面
    const editFlowVisually = (flow) => {
      router.push(`/dataflows/${flow.flow_id}/edit`)
    }

    // 处理下拉菜单命令
    const handleCommand = (command, flow) => {
      if (command === 'edit') {
        editDataFlow(flow)
      } else if (command === 'run') {
        runDataFlow(flow)
      } else if (command === 'duplicate') {
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
          name: `${flow.name} (${$t('dataflow.copy')})`,
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
      editFlowVisually,
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
  gap: 10px;
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
  line-clamp: 2;
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
