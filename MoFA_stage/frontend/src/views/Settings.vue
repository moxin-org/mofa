<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">设置</h1>
      <div class="page-actions">
        <el-button @click="resetSettings" :loading="isResetting">重置为默认</el-button>
        <el-button type="primary" @click="saveSettings" :loading="isSaving">保存设置</el-button>
      </div>
    </div>

    <el-card v-if="isLoading" class="loading-card">
      <el-skeleton :rows="6" animated />
    </el-card>

    <div v-else class="settings-container">
      <el-card class="settings-card">
        <template #header>
          <div class="card-header">
            <h3>MoFA 环境设置</h3>
          </div>
        </template>

        <el-form :model="settingsForm" label-position="top">
          <el-form-item label="MoFA 命令源">
            <el-radio-group v-model="settingsForm.use_system_mofa">
              <el-radio :label="true">使用系统安装的MOFA</el-radio>
              <el-radio :label="false">使用虚拟环境</el-radio>
            </el-radio-group>
            <div class="form-help">            使用系统全局安装的MOFA或自定义虚拟环境</div>
          </el-form-item>

          <el-form-item label="MoFA 环境路径" v-if="!settingsForm.use_system_mofa">
            <el-input 
              v-model="settingsForm.mofa_env_path" 
              placeholder="/path/to/mofa_venv"
            >
              <template #append>
                <el-button @click="selectMofaEnvPath">浏览</el-button>
              </template>
            </el-input>
            <div class="form-help">指定 MoFA 虚拟环境路径，例如：/mnt/c/Users/ufop/Desktop/code/mofa_second_stage/mofa/mofa_test_env</div>
          </el-form-item>

          <el-form-item label="MoFA 项目目录">
            <el-input 
              v-model="settingsForm.mofa_dir" 
              placeholder="/path/to/mofa"
            >
              <template #append>
                <el-button @click="selectMofaDir">浏览</el-button>
              </template>
            </el-input>
            <div class="form-help">指定 MoFA 项目根目录，例如：/mnt/c/Users/ufop/Desktop/code/mofa_second_stage/mofa</div>
          </el-form-item>

          <el-form-item label="Agent 存储位置">
            <el-select v-model="settingsForm.agent_storage" style="width: 100%">
              <el-option label="examples目录 (/python/examples)" value="examples" />
              <el-option label="agent-hub目录 (/python/agent-hub)" value="agent-hub" />
              <el-option label="自定义目录" value="custom" />
            </el-select>
            <div class="form-help">选择存放Agent的目录，官方推荐使用agent-hub目录</div>
          </el-form-item>

          <el-form-item label="自定义Agent路径" v-if="settingsForm.agent_storage === 'custom'">
            <el-input 
              v-model="settingsForm.custom_agent_path" 
              placeholder="/path/to/custom/agent/directory"
            >
              <template #append>
                <el-button @click="selectCustomAgentPath">浏览</el-button>
              </template>
            </el-input>
            <div class="form-help">输入存储Agent的完整目录路径</div>
          </el-form-item>
        </el-form>
      </el-card>

      <el-card class="settings-card">
        <template #header>
          <div class="card-header">
            <h3>编辑器设置</h3>
          </div>
        </template>

        <el-form :model="settingsForm" label-position="top">
          <el-form-item label="主题">
            <el-select v-model="settingsForm.theme" style="width: 100%">
              <el-option label="亮色" value="light" />
              <el-option label="暗色" value="dark" />
            </el-select>
          </el-form-item>

          <el-form-item label="编辑器字体大小">
            <el-slider 
              v-model="settingsForm.editor_font_size" 
              :min="10" 
              :max="20" 
              :step="1"
              show-input
            />
          </el-form-item>

          <el-form-item label="编辑器缩进大小">
            <el-slider 
              v-model="settingsForm.editor_tab_size" 
              :min="2" 
              :max="8" 
              :step="1"
              show-input
            />
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useSettingsStore } from '../store/settings'
import { ElMessage } from 'element-plus'
import { Setting, Folder, Document } from '@element-plus/icons-vue'

export default {
  name: 'Settings',
  setup() {
    const settingsStore = useSettingsStore()
    
    const settingsForm = reactive({
      mofa_env_path: '',
      mofa_dir: '',
      use_system_mofa: true,
      agent_storage: 'examples',
      custom_agent_path: '',
      theme: 'light',
      editor_font_size: 14,
      editor_tab_size: 4
    })
    
    const isLoading = computed(() => settingsStore.isLoading)
    const isSaving = ref(false)
    const isResetting = ref(false)
    
    const loadSettings = async () => {
      const settings = await settingsStore.fetchSettings()
      if (settings) {
        Object.assign(settingsForm, settings)
      }
    }
    
    const saveSettings = async () => {
      isSaving.value = true
      try {
        const result = await settingsStore.saveSettings(settingsForm)
        if (result) {
          applyTheme(settingsForm.theme)
          ElMessage.success('设置已保存')
        } else {
          ElMessage.error(`保存设置失败: ${settingsStore.error}`)
        }
      } catch (error) {
        ElMessage.error(`保存设置失败: ${error.message}`)
      } finally {
        isSaving.value = false
      }
    }
    
    const resetSettings = async () => {
      isResetting.value = true
      try {
        const result = await settingsStore.resetSettings()
        if (result) {
          Object.assign(settingsForm, settingsStore.settings)
          applyTheme(settingsStore.settings.theme)
          ElMessage.success('设置已重置为默认值')
        } else {
          ElMessage.error(`重置设置失败: ${settingsStore.error}`)
        }
      } catch (error) {
        ElMessage.error(`重置设置失败: ${error.message}`)
      } finally {
        isResetting.value = false
      }
    }
    
    const selectMofaEnvPath = () => {
      // 在实际环境中，这里可以集成文件选择对话框
      ElMessage.info('需要集成服务器端文件选择')
    }
    
    const selectMofaDir = () => {
      // 在实际环境中，这里可以集成文件选择对话框
      ElMessage.info('需要集成服务器端文件选择')
    }
    
    const selectCustomAgentPath = () => {
      // 在实际环境中，这里可以集成文件选择对话框
      ElMessage.info('需要集成服务器端文件选择')
    }
    
    // Apply theme when it changes
    const applyTheme = (theme) => {
      document.documentElement.setAttribute('data-theme', theme)
    }

    // Watch for theme changes in the form and apply them immediately
    watch(() => settingsForm.theme, (newTheme) => {
      applyTheme(newTheme)
    })

    onMounted(() => {
      loadSettings()
      // Apply theme on initial load
      applyTheme(settingsForm.theme)
    })
    
    return {
      settingsForm,
      isLoading,
      isSaving,
      isResetting,
      saveSettings,
      resetSettings,
      selectMofaEnvPath,
      selectMofaDir,
      selectCustomAgentPath
    }
  }
}
</script>

<style scoped>
.settings-container {
  max-width: 800px;
  margin: 0 auto;
}

.settings-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.form-help {
  font-size: 12px;
  color: var(--text-color-secondary);
  margin-top: 5px;
}

.loading-card {
  padding: 20px;
}
</style>
