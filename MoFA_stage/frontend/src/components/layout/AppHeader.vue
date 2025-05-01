<template>
  <header class="header">
    <div class="logo-container">
      <el-icon class="app-logo" :size="24"><Connection /></el-icon>
      <h1 class="app-title">MoFA Stage</h1>
    </div>
    <div class="search-container">
      <el-input
        v-model="searchQuery"
        placeholder="搜索Agent..."
        clearable
        @input="emitSearch"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
    </div>
    <div class="header-actions">
      <el-button type="primary" @click="handleCreateAgent">
        <el-icon><Plus /></el-icon>
        创建 Agent
      </el-button>
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
    const searchQuery = ref('')
    
    const handleCreateAgent = () => {
      router.push('/agents/create')
    }
    
    const goToSettings = () => {
      router.push('/settings')
    }
    
    const emitSearch = () => {
      emit('search', searchQuery.value)
    }
    
    return {
      searchQuery,
      handleCreateAgent,
      goToSettings,
      emitSearch
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

.search-container {
  flex: 1;
  max-width: 500px;
  margin: 0 20px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}
</style>
