<template>
  <header class="header">
    <div class="logo-container">
      <el-icon class="app-logo" :size="24"><Connection /></el-icon>
      <h1 class="app-title">MoFA Stage</h1>
    </div>

    <div class="header-actions">
      <!-- 隐藏的创建Agent按钮 - 
      <el-button type="primary" @click="handleCreateAgent">
        <el-icon><Plus /></el-icon>
        创建 Agent
      </el-button>
      -->
      <el-tooltip content="应用设置" placement="bottom">
        <el-button circle @click="goToSettings">
          <el-icon><Setting /></el-icon>
        </el-button>
      </el-tooltip>
    </div>
  </header>
</template>

<script>
import { useRouter } from 'vue-router'
import { Plus, Setting, Search, Connection } from '@element-plus/icons-vue'
import { ref } from 'vue'

export default {
  name: 'AppHeader',
  components: {
    Plus,
    Setting,
    Search,
    Connection
  },
  setup(props, { emit }) {
    const router = useRouter()
    const handleCreateAgent = () => {
      router.push('/agents/create')
    }
    
    const goToSettings = () => {
      router.push('/settings')
    }
    
    return {
      handleCreateAgent,
      goToSettings
    }
  }
}
</script>

<style scoped>
.header {
  background-color: var(--header-background);
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  padding: 0 20px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo-container {
  display: flex;
  align-items: center;
  min-width: 180px;
  gap: 10px;
}

.app-logo {
  color: var(--primary-color);
  animation: pulse 1.5s infinite alternate;
}

@keyframes pulse {
  from {
    opacity: 0.8;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1.05);
  }
}

.app-title {
  font-size: 20px;
  font-weight: 600;
  margin: 0;
  color: var(--primary-color);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}
</style>
