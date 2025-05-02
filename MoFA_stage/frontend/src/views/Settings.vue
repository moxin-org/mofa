<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">{{ $t('settings.title') }}</h1>
      <div class="page-actions">
        <el-button @click="resetSettings" :loading="isResetting">{{ $t('settings.reset') }}</el-button>
        <el-button type="primary" @click="saveSettings" :loading="isSaving">{{ $t('settings.save') }}</el-button>
      </div>
    </div>

    <el-card v-if="isLoading" class="loading-card">
      <el-skeleton :rows="6" animated />
    </el-card>

    <div v-else class="settings-container">
      <el-card class="settings-card">
        <template #header>
          <div class="card-header">
            <h3>{{ $t('settings.mofaEnvironment') }}</h3>
          </div>
        </template>

        <el-form :model="settingsForm" label-position="top">
          <el-form-item :label="$t('settings.mofaCommandSource')">
            <el-radio-group v-model="settingsForm.use_system_mofa">
              <el-radio :label="true">{{ $t('settings.useSystemMofa') }}</el-radio>
              <el-radio :label="false">{{ $t('settings.useVirtualEnv') }}</el-radio>
            </el-radio-group>
            <div class="form-help"></div>
          </el-form-item>

          <el-form-item :label="$t('settings.mofaEnvPath')" v-if="!settingsForm.use_system_mofa">
            <el-input 
              v-model="settingsForm.mofa_env_path" 
              placeholder="/path/to/mofa_venv"
            >
              <template #append>
                <el-button @click="selectMofaEnvPath">{{ $t('settings.browse') }}</el-button>
              </template>
            </el-input>
            <div class="form-help">{{ $t('settings.mofaEnvPathHelp') }}</div>
          </el-form-item>

          <el-form-item :label="$t('settings.mofaDir')">
            <el-input 
              v-model="settingsForm.mofa_dir" 
              placeholder="/path/to/mofa"
            >
              <template #append>
                <el-button @click="selectMofaDir">{{ $t('settings.browse') }}</el-button>
              </template>
            </el-input>
            <div class="form-help">{{ $t('settings.mofaDirHelp') }}</div>
          </el-form-item>

          <el-form-item :label="$t('settings.agentStorage')">
            <el-select v-model="settingsForm.agent_storage" style="width: 100%">
              <el-option :label="$t('settings.examplesDir')" value="examples" />
              <el-option :label="$t('settings.agentHubDir')" value="agent-hub" />
              <el-option :label="$t('settings.customDir')" value="custom" />
            </el-select>
            <div class="form-help">{{ $t('settings.agentStorageHelp') }}</div>
          </el-form-item>

          <el-form-item :label="$t('settings.customAgentPath')" v-if="settingsForm.agent_storage === 'custom'">
            <el-input 
              v-model="settingsForm.custom_agent_path" 
              placeholder="/path/to/custom/agent/directory"
            >
              <template #append>
                <el-button @click="selectCustomAgentPath">{{ $t('settings.browse') }}</el-button>
              </template>
            </el-input>
            <div class="form-help">{{ $t('settings.customAgentPathHelp') }}</div>
          </el-form-item>
        </el-form>
      </el-card>

      <el-card class="settings-card">
        <template #header>
          <div class="card-header">
            <h3>{{ $t('settings.editorSettings') }}</h3>
          </div>
        </template>

        <el-form :model="settingsForm" label-position="top">
          <el-form-item :label="$t('settings.language')">
            <el-select v-model="settingsForm.language" style="width: 100%" @change="handleLanguageChange">
              <el-option label="中文" value="zh" />
              <el-option label="English" value="en" />
            </el-select>
          </el-form-item>

          <el-form-item :label="$t('settings.theme')">
            <el-select v-model="settingsForm.theme" style="width: 100%">
              <el-option :label="$t('settings.lightTheme')" value="light" />
              <el-option :label="$t('settings.darkTheme')" value="dark" />
            </el-select>
          </el-form-item>

          <el-form-item :label="$t('settings.editorFontSize')">
            <el-slider 
              v-model="settingsForm.editor_font_size" 
              :min="10" 
              :max="20" 
              :step="1"
              show-input
            />
          </el-form-item>

          <el-form-item :label="$t('settings.editorTabSize')">
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
import { setLanguage } from '../utils/i18n'

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
      editor_tab_size: 4,
      language: localStorage.getItem('language') || 'zh'
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

    const handleLanguageChange = (value) => {
      // Update language immediately without waiting for save
      setLanguage(value)
      
      // Save settings to apply changes server-side
      saveSettings()
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
      selectCustomAgentPath,
      handleLanguageChange
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
