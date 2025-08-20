<template>
  <div class="page-container webssh-view">
    <div class="page-header">
      <h1 class="page-title">{{ $t('sidebar.webSSH') || 'Web SSH' }}</h1>
    </div>

    <div class="webssh-layout">
      <!-- Examples Sidebar -->
      <div class="examples-sidebar">
        <div class="examples-header">Dataflows</div>
        <div class="examples-search">
          <el-input
            v-model="searchQuery"
            placeholder="Search Dataflows..."
            clearable
            @input="filterExamples"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>
        <div class="examples-list">
          <div 
            v-for="example in filteredExamples" 
            :key="example.name" 
            class="example-item" 
            :class="{ active: selectedExample === example.name }"
            @click="selectExample(example.name)"
          >
            {{ example.name }}
          </div>
        </div>
      </div>
      
      <!-- SSH Terminal Card -->
      <el-card class="ssh-card">
        <el-tabs 
          v-model="activeTabName" 
          type="card" 
          addable 
          closable 
          @tab-add="handleTabAdd" 
          @tab-remove="handleTabRemove"
          @tab-change="handleTabChange"
          class="terminal-tabs"
      >
        <el-tab-pane
          v-for="session in sessions"
          :key="session.name" 
          :label="session.title"
          :name="session.name"
          class="terminal-tab-pane"
        >
          <template #label>
             <span class="tab-label">
               <el-icon v-if="session.status === 'connecting'" class="is-loading"><Loading /></el-icon>
               <el-icon v-else-if="session.status === 'connected'"><Monitor /></el-icon>
               <el-icon v-else><QuestionFilled /></el-icon>
               {{ session.title }}
             </span>
           </template>
           <!-- Ensure terminal takes full height -->
           <div class="terminal-tab-content">
             <XtermTerminalTab 
               v-show="activeTabName === session.name" 
               :session-id="session.id" 
               :ssh-config="session.config"
               :ref="el => setSessionRef(session.id, el)" 
               @status-change="(status) => handleStatusChange(session.id, status)"
               @error="(msg) => handleSessionError(session.id, msg)"
               @connected="() => handleStatusChange(session.id, 'connected')"
               @disconnected="() => handleStatusChange(session.id, 'disconnected')"
             />
          </div>
        </el-tab-pane>
      </el-tabs>
       <div v-if="sessions.length === 0" class="no-tabs-placeholder">
         <div class="env-info">
           <h3>Environment Information</h3>
           <p>Environment Type: Use System Installed MOFA</p>
           <p>MOFA Directory: {{ savedMofaDir || 'Not Set' }}</p>
           <h3>Platform Information</h3>
           <p>{{ platformInfo || 'Loading system information...' }}</p>
         </div>
         <div class="action-hint">
           Click the '+' button to open a new SSH tab.
         </div>
        </div>
      </el-card>
    </div>

    <!-- SSH Settings Dialog -->
    <el-dialog
      v-model="showSettingsDialog"
      :title="$t('ssh.newConnection') || 'New SSH Connection'"
      width="500px"
      @closed="resetSshConfig" 
    >
      <el-form :model="sshConfig" label-width="120px" ref="sshConfigForm">
        <el-form-item :label="$t('ssh.hostname') || 'Hostname'" prop="hostname" :rules="[{ required: true, message: 'Hostname is required', trigger: 'blur' }]">
          <el-input v-model="sshConfig.hostname" placeholder="127.0.0.1" />
        </el-form-item>
        <el-form-item :label="$t('ssh.port') || 'Port'" prop="port" :rules="[{ required: true, type: 'number', message: 'Port is required', trigger: 'blur' }]">
          <el-input-number v-model="sshConfig.port" :min="1" :max="65535" />
        </el-form-item>
        <el-form-item :label="$t('ssh.username') || 'Username'" prop="username" :rules="[{ required: true, message: 'Username is required', trigger: 'blur' }]">
          <el-input v-model="sshConfig.username" />
        </el-form-item>
        <el-form-item :label="$t('ssh.password') || 'Password'">
          <el-input v-model="sshConfig.password" type="password" show-password />
        </el-form-item>
         <el-form-item :label="$t('ssh.remember') || 'Remember Config'">
          <el-switch v-model="rememberConfig" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showSettingsDialog = false">{{ $t('common.cancel') || 'Cancel' }}</el-button>
          <el-button type="primary" @click="saveSettingsAndAddTab">{{ $t('ssh.connect') || 'Connect' }}</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted, onBeforeUnmount, nextTick, watch, shallowRef, onActivated, onDeactivated } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useSettingsStore } from '../store/settings'
import { useAgentStore } from '../store/agent'
import XtermTerminalTab from '../components/XtermTerminalTab.vue'
import { Loading, Monitor, QuestionFilled, VideoPlay, Search } from '@element-plus/icons-vue'

export default {
  name: 'WebSSH',
  components: {
    XtermTerminalTab,
    Loading,
    Monitor,
    QuestionFilled,
    VideoPlay,
    Search,
  },
  setup() {
    const settingsStore = useSettingsStore()
    const agentStore = useAgentStore()
    const showSettingsDialog = ref(false)
    const activeTabName = ref('')
    const sessions = ref([])
    const sessionRefs = reactive({})
    const platformInfo = ref('')
    const savedMofaDir = ref('')
    const examples = ref([])
    const filteredExamples = ref([])
    const searchQuery = ref('')
    const selectedExample = ref('')
    const sshConfigForm = ref(null)
    const rememberConfig = ref(true)
    const isInitialized = ref(false)
    const nextTabId = ref(1)

    // Default/Current SSH Config for the dialog
    const sshConfig = reactive({
      hostname: '',
      port: 22,
      username: '',
      password: '',
    })

    // Function to store refs, compatible with Vue 3 script setup ref binding
    const setSessionRef = (sessionId, el) => {
      if (el) {
        sessionRefs[sessionId] = el
      }
    }

    const initializeComponent = async () => {
      try {
        // Load settings
        await settingsStore.fetchSettings()
        const settings = settingsStore.settings
        savedMofaDir.value = settings.mofa_dir || 'Not Set'

        // Get platform info
        try {
          const response = await fetch('/api/system/info')
          if (response.ok) {
            const data = await response.json()
            platformInfo.value = data.platform_info || 'Unknown platform'
          } else {
            console.error('Failed to fetch platform info:', response.statusText)
            platformInfo.value = 'Error fetching platform info'
          }
        } catch (error) {
          console.error('Error fetching platform info:', error)
          platformInfo.value = 'Error: ' + error.message
        }

        // Load SSH settings if available
        if (settingsStore.settings && settingsStore.settings.ssh) {
          // Copy SSH settings to local config
          Object.assign(sshConfig, settingsStore.settings.ssh)
          console.log('Loaded SSH settings from store:', 
              {...sshConfig, password: sshConfig.password ? '******' : ''})
        } else {
          console.warn('No SSH settings found in store')
        }
        
        // Attempt to load last used config from local storage as fallback
        const savedConfig = localStorage.getItem('webssh_last_config')
        if (savedConfig) {
          try {
            const parsed = JSON.parse(savedConfig)
            // Only override non-empty fields from local storage
            if (parsed.hostname) sshConfig.hostname = parsed.hostname
            if (parsed.port) sshConfig.port = parsed.port
            if (parsed.username) sshConfig.username = parsed.username
            // Password will be loaded from store, not localStorage
            
            console.log('Merged with localStorage config:', 
                {...sshConfig, password: sshConfig.password ? '******' : ''})
          } catch(e) {
            console.error('Failed to parse saved SSH config', e)
            localStorage.removeItem('webssh_last_config')
          }
        }
        
        // Fetch examples list from API
        try {
          // 使用agent store获取examples列表
          await agentStore.fetchAgents()
          
          // 从store中获取example_agents
          const exampleAgents = agentStore.exampleAgents || []
          
          // 转换为与当前组件兼容的格式
          if (exampleAgents.length > 0) {
            examples.value = exampleAgents.map(name => {
              return {
                name: name,
                path: `/mnt/c/Users/Yao/Desktop/code/mofa/mofa/python/examples/${name}`
              }
            })
            filteredExamples.value = examples.value
          } else {
            console.warn('No examples found from API, using fallback')
            // 如果API没有返回examples，使用默认的fallback
            examples.value = [
              { name: 'hello_world', path: '/mnt/c/Users/Yao/Desktop/code/mofa/mofa/python/examples/hello_world' },
              { name: 'add_numbers', path: '/mnt/c/Users/Yao/Desktop/code/mofa/mofa/python/examples/add_numbers' }
            ]
            filteredExamples.value = examples.value
          }
        } catch (error) {
          console.error('Error fetching examples:', error)
          // 出错时使用默认的fallback
          examples.value = [
            { name: 'hello_world', path: '/mnt/c/Users/Yao/Desktop/code/mofa/mofa/python/examples/hello_world' },
            { name: 'add_numbers', path: '/mnt/c/Users/Yao/Desktop/code/mofa/mofa/python/examples/add_numbers' }
          ]
          filteredExamples.value = examples.value
        }
        
        // Automatically open a tab if config is valid and no sessions exist
        if (sessions.value.length === 0 && sshConfig.hostname && sshConfig.username) {
          addTab({...sshConfig})
        }
        
        isInitialized.value = true
      } catch (error) {
        console.error('Error initializing component:', error)
        platformInfo.value = 'Error: ' + error.message
      }
    };
    
    // Load settings on mount
    onMounted(() => {
      initializeComponent();
    });
    
    // Handle component activation (when switching back to this view)
    onActivated(() => {
      console.log('WebSSH activated, sessions:', sessions.value.length);
      
      // Initialize if not already done
      if (!isInitialized.value) {
        console.log('WebSSH initializing for the first time');
        initializeComponent();
      }
      
      // Resize all terminal tabs when the component is activated
      nextTick(() => {
        console.log('Resizing all terminal sessions');
        Object.values(sessionRefs).forEach(termRef => {
          if (termRef && typeof termRef.resizeTerminal === 'function') {
            setTimeout(() => {
              termRef.resizeTerminal();
            }, 100);
          }
        });
      });
    });
    
    // Handle component deactivation (when switching away from this view)
    onDeactivated(() => {
      console.log('WebSSH deactivated, sessions remaining active:', sessions.value.length);
      // We keep all sessions running in the background
    });

    onBeforeUnmount(() => {
      // This should only happen when the entire app is being unmounted
      // Clean up any remaining session refs on component unmount
      console.log('WebSSH unmounting, cleaning up all sessions');
      sessionRefs.value = {}
      // Sessions are cleaned up by closing tabs, but good practice:
      sessions.value.forEach(session => {
           const termRef = sessionRefs.value[session.id];
           if (termRef && typeof termRef.disconnect === 'function') {
               termRef.disconnect();
           }
       });
       sessions.value = [];
    });

    const resetSshConfig = () => {
       // Keep remembered config if checkbox was checked
       // Let's simplify: always keep the last loaded config, but clear password
       /* if (!rememberConfig.value) {
           sshConfig.hostname = '';
           sshConfig.port = 22;
           sshConfig.username = '';
           sshConfig.password = '';
       } */
       // Always clear password when dialog closes/reopens
       sshConfig.password = '';
       // Reset form validation if needed
       sshConfigForm.value?.clearValidate();
    };

    const addTab = (configToAdd) => {
      const newId = nextTabId.value++;
      const newName = `session-${newId}`;
      const newTitle = `${configToAdd.username}@${configToAdd.hostname}`;
      
      const newSession = {
        id: newId,
        name: newName,
        title: newTitle,
        config: { ...configToAdd }, // Copy config
        status: 'connecting', // Initial status
        ref: null // Ref will be set by setSessionRef
      };

      sessions.value.push(newSession)
      activeTabName.value = newName
      
      // Save config if remember checkbox is checked
      if (rememberConfig.value) {
          try {
              localStorage.setItem('webssh_last_config', JSON.stringify(configToAdd));
          } catch (e) {
              console.error('Failed to save SSH config to localStorage', e);
          }
          }
        }
        
    const handleTabAdd = () => {
        // Instead of showing settings dialog, directly use current config
        if (sshConfig.hostname && sshConfig.username) {
            // Use current settings from store/config
            addTab({...sshConfig});
        } else {
            // Show message that settings are incomplete
            ElMessage.warning('SSH settings are incomplete. Please configure them in the Settings page.');
            
            // Optional: You could navigate to settings page
            // router.push('/settings');
        }
    }

    const handleTabRemove = (targetName) => {
      const sessionIndex = sessions.value.findIndex(s => s.name === targetName)
      if (sessionIndex === -1) return;

      const session = sessions.value[sessionIndex]
      const termRef = sessionRefs.value[session.id]

      // Call disconnect on the terminal component instance
      if (termRef && typeof termRef.disconnect === 'function') {
        termRef.disconnect()
      } else {
          console.warn(`Could not find terminal ref for session ${session.id} to disconnect.`);
    }

      // Remove the session from the list
      sessions.value.splice(sessionIndex, 1)

      // Clean up the ref
      delete sessionRefs.value[session.id]

      // If the closed tab was the active one, activate the next/previous tab
      if (activeTabName.value === targetName) {
        const nextTab = sessions.value[sessionIndex] || sessions.value[sessionIndex - 1]
        activeTabName.value = nextTab ? nextTab.name : ''
      }
    }
    
    const handleTabChange = (newTabName) => {
        // When tab changes, try to resize the newly visible terminal
        nextTick(() => {
            const activeSession = sessions.value.find(s => s.name === newTabName);
            if (activeSession) {
                const termRef = sessionRefs.value[activeSession.id];
                if (termRef && typeof termRef.resizeTerminal === 'function') {
                    // Add a small delay to ensure transition/rendering completes
                    // Use multiple resize calls with increasing delays to ensure it catches
                    termRef.resizeTerminal();
                    
                    setTimeout(() => {
                        termRef.resizeTerminal();
                    }, 50);
                    
                    setTimeout(() => {
                        termRef.resizeTerminal();
                    }, 200);
                    
                    setTimeout(() => {
                        termRef.resizeTerminal();
                    }, 500);
                } else {
                    console.warn(`Terminal ref not ready for resize on tab change: ${newTabName}`);
      }
    }
        });
    };

    const saveSettingsAndAddTab = async () => {
       if (!sshConfigForm.value) return;
       try {
         await sshConfigForm.value.validate();
         // Validation passed
         const configToUse = { ...sshConfig };
         addTab(configToUse);
         showSettingsDialog.value = false;
       } catch (validationError) {
         // Validation failed
         console.log('SSH Config validation failed:', validationError);
         ElMessage.error('Please fill in all required fields.');
      }
    }

    const handleStatusChange = (sessionId, status) => {
      const session = sessions.value.find(s => s.id === sessionId)
      if (session) {
        session.status = status
        // Optionally update title based on status
        // if (status === 'connected') session.title = `${session.config.username}@${session.config.hostname}`;
        // else if (status === 'connecting') session.title = `Connecting...`;
        // else session.title = `Disconnected`; // Or keep original title
      }
    }

    const handleSessionError = (sessionId, msg) => {
      // Check if terminal_display_mode is ttyd, if so, don't show error messages
      if (settingsStore.settings?.terminal_display_mode === 'ttyd') {
        console.log(`Suppressing error in ttyd mode: session ${sessionId}: ${msg}`)
        return
      }
      
      const session = sessions.value.find(s => s.id === sessionId)
      ElMessage.error(`Error in session ${session ? session.title : sessionId}: ${msg}`)
      // Optionally close the tab on error, or mark it visually
      // handleTabRemove(session.name); 
    }

    // Select an example from the sidebar and copy to clipboard
    const selectExample = async (exampleName) => {
      selectedExample.value = exampleName
      
      try {
        // 动态获取实际的 dataflow 文件名
        const response = await fetch(`/api/agents/${exampleName}/dataflow-file`);
        let dataflowFile = `${exampleName}_dataflow.yml`; // 默认文件名作为兜底
        let examplesPath = '';
        
        if (response.ok) {
          const data = await response.json();
          if (data.success) {
            dataflowFile = data.dataflow_file;
            examplesPath = data.agent_path;
            console.log(`检测到 dataflow 文件: ${dataflowFile}`);
          }
        }
        
        // 如果 API 调用失败，使用设置中的路径作为兜底
        if (!examplesPath) {
          const settings = settingsStore.settings;
          // 优先使用custom_examples_path，如果不存在则使用examples_path
          if (settings.custom_examples_path) {
            examplesPath = settings.custom_examples_path;
          } else if (settings.examples_path) {
            examplesPath = settings.examples_path;
          } else {
            examplesPath = '/mnt/c/Users/Yao/Desktop/code/mofa/mofa/python/examples';
          }
          examplesPath = `${examplesPath}/${exampleName}`;
        }
        
        // 构建完整命令
        const fullCommand = `cd ${examplesPath} && dora up && dora build ${dataflowFile} && dora start ${dataflowFile}`;
        
        // 复制命令到剪贴板
        await navigator.clipboard.writeText(fullCommand);
        ElMessage.success(`Command copied to clipboard (${dataflowFile})`);
        
      } catch (err) {
        console.error('Failed to copy text: ', err);
        ElMessage.error('Copy Failed');
        
        // 兜底方案：使用默认命名约定
        const settings = settingsStore.settings;
        let examplesPath = '';
        if (settings.custom_examples_path) {
          examplesPath = settings.custom_examples_path;
        } else if (settings.examples_path) {
          examplesPath = settings.examples_path;
        } else {
          examplesPath = '/mnt/c/Users/Yao/Desktop/code/mofa/mofa/python/examples';
        }
        
        const fallbackCommand = `cd ${examplesPath}/${exampleName} && dora up && dora build ${exampleName}_dataflow.yml && dora start ${exampleName}_dataflow.yml`;
        try {
          await navigator.clipboard.writeText(fallbackCommand);
          ElMessage.warning(`Command copied with default filename (${exampleName}_dataflow.yml)`);
        } catch (fallbackErr) {
          console.error('Fallback copy also failed:', fallbackErr);
          ElMessage.error('Copy Failed');
        }
      }
    }
    
    // Run the selected example
    const runSelectedExample = async () => {
      if (!selectedExample.value) {
        ElMessage.warning('Please select an example first')
        return
      }
      
      // Find the active terminal session
      const activeSession = sessions.value.find(s => s.name === activeTabName.value)
      if (!activeSession) {
        ElMessage.warning('Please open a terminal tab first')
        return
      }
      
      // Get the terminal component reference
      const terminalComponent = sessionRefs[activeSession.id]
      if (!terminalComponent) {
        ElMessage.error('Terminal component not found')
        return
      }
      
      // Find the example path
      const example = examples.value.find(e => e.name === selectedExample.value)
      if (!example) {
        ElMessage.error('Example not found')
        return
      }
      
      try {
        // 动态获取实际的 dataflow 文件名
        const response = await fetch(`/api/agents/${selectedExample.value}/dataflow-file`);
        let dataflowFile = `${selectedExample.value}_dataflow.yml`; // 默认文件名作为兜底
        
        if (response.ok) {
          const data = await response.json();
          if (data.success) {
            dataflowFile = data.dataflow_file;
            console.log(`检测到 dataflow 文件: ${dataflowFile}`);
          }
        }
        
        // Create the command to run with detected file name
        const commands = [
          `cd ${example.path} &&`,
          'dora up &&', 
          `dora build ${dataflowFile} &&`, 
          `dora start ${dataflowFile}`
        ]
        
        // Send the commands to the terminal
        const commandString = commands.join(' ')
        
        // Send command to the terminal
        if (terminalComponent && terminalComponent.ws && terminalComponent.ws.readyState === WebSocket.OPEN) {
          // Send the command to the terminal
          terminalComponent.ws.send(JSON.stringify({ type: 'input', data: commandString }))
          
          // Send Enter key
          terminalComponent.ws.send(JSON.stringify({ type: 'input', data: '\r' }))
          
          ElMessage.success(`Running example: ${selectedExample.value} (${dataflowFile})`)
        } else {
          ElMessage.error('Terminal not connected')
        }
      } catch (err) {
        console.error('Failed to get dataflow file:', err);
        
        // 兜底方案：使用默认命名约定
        const commands = [
          `cd ${example.path} &&`,
          'dora up &&', 
          `dora build ${selectedExample.value}_dataflow.yml &&`, 
          `dora start ${selectedExample.value}_dataflow.yml`
        ]
        
        const commandString = commands.join(' ')
        
        if (terminalComponent && terminalComponent.ws && terminalComponent.ws.readyState === WebSocket.OPEN) {
          terminalComponent.ws.send(JSON.stringify({ type: 'input', data: commandString }))
          terminalComponent.ws.send(JSON.stringify({ type: 'input', data: '\r' }))
          ElMessage.warning(`Running example with default filename: ${selectedExample.value}`)
        } else {
          ElMessage.error('Terminal not connected')
        }
      }
    }
    
    // Initialize component on mount
    onMounted(() => {
      initializeComponent()
    })
    
    // 过滤examples列表
const filterExamples = () => {
  if (!searchQuery.value) {
    filteredExamples.value = examples.value
  } else {
    const query = searchQuery.value.toLowerCase()
    filteredExamples.value = examples.value.filter(example => 
      example.name.toLowerCase().includes(query)
    )
  }
}

return {
      showSettingsDialog,
      sshConfig,
      sshConfigForm,
      rememberConfig,
      sessions,
      activeTabName,
      platformInfo,
      savedMofaDir,
      examples,
      filteredExamples,
      searchQuery,
      selectedExample,
      handleTabAdd,
      handleTabRemove,
      handleTabChange,
      saveSettingsAndAddTab,
      handleStatusChange,
      handleSessionError,
      setSessionRef,
      resetSshConfig,
      selectExample,
      runSelectedExample,
      filterExamples
    }
  }
}
</script>

<style scoped>
.webssh-view {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 60px); /* Adjust based on your layout's header height */
  min-height: 600px; /* Ensure minimum height */
  overflow: hidden; /* Prevent overflow at the container level */
  max-width: 100%; /* Prevent horizontal overflow */
  contain: layout style; /* 提高渲染性能 */
  will-change: opacity; /* 告诉浏览器这个元素可能会产生变化，帮助优化渲染 */
  transition: none !important; /* 禁用任何过渡效果 */
}

.page-header {
  margin-bottom: 10px; /* Reduce header margin to save space */
  flex-shrink: 0; /* Prevent header from shrinking */
  transition: none !important; /* 禁用过渡效果 */
}

.webssh-layout {
  display: flex;
  flex-grow: 1;
  min-height: 500px;
  gap: 15px;
  overflow: hidden; /* Prevent overflow in the layout */
  width: 100%; /* Ensure it takes full width */
  position: relative; /* For absolute positioning if needed */
  contain: layout; /* 提高渲染性能 */
  transition: none !important; /* 禁用过渡效果 */
}

.ssh-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden; /* Prevent card content from overflowing */
  min-height: 500px; /* Ensure minimum height for the card */
  width: 0; /* Allow it to grow but start with 0 width */
  contain: layout; /* 提高渲染性能 */
  transition: none !important; /* 禁用过渡效果 */
}

.examples-sidebar {
  width: 250px;
  min-width: 200px; /* Minimum width */
  max-width: 250px; /* Maximum width */
  flex-shrink: 0; /* Prevent sidebar from shrinking */
  background-color: #f5f7fa;
  border-radius: 4px;
  border: 1px solid #e4e7ed;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.examples-header {
  padding: 10px; /* Reduce padding */
  background-color: #f0f2f5;
  border-bottom: 1px solid #e4e7ed;
  font-weight: bold;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-shrink: 0; /* Prevent header from shrinking */
}

.run-button {
  margin: 10px 15px;
}

.examples-search {
  margin: 10px;
  flex-shrink: 0; /* Prevent search from shrinking */
}

.examples-list {
  flex-grow: 1;
  overflow-y: auto;
  padding: 0 15px;
}

.example-item {
  padding: 10px 0;
  border-bottom: 1px solid #ebeef5;
  cursor: pointer;
  transition: all 0.3s;
}

.example-item:hover {
  color: #409eff;
}

.example-item.active {
  color: #409eff;
  font-weight: bold;
}

/* Make tabs container flexible */
.terminal-tabs {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 500px; /* Ensure minimum height for the tabs */
  overflow: hidden; /* Add overflow hidden to prevent content from exceeding */
  width: 100%; /* Ensure full width */
}

/* Tabs header styling */
:deep(.el-tabs__header) {
  flex-shrink: 0; /* Prevent header from shrinking */
  margin-bottom: 0; /* Remove bottom margin */
  width: 100%; /* Full width */
  overflow-x: auto; /* Allow horizontal scrolling for many tabs */
  scrollbar-width: thin; /* Firefox */
}

/* Allow horizontal scrolling in tab bar */
:deep(.el-tabs__nav-wrap) {
  overflow-x: auto !important;
  margin-bottom: 0 !important; /* Remove bottom margin */
}

/* Hide the bottom shadow/line that appears with scroll */
:deep(.el-tabs__nav-wrap::after) {
  display: none !important;
}

/* Ensure tabs don't wrap */
:deep(.el-tabs__nav) {
  white-space: nowrap !important;
  display: flex !important;
  flex-wrap: nowrap !important; /* Prevent tab wrapping */
}

/* Tab label styling */
.tab-label {
  font-size: 0.9em; /* Reduce font size slightly */
  max-width: 180px; /* Limit tab width */
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Make tab content area grow */
:deep(.el-tabs__content) {
  flex: 1;
  height: 100%; /* Use 100% instead of 0 for consistent height calculation */
  padding: 0; /* Remove default padding if needed */
  overflow: hidden; /* Prevent overflow */
  min-height: 300px; /* Ensure minimum height */
  position: relative; /* Add position relative for absolute positioning child content */
}

.terminal-tab-pane {
  height: 100%; /* Ensure pane takes full height */
  min-height: 500px; /* Ensure minimum height */
  display: flex; /* Use flex for content */
  flex-direction: column;
  overflow: hidden;
  position: relative; /* Position relative for absolute child positioning */
}

.terminal-tab-content {
  flex-grow: 1; /* Make terminal component container grow */
  min-height: 500px; /* Ensure minimum height */
  height: 100%; /* Ensure it fills the pane */
  overflow: auto; /* Change from hidden to auto to allow scrolling */
  background-color: #1e1e1e; /* Set terminal background color */
  border-radius: 0 0 4px 4px;
  position: absolute; /* Position absolutely within parent */
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  contain: strict; /* 最严格的性能优化 */
  transition: none !important; /* 禁用过渡效果 */
}

/* Ensure XTerm content can be scrolled */
:deep(.xterm-viewport) {
  overflow-y: auto !important;
}

/* Add some styling for scrollbars */
:deep(.xterm-viewport::-webkit-scrollbar),
:deep(.el-tabs__nav-wrap::-webkit-scrollbar) {
  width: 6px;
  height: 6px;
}

:deep(.xterm-viewport::-webkit-scrollbar-track),
:deep(.el-tabs__nav-wrap::-webkit-scrollbar-track) {
  background: #1e1e1e;
}

:deep(.xterm-viewport::-webkit-scrollbar-thumb),
:deep(.el-tabs__nav-wrap::-webkit-scrollbar-thumb) {
  background-color: #555;
  border-radius: 4px;
}

.no-tabs-placeholder {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #909399;
  font-size: 1em;
  text-align: left;
}

.env-info {
  margin-bottom: 2em;
  padding: 1em;
  border-radius: 8px;
  background-color: #f5f7fa;
  width: 80%;
  max-width: 300px;
}

.env-info h3 {
  color: #606266;
  margin: 0.5em 0;
  font-size: 1.1em;
  font-weight: 600;
}

.env-info p {
  margin: 0.5em 0;
  color: #606266;
}

.action-hint {
  color: #909399;
  font-size: 1.1em;
}

/* Style for label icons */
.el-icon {
  vertical-align: middle;
  margin-right: 4px;
}

.page-container {
  padding: 10px 20px; /* Reduce top/bottom padding */
  max-width: 100%;
  box-sizing: border-box;
}

.page-title {
  margin: 0;
  font-size: 1.5em; /* Slightly smaller title */
}

.dialog-footer {
  text-align: right;
}

/* Media query for smaller screens */
@media (max-width: 768px) {
  .webssh-layout {
    flex-direction: column;
  }
  
  .examples-sidebar {
    width: 100%;
    max-width: 100%;
    min-height: 150px;
    max-height: 200px;
  }
}
</style>
