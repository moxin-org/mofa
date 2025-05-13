<template>
  <div class="page-container ttyd-view">
    <div class="page-header">
      <h1 class="page-title">{{ $t('sidebar.ttyd') || 'ttyd Terminal' }}</h1>
      <div class="page-actions">
        <el-tooltip content="Restart ttyd Service" placement="top">
          <el-button type="primary" size="small" @click="restartTtyd" :icon="Refresh">
            {{ $t('ttyd.restart') || 'Restart Service' }}
          </el-button>
        </el-tooltip>
      </div>
    </div>

    <div class="ttyd-layout">
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
      
      <!-- Ttyd Terminal Tabs -->
      <el-card class="ttyd-card">
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
               <el-icon v-if="session.status === 'connecting'"><Loading /></el-icon>
               <el-icon v-else-if="session.status === 'connected'"><Monitor /></el-icon>
               <el-icon v-else><QuestionFilled /></el-icon>
               {{ session.title }}
             </span>
           </template>
           <!-- ttyd iframe -->
           <div class="terminal-tab-content">
             <iframe 
               v-show="activeTabName === session.name" 
               :src="session.url" 
               :id="`ttyd-frame-${session.id}`" 
               class="ttyd-iframe"
               tabindex="0"
               allow="clipboard-read; clipboard-write"
               @load="handleIframeLoad(session.id)"
               @click="focusIframe(session.id)"
               @error="handleIframeError(session.id)"
             ></iframe>
          </div>
        </el-tab-pane>
      </el-tabs>
       <div v-if="sessions.length === 0" class="no-tabs-placeholder">
         <div class="env-info">
           <h3>Environment Information</h3>
           <p>Environment Type: {{ systemInfo.useSystemMofa ? 'System Installed MOFA' : 'Virtual Environment MOFA' }}</p>
           <p>MOFA Directory: {{ systemInfo.mofaDir || 'Not Set' }}</p>
           <h3>Platform Information</h3>
           <p>{{ systemInfo.platformInfo || 'Loading system information...' }}</p>
         </div>
         <div class="action-hint">
           Click the '+' button to open a new ttyd terminal tab.
         </div>
        </div>
      </el-card>
    </div>

    <!-- New Tab Dialog -->
    <el-dialog
      v-model="showNewTabDialog"
      :title="$t('ttyd.newTab') || 'New Terminal Tab'"
      width="500px"
    >
      <el-form :model="newTabForm" label-width="120px" ref="newTabFormRef">
        <el-form-item :label="$t('ttyd.tabName') || 'Tab Name'" prop="title" :rules="[{ required: true, message: 'Tab name is required', trigger: 'blur' }]">
          <el-input v-model="newTabForm.title" placeholder="Terminal" />
        </el-form-item>
        <el-form-item :label="$t('ttyd.workingDir') || 'Working Directory'">
          <el-input v-model="newTabForm.workingDir" placeholder="/path/to/directory" />
        </el-form-item>
        <el-form-item :label="$t('ttyd.command') || 'Custom Command'">
          <el-input v-model="newTabForm.command" placeholder="bash" />
          <div class="form-help">{{ $t('ttyd.commandHelp') || 'Leave empty to use the default shell' }}</div>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showNewTabDialog = false">{{ $t('common.cancel') || 'Cancel' }}</el-button>
          <el-button type="primary" @click="createNewTab">{{ $t('common.create') || 'Create' }}</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted, onBeforeUnmount, nextTick, watch, onActivated, onDeactivated } from 'vue'
import { ElMessage } from 'element-plus'
import { useSettingsStore } from '../store/settings'
import { useAgentStore } from '../store/agent'
import { Loading, Monitor, QuestionFilled, Search, Refresh } from '@element-plus/icons-vue'

export default {
  name: 'TtydTerminal',
  components: {
    Loading,
    Monitor,
    QuestionFilled,
    Search,
    Refresh,
  },
  setup() {
    const settingsStore = useSettingsStore()
    const agentStore = useAgentStore()
    const showNewTabDialog = ref(false)
    const activeTabName = ref('')
    const sessions = ref([])
    const systemInfo = reactive({
      mofaDir: '',
      platformInfo: '',
      useSystemMofa: true
    })
    const examples = ref([])
    const filteredExamples = ref([])
    const searchQuery = ref('')
    const selectedExample = ref('')
    const newTabFormRef = ref(null)
    const isInitialized = ref(false)
    const nextTabId = ref(1)

    // Default values for new tab form
    const newTabForm = reactive({
      title: 'Terminal',
      workingDir: '',
      command: ''
    })

    const initializeComponent = async () => {
      try {
        // Load settings
        await settingsStore.fetchSettings()
        const settings = settingsStore.settings
        systemInfo.mofaDir = settings.mofa_dir || 'Not Set'
        systemInfo.useSystemMofa = settings.use_system_mofa !== false

        // Check ttyd service status and start if needed
        await checkTtydService();
        
        // Get platform info
        try {
          const response = await fetch('/api/system/info')
          if (response.ok) {
            const data = await response.json()
            systemInfo.platformInfo = data.platform_info || 'Unknown platform'
          } else {
            console.error('Failed to fetch platform info:', response.statusText)
            systemInfo.platformInfo = 'Error fetching platform info'
          }
        } catch (error) {
          console.error('Error fetching platform info:', error)
          systemInfo.platformInfo = 'Error: ' + error.message
        }
        
        // Fetch examples list from API
        try {
          // Use agent store to get examples list
          await agentStore.fetchAgents()
          
          // Get example_agents from store
          const exampleAgents = agentStore.exampleAgents || []
          
          // Convert to format compatible with this component
          if (exampleAgents.length > 0) {
            examples.value = exampleAgents.map(name => {
              return {
                name: name,
                path: `${systemInfo.mofaDir}/python/examples/${name}`
              }
            })
            filteredExamples.value = examples.value
          } else {
            console.warn('No examples found from API, using fallback')
            // If API doesn't return examples, use default fallback
            examples.value = [
              { name: 'hello_world', path: `${systemInfo.mofaDir}/python/examples/hello_world` },
              { name: 'add_numbers', path: `${systemInfo.mofaDir}/python/examples/add_numbers` }
            ]
            filteredExamples.value = examples.value
          }
        } catch (error) {
          console.error('Error fetching examples:', error)
          // Use default fallback on error
          examples.value = [
            { name: 'hello_world', path: `${systemInfo.mofaDir}/python/examples/hello_world` },
            { name: 'add_numbers', path: `${systemInfo.mofaDir}/python/examples/add_numbers` }
          ]
          filteredExamples.value = examples.value
        }
        
        // Automatically open a tab when initialized
        if (sessions.value.length === 0) {
          addDefaultTab()
        }
        
        isInitialized.value = true
      } catch (error) {
        console.error('Error initializing component:', error)
        systemInfo.platformInfo = 'Error: ' + error.message
      }
    };

    // Load settings on mount
    onMounted(() => {
      initializeComponent();
    });
    
    // Handle component activation (when switching back to this view)
    onActivated(() => {
      console.log('TtydTerminal activated, sessions:', sessions.value.length);
      
      // Initialize if not already done
      if (!isInitialized.value) {
        console.log('TtydTerminal initializing for the first time');
        initializeComponent();
      } else {
        console.log('TtydTerminal already initialized, just checking service');
        // If already initialized, check ttyd service status silently
        fetch('/api/ttyd/status')
          .then(response => response.json())
          .then(data => {
            console.log('ttyd service status on activation:', data.status);
            if (data.status !== 'running') {
              // If not running, start it quietly
              console.log('ttyd service not running, starting silently');
              return fetch('/api/ttyd/start', { 
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
              });
            }
          })
          .catch(err => {
            console.error('Error checking ttyd service on activation:', err);
          });
          
        // Set a small timeout to ensure all UI elements are fully rendered
        setTimeout(() => {
          // Focus the active terminal tab
          const activeSession = sessions.value.find(s => s.name === activeTabName.value);
          if (activeSession) {
            console.log('Focusing active terminal:', activeSession.title);
            // Use multiple focus attempts with increasing delays for reliability
            focusIframe(activeSession.id);
            
            setTimeout(() => {
              focusIframe(activeSession.id);
            }, 200);
          }
        }, 100);
      }
    });
    
    // Handle component deactivation (when switching away from this view)
    onDeactivated(() => {
      console.log('TtydTerminal deactivated, sessions remaining:', sessions.value.length);
      // We don't reset or disconnect sessions here, allowing them to run in the background
      // This is similar to how WebSSH.vue handles deactivation
    });

    onBeforeUnmount(() => {
      // Only clean up when the component is truly being unmounted from the DOM
      // Not when it's just being hidden by keep-alive
      console.log('TtydTerminal unmounting, preserving active sessions');
      // We keep sessions intact to preserve state when using keep-alive
      // sessions.value = []; (commented out to preserve sessions)
    });

    // Get the base URL for ttyd service
    const getTtydBaseUrl = () => {
      const protocol = window.location.protocol;
      const hostname = window.location.hostname;
      
      // Get port from settings
      const ttydPort = settingsStore.settings.ttyd_port || 7681;
      
      return `${protocol}//${hostname}:${ttydPort}`;
    };
    
    // Check ttyd service status and start if needed
    const checkTtydService = async () => {
      try {
        // Check status
        const response = await fetch('/api/ttyd/status');
        if (!response.ok) {
          throw new Error('Failed to fetch ttyd status');
        }
        
        const data = await response.json();
        console.log('ttyd service status:', data);
        
        // If not installed, install it
        if (!data.installed) {
          ElMessage.warning('ttyd is not installed. Attempting to install...');
          await installTtyd();
          return;
        }
        
        // If not running, start it
        if (data.status !== 'running') {
          ElMessage.info('Starting ttyd service...');
          try {
            const startResponse = await fetch('/api/ttyd/start', { 
              method: 'POST',
              headers: { 'Content-Type': 'application/json' }
            });
            
            if (!startResponse.ok) {
              throw new Error('Failed to start ttyd service');
            }
            
            const startData = await startResponse.json();
            if (!startData.success) {
              // If start failed, try restarting
              ElMessage.info('Start failed, trying to restart ttyd service...');
              await restartTtyd();
            }
          } catch (e) {
            console.error('Error starting ttyd:', e);
            ElMessage.info('Restarting ttyd service...');
            await restartTtyd();
          }
        } else {
          console.log(`ttyd is running on port ${data.port}`);
          // Even if running, try restarting if we have empty tabs
          if (sessions.value.length > 0 && sessions.value.some(s => s.status === 'error')) {
            console.log('Some sessions have errors, trying to restart ttyd...');
            await restartTtyd();
          }
        }
      } catch (error) {
        console.error('Failed to check ttyd service:', error);
        ElMessage.error('Failed to check ttyd service. Check the console for details.');
      }
    };
    
    // Install ttyd
    const installTtyd = async () => {
      try {
        const response = await fetch('/api/ttyd/install', { 
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        });
        
        if (!response.ok) {
          throw new Error('Failed to install ttyd');
        }
        
        const data = await response.json();
        if (data.success) {
          ElMessage.success('ttyd installed successfully.');
          await startTtyd();
        } else {
          throw new Error(data.message || 'Unknown error during installation');
        }
      } catch (error) {
        console.error('Failed to install ttyd:', error);
        ElMessage.error('Failed to install ttyd. Check the console for details.');
      }
    };
    
    // Start ttyd service
    const startTtyd = async () => {
      try {
        const response = await fetch('/api/ttyd/start', { 
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        });
        
        if (!response.ok) {
          throw new Error('Failed to start ttyd service');
        }
        
        const data = await response.json();
        if (data.success) {
          ElMessage.success('ttyd service started successfully.');
        } else {
          throw new Error(data.message || 'Unknown error starting service');
        }
      } catch (error) {
        console.error('Failed to start ttyd service:', error);
        ElMessage.error('Failed to start ttyd service. Check the console for details.');
      }
    };
    
    // Restart ttyd service
    const restartTtyd = async () => {
      try {
        const response = await fetch('/api/ttyd/restart', { 
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        });
        
        if (!response.ok) {
          throw new Error('Failed to restart ttyd service');
        }
        
        const data = await response.json();
        if (data.success) {
          ElMessage.success('ttyd service restarted successfully.');
          
          const baseUrl = getTtydBaseUrl();
          
          // Only refresh sessions that are in error state or disconnected
          sessions.value.forEach(session => {
            if (session.status === 'error' || session.status === 'disconnected') {
              session.status = 'connecting';
              // Update with a timestamp to force iframe refresh
              session.url = `${baseUrl}?t=${Date.now()}`; 
            }
          });
          
          // After a short delay, try to focus the active tab
          setTimeout(() => {
            const activeSession = sessions.value.find(s => s.name === activeTabName.value);
            if (activeSession) {
              focusIframe(activeSession.id);
            }
          }, 1000);
        } else {
          throw new Error(data.message || 'Unknown error restarting service');
        }
      } catch (error) {
        console.error('Failed to restart ttyd service:', error);
        ElMessage.error('Failed to restart ttyd service. Check the console for details.');
      }
    };

    // Add a default tab with default settings
    const addDefaultTab = () => {
      const newId = nextTabId.value++;
      const newName = `tab-${newId}`;
      const baseUrl = getTtydBaseUrl();
      
      const newSession = {
        id: newId,
        name: newName,
        title: `Terminal ${newId}`,
        url: baseUrl,
        status: 'connecting',
      };

      sessions.value.push(newSession);
      activeTabName.value = newName;
    };

    // Handle adding a new tab with custom settings
    const handleTabAdd = () => {
      // Skip the dialog and create a default tab directly
      addDefaultTab();
      
      // Previous code commented out:
      /*
      // Initialize form with default values
      newTabForm.title = 'Terminal';
      newTabForm.workingDir = '';
      newTabForm.command = '';
      
      // Show dialog to configure new tab
      showNewTabDialog.value = true;
      */
    };

    // Create a new tab with configured settings
    const createNewTab = async () => {
      if (!newTabFormRef.value) return;
      
      try {
        await newTabFormRef.value.validate();
        
        const newId = nextTabId.value++;
        const newName = `tab-${newId}`;
        let baseUrl = getTtydBaseUrl();
        
        // Append query parameters for custom settings
        const queryParams = new URLSearchParams();
        
        if (newTabForm.workingDir) {
          queryParams.append('cwd', newTabForm.workingDir);
        }
        
        if (newTabForm.command) {
          // The command needs to be properly handled by the backend
          queryParams.append('cmd', newTabForm.command);
        }
        
        const queryString = queryParams.toString();
        const url = queryString ? `${baseUrl}?${queryString}` : baseUrl;
        
        const newSession = {
          id: newId,
          name: newName,
          title: newTabForm.title,
          url: url,
          status: 'connecting',
        };

        sessions.value.push(newSession);
        activeTabName.value = newName;
        showNewTabDialog.value = false;
        
      } catch (validationError) {
        console.log('Form validation failed:', validationError);
        ElMessage.error('Please fill in all required fields.');
      }
    };

    // Handle tab removal
    const handleTabRemove = (targetName) => {
      const sessionIndex = sessions.value.findIndex(s => s.name === targetName);
      if (sessionIndex === -1) return;

      // Remove the session from the list
      sessions.value.splice(sessionIndex, 1);

      // If the closed tab was the active one, activate the next/previous tab
      if (activeTabName.value === targetName) {
        const nextTab = sessions.value[sessionIndex] || sessions.value[sessionIndex - 1];
        activeTabName.value = nextTab ? nextTab.name : '';
      }
    };
    
    // Handle tab change
    const handleTabChange = (newTabName) => {
      // Update active tab name
      activeTabName.value = newTabName;
      
      // Add focus to the iframe after a short delay to ensure it's visible
      nextTick(() => {
        const activeSession = sessions.value.find(s => s.name === newTabName);
        if (activeSession) {
          focusIframe(activeSession.id);
        }
      });
    };

    // Handle iframe load event
    const handleIframeLoad = (sessionId) => {
      const session = sessions.value.find(s => s.id === sessionId);
      if (session) {
        session.status = 'connected';
        
        // Focus the iframe once it's loaded - use the focusIframe method for consistency
        if (activeTabName.value === session.name) {
          // Add a short delay to ensure the iframe content is fully loaded
          setTimeout(() => {
            focusIframe(sessionId);
          }, 500);
        }
      }
    };

    // Handle iframe loading error
    const handleIframeError = (sessionId) => {
      console.error(`Iframe ${sessionId} encountered an error loading`);
      const session = sessions.value.find(s => s.id === sessionId);
      if (session) {
        session.status = 'error';
        
        // Try to reconnect after a short delay
        setTimeout(() => {
          console.log(`Attempting to reconnect iframe ${sessionId}...`);
          // Update URL with timestamp to force reload
          session.url = `${getTtydBaseUrl()}?reconnect=${Date.now()}`;
          session.status = 'connecting';
        }, 2000);
      }
    };

    // Select an example from the sidebar and copy command to clipboard
    const selectExample = (exampleName) => {
      selectedExample.value = exampleName;
      
      // Get examples path from settings
      const settings = settingsStore.settings;
      let examplesPath = '';
      
      // Prefer custom_examples_path, fall back to examples_path
      if (settings.custom_examples_path) {
        examplesPath = settings.custom_examples_path;
      } else if (settings.examples_path) {
        examplesPath = settings.examples_path;
      } else {
        examplesPath = `${systemInfo.mofaDir}/python/examples`;
      }
      
      // Construct full command
      const fullCommand = `cd ${examplesPath}/${exampleName} && dora up && dora build ${exampleName}_dataflow.yml && dora start ${exampleName}_dataflow.yml`;
      
      // Copy command to clipboard
      navigator.clipboard.writeText(fullCommand)
        .then(() => {
          ElMessage.success(`Command Copied to clipboard`);
        })
        .catch(err => {
          console.error('Failed to copy text: ', err);
          ElMessage.error('Copy Failed');
        });
    };
    
    // Filter examples based on search query
    const filterExamples = () => {
      if (!searchQuery.value) {
        filteredExamples.value = examples.value;
      } else {
        const query = searchQuery.value.toLowerCase();
        filteredExamples.value = examples.value.filter(example => 
          example.name.toLowerCase().includes(query)
        );
      }
    };

    // Add a new method to handle iframe focus specifically
    const focusIframe = (sessionId) => {
      const iframeElement = document.getElementById(`ttyd-frame-${sessionId}`);
      if (iframeElement) {
        // Force focus to the iframe and prevent default events
        iframeElement.focus({preventScroll: false});
        
        // Dispatch a focus event to ensure the ttyd terminal inside knows it has focus
        try {
          iframeElement.contentWindow.focus();
          
          // Try to send a click event to wake up the terminal
          if (iframeElement.contentDocument) {
            const clickEvent = new MouseEvent('click', {
              bubbles: true,
              cancelable: true,
              view: window
            });
            iframeElement.contentDocument.dispatchEvent(clickEvent);
          }
        } catch (e) {
          console.log('Could not focus iframe content window:', e);
        }
      }
    };

    return {
      showNewTabDialog,
      newTabForm,
      newTabFormRef,
      sessions,
      activeTabName,
      systemInfo,
      examples,
      filteredExamples,
      searchQuery,
      selectedExample,
      handleTabAdd,
      handleTabRemove,
      handleTabChange,
      handleIframeLoad,
      handleIframeError,
      createNewTab,
      selectExample,
      filterExamples,
      checkTtydService,
      restartTtyd,
      focusIframe
    };
  }
};
</script>

<style scoped>
.ttyd-view {
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
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: none !important; /* 禁用过渡效果 */
}

.ttyd-layout {
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

.ttyd-card {
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
  overflow: hidden; /* Prevent scrolling outside the iframe */
  border-radius: 0 0 4px 4px;
  position: absolute; /* Position absolutely within parent */
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

/* ttyd iframe styling */
.ttyd-iframe {
  width: 100%;
  height: 100%;
  border: none;
  background-color: #1e1e1e;
  contain: strict; /* 最严格的性能优化 */
  transition: none !important; /* 禁用过渡效果 */
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

.form-help {
  font-size: 12px;
  color: var(--text-color-secondary);
  margin-top: 5px;
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

.page-actions {
  display: flex;
  gap: 10px;
}

/* Media query for smaller screens */
@media (max-width: 768px) {
  .ttyd-layout {
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