<template>
  <div class="app-container">
    <AppLayout>
      <!-- 始终加载TtydTerminal和WebSSH组件，但根据路由显示或隐藏 -->
      <TtydTerminal v-if="isTtydRoute || alwaysLoadTerminals" v-show="isTtydRoute" class="persistent-view" />
      <WebSSH v-if="isWebSSHRoute || alwaysLoadTerminals" v-show="isWebSSHRoute" class="persistent-view" />
      
      <!-- 其他路由使用常规的router-view处理 -->
      <router-view v-slot="{ Component, route }" v-if="!isTtydRoute && !isWebSSHRoute">
        <keep-alive>
          <component :is="Component" v-if="route.meta.keepAlive" />
        </keep-alive>
        <component :is="Component" v-if="!route.meta.keepAlive" />
      </router-view>
    </AppLayout>
  </div>
</template>

<script>
import { onMounted, computed, ref, watch } from 'vue'
import { useAgentStore } from './store/agent'
import { useSettingsStore } from './store/settings'
import { useRoute } from 'vue-router'
import AppLayout from './components/layout/AppLayout.vue'
import { setLanguage } from './utils/i18n'
import TtydTerminal from './views/TtydTerminal.vue'
import WebSSH from './views/WebSSH.vue'

export default {
  name: 'App',
  components: {
    AppLayout,
    TtydTerminal,
    WebSSH
  },
  setup() {
    const agentStore = useAgentStore()
    const settingsStore = useSettingsStore()
    const route = useRoute()
    
    // 控制是否始终加载终端组件
    const alwaysLoadTerminals = ref(true)
    
    // 计算当前是否在ttyd终端路由
    const isTtydRoute = computed(() => {
      return route.path === '/ttyd'
    })
    
    // 计算当前是否在WebSSH路由
    const isWebSSHRoute = computed(() => {
      return route.path === '/webssh'
    })
    
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
    
    return {
      alwaysLoadTerminals,
      isTtydRoute,
      isWebSSHRoute
    }
  }
}
</script>

<style>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.persistent-view {
  height: 100%;
  width: 100%;
}
</style>
