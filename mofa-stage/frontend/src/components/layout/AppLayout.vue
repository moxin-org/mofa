<template>
  <div class="main-layout">
    <AppHeader />
    <div class="main-body">
      <AppSidebar />
      <div class="content-container">
        <slot></slot>
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
    return {}
  }
}
</script>

<style scoped>
.main-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.main-body {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.content-container {
  flex: 1;
  padding: 20px;
  background-color: var(--background-color);
  overflow-y: auto;
  height: calc(100vh - 70px);
  position: relative;
  transition: none;
  contain: layout size;
}
</style>
