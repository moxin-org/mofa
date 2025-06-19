<template>
  <header class="header">
    <div class="logo-section">
      <img src="/mofa-logo.png" alt="MoFA Logo" class="app-logo" />
      <div class="brand-info">
        <h1 class="app-title">MoFA Stage</h1>
        <p class="app-subtitle">Mission Control for MoFA</p>
      </div>
    </div>

    <div class="page-info">
      <h2 class="page-title">{{ pageTitle }}</h2>
    </div>

    <div class="header-actions">
      <!-- 隐藏的创建Agent按钮 - 
      <el-button type="primary" @click="handleCreateAgent">
        <el-icon><Plus /></el-icon>
        创建 Agent
      </el-button>
      -->
      <el-tooltip content="应用设置" placement="bottom">
        <el-button circle @click="goToSettings" class="settings-btn">
          <el-icon><Setting /></el-icon>
        </el-button>
      </el-tooltip>
    </div>
  </header>
</template>

<script>
import { useRouter, useRoute } from 'vue-router'
import { Setting } from '@element-plus/icons-vue'
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

export default {
  name: 'AppHeader',
  components: {
    Setting
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const { t } = useI18n()
    
    const pageTitle = computed(() => {
      const path = route.path
      switch (path) {
        case '/agents':
          return t('sidebar.agentsList') || 'Agent Hub'
        case '/agents/create':
          return t('agent.createAgent') || 'Create Agent'
        case '/terminal':
          return t('sidebar.commandLine') || 'Command Line'
        case '/webssh':
          return t('sidebar.webSSH') || 'Web SSH'
        case '/ttyd':
          return t('sidebar.ttyd') || 'ttyd Terminal'
        case '/settings':
          return t('sidebar.settings') || 'Settings'
        default:
          if (path.includes('/agents/edit/')) {
            return t('agent.editAgent') || 'Edit Agent'
          }
          return 'MoFA Stage'
      }
    })
    
    const goToSettings = () => {
      router.push('/settings')
    }
    
    return {
      goToSettings,
      pageTitle
    }
  }
}
</script>

<style scoped>
.header {
  background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFE 100%);
  border-bottom: 1px solid var(--border-color);
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.04);
  padding: 0 32px;
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  backdrop-filter: blur(10px);
  position: relative;
  width: 100%;
  z-index: 1000;
}

.header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(
    90deg,
    var(--mofa-red) 0%,
    var(--mofa-orange) 25%,
    var(--mofa-yellow) 50%,
    var(--mofa-teal) 75%,
    var(--mofa-red) 100%
  );
  background-size: 300% 100%;
  animation: flowing-border 16s ease-in-out infinite;
}

.logo-section {
  display: flex;
  align-items: center;
  min-width: 200px;
  gap: 12px;
}

.app-logo {
  width: 40px;
  height: 40px;
  border-radius: 0;
  transition: all 0.3s ease;
}

.app-logo:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 16px rgba(255, 92, 72, 0.2);
}

.brand-info {
  display: flex;
  flex-direction: column;
}

.app-title {
  font-size: 22px;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(
    45deg,
    var(--mofa-red) 0%,
    var(--mofa-orange) 25%,
    var(--mofa-yellow) 50%,
    var(--mofa-teal) 75%,
    var(--mofa-red) 100%
  );
  background-size: 300% 300%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.5px;
  animation: flowing-gradient 12s ease-in-out infinite;
}

.app-subtitle {
  font-size: 12px;
  font-weight: 500;
  margin: 0;
  color: var(--text-color-secondary);
  opacity: 0.8;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.page-info {
  display: flex;
  align-items: center;
  min-width: 200px;
  justify-content: center;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  margin: 0;
  color: var(--text-color-primary);
  letter-spacing: -0.3px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.settings-btn {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid var(--border-color);
  color: var(--text-color-secondary);
  transition: all 0.3s ease;
}

.settings-btn:hover {
  background: var(--mofa-teal);
  color: white;
  border-color: var(--mofa-teal);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(107, 206, 210, 0.3);
}

/* Dark theme adjustments */
[data-theme="dark"] .header {
  background: linear-gradient(135deg, var(--header-background) 0%, #0D1117 100%);
  border-bottom-color: var(--border-color);
}

[data-theme="dark"] .app-subtitle {
  color: var(--text-color-secondary);
}

[data-theme="dark"] .settings-btn {
  background: rgba(22, 27, 34, 0.8);
  border-color: var(--border-color);
  color: var(--text-color-secondary);
}

[data-theme="dark"] .settings-btn:hover {
  background: var(--mofa-teal);
  color: white;
  border-color: var(--mofa-teal);
}
</style>
