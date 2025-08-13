<template>
  <div :class="embedded ? 'ttyd-embedded' : 'ttyd-view'">
    <!-- Header (hidden when embedded) -->
    <div v-if="!embedded" class="page-header">
      <h1 class="page-title">{{ $t('sidebar.ttyd') || 'ttyd Terminal' }}</h1>
      <div class="page-actions">
        <el-tooltip content="Restart ttyd Service" placement="top">
          <el-button type="primary" size="small" @click="restartTtyd" :icon="Refresh">
            {{ $t('ttyd.restart') || 'Restart Service' }}
          </el-button>
        </el-tooltip>
      </div>
    </div>

    <div :class="embedded ? 'ttyd-layout-embedded' : 'ttyd-layout'">
      <!-- Examples Sidebar (hidden when embedded) -->
      <div v-if="!embedded" class="examples-sidebar" :class="{ 'collapsed': isDataflowCollapsed }">
        <div class="examples-header" @click="toggleDataflowList">
          <span v-show="!isDataflowCollapsed" class="examples-title">Dataflows</span>
          <span v-show="isDataflowCollapsed" class="examples-title-collapsed">D</span>
          <el-icon class="collapse-icon" :class="{ 'rotated': isDataflowCollapsed }">
            <ArrowRight />
          </el-icon>
        </div>
        <div v-show="!isDataflowCollapsed" class="examples-content">
          <div class="examples-search">
            <el-input
              v-model="searchQuery"
              placeholder="Search Dataflows..."
              clearable
              @input="filterExamples"
              size="small"
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
              <el-icon class="example-icon"><Document /></el-icon>
              <span class="example-name">{{ example.name }}</span>
            </div>
            <div v-if="filteredExamples.length === 0" class="no-examples">
              <el-empty :image-size="60" description="No dataflows found" />
            </div>
          </div>
        </div>
        <!-- Collapsed state content -->
        <div v-show="isDataflowCollapsed" class="collapsed-content">
          <el-tooltip content="Click to see Dataflows List" placement="right">
            <div class="collapsed-info">
              <div class="collapsed-count">{{ filteredExamples.length }}</div>
              <div class="collapsed-label">Items</div>
            </div>
          </el-tooltip>
        </div>
      </div>
      
      <!-- Ttyd Terminal Tabs -->
      <el-card :class="['ttyd-card', embedded ? 'ttyd-card-embedded' : '']" :body-style="embedded ? {padding: '0'} : {}" :style="embedded ? 'width:100%; height:100%; min-height:0;' : ''">
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
               sandbox="allow-scripts allow-same-origin allow-forms allow-modals allow-downloads allow-popups allow-popups-to-escape-sandbox"
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
import { Loading, Monitor, QuestionFilled, Search, Refresh, ArrowRight, Document } from '@element-plus/icons-vue'

export default {
  name: 'TtydTerminal',
  props: {
    embedded: {
      type: Boolean,
      default: false
    }
  },
  components: {
    Loading,
    Monitor,
    QuestionFilled,
    Search,
    Refresh,
    ArrowRight,
    Document,
  },
  setup() {
    const props = arguments[0] // Access props in setup
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

    // 新增：Dataflows 列表折叠状态
    const isDataflowCollapsed = ref(false)
    
    // 初始化折叠状态
    const initDataflowCollapsedState = () => {
      const saved = localStorage.getItem('ttyd-dataflow-collapsed')
      if (saved) {
        isDataflowCollapsed.value = JSON.parse(saved)
      }
    }

    // 切换 Dataflows 列表折叠状态
    const toggleDataflowList = () => {
      isDataflowCollapsed.value = !isDataflowCollapsed.value
      localStorage.setItem('ttyd-dataflow-collapsed', JSON.stringify(isDataflowCollapsed.value))
    }

    // Default values for new tab form
    const newTabForm = reactive({
      title: 'Terminal',
      workingDir: '',
      command: ''
    })

    const initializeComponent = async () => {
      try {
        // 初始化 Dataflows 折叠状态
        initDataflowCollapsedState()
        
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
        
        // Fetch examples list from API (only for non-embedded mode)
        if (!props.embedded) {
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
    const selectExample = async (exampleName) => {
      selectedExample.value = exampleName;
      
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
          // Prefer custom_examples_path, fall back to examples_path
          if (settings.custom_examples_path) {
            examplesPath = settings.custom_examples_path;
          } else if (settings.examples_path) {
            examplesPath = settings.examples_path;
          } else {
            examplesPath = `${systemInfo.mofaDir}/python/examples`;
          }
          examplesPath = `${examplesPath}/${exampleName}`;
        }
        
        // Construct full command with detected file name
        const fullCommand = `cd ${examplesPath} && dora up && dora build ${dataflowFile} && dora start ${dataflowFile}`;
        
        // Copy command to clipboard
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
          examplesPath = `${systemInfo.mofaDir}/python/examples`;
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
      focusIframe,
      isDataflowCollapsed,
      toggleDataflowList
    };
  }
};
</script>

<style scoped>
.ttyd-view {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
  background-color: var(--background-color);
}

.page-header {
  margin-bottom: 16px;
  flex-shrink: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-color);
  margin: 0;
}

.page-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.ttyd-layout {
  display: flex;
  flex-grow: 1;
  gap: 16px;
  overflow: hidden;
  width: 100%;
  position: relative;
}

.ttyd-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  width: 0;
  background: var(--card-background);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  box-shadow: var(--card-shadow);
}

.ttyd-card:hover {
  box-shadow: var(--card-shadow-hover);
}

.ttyd-card :deep(.el-card__body) {
  padding: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.ttyd-card-embedded :deep(.el-card__body) {
  height: 100%;
}

.examples-sidebar {
  width: 280px;
  min-width: 250px;
  max-width: 320px;
  flex-shrink: 0;
  background: var(--card-background);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  box-shadow: var(--card-shadow);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.examples-sidebar.collapsed {
  width: 60px;
  min-width: 60px;
  max-width: 60px;
}

.examples-sidebar:hover {
  box-shadow: var(--card-shadow-hover);
}

.examples-header {
  padding: 16px 20px;
  background: linear-gradient(135deg, var(--mofa-red) 0%, var(--mofa-orange) 100%);
  color: white;
  font-weight: 600;
  font-size: 14px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  user-select: none;
  min-height: 52px;
}

.examples-sidebar.collapsed .examples-header {
  padding: 16px 8px;
  justify-content: center;
}

.examples-header:hover {
  background: linear-gradient(135deg, var(--mofa-orange) 0%, var(--mofa-red) 100%);
}

.examples-title {
  font-weight: 600;
  letter-spacing: 0.5px;
  opacity: 1;
  transition: opacity 0.2s ease;
}

.examples-title-collapsed {
  font-weight: 700;
  font-size: 16px;
  letter-spacing: 0.5px;
  color: white;
  opacity: 0.9;
}

.collapse-icon {
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  font-size: 14px;
}

.collapse-icon.rotated {
  transform: rotate(180deg);
}

.examples-sidebar.collapsed .collapse-icon {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%) rotate(180deg);
}

.examples-content {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
}

.collapsed-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 16px 8px;
}

.collapsed-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.collapsed-info:hover {
  transform: scale(1.05);
}

.collapsed-count {
  font-size: 18px;
  font-weight: 700;
  color: var(--primary-color);
  line-height: 1;
}

.collapsed-label {
  font-size: 10px;
  color: var(--text-color-secondary);
  font-weight: 500;
  text-align: center;
  opacity: 0.8;
}

.examples-search {
  padding: 16px 20px;
  flex-shrink: 0;
  border-bottom: 1px solid var(--border-color-light);
}

.examples-list {
  flex-grow: 1;
  overflow-y: auto;
  padding: 8px 0;
  max-height: calc(100% - 120px);
}

.example-item {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  border-left: 3px solid transparent;
  color: var(--text-color-secondary);
}

.example-item:hover {
  background-color: var(--border-color-light);
  color: var(--primary-color);
  border-left-color: var(--primary-color);
}

.example-item.active {
  background-color: rgba(255, 92, 72, 0.1);
  color: var(--primary-color);
  font-weight: 600;
  border-left-color: var(--primary-color);
}

.example-icon {
  margin-right: 8px;
  font-size: 14px;
  opacity: 0.7;
}

.example-name {
  font-size: 13px;
  line-height: 1.4;
}

.no-examples {
  padding: 20px;
  text-align: center;
}

/* Terminal tabs styling */
.terminal-tabs {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
  width: 100%;
  border-radius: 12px;
}

/* Tabs header styling */
:deep(.el-tabs__header) {
  flex-shrink: 0;
  margin-bottom: 0;
  width: 100%;
  overflow-x: auto;
  scrollbar-width: thin;
  background: var(--card-background);
  border-radius: 12px 12px 0 0;
}

:deep(.el-tabs__nav-wrap) {
  overflow-x: auto !important;
  margin-bottom: 0 !important;
  border-radius: 12px 12px 0 0;
}

:deep(.el-tabs__nav-wrap::after) {
  display: none !important;
}

:deep(.el-tabs__nav) {
  white-space: nowrap !important;
  display: flex !important;
  flex-wrap: nowrap !important;
}

:deep(.el-tabs__item) {
  border: none !important;
  background: transparent;
  color: var(--text-color-secondary);
  transition: all 0.3s ease;
  margin-right: 4px;
  border-radius: 8px 8px 0 0;
}

:deep(.el-tabs__item:hover) {
  color: var(--primary-color);
  background: rgba(255, 92, 72, 0.1);
}

:deep(.el-tabs__item.is-active) {
  color: var(--primary-color) !important;
  background: linear-gradient(135deg, rgba(255, 92, 72, 0.1) 0%, rgba(255, 104, 87, 0.1) 100%);
  font-weight: 600;
}

.tab-label {
  font-size: 13px;
  max-width: 180px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 6px;
}

:deep(.el-tabs__content) {
  flex: 1;
  padding: 0;
  overflow: hidden;
  position: relative;
  background: var(--card-background);
  border-radius: 0 0 12px 12px;
}

.terminal-tab-pane {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

.terminal-tab-content {
  flex-grow: 1;
  height: 100%;
  overflow: hidden;
  border-radius: 0 0 12px 12px;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: #1a1a1a;
}

/* ttyd iframe styling */
.ttyd-iframe {
  width: 100%;
  height: 100%;
  border: none;
  background-color: #1a1a1a;
  border-radius: 0 0 12px 12px;
}

.no-tabs-placeholder {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  padding: 40px 20px;
  text-align: center;
  background: var(--card-background);
  border-radius: 0 0 12px 12px;
}

.env-info {
  margin-bottom: 32px;
  padding: 24px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--border-color-light) 0%, rgba(255, 255, 255, 0.5) 100%);
  border: 1px solid var(--border-color);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  width: 100%;
  max-width: 400px;
}

.env-info h3 {
  color: var(--text-color);
  margin: 16px 0 8px 0;
  font-size: 16px;
  font-weight: 600;
}

.env-info h3:first-child {
  margin-top: 0;
}

.env-info p {
  margin: 8px 0;
  color: var(--text-color-secondary);
  font-size: 14px;
  line-height: 1.5;
}

.action-hint {
  color: var(--text-color-light);
  font-size: 14px;
  padding: 16px;
  background: rgba(255, 92, 72, 0.05);
  border: 1px dashed var(--primary-color);
  border-radius: 8px;
  max-width: 300px;
}

.form-help {
  font-size: 12px;
  color: var(--text-color-secondary);
  margin-top: 5px;
}

.dialog-footer {
  text-align: right;
}

/* Responsive design */
@media (max-width: 1024px) {
  .examples-sidebar {
    width: 260px;
    min-width: 220px;
  }
  
  .examples-sidebar.collapsed {
    width: 50px;
    min-width: 50px;
    max-width: 50px;
  }
}

@media (max-width: 768px) {
  .ttyd-layout {
    flex-direction: column;
    gap: 12px;
  }
  
  .examples-sidebar {
    width: 100%;
    max-width: 100%;
    min-height: auto;
    max-height: 300px;
    order: 2;
  }
  
  .examples-sidebar.collapsed {
    width: 100%;
    max-height: 60px;
    min-height: 60px;
  }
  
  .examples-sidebar.collapsed .examples-header {
    padding: 16px 20px;
    justify-content: space-between;
  }
  
  .examples-sidebar.collapsed .collapse-icon {
    position: static;
    transform: rotate(180deg);
  }
  
  .collapsed-tooltip {
    display: none;
  }
  
  .examples-content {
    max-height: 250px;
  }
  
  .ttyd-card {
    order: 1;
    min-height: 300px;
  }
  
  .page-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
    padding: 12px 0;
  }
  
  .page-actions {
    align-self: stretch;
  }
}

@media (max-width: 480px) {
  .page-container {
    padding: 16px;
  }
  
  .examples-sidebar {
    max-height: 200px;
  }
  
  .examples-content {
    max-height: 150px;
  }
}

/* Embedded mode styles */
.ttyd-embedded {
  width: 100%;
  height: 100%;
  background: transparent;
}

.ttyd-layout-embedded {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  gap: 0;
}

/* Dark theme specific adjustments */
[data-theme="dark"] .env-info {
  background: linear-gradient(135deg, var(--border-color) 0%, rgba(0, 0, 0, 0.3) 100%);
}

[data-theme="dark"] .action-hint {
  background: rgba(255, 92, 72, 0.08);
}

[data-theme="dark"] .example-item.active {
  background-color: rgba(255, 92, 72, 0.15);
}
</style> 