<template>
  <div class="sidebar">
    <div class="sidebar-header">
      <h2 class="sidebar-title">{{ $t('sidebar.controlCenter') }}</h2>
    </div>
    <div class="sidebar-menu">
      <el-menu
        router
        :default-active="activeRoute"
        class="sidebar-nav"
        :background-color="computedTheme.bgColor"
        :text-color="computedTheme.textColor"
        :active-text-color="computedTheme.activeTextColor">
        <el-menu-item index="/agents">
          <el-icon><Menu /></el-icon>
          <span>{{ $t('sidebar.agentsList') }}</span>
        </el-menu-item>
        <!-- Hidden dataflow orchestration tab as requested
        <el-menu-item index="/dataflows">
          <el-icon><Connection /></el-icon>
          <span>{{ $t('sidebar.dataflowOrchestration') }}</span>
        </el-menu-item>
        -->
        <el-menu-item index="/terminal" v-if="showTerminal">
          <el-icon><Monitor /></el-icon>
          <span>{{ $t('sidebar.commandLine') }}</span>
        </el-menu-item>
        <el-menu-item index="/webssh" v-if="showWebSSH">
          <el-icon><Monitor /></el-icon>
          <span>{{ $t('sidebar.webSSH') }}</span>
        </el-menu-item>
        <el-menu-item index="/ttyd" v-if="showTtyd">
          <el-icon><Monitor /></el-icon>
          <span>{{ $t('sidebar.ttyd') || 'ttyd Terminal' }}</span>
        </el-menu-item>
        <el-menu-item index="/settings">
          <el-icon><Setting /></el-icon>
          <span>{{ $t('sidebar.settings') }}</span>
        </el-menu-item>
      </el-menu>
    </div>
    <div class="sidebar-footer">
      <span>MoFA_Stage v0.3.0</span>
    </div>
  </div>
</template>

<script>
import { computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useSettingsStore } from '../../store/settings'
import { useI18n } from 'vue-i18n'
import { Menu, Setting, Connection, Monitor } from '@element-plus/icons-vue'

export default {
  name: 'AppSidebar',
  components: {
    Menu,
    Setting,
    Connection,
    Monitor
  },
  setup() {
    const route = useRoute()
    const settingsStore = useSettingsStore()
    const { t } = useI18n()
    
    const activeRoute = computed(() => {
      return route.path
    })
    
    const computedTheme = computed(() => {
      const isDark = settingsStore.settings.theme === 'dark'
      return {
        bgColor: isDark ? 'var(--sidebar-background)' : '#304156',
        textColor: isDark ? 'var(--sidebar-text-color)' : '#bfcbd9',
        activeTextColor: isDark ? 'var(--sidebar-active-text-color)' : '#409EFF'
      }
    })
    
    const showTerminal = computed(() => {
      const mode = settingsStore.settings.terminal_display_mode || 'both'
      return mode === 'both' || mode === 'terminal'
    })
    
    const showWebSSH = computed(() => {
      const mode = settingsStore.settings.terminal_display_mode || 'both'
      return mode === 'both' || mode === 'webssh'
    })
    
    const showTtyd = computed(() => {
      const mode = settingsStore.settings.terminal_display_mode || 'both'
      return mode === 'both' || mode === 'ttyd'
    })
    
    // Watch for terminal display mode changes
    watch(
      () => settingsStore.settings.terminal_display_mode,
      (newMode) => {
        console.log('Terminal display mode changed:', newMode);
      }
    );
    
    return {
      activeRoute,
      computedTheme,
      showTerminal,
      showWebSSH,
      showTtyd
    }
  }
}
</script>

<style scoped>
.sidebar {
  width: 220px;
  background-color: #304156;
  color: #fff;
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow-y: auto;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.sidebar-menu {
  flex: 1;
  overflow-y: auto;
}

.sidebar-nav {
  border-right: none;
}

.sidebar-footer {
  padding: 10px 20px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
  text-align: center;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}
</style>
