<template>
  <div class="main-layout">
    <AppSidebar />
    <div class="main-content">
      <AppHeader @search="handleSearch" />
      <div class="content-container">
        <slot :searchQuery="searchQuery"></slot>
      </div>
    </div>
  </div>
</template>

<script>
import AppHeader from './AppHeader.vue'
import AppSidebar from './AppSidebar.vue'
import { ref, provide } from 'vue'

export default {
  name: 'AppLayout',
  components: {
    AppHeader,
    AppSidebar
  },
  setup() {
    const searchQuery = ref('')
    
    // 提供搜索查询给所有子组件
    provide('searchQuery', searchQuery)
    
    const handleSearch = (query) => {
      searchQuery.value = query
    }
    
    return {
      searchQuery,
      handleSearch
    }
  }
}
</script>

<style scoped>
.main-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.content-container {
  flex: 1;
  padding: 20px;
  background-color: var(--background-color);
  overflow-y: auto;
  height: calc(100vh - 60px);
}
</style>
