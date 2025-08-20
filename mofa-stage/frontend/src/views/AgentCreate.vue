<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">创建新 Agent</h1>
      <div class="page-actions">
        <el-button @click="goBack">返回</el-button>
      </div>
    </div>

    <el-card class="create-options">
      <el-tabs v-model="activeTab">
        <!-- 创建方式：Hello World 模板 -->
        <el-tab-pane label="Hello World 模板" name="hello-world">
          <div class="tab-content">
            <h3>基于 Hello World 模板创建</h3>
            <p>使用基础的 Hello World 模板创建一个新的 Agent。适合刚开始使用 MoFA 的用户。</p>

            <el-form :model="helloWorldForm" label-width="100px" class="create-form">
              <el-form-item label="Agent 名称" required>
                <el-input v-model="helloWorldForm.name" placeholder="输入唯一的 Agent 名称" />
              </el-form-item>
              <el-form-item label="版本">
                <el-input v-model="helloWorldForm.version" placeholder="如: 0.0.1" />
              </el-form-item>
              <el-form-item label="作者">
                <el-input v-model="helloWorldForm.authors" placeholder="您的名字" />
              </el-form-item>
              <el-form-item label="Agent 类型">
                <el-radio-group v-model="helloWorldForm.agentType">
                  <el-radio label="agent-hub">{{ $t('settings.agentHubDir') }}</el-radio>
                  <el-radio label="examples">{{ $t('settings.examplesDir') }}</el-radio>
                </el-radio-group>
                <div class="form-help">{{ $t('agent.agentTypeHelp') }}</div>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="createHelloWorldAgent" :loading="isCreating">
                  创建 Agent
                </el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-tab-pane>

        <!-- 创建方式：复制现有 Agent -->
        <el-tab-pane label="复制现有 Agent" name="copy">
          <div class="tab-content">
            <h3>基于现有 Agent 创建</h3>
            <p>复制一个现有的 Agent 作为起点。适合希望修改现有 Agent 功能的用户。</p>

            <el-form :model="copyForm" label-width="100px" class="create-form">
              <el-form-item label="源 Agent" required>
                <el-select v-model="copyForm.source" placeholder="选择一个现有 Agent" style="width: 100%;">
                  <el-option v-for="agent in agents" :key="agent" :label="agent" :value="agent" />
                </el-select>
              </el-form-item>
              <el-form-item label="新 Agent 名称" required>
                <el-input v-model="copyForm.target" placeholder="输入唯一的 Agent 名称" />
              </el-form-item>
              <el-form-item label="Agent 类型">
                <el-radio-group v-model="copyForm.agentType">
                  <el-radio label="auto">{{ $t('agent.autoDetect') }}</el-radio>
                  <el-radio label="agent-hub">{{ $t('settings.agentHubDir') }}</el-radio>
                  <el-radio label="examples">{{ $t('settings.examplesDir') }}</el-radio>
                </el-radio-group>
                <div class="form-help">{{ $t('agent.agentTypeHelp') }}</div>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="createCopyAgent" :loading="isCreating">
                  创建 Agent
                </el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <el-dialog 
      v-model="creationSuccessDialog"
      title="Agent 创建成功"
      width="30%">
      <span>Agent "{{ newAgentName }}" 已成功创建！</span>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="goBack">返回列表</el-button>
          <el-button type="primary" @click="goToEdit">
            编辑 Agent
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAgentStore } from '../store/agent'
import { ElMessage } from 'element-plus'
import { useI18n } from 'vue-i18n'

export default {
  name: 'AgentCreate',
  setup() {
    const router = useRouter()
    const agentStore = useAgentStore()
    const { t } = useI18n()
    
    const activeTab = ref('hello-world')
    const isCreating = ref(false)
    const creationSuccessDialog = ref(false)
    const newAgentName = ref('')
    
    const helloWorldForm = ref({
      name: '',
      version: '0.0.1',
      authors: 'MoFA_Stage User',
      agentType: 'agent-hub' // 默认为 agent-hub 类型
    })
    
    const copyForm = ref({
      source: '',
      target: '',
      agentType: 'auto' // 默认为自动检测类型
    })
    
    const agents = computed(() => agentStore.allAgents)
    
    // 从 Hello World 模板创建 Agent
    const createHelloWorldAgent = async () => {
      if (!helloWorldForm.value.name) {
        ElMessage.warning('Please enter the Agent name')
        return
      }
      
      isCreating.value = true
      const result = await agentStore.createAgent({
        name: helloWorldForm.value.name,
        version: helloWorldForm.value.version,
        authors: helloWorldForm.value.authors,
        agent_type: helloWorldForm.value.agentType // 传递 Agent 类型
      })
      isCreating.value = false
      
      if (result) {
        newAgentName.value = helloWorldForm.value.name
        creationSuccessDialog.value = true
      } else {
        ElMessage.error(`Failed to create Agent: ${agentStore.error}`)
      }
    }
    
    // 复制现有 Agent 创建新 Agent
    const createCopyAgent = async () => {
      if (!copyForm.value.source || !copyForm.value.target) {
        ElMessage.warning('Please select a source Agent and enter a new Agent name')
        return
      }
      
      isCreating.value = true
      // 如果选择了 'auto'，则传递 null 作为 agentType
      const agentType = copyForm.value.agentType === 'auto' ? null : copyForm.value.agentType
      const result = await agentStore.copyAgent(
        copyForm.value.source,
        copyForm.value.target,
        agentType // 传递 Agent 类型
      )
      isCreating.value = false
      
      if (result) {
        newAgentName.value = copyForm.value.target
        creationSuccessDialog.value = true
      } else {
        ElMessage.error(`Failed to copy Agent: ${agentStore.error}`)
      }
    }
    
    // 导航方法
    const goBack = () => {
      router.push('/agents')
    }
    
    const goToEdit = () => {
      router.push(`/agents/${newAgentName.value}/edit`)
    }
    
    onMounted(async () => {
      // 确保已加载 agent 列表
      if (agents.value.length === 0) {
        await agentStore.fetchAgents()
      }
    })
    
    return {
      activeTab,
      isCreating,
      helloWorldForm,
      copyForm,
      agents,
      creationSuccessDialog,
      newAgentName,
      createHelloWorldAgent,
      createCopyAgent,
      goBack,
      goToEdit
    }
  }
}
</script>

<style scoped>
.create-options {
  max-width: 800px;
  margin: 0 auto;
}

.tab-content {
  padding: 20px 0;
}

.create-form {
  margin-top: 20px;
  max-width: 500px;
}

h3 {
  margin-top: 0;
  margin-bottom: 10px;
}

p {
  color: var(--text-color-secondary);
  margin-bottom: 20px;
}

.form-help {
  font-size: 12px;
  color: var(--text-color-secondary);
  margin-top: 4px;
}
</style>
