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

          <!-- 相对路径设置 -->
          <el-form-item :label="$t('settings.useRelativePaths')">
            <el-switch v-model="settingsForm.use_relative_paths" />
            <div class="form-help">{{ $t('settings.useRelativePathsHelp') }}</div>
          </el-form-item>

          <!-- Agent Hub 设置 -->
          <el-form-item :label="$t('settings.agentHubStorage')">
            <el-radio-group v-model="settingsForm.use_default_agent_hub_path">
              <el-radio :label="true">{{ $t('settings.useDefaultPath') }}</el-radio>
              <el-radio :label="false">{{ $t('settings.useCustomPath') }}</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item :label="$t('settings.agentHubPath')" v-if="!settingsForm.use_default_agent_hub_path">
            <el-input 
              v-model="settingsForm.custom_agent_hub_path" 
              placeholder="/path/to/custom/agent-hub/directory"
            >
              <template #append>
                <el-button @click="selectCustomAgentHubPath">{{ $t('settings.browse') }}</el-button>
              </template>
            </el-input>
            <div class="form-help">{{ $t('settings.agentHubPathHelp') }}</div>
          </el-form-item>

          <!-- Examples 设置 -->
          <el-form-item :label="$t('settings.examplesStorage')">
            <el-radio-group v-model="settingsForm.use_default_examples_path">
              <el-radio :label="true">{{ $t('settings.useDefaultPath') }}</el-radio>
              <el-radio :label="false">{{ $t('settings.useCustomPath') }}</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item :label="$t('settings.examplesPath')" v-if="!settingsForm.use_default_examples_path">
            <el-input 
              v-model="settingsForm.custom_examples_path" 
              placeholder="/path/to/custom/examples/directory"
            >
              <template #append>
                <el-button @click="selectCustomExamplesPath">{{ $t('settings.browse') }}</el-button>
              </template>
            </el-input>
            <div class="form-help">{{ $t('settings.examplesPathHelp') }}</div>
          </el-form-item>
        </el-form>
      </el-card>

      <el-card class="settings-card">
        <template #header>
          <div class="card-header">
            <h3>{{ $t('settings.sshSettings') || 'SSH Settings' }}</h3>
          </div>
        </template>

        <el-form :model="settingsForm.ssh" label-position="top">
          <el-form-item :label="$t('ssh.hostname') || 'Hostname'">
            <el-input v-model="settingsForm.ssh.hostname" placeholder="127.0.0.1" />
          </el-form-item>

          <el-form-item :label="$t('ssh.port') || 'Port'">
            <el-input-number v-model="settingsForm.ssh.port" :min="1" :max="65535" style="width: 100%" />
          </el-form-item>

          <el-form-item :label="$t('ssh.username') || 'Username'">
            <el-input v-model="settingsForm.ssh.username" />
          </el-form-item>

          <el-form-item :label="$t('ssh.password') || 'Password'">
            <el-input v-model="settingsForm.ssh.password" type="password" show-password />
          </el-form-item>

          <el-form-item :label="$t('ssh.autoConnect') || 'Auto Connect'">
            <el-switch v-model="settingsForm.ssh.auto_connect" />
            <div class="form-help">{{ $t('ssh.autoConnectHelp') || 'Automatically connect to SSH when opening the SSH terminal' }}</div>
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
          <el-form-item :label="$t('settings.terminalDisplayMode') || '终端显示模式'">
            <el-select v-model="settingsForm.terminal_display_mode" style="width: 100%">
              <!-- <el-option 
                :label="$t('settings.showBothTerminals') || '显示两种终端'" 
                value="both" /> -->
              <!-- <el-option 
                :label="$t('settings.showOnlyTerminal') || '仅显示旧命令行'" 
                value="terminal" /> -->
              <el-option 
                :label="$t('settings.showOnlyWebSSH')" 
                value="webssh" />
              <el-option 
                :label="$t('settings.showOnlyTtyd')" 
                value="ttyd" />
            </el-select>
            <div class="form-help">
              {{ $t('settings.terminalDisplayModeHelp') || '选择在侧边栏显示哪种终端。修改后需要刷新页面生效。' }}
            </div>
          </el-form-item>

          <el-form-item :label="$t('settings.ttydPort') || 'ttyd 端口'" v-if="settingsForm.terminal_display_mode === 'ttyd'">
            <el-input-number v-model="settingsForm.ttyd_port" :min="1024" :max="65535" style="width: 100%" />
            <div class="form-help">
              {{ $t('settings.ttydPortHelp') || 'ttyd服务将运行在此端口上。默认为7681。修改后需重启服务生效。' }}
            </div>
          </el-form-item>

          <el-form-item :label="$t('settings.language')">
            <el-select v-model="settingsForm.language" style="width: 100%" @change="handleLanguageChange">
              <el-option label="简体中文" value="zh" />
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
      use_default_agent_hub_path: true,
      use_default_examples_path: true,
      agent_hub_path: '',
      examples_path: '',
      custom_agent_hub_path: '',
      custom_examples_path: '',
      theme: 'light',
      editor_font_size: 14,
      editor_tab_size: 4,
      language: localStorage.getItem('language') || 'zh',
      terminal_display_mode: 'both',
      ttyd_port: 7681,
      ssh: {
        hostname: '127.0.0.1',
        port: 22,
        username: '',
        password: '',
        auto_connect: true
      }
    })
    
    const isLoading = computed(() => settingsStore.isLoading)
    const isSaving = ref(false)
    const isResetting = ref(false)
    
    const loadSettings = async () => {
      const settings = await settingsStore.fetchSettings()
      if (settings) {
        // 使用更安全的方式合并设置，确保不会覆盖现有值
        // 首先保留一些默认值
        const currentPaths = {
          mofa_dir: settingsForm.mofa_dir,
          agent_hub_path: settingsForm.agent_hub_path,
          examples_path: settingsForm.examples_path,
          custom_agent_hub_path: settingsForm.custom_agent_hub_path,
          custom_examples_path: settingsForm.custom_examples_path
        };
        
        // 合并设置
        Object.assign(settingsForm, settings)
        
        // 如果后端返回的路径为空，但本地有值，则保留本地值
        if (!settingsForm.mofa_dir && currentPaths.mofa_dir) {
          settingsForm.mofa_dir = currentPaths.mofa_dir;
        }
        
        if (!settingsForm.agent_hub_path && currentPaths.agent_hub_path) {
          settingsForm.agent_hub_path = currentPaths.agent_hub_path;
        }
        
        if (!settingsForm.examples_path && currentPaths.examples_path) {
          settingsForm.examples_path = currentPaths.examples_path;
        }
        
        if (!settingsForm.custom_agent_hub_path && currentPaths.custom_agent_hub_path) {
          settingsForm.custom_agent_hub_path = currentPaths.custom_agent_hub_path;
        }
        
        if (!settingsForm.custom_examples_path && currentPaths.custom_examples_path) {
          settingsForm.custom_examples_path = currentPaths.custom_examples_path;
        }
        
        // 确保路径选项有默认值
        if (settingsForm.use_default_agent_hub_path === undefined) {
          settingsForm.use_default_agent_hub_path = true;
        }
        
        if (settingsForm.use_default_examples_path === undefined) {
          settingsForm.use_default_examples_path = true;
        }
        
        // 确保ssh对象存在
        if (!settingsForm.ssh) {
          settingsForm.ssh = {
            hostname: '127.0.0.1',
            port: 22,
            username: '',
            password: '',
            auto_connect: true
          }
        }
      }
    }
    
    const saveSettings = async () => {
      isSaving.value = true
      try {
        // 在保存前确保路径不会丢失
        if (!settingsForm.mofa_dir) {
          settingsForm.mofa_dir = localStorage.getItem('mofa_dir') || '';
        } else {
          // 在localStorage中备份路径
          localStorage.setItem('mofa_dir', settingsForm.mofa_dir);
        }
        
        // 备份所有路径字段
        localStorage.setItem('agent_hub_path', settingsForm.agent_hub_path || '');
        localStorage.setItem('examples_path', settingsForm.examples_path || '');
        localStorage.setItem('custom_agent_hub_path', settingsForm.custom_agent_hub_path || '');
        localStorage.setItem('custom_examples_path', settingsForm.custom_examples_path || '');
        
        // 确保路径不为空
        // 如果使用默认路径是true，但路径为空，尝试设置一个合理默认值
        if (settingsForm.use_default_agent_hub_path && !settingsForm.agent_hub_path) {
          settingsForm.agent_hub_path = `${settingsForm.mofa_dir}/agent-hub`;
        }
        
        if (settingsForm.use_default_examples_path && !settingsForm.examples_path) {
          settingsForm.examples_path = `${settingsForm.mofa_dir}/examples`;
        }
        
        const result = await settingsStore.saveSettings(settingsForm)
        if (result) {
          applyTheme(settingsForm.theme)
          ElMessage.success('Settings saved successfully')
        } else {
          ElMessage.error(`Failed to save settings: ${settingsStore.error}`)
        }
      } catch (error) {
        ElMessage.error(`Failed to save settings: ${error.message}`)
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
          ElMessage.success('Settings reset to default successfully')
        } else {
          ElMessage.error(`Failed to reset settings: ${settingsStore.error}`)
        }
      } catch (error) {
        ElMessage.error(`Failed to reset settings: ${error.message}`)
      } finally {
        isResetting.value = false
      }
    }
    
    const selectMofaEnvPath = () => {
      // todo: 集成文件选择对话框
      ElMessage.info('File Selection Dialog')
    }
    
    const selectMofaDir = () => {
      // todo: 集成文件选择对话框
      ElMessage.info('File Selection Dialog')
    }
    
    const selectCustomAgentHubPath = () => {
      // todo: 集成文件选择对话框
      ElMessage.info('File Selection Dialog')
    }
    
    const selectCustomExamplesPath = () => {
      // todo: 集成文件选择对话框
      ElMessage.info('File Selection Dialog')
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
      // 尝试从localStorage中加载备份的路径
      const savedMofaDir = localStorage.getItem('mofa_dir');
      if (savedMofaDir) {
        settingsForm.mofa_dir = savedMofaDir;
      } else {
        // 设置一个默认路径，根据当前环境
        const isWindows = navigator.platform.indexOf('Win') > -1;
        if (isWindows) {
          settingsForm.mofa_dir = 'C:\\Users\\Username\\path\\to\\mofa';
        } else {
          // 假设是Linux/Mac
          settingsForm.mofa_dir = '/mnt/c/Users/Yao/Desktop/code/mofa/mofa';
        }
      }
      
      // 加载Agent Hub和Examples相关备份路径
      const savedAgentHubPath = localStorage.getItem('agent_hub_path');
      if (savedAgentHubPath) {
        settingsForm.agent_hub_path = savedAgentHubPath;
      }
      
      const savedExamplesPath = localStorage.getItem('examples_path');
      if (savedExamplesPath) {
        settingsForm.examples_path = savedExamplesPath;
      }
      
      const savedCustomAgentHubPath = localStorage.getItem('custom_agent_hub_path');
      if (savedCustomAgentHubPath) {
        settingsForm.custom_agent_hub_path = savedCustomAgentHubPath;
      }
      
      const savedCustomExamplesPath = localStorage.getItem('custom_examples_path');
      if (savedCustomExamplesPath) {
        settingsForm.custom_examples_path = savedCustomExamplesPath;
      }
      
      // 加载其他设置
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
      selectCustomAgentHubPath,
      selectCustomExamplesPath,
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
