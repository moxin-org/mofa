<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">{{ $t('sidebar.commandLine') }}</h1>
      <div class="page-actions" v-if="isEnvironmentConfigured">
        <el-button type="primary" @click="addNewTab">
          {{ $t('terminal.newTab') }}
        </el-button>
      </div>
    </div>

    <el-card v-if="isLoading" class="loading-card">
      <el-skeleton :rows="6" animated />
    </el-card>

    <div v-else class="terminal-container">
      <el-card class="terminal-card">
        <!-- Terminal section moved to the top -->
        <div class="terminal-tabs" v-if="isEnvironmentConfigured && terminalTabs.length > 0">
          <el-tabs v-model="activeTabId" type="card" closable @tab-remove="closeTab" @tab-click="focusActiveTab">
            <el-tab-pane 
              v-for="tab in terminalTabs" 
              :key="tab.id" 
              :label="tab.title" 
              :name="tab.id"
            >
              <div class="terminal-wrapper">
                <div class="terminal-output" :ref="el => { if (el) terminalOutputRefs[tab.id] = el }">
                  <div v-for="(line, index) in tab.lines" :key="index" :class="{ 'command-line': line.isCommand }">
                    <span v-if="line.isCommand" class="prompt" v-html="line.prompt || tab.prompt"></span>{{ line.text }}
                  </div>
                  <div class="current-input-line">
                    <span class="prompt" v-html="tab.prompt"></span>
                    <input 
                      :ref="el => { if (el) terminalInputRefs[tab.id] = el }"
                      v-model="tab.currentCommand" 
                      @keydown="handleKeyDown($event, tab)"
                      :disabled="tab.isExecuting"
                      class="command-input"
                      :placeholder="tab.isExecuting ? $t('terminal.executing') : $t('terminal.enterCommand')"
                    />
                  </div>
                </div>
                <div class="terminal-actions">
                  <el-button size="small" @click="clearTerminal(tab)" :disabled="tab.isExecuting">
                    {{ $t('terminal.clear') }}
                  </el-button>
                  <el-button size="small" @click="executeCommand(tab)" :disabled="tab.isExecuting || !tab.currentCommand">
                    {{ $t('terminal.execute') }}
                  </el-button>
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>

        <!-- Environment info moved after terminal -->
        <div class="terminal-info">
          <h3>{{ $t('terminal.environmentInfo') }}</h3>
          <div class="env-details">
            <p><strong>{{ $t('terminal.environmentType') }}:</strong> 
              {{ settings.use_system_mofa ? $t('settings.useSystemMofa') : $t('settings.useVirtualEnv') }}
            </p>
            <p v-if="!settings.use_system_mofa">
              <strong>{{ $t('settings.mofaEnvPath') }}:</strong> {{ settings.mofa_env_path || $t('terminal.notConfigured') }}
            </p>
            <p>
              <strong>{{ $t('settings.mofaDir') }}:</strong> {{ settings.mofa_dir || $t('terminal.notConfigured') }}
            </p>
          </div>
        </div>

        <div v-if="!isEnvironmentConfigured" class="terminal-warning">
          {{ $t('terminal.configurationRequired') }}
        </div>

        <div v-if="platformInfo" class="platform-info">
          <h4>{{ $t('terminal.platformInfo') }}</h4>
          <p>{{ platformInfo }}</p>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, nextTick, watch, reactive } from 'vue'
import { useSettingsStore } from '../store/settings'
import { ElMessage } from 'element-plus'

export default {
  name: 'Terminal',
  setup() {
    const settingsStore = useSettingsStore()
    const isLoading = ref(true)
    const platformInfo = ref('')
    const terminalTabs = ref([])
    const activeTabId = ref('')
    const terminalOutputRefs = reactive({})
    const terminalInputRefs = reactive({})
    const tabCounter = ref(1)
    const systemInfo = ref({
      username: 'user',
      hostname: 'localhost',
      platform: ''
    })
    
    // Get the platform information from the backend
    const getPlatformInfo = async () => {
      try {
        const response = await fetch('/api/terminal/platform')
        const data = await response.json()
        if (data.success) {
          platformInfo.value = data.platform
          // Try to extract system info from platform info
          if (data.system_info) {
            systemInfo.value = data.system_info
          }
        }
      } catch (error) {
        console.error('Failed to get platform information:', error)
      }
    }
    
    // Computed property to get settings from the store
    const settings = computed(() => settingsStore.settings)
    
    // Check if the environment is properly configured
    const isEnvironmentConfigured = computed(() => {
      if (settings.value.use_system_mofa) {
        // For system MOFA, we just need the MOFA directory
        return !!settings.value.mofa_dir
      } else {
        // For virtual environment, we need both the MOFA directory and the environment path
        return !!settings.value.mofa_dir && !!settings.value.mofa_env_path
      }
    })
    
    // Create a new terminal tab
    const addNewTab = async () => {
      try {
        // Create a new terminal session
        const response = await fetch('/api/terminal/session', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            use_system_mofa: settings.value.use_system_mofa,
            mofa_env_path: settings.value.mofa_env_path,
            mofa_dir: settings.value.mofa_dir
          })
        })
        
        const data = await response.json()
        if (data.success) {
          const tabId = `tab-${tabCounter.value++}`
          const newTab = {
            id: tabId,
            title: `Terminal ${terminalTabs.value.length + 1}`,
            sessionId: data.session_id,
            lines: [
              { text: data.message, isCommand: false }
            ],
            currentCommand: '',
            isExecuting: false,
            commandHistory: [],
            historyIndex: -1,
            cwd: data.cwd || settings.value.mofa_dir,
            prompt: generatePrompt(data.cwd || settings.value.mofa_dir)
          }
          
          terminalTabs.value.push(newTab)
          activeTabId.value = tabId
          
          // Focus the new tab's input after it's created
          await nextTick()
          focusActiveTab()
        } else {
          ElMessage.error(data.message || 'Failed to initialize terminal session')
        }
      } catch (error) {
        console.error('Failed to create new terminal tab:', error)
        ElMessage.error('Failed to create new terminal tab: ' + error.message)
      }
    }
    
    // Close a terminal tab
    const closeTab = async (tabId) => {
      const tabIndex = terminalTabs.value.findIndex(tab => tab.id === tabId)
      if (tabIndex === -1) return
      
      const tab = terminalTabs.value[tabIndex]
      
      try {
        // Close the terminal session on the backend
        await fetch('/api/terminal/close', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            session_id: tab.sessionId
          })
        })
      } catch (error) {
        console.error('Error closing terminal session:', error)
      }
      
      // Remove the tab
      terminalTabs.value.splice(tabIndex, 1)
      
      // Clean up references
      delete terminalOutputRefs[tabId]
      delete terminalInputRefs[tabId]
      
      // If we closed the active tab, activate another one if available
      if (terminalTabs.value.length > 0 && activeTabId.value === tabId) {
        activeTabId.value = terminalTabs.value[0].id
        await nextTick()
        focusActiveTab()
      }
    }
    
    // Focus the active tab's input
    const focusActiveTab = async () => {
      await nextTick()
      const activeTab = terminalTabs.value.find(tab => tab.id === activeTabId.value)
      if (activeTab && terminalInputRefs[activeTab.id]) {
        terminalInputRefs[activeTab.id].focus()
        scrollToBottom(activeTab.id)
      }
    }
    
    // Generate terminal prompt based on current directory
    const generatePrompt = (cwd) => {
      const username = systemInfo.value.username || 'user'
      const hostname = systemInfo.value.hostname || 'localhost'
      return `<span class="user-host">${username}@${hostname}</span>:<span class="path">${cwd}</span>$ `
    }
    
    // Handle keyboard shortcuts
    const handleKeyDown = (event, tab) => {
      // Handle Enter key to execute command
      if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault()
        executeCommand(tab)
      }
      
      // Handle Ctrl+C to interrupt
      else if (event.ctrlKey && event.key === 'c') {
        if (tab.isExecuting) {
          interruptCommand(tab)
        } else {
          // Add ^C to the terminal output
          tab.lines.push({ text: '^C', isCommand: false })
          tab.currentCommand = ''
        }
      }
      
      // Handle Up Arrow for command history
      else if (event.key === 'ArrowUp') {
        event.preventDefault()
        navigateHistory(tab, 'up')
      }
      
      // Handle Down Arrow for command history
      else if (event.key === 'ArrowDown') {
        event.preventDefault()
        navigateHistory(tab, 'down')
      }
      
      // Handle Tab for auto-completion (future enhancement)
      else if (event.key === 'Tab') {
        event.preventDefault()
        // Auto-completion could be implemented here
      }
    }
    
    // Navigate command history
    const navigateHistory = (tab, direction) => {
      if (tab.commandHistory.length === 0) return
      
      if (direction === 'up') {
        if (tab.historyIndex < tab.commandHistory.length - 1) {
          tab.historyIndex++
        }
      } else if (direction === 'down') {
        if (tab.historyIndex > -1) {
          tab.historyIndex--
        }
      }
      
      if (tab.historyIndex === -1) {
        tab.currentCommand = ''
      } else {
        tab.currentCommand = tab.commandHistory[tab.historyIndex]
      }
    }
    
    // Interrupt a running command
    const interruptCommand = async (tab) => {
      if (!tab.isExecuting) return
      
      try {
        const response = await fetch('/api/terminal/interrupt', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            session_id: tab.sessionId
          })
        })
        
        const data = await response.json()
        if (data.success) {
          tab.lines.push({ text: '^C', isCommand: false })
          tab.isExecuting = false
        } else {
          tab.lines.push({ text: `Error: ${data.message}`, isCommand: false })
        }
      } catch (error) {
        console.error('Failed to interrupt command:', error)
        tab.lines.push({ text: `Error interrupting command: ${error.message}`, isCommand: false })
      } finally {
        scrollToBottom(tab.id)
        focusInput(tab.id)
      }
    }
    
    // Execute a command in the terminal
    const executeCommand = async (tab) => {
      if (!tab || !tab.currentCommand.trim() || tab.isExecuting) return
      
      const command = tab.currentCommand.trim()
      
      // Add command to history (avoid duplicates at the start)
      if (tab.commandHistory.length === 0 || tab.commandHistory[0] !== command) {
        tab.commandHistory.unshift(command)
      }
      tab.historyIndex = -1
      
      // Display command in terminal with the current prompt
      tab.lines.push({ 
        text: command, 
        isCommand: true, 
        prompt: tab.prompt // Store the current prompt with this command
      })
      tab.currentCommand = ''
      tab.isExecuting = true
      
      try {
        const response = await fetch('/api/terminal/execute', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            session_id: tab.sessionId,
            command: command
          })
        })
        
        const data = await response.json()
        if (data.success) {
          // Split output by newlines and add each line to terminal
          if (data.output) {
            const outputLines = data.output.split('\n')
            outputLines.forEach(line => {
              if (line.trim()) {
                tab.lines.push({ text: line, isCommand: false })
              }
            })
          }
          
          // Update current directory and prompt if changed
          if (data.cwd && data.cwd !== tab.cwd) {
            // Store the old prompt for reference in case we need to update any existing lines
            const oldPrompt = tab.prompt
            
            // Update the current working directory and prompt
            tab.cwd = data.cwd
            tab.prompt = generatePrompt(data.cwd)
            
            // If this was a cd command and we have old_cwd info, we don't need to update any existing prompts
            // The command itself will have the correct prompt stored with it already
          }
        } else {
          tab.lines.push({ text: `Error: ${data.message}`, isCommand: false })
        }
      } catch (error) {
        console.error('Failed to execute command:', error)
        tab.lines.push({ text: `Error: ${error.message}`, isCommand: false })
      } finally {
        tab.isExecuting = false
        scrollToBottom(tab.id)
        focusInput(tab.id)
      }
    }
    
    // Clear the terminal
    const clearTerminal = (tab) => {
      if (!tab) return
      tab.lines = []
      focusInput(tab.id)
    }
    
    // Scroll to the bottom of the terminal output
    const scrollToBottom = async (tabId) => {
      await nextTick()
      const outputElement = terminalOutputRefs[tabId]
      if (outputElement) {
        outputElement.scrollTop = outputElement.scrollHeight
      }
    }
    
    // Focus the input of a specific tab
    const focusInput = async (tabId) => {
      await nextTick()
      const inputElement = terminalInputRefs[tabId]
      if (inputElement) {
        inputElement.focus()
      }
    }
    
    // Load settings and platform info when component is mounted
    onMounted(async () => {
      await settingsStore.fetchSettings()
      await getPlatformInfo()
      isLoading.value = false
      
      if (isEnvironmentConfigured.value) {
        // Create initial tab
        await addNewTab()
      }
    })
    
    return {
      settings,
      isLoading,
      isEnvironmentConfigured,
      platformInfo,
      terminalTabs,
      activeTabId,
      terminalOutputRefs,
      terminalInputRefs,
      addNewTab,
      closeTab,
      focusActiveTab,
      handleKeyDown,
      executeCommand,
      clearTerminal
    }
  }
}
</script>

<style scoped>
.page-container {
  display: flex;
  flex-direction: column;
  height: auto;
  min-height: calc(100vh - 80px);
  overflow-y: auto;
  padding-bottom: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.terminal-container {
  flex: none;
  display: flex;
  flex-direction: column;
  overflow: visible;
  min-height: 0; /* Important for Firefox */
}

.terminal-card {
  flex: none;
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
  overflow: visible;
  min-height: 0; /* Important for Firefox */
}

.terminal-info {
  margin-bottom: 20px;
}

.env-details {
  background-color: var(--el-fill-color-light);
  padding: 15px;
  border-radius: 4px;
  margin-top: 10px;
}

.terminal-warning {
  color: var(--el-color-danger);
  margin: 15px 0;
  font-size: 14px;
}

.platform-info {
  margin: 15px 0;
  padding: 15px;
  background-color: var(--el-fill-color-light);
  border-radius: 4px;
}

.loading-card {
  padding: 20px;
}

.terminal-tabs {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-height: 0; /* Important for Firefox */
}

.terminal-tabs :deep(.el-tabs) {
  display: flex;
  flex-direction: column;
  height: auto;
  min-height: 0; /* Important for Firefox */
}

.terminal-tabs :deep(.el-tabs__content) {
  flex: none;
  overflow: hidden;
  min-height: 0; /* Important for Firefox */
}

.terminal-tabs :deep(.el-tab-pane) {
  height: auto;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.terminal-wrapper {
  height: 400px; 
  border: 1px solid var(--el-border-color);
  border-radius: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  min-height: 0; /* Important for Firefox */
  flex: none; /* Prevent flex growth */
  margin-bottom: 20px; /* Add space between terminal and info sections */
}

.terminal-output {
  flex: 1;
  background-color: #1e1e1e;
  color: #f0f0f0;
  font-family: 'Courier New', monospace;
  padding: 10px;
  overflow-y: scroll;
  white-space: pre-wrap;
  word-break: break-all;
  min-height: 0; /* Important for Firefox */
  height: 420px; /* Increased fixed height for the output area */
  max-height: 420px; /* Ensure it doesn't grow beyond this */
}

.command-line {
  color: #4CAF50;
  margin-bottom: 5px;
}

.prompt {
  margin-right: 5px;
  white-space: nowrap;
}

.user-host {
  color: #4CAF50;
  font-weight: bold;
}

.path {
  color: #3498db;
  font-weight: bold;
}

.current-input-line {
  display: flex;
  align-items: center;
  margin-top: 5px;
}

.command-input {
  background-color: transparent;
  border: none;
  color: #f0f0f0;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  flex-grow: 1;
  outline: none;
  padding: 5px 0;
}

.terminal-actions {
  display: flex;
  justify-content: flex-end;
  padding: 10px;
  background-color: #f5f7fa;
  border-top: 1px solid var(--el-border-color);
}
</style>