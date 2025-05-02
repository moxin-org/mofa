<template>
  <div class="app-container">
    <AppLayout>
      <router-view />
    </AppLayout>
  </div>
</template>

<script>
import { onMounted } from 'vue'
import { useAgentStore } from './store/agent'
import { useSettingsStore } from './store/settings'
import AppLayout from './components/layout/AppLayout.vue'
import { setLanguage } from './utils/i18n'

export default {
  name: 'App',
  components: {
    AppLayout
  },
  setup() {
    const agentStore = useAgentStore()
    const settingsStore = useSettingsStore()
    
    // 应用主题设置
    const applyTheme = () => {
      const theme = settingsStore.settings.theme || 'light'
      document.documentElement.setAttribute('data-theme', theme)
    }
    
    // 应用语言设置
    const applyLanguage = () => {
      const lang = settingsStore.settings.language || 'zh'
      setLanguage(lang)
    }
    
    onMounted(async () => {
      // 初始化应用时加载设置和 agent 列表
      await settingsStore.fetchSettings()
      await agentStore.fetchAgents()
      
      // 应用主题和语言设置
      applyTheme()
      applyLanguage()
    })
    
    return {}
  }
}
</script>

<style>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>
