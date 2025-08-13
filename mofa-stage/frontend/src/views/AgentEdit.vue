<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <el-button @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
        </el-button>
        <h1 class="page-title">{{ agentName }}</h1>
        <el-tag v-if="isAgentRunning" type="success">运行中</el-tag>
      </div>
      
      <div class="header-actions">
        <el-button-group>
          <el-button 
            v-if="useNewEditor && vscodeStatus.running" 
            @click="installExtensions" 
            type="success" 
            size="small">
            <el-icon><Download /></el-icon>
            扩展
          </el-button>
          <el-button 
            v-if="useNewEditor && vscodeStatus.running" 
            @click="updateVSCodeConfig" 
            type="info" 
            size="small">
            <el-icon><Setting /></el-icon>
            配置
          </el-button>
          <el-button class="custom-save-btn" @click="saveCurrentFile" :disabled="!hasChanges" :loading="isSaving">
            <el-icon><Document /></el-icon>
            Save
          </el-button>
          <el-button v-if="!isAgentRunning" class="custom-run-btn" @click="runAgent">
            <el-icon><VideoPlay /></el-icon>
            Run
          </el-button>
          <el-button v-else type="danger" @click="stopAgent">
            <el-icon><VideoPause /></el-icon>
            Stop
          </el-button>
        </el-button-group>
      </div>
    </div>

    <!-- 加载中 -->
    <el-card v-if="isLoading" class="loading-container">
      <el-skeleton :rows="10" animated />
    </el-card>

    <!-- 主编辑区 -->
    <div v-else>
      <!-- 新版编辑器 - VS Code Web 嵌入 -->
      <div v-if="useNewEditor" class="vscode-full-container">
        <div v-if="vscodeStatus.loading" class="vscode-loading">
          <div v-loading="true" element-loading-text="正在启动 VS Code Web..." class="loading-container">
          </div>
        </div>
        <div v-else-if="vscodeStatus.error" class="vscode-error">
          <el-alert
            title="VS Code Web 启动失败"
            type="error"
            :description="vscodeStatus.error"
            show-icon
          />
          <el-button @click="startVSCodeServer" type="primary" style="margin-top: 10px;">
            重试启动
          </el-button>
        </div>
        <VSCodeEmbed 
          v-else-if="vscodeStatus.running"
          :folder-path="agentFolderPath" 
          :vscode-base-url="vscodeBaseUrl" 
        />
        <div v-else class="vscode-starting">
          <el-empty description="正在准备 VS Code Web...">
            <el-button @click="startVSCodeServer" type="primary">
              启动 VS Code
            </el-button>
            <el-button @click="installExtensions" type="success" style="margin-left: 10px;">
              安装推荐扩展
            </el-button>
            <el-button @click="updateVSCodeConfig" type="info" style="margin-left: 10px;">
              更新配置
            </el-button>
          </el-empty>
        </div>
      </div>
      <!-- 经典编辑器 -->
      <div v-else class="edit-container">
        <!-- 文件树侧边栏 -->
        <div v-if="!useNewEditor" class="file-tree-sidebar" :style="{ width: fileSidebarWidth + 'px' }">
          <div class="file-tree-resize-handle" @mousedown="startResizeFileSidebar"></div>
          <div class="sidebar-header">
            <h3>文件列表</h3>
            <el-input
              placeholder="搜索文件"
              v-model="fileSearchQuery"
              prefix-icon="Search"
              clearable
              size="small"
            />
          </div>
          
          <div class="file-tree-wrapper" ref="fileTreeWrapper" @scroll="rememberFileTreeScroll">
            <el-tree
              :data="fileTreeData"
              :props="defaultProps"
              :filter-node-method="filterNode"
              @node-click="handleFileClick"
              ref="fileTree"
              default-expand-all
              highlight-current
            />
          </div>

          <div class="sidebar-footer">
            <el-button size="small" @click="addNewFile" icon="Plus">Create New File</el-button>
          </div>
        </div>

        <!-- 编辑器区域 -->
        <div class="editor-area">
          <div v-if="currentFile" class="editor-container">
            <div class="editor-header">
              <div class="file-path">{{ currentFile.path }}</div>
              <div class="file-actions">
                <el-button-group>
                  <el-button 
                    size="small" 
                    @click="saveCurrentFile" 
                    :disabled="!hasChanges"
                    :loading="isSaving">
                    保存
                  </el-button>
                </el-button-group>
              </div>
            </div>

            <!-- 代码编辑器/预览 -->
            <div class="editor-content">
              <div class="code-editor-wrapper">
                <!-- 对于 dataflow YAML，使用 Tab 形式同时展示代码与图形 -->
                <template v-if="showYamlTabs && isDataflowYaml">
                  <el-tabs v-model="activeYamlTab" type="border-card" class="yaml-preview-tabs" >
                    <el-tab-pane label="YAML" name="yaml">
                      <!-- 根据设置选择编辑器版本 -->
                      <CodeEditor
                        v-if="!useNewEditor"
                        v-model="editorContent"
                        :language="editorLanguage"
                        @save="saveCurrentFile"
                        ref="codeEditorRef"
                      />
                      <div v-else class="new-editor-placeholder">
                        <el-empty description="请选择文件或切换到新版编辑器" />
                      </div>
                    </el-tab-pane>
                    <el-tab-pane label="Graph" name="graph">
                      <MermaidViewer :code="mermaidCode" @node-click="handleMermaidNodeClick" />
                    </el-tab-pane>
                  </el-tabs>
                </template>

                <!-- 其他文件类型沿用原先的预览/编辑器切换逻辑 -->
                <template v-else>
                  <template v-if="previewMode">
                    <!-- Markdown 文件预览 -->
                    <div v-if="isMarkdownFile" class="markdown-preview" v-html="renderedMarkdown"></div>
                    <!-- Dataflow YAML -> Mermaid 预览 -->
                    <MermaidViewer v-else-if="isDataflowYaml" :code="mermaidCode" @node-click="handleMermaidNodeClick" />
                    <!-- Mermaid HTML 预览 -->
                    <iframe v-else-if="isMermaidHtml" class="mermaid-html-preview" :srcdoc="editorContent" />
                    <!-- 其他文件暂不支持预览 -->
                    <div v-else class="empty-preview"></div>
                  </template>
                  <template v-else>
                    <!-- 根据设置选择编辑器版本 -->
                    <CodeEditor
                      v-if="!useNewEditor"
                      v-model="editorContent"
                      :language="editorLanguage"
                      @save="saveCurrentFile"
                      ref="codeEditorRef"
                    />
                    <div v-else class="new-editor-placeholder">
                      <el-empty description="请选择文件或切换到新版编辑器" />
                    </div>
                  </template>
                </template>
              </div>
              <!-- 底部折叠终端面板 -->
              <div class="terminal-collapse-container">
                <div class="terminal-collapse-header" @click="showTerminal = !showTerminal">
                  <div class="collapse-header-content">
                    <el-icon class="collapse-icon" :class="{ 'collapsed': !showTerminal }">
                      <ArrowUp />
                    </el-icon>
                    <span class="collapse-title">Terminal</span>
                    <div class="terminal-status" v-if="showTerminal">
                      <span class="status-dot connected"></span>
                      <span class="status-text">Connected</span>
                    </div>
                  </div>
                </div>
                <div v-show="showTerminal" class="terminal-panel" :style="{ height: terminalHeight + 'px' }">
                  <div class="terminal-resize-handle" @mousedown="startResizeTerminal"></div>
                  <keep-alive>
                    <TtydTerminal :embedded="true" />
                  </keep-alive>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="empty-editor">
            <el-empty description="Please select a file or create a new file">
              <el-button @click="addNewFile" type="primary">Create New File</el-button>
            </el-empty>
          </div>
        </div>

                 <!-- HTML 预览窄栏 -->
         <div v-if="!useNewEditor && isDataflowYaml" class="mermaid-toggle-bar" @click="toggleMermaidSidebar" :title="showMermaidSidebar ? '关闭 HTML 预览' : '打开 HTML 预览'">
           <el-icon class="mermaid-icon" :class="{ 'expanded': showMermaidSidebar }">
             <Promotion />
           </el-icon>
         </div>
        
        <!-- Mermaid 预览面板 -->
        <div v-if="!useNewEditor && isDataflowYaml && showMermaidSidebar" class="mermaid-preview-sidebar" :style="{ width: mermaidSidebarWidth + 'px' }">
           <div class="mermaid-resize-handle" @mousedown="startResizeMermaid"></div>
                     <div class="mermaid-sidebar-header">
             <h4>数据流图</h4>
             <div class="mermaid-toolbar">
               <el-tooltip content="放大" placement="top">
                 <el-button size="small" text @click="zoomIn"><el-icon><Plus /></el-icon></el-button>
               </el-tooltip>
               <el-tooltip content="缩小" placement="top">
                 <el-button size="small" text @click="zoomOut"><el-icon><Minus /></el-icon></el-button>
               </el-tooltip>
               <el-tooltip content="重置" placement="top">
                 <el-button size="small" text @click="resetZoom"><el-icon><Refresh /></el-icon></el-button>
               </el-tooltip>
               <el-tooltip content="新标签页打开" placement="top">
                 <el-button size="small" text @click="openMermaidInNewTab"><el-icon><Document /></el-icon></el-button>
               </el-tooltip>
               <el-tooltip content="关闭" placement="top">
                 <el-button size="small" text @click="toggleMermaidSidebar"><el-icon><Close /></el-icon></el-button>
               </el-tooltip>
             </div>
           </div>
          
          <div v-if="mermaidHtmlFiles.length > 1" class="mermaid-file-selector">
            <el-select v-model="selectedMermaidHtml" @change="loadMermaidContent" size="small" style="width: 100%">
              <el-option 
                v-for="file in mermaidHtmlFiles" 
                :key="file" 
                :label="file.split('/').pop()" 
                :value="file" 
              />
            </el-select>
          </div>
          
          <div class="mermaid-preview-content">
            <div v-if="loadingMermaidContent" v-loading="true" class="mermaid-loading">
              加载中...
            </div>
            <div v-else-if="mermaidHtmlContent"
                 class="mermaid-zoom-wrapper"
                 :style="{ transform: `scale(${zoomLevel})`, transformOrigin: 'top left' }">
              <iframe class="mermaid-content-iframe" :srcdoc="mermaidHtmlContent" />
            </div>
                         <div v-else class="mermaid-empty">
               <el-empty description="未找到 HTML 文件" size="small" />
             </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 新建文件对话框 -->
    <el-dialog v-model="newFileDialogVisible" title="Create New File" width="30%">
      <el-form :model="newFileForm" label-width="80px">
        <el-form-item label="File Name" required>
          <el-input v-model="newFileForm.fullName" placeholder="Example: helper.py">
          </el-input>
        </el-form-item>
        <el-form-item label="Directory">
          <el-input v-model="newFileForm.path" placeholder="Leave blank for root directory" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="newFileDialogVisible = false">Cancel</el-button>
          <el-button type="primary" @click="createNewFile" :loading="isCreatingFile">
            Create
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts">
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAgentStore } from '../store/agent'
import { useSettingsStore } from '../store/settings'
import CodeEditor from '../components/editor/CodeEditor.vue'
import { Document, ArrowLeft, VideoPlay, VideoPause, Search, Plus, Minus, Refresh, Download, Setting, ArrowUp, Promotion, Close } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import MarkdownIt from 'markdown-it'
import MermaidViewer from '../components/MermaidViewer.vue'
import VSCodeEmbed from '../components/editor/VSCodeEmbed.vue'
import vscodeApi from '../api/vscode'
import TtydTerminal from './TtydTerminal.vue'

export default {
  name: 'AgentEdit',
  components: {
    CodeEditor,
    Document,
    ArrowLeft,
    VideoPlay,
    VideoPause,
    Search,
    Plus,
    Minus,
    Refresh,
    Download,
    Setting,
    ArrowUp,
    Promotion,
    Close,
    MermaidViewer,
    VSCodeEmbed,
    TtydTerminal
  },
  props: {
    agentName: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const router = useRouter()
    const route = useRoute()
    const agentStore = useAgentStore()
    const settingsStore = useSettingsStore()
    const md = new MarkdownIt()

    // 状态变量
    const isLoading = computed(() => agentStore.isLoading)
    const error = computed(() => agentStore.error)
    const fileTree = ref(null)
    const fileSearchQuery = ref('')
    const fileTreeData = ref([])
    const currentFile = ref(null)
    const originalContent = ref('')
    const editorContent = ref('')
    const hasChanges = computed(() => editorContent.value !== originalContent.value)
    const isSaving = ref(false)
    const previewMode = ref(false)
    const activeYamlTab = ref('yaml')
    const showYamlTabs = ref(false)
    const isAgentRunning = computed(() => agentStore.isAgentRunning(props.agentName))
    
    // 是否使用新版编辑器
    const useNewEditor = computed(() => settingsStore.settings.editor_version === 'new')

    // 新建文件相关
    const newFileDialogVisible = ref(false)
    const newFileForm = ref({
      fullName: '',
      path: ''
    })
    const isCreatingFile = ref(false)

    // 计算属性
    const defaultProps = {
      children: 'children',
      label: 'label'
    }

    const editorLanguage = computed(() => {
      if (!currentFile.value) return 'python'
      
      const ext = currentFile.value.path.split('.').pop().toLowerCase()
      const langMap = {
        'py': 'python',
        'js': 'javascript',
        'md': 'markdown',
        'yml': 'yaml',
        'yaml': 'yaml',
        'json': 'json',
        'toml': 'toml',
        'env': 'plaintext',
        'txt': 'plaintext'
      }
      return langMap[ext] || 'plaintext'
    })
    
    const isMarkdownFile = computed(() => {
      if (!currentFile.value) return false
      return currentFile.value.path.toLowerCase().endsWith('.md')
    })
    
    const renderedMarkdown = computed(() => {
      return md.render(editorContent.value || '')
    })

    const isYaml = computed(() => currentFile.value && (currentFile.value.path.endsWith('.yml') || currentFile.value.path.endsWith('.yaml')))
    const isDataflowYaml = computed(() => {
      if (!isYaml.value) return false
      const pathMatch = currentFile.value.path.includes('dataflow')
      const contentMatch = editorContent.value && editorContent.value.trimStart().startsWith('nodes:')
      return pathMatch || contentMatch
    })
    const mermaidCode = ref('')
    // 新增：是否为 Mermaid HTML
    const isMermaidHtml = computed(() => {
      if (!currentFile.value) return false
      const lowerPath = currentFile.value.path.toLowerCase()
      return lowerPath.endsWith('.html') && lowerPath.includes('graph')
    })

    // 计算 VSCode Web 需要打开的文件夹路径
    const agentFolderPath = computed(() => {
      let baseDir = settingsStore.settings.mofa_dir || ''
      const name = props.agentName
      // 判断 Agent 类型（hub / examples）
      if (agentStore.hubAgents.includes(name)) {
        baseDir = settingsStore.settings.agent_hub_path || baseDir
      } else if (agentStore.exampleAgents.includes(name)) {
        baseDir = settingsStore.settings.examples_path || baseDir
      }
      // 去除尾部斜杠
      const trimmed = baseDir.replace(/\/$/, '')
      return `${trimmed}/${name}`
    })

    const vscodePort = ref(null)

    const vscodeBaseUrl = computed(() => {
       // 使用动态端口优先
       if (vscodePort.value) {
         const host = window.location.hostname || 'localhost'
         const protocol = window.location.protocol || 'http:'
         return `${protocol}//${host}:${vscodePort.value}`
       }
       // 使用集成的 code-server，默认端口 8080
       const envUrl = import.meta.env.VITE_VSCODE_WEB_URL
       if (envUrl) return envUrl

       const envPort = import.meta.env.VITE_VSCODE_WEB_PORT || '8080'
       const host = window.location.hostname || 'localhost'
       const protocol = window.location.protocol || 'http:'
       return `${protocol}//${host}:${envPort}`
     })

    // VS Code 状态管理
    const vscodeStatus = ref({
      running: false,
      loading: false,
      error: null
    })

    // 新增：终端高度和 Mermaid 侧栏宽度，可拖拽调整
    const terminalHeight = ref(350)
    const mermaidSidebarWidth = ref(300)
    // 新增：文件树侧边栏宽度
    const fileSidebarWidth = ref(250)

    // 启动 VS Code 服务
    const startVSCodeServer = async () => {
      vscodeStatus.value.loading = true
      vscodeStatus.value.error = null
      
      try {
        const result = await vscodeApi.startVSCode(props.agentName)
        if (result.success) {
          vscodeStatus.value.running = true
          vscodePort.value = result.port || 8080
          ElMessage.success('VS Code Web 启动成功')
        } else {
          vscodeStatus.value.error = result.error
          ElMessage.error(`启动失败: ${result.error}`)
        }
      } catch (error) {
        vscodeStatus.value.error = error.message
        ElMessage.error(`启动失败: ${error.message}`)
      } finally {
        vscodeStatus.value.loading = false
      }
    }

    // 检查 VS Code 状态
    const checkVSCodeStatus = async () => {
      try {
        const result = await vscodeApi.getVSCodeStatus()
        if (result.success) {
          vscodeStatus.value.running = result.running
          if (result.port) vscodePort.value = result.port
        }
      } catch (error) {
        console.warn('Failed to check VS Code status:', error)
      }
    }

    // 安装推荐扩展
    const installExtensions = async () => {
      ElMessage.info('正在安装 VS Code 扩展...')
      try {
        const result = await vscodeApi.installExtensions(props.agentName)
        if (result.success) {
          ElMessage.success(`扩展安装完成: ${result.installed.length} 个成功, ${result.failed.length} 个失败`)
        } else {
          ElMessage.error(`扩展安装失败: ${result.error}`)
        }
      } catch (error) {
        ElMessage.error(`扩展安装失败: ${error.message}`)
      }
    }

    // 更新 VS Code 配置
    const updateVSCodeConfig = async () => {
      try {
        const result = await vscodeApi.updateConfig(props.agentName)
        if (result.success) {
          ElMessage.success('VS Code 配置已更新')
        } else {
          ElMessage.error(`配置更新失败: ${result.error}`)
        }
      } catch (error) {
        ElMessage.error(`配置更新失败: ${error.message}`)
      }
    }

    watch(editorContent, async (newVal) => {
      if (isDataflowYaml.value) {
        // call backend to generate mermaid
        try {
          const resp = await fetch('/api/mermaid/preview', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ yaml: newVal })
          })
          const data = await resp.json()
          if (data.success) mermaidCode.value = data.mermaid
        } catch (e) { }
      }
    }, { immediate: true })

    // 方法
    const goBack = () => {
      // 如果有未保存的更改，提示保存
      if (hasChanges.value) {
        ElMessageBox.confirm(
          '有未保存的更改，是否保存后再离开？',
          '未保存的更改',
          {
            confirmButtonText: '保存并离开',
            cancelButtonText: '放弃更改',
            type: 'warning',
            distinguishCancelAndClose: true
          }
        )
          .then(async () => {
            await saveCurrentFile()
            router.push('/agents')
          })
          .catch((action) => {
            if (action === 'cancel') {
              router.push('/agents')
            }
          })
      } else {
        router.push('/agents')
      }
    }

    const loadAgentFiles = async () => {
      try {
        const files = await agentStore.fetchAgentFiles(props.agentName)
        generateFileTree(files)
      } catch (err) {
        ElMessage.error(`Failed to load Agent files: ${err.message}`)
      }
    }

    const generateFileTree = (files) => {
      const treeData = []
      const fileMap = {}
      
      // 创建根目录节点
      fileMap[''] = {
        label: props.agentName,
        path: '',
        children: [],
        isDirectory: true
      }
      treeData.push(fileMap[''])
      
      // 处理每个文件
      files.forEach(file => {
        const pathParts = file.path.split('/')
        const fileName = pathParts.pop()
        const dirPath = pathParts.join('/')
        
        // 确保目录路径存在
        if (dirPath && !fileMap[dirPath]) {
          // 创建缺失的目录路径
          let currentPath = ''
          pathParts.forEach(part => {
            const prevPath = currentPath
            currentPath = currentPath ? `${currentPath}/${part}` : part
            
            if (!fileMap[currentPath]) {
              const dirNode = {
                label: part,
                path: currentPath,
                children: [],
                isDirectory: true
              }
              fileMap[currentPath] = dirNode
              
              if (prevPath) {
                fileMap[prevPath].children.push(dirNode)
              } else {
                fileMap[''].children.push(dirNode)
              }
            }
          })
        }
        
        // 创建文件节点
        const fileNode = {
          label: fileName,
          path: file.path,
          isDirectory: false,
          fileType: file.type
        }
        
        // 添加到父目录
        const parentDir = fileMap[dirPath] || fileMap['']
        parentDir.children.push(fileNode)
      })
      
      // 排序 - 目录在前，文件在后，按字母排序
      const sortNodes = (nodes) => {
        nodes.sort((a, b) => {
          if (a.isDirectory && !b.isDirectory) return -1
          if (!a.isDirectory && b.isDirectory) return 1
          return a.label.localeCompare(b.label)
        })
        
        nodes.forEach(node => {
          if (node.children) {
            sortNodes(node.children)
          }
        })
      }
      
      sortNodes(treeData)
      fileTreeData.value = treeData
    }

    const fileTreeWrapper = ref(null)
    const fileTreeScrollTop = ref(0)

    const rememberFileTreeScroll = () => {
      if (fileTreeWrapper.value) {
        fileTreeScrollTop.value = fileTreeWrapper.value.scrollTop
      }
    }

    const restoreFileTreeScroll = () => {
      nextTick(() => {
        if (fileTreeWrapper.value) {
          fileTreeWrapper.value.scrollTop = fileTreeScrollTop.value
        }
      })
    }

    const handleFileClick = async (data) => {
      if (data.isDirectory) return
      
      // 如果当前有未保存的更改，提示保存
      if (currentFile.value && hasChanges.value) {
        try {
          await ElMessageBox.confirm(
            '有未保存的更改，是否保存？',
            '未保存的更改',
            {
              confirmButtonText: '保存',
              cancelButtonText: '放弃更改',
              type: 'warning'
            }
          )
          await saveCurrentFile()
        } catch (e) {
          // 用户选择放弃更改，继续打开新文件
        }
      }
      
      await loadFileContent(data.path)
      restoreFileTreeScroll()
    }

    const loadFileContent = async (filePath) => {
      try {
        const fileData = await agentStore.fetchFileContent(props.agentName, filePath)
        if (fileData) {
          currentFile.value = {
            path: filePath,
            type: fileData.type
          }
          originalContent.value = fileData.content
          editorContent.value = fileData.content
          // 如果是 Mermaid HTML，则自动进入预览模式
          previewMode.value = isMermaidHtml.value
        }
      } catch (err) {
        ElMessage.error(`Failed to load file content: ${err.message}`)
      }
    }

    const saveCurrentFile = async () => {
      if (!currentFile.value || !hasChanges.value) return
      
      isSaving.value = true
      try {
        const result = await agentStore.saveFileContent(
          props.agentName,
          currentFile.value.path,
          editorContent.value
        )
        
        if (result) {
          originalContent.value = editorContent.value
          ElMessage.success('File saved successfully')

          // 如果是 dataflow YAML，调用后端导出 HTML
          if (isDataflowYaml.value) {
            try {
              const resp = await fetch('/api/mermaid/export', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                  agent: props.agentName,
                  yaml_path: currentFile.value.path,
                  yaml: editorContent.value
                })
              })
              const data = await resp.json()
              if (data.success) {
                ElMessage.success('Mermaid HTML 生成成功: ' + data.html_path)
                // 刷新 mermaidHtmlFiles，下次侧边栏可见
                scanMermaidHtmlFiles()
                await loadAgentFiles()
              } else {
                console.warn('Mermaid export failed', data)
              }
            } catch (e) {
              console.error('Mermaid export error', e)
            }
          }
        } else {
          ElMessage.error(`Failed to save file: ${error.value}`)
        }
      } catch (err) {
        ElMessage.error(`Failed to save file: ${err.message}`)
      } finally {
        isSaving.value = false
      }
    }

    const togglePreviewMode = () => {
      previewMode.value = !previewMode.value
    }

    const filterNode = (value, data) => {
      if (!value) return true
      return data.label.toLowerCase().includes(value.toLowerCase())
    }

    const addNewFile = () => {
      newFileForm.value = {
        fullName: '',
        path: ''
      }
      newFileDialogVisible.value = true
    }

    const createNewFile = async () => {
      if (!newFileForm.value.fullName.trim()) {
        ElMessage.warning('Please enter a file name')
        return
      }
      
      isCreatingFile.value = true
      try {
        const filePath = newFileForm.value.path 
          ? `${newFileForm.value.path}/${newFileForm.value.fullName}`
          : newFileForm.value.fullName
        
        // Extract file extension for default content
        const fileNameParts = newFileForm.value.fullName.split('.')
        const ext = fileNameParts.length > 1 ? fileNameParts.pop().toLowerCase() : ''
        const fileName = fileNameParts.join('.')
        
        // 创建默认内容
        let defaultContent = ''
          
        switch (ext) {
          case 'py':
            defaultContent = `# ${fileName}.py\n# Created in MoFA_Stage\n\ndef main():\n    print("Hello from ${fileName}")\n\nif __name__ == "__main__":\n    main()\n`
            break
          case 'md':
            defaultContent = `# ${fileName}\n\n## Overview\n\nThis is a new file created in MoFA_Stage.\n`
            break
          case 'yml':
          case 'yaml':
            defaultContent = `# ${fileName}.${ext}\n# Configuration file\n\nname: ${props.agentName}\n`
            break
          case 'env':
            defaultContent = `# Environment variables for ${props.agentName}\n\nDEBUG=True\n`
            break
          case 'json':
            defaultContent = `{\n  "name": "${props.agentName}",\n  "description": "A MoFA agent",\n  "version": "1.0.0",\n  "created": "${new Date().toISOString()}"\n}\n`
            break
          case 'js':
            defaultContent = `// ${fileName}.js\n// Created in MoFA_Stage\n\nfunction main() {\n  console.log("Hello from ${fileName}");\n}\n\nmain();\n`
            break
          case 'ts':
            defaultContent = `// ${fileName}.ts\n// Created in MoFA_Stage\n\nfunction main(): void {\n  console.log("Hello from ${fileName}");\n}\n\nmain();\n`
            break
          case 'html':
            defaultContent = `<!DOCTYPE html>\n<html lang="en">\n<head>\n  <meta charset="UTF-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n  <title>${fileName}</title>\n</head>\n<body>\n  <h1>Hello from ${props.agentName}</h1>\n</body>\n</html>\n`
            break
          case 'css':
            defaultContent = `/* ${fileName}.css */\n/* Created in MoFA_Stage */\n\nbody {\n  font-family: Arial, sans-serif;\n  margin: 0;\n  padding: 20px;\n}\n`
            break
          case 'sh':
            defaultContent = `#!/bin/bash\n# ${fileName}.sh\n# Created in MoFA_Stage\n\necho "Hello from ${props.agentName}"\n`
            break
          case 'toml':
            defaultContent = `# ${fileName}.toml\n# Created in MoFA_Stage\n\n[package]\nname = "${props.agentName}"\nversion = "0.1.0"\n`
            break
          default:
            // 对于未知扩展名或无扩展名，提供一个通用的默认内容
            defaultContent = `# ${newFileForm.value.fullName}\n# Created in MoFA_Stage for ${props.agentName}\n\n`
            break
        }
        
        const result = await agentStore.saveFileContent(
          props.agentName,
          filePath,
          defaultContent
        )
        
        if (result) {
          ElMessage.success('File created successfully')
          newFileDialogVisible.value = false
          
          // 重新加载文件列表并打开新文件
          await loadAgentFiles()
          loadFileContent(filePath)
        } else {
          ElMessage.error(`Failed to create file: ${error.value}`)
        }
      } catch (err) {
        ElMessage.error(`Failed to create file: ${err.message}`)
      } finally {
        isCreatingFile.value = false
      }
    }

    const runAgent = async () => {
      const result = await agentStore.runAgent(props.agentName)
      if (result.success) {
        ElMessage.success(`Agent ${props.agentName} started successfully`)
      } else {
        ElMessage.error(`Failed to start Agent: ${result.error}`)
      }
    }

    const stopAgent = async () => {
      const result = await agentStore.stopAgent(props.agentName)
      if (result.success) {
        ElMessage.success(`Agent ${props.agentName} stopped successfully`)
      } else {
        ElMessage.error(`Failed to stop Agent: ${result.error}`)
      }
    }

    // 监听搜索词变化
    watch(fileSearchQuery, (val) => {
      fileTree.value?.filter(val)
    })

    const showTerminal = ref(false)

    // Mermaid 预览相关
    const showMermaidSidebar = ref(false)
    const mermaidHtmlFiles = ref([])
    const selectedMermaidHtml = ref('')
    const mermaidHtmlContent = ref('')
    const loadingMermaidContent = ref(false)
    const zoomLevel = ref(1)

    const zoomIn = () => {
      zoomLevel.value = Math.min(zoomLevel.value + 0.1, 3)
    }

    const zoomOut = () => {
      zoomLevel.value = Math.max(zoomLevel.value - 0.1, 0.3)
    }

    const resetZoom = () => {
      zoomLevel.value = 1
    }

    // 当切换到非 dataflow YAML 文件时，自动关闭 Mermaid 侧边栏
    watch(isDataflowYaml, (val) => {
      if (!val) {
        showMermaidSidebar.value = false
      }
    })

    const openMermaidInNewTab = () => {
      if (!mermaidHtmlContent.value) return
      try {
        const blob = new Blob([mermaidHtmlContent.value], { type: 'text/html' })
        const url = URL.createObjectURL(blob)
        window.open(url, '_blank')
      } catch (e) {
        console.error('Failed to open Mermaid HTML in new tab', e)
      }
    }

    // 切换 Mermaid 侧边栏
    const toggleMermaidSidebar = async () => {
      showMermaidSidebar.value = !showMermaidSidebar.value
      
      if (showMermaidSidebar.value && mermaidHtmlFiles.value.length === 0) {
        // 首次打开时，扫描 mermaid HTML 文件
        await scanMermaidHtmlFiles()
      }
      
      if (showMermaidSidebar.value && selectedMermaidHtml.value && !mermaidHtmlContent.value) {
        // 加载选中文件内容
        await loadMermaidContent()
      }
    }

    // 扫描当前 agent 目录中的 HTML 文件
    const scanMermaidHtmlFiles = async () => {
      try {
        const files = await agentStore.fetchAgentFiles(props.agentName)
        const htmlFiles = files.filter(file => {
          const lowerPath = file.path.toLowerCase()
          return lowerPath.endsWith('.html')
        }).map(file => file.path)
        
        mermaidHtmlFiles.value = htmlFiles
        
        if (htmlFiles.length > 0) {
          selectedMermaidHtml.value = htmlFiles[0]
          await loadMermaidContent()
        }
      } catch (err) {
        console.error('Failed to scan HTML files:', err)
      }
    }

    // 加载 mermaid HTML 内容
    const loadMermaidContent = async () => {
      if (!selectedMermaidHtml.value) return
      
      loadingMermaidContent.value = true
      try {
        const fileData = await agentStore.fetchFileContent(props.agentName, selectedMermaidHtml.value)
        if (fileData) {
          mermaidHtmlContent.value = fileData.content
        }
             } catch (err) {
         ElMessage.error(`加载 HTML 失败: ${err.message}`)
       } finally {
        loadingMermaidContent.value = false
      }
    }

    // 拖拽调整终端高度
    const startResizeTerminal = (e) => {
      e.preventDefault()
      const startY = e.clientY
      const startH = terminalHeight.value
      const onMove = (m) => {
        terminalHeight.value = Math.min(600, Math.max(150, startH + (startY - m.clientY)))
      }
      const onUp = () => {
        window.removeEventListener('mousemove', onMove)
        window.removeEventListener('mouseup', onUp)
      }
      window.addEventListener('mousemove', onMove)
      window.addEventListener('mouseup', onUp)
    }

    // 拖拽调整 Mermaid 侧栏宽度
    const startResizeMermaid = (e) => {
      e.preventDefault()
      const startX = e.clientX
      const startW = mermaidSidebarWidth.value
      const onMove = (m) => {
        mermaidSidebarWidth.value = Math.min(600, Math.max(200, startW + (startX - m.clientX)))
      }
      const onUp = () => {
        window.removeEventListener('mousemove', onMove)
        window.removeEventListener('mouseup', onUp)
      }
      window.addEventListener('mousemove', onMove)
      window.addEventListener('mouseup', onUp)
    }

    // 拖拽调整文件树侧边栏宽度
    const startResizeFileSidebar = (e) => {
      e.preventDefault()
      const startX = e.clientX
      const startW = fileSidebarWidth.value
      const onMove = (m) => {
        fileSidebarWidth.value = Math.min(400, Math.max(180, startW + (m.clientX - startX)))
      }
      const onUp = () => {
        window.removeEventListener('mousemove', onMove)
        window.removeEventListener('mouseup', onUp)
      }
      window.addEventListener('mousemove', onMove)
      window.addEventListener('mouseup', onUp)
    }

    // add ref to CodeEditor
    const codeEditorRef = ref(null)

    const handleMermaidNodeClick = (nodeId) => {
      if (!codeEditorRef.value) return
      const lines = editorContent.value.split('\n')
      let start = -1
      for (let i = 0; i < lines.length; i++) {
        const trimmed = lines[i].trim()
        if (trimmed.startsWith('- id:') && trimmed.includes(nodeId)) {
          start = i
          break
        }
      }
      if (start === -1) return
      let end = lines.length - 1
      for (let j = start + 1; j < lines.length; j++) {
        const t = lines[j].trim()
        if (t.startsWith('- id:')) {
          end = j - 1
          break
        }
      }
      // monaco uses 1-based line numbers
      codeEditorRef.value.selectLines(start + 1, end + 1)
      // Switch to YAML tab if graph tab is active
      if (showYamlTabs.value) activeYamlTab.value = 'yaml'
    }

    onMounted(async () => {
      await loadAgentFiles()
      // 如果使用新版编辑器，检查并启动 VS Code 服务
      if (useNewEditor.value) {
        await checkVSCodeStatus()
        if (!vscodeStatus.value.running) {
          await startVSCodeServer()
        }
      }
    })

    return {
      isLoading,
      fileTree,
      fileSearchQuery,
      fileTreeData,
      defaultProps,
      currentFile,
      editorContent,
      editorLanguage,
      hasChanges,
      isSaving,
      isMarkdownFile,
      previewMode,
      renderedMarkdown,
      isAgentRunning,
      newFileDialogVisible,
      newFileForm,
      isCreatingFile,
      goBack,
      handleFileClick,
      saveCurrentFile,
      togglePreviewMode,
      filterNode,
      addNewFile,
      createNewFile,
      runAgent,
      stopAgent,
      isYaml,
      isDataflowYaml,
      mermaidCode,
      useNewEditor,
      agentFolderPath,
      vscodeBaseUrl,
      vscodeStatus,
      startVSCodeServer,
      installExtensions,
      updateVSCodeConfig,
      showTerminal,
      isMermaidHtml,
      showMermaidSidebar,
      mermaidHtmlFiles,
      selectedMermaidHtml,
      mermaidHtmlContent,
      loadingMermaidContent,
      toggleMermaidSidebar,
      loadMermaidContent,
      activeYamlTab,
      showYamlTabs,
      zoomLevel,
      zoomIn,
      zoomOut,
      resetZoom,
      openMermaidInNewTab,
      fileTreeWrapper,
      rememberFileTreeScroll,
      restoreFileTreeScroll,
      terminalHeight,
      mermaidSidebarWidth,
      fileSidebarWidth,
      startResizeTerminal,
      startResizeMermaid,
      startResizeFileSidebar,
      codeEditorRef,
      handleMermaidNodeClick
    }
  }
}
</script>

<style scoped>
.page-header {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.edit-container {
  display: flex;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: var(--card-shadow);
  overflow: hidden;
  height: calc(100vh - 140px);
}

.file-tree-sidebar {
  width: 250px;
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative; /* 使手柄绝对定位 */
  transition: width .2s ease;
}

.file-tree-resize-handle {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 6px;
  cursor: col-resize;
  background-color: var(--border-color);
  z-index: 5;
}

.sidebar-header {
  padding: 15px;
  border-bottom: 1px solid var(--border-color);
}

.sidebar-header h3 {
  margin: 0 0 10px 0;
  font-size: 16px;
}

.sidebar-footer {
  padding: 10px;
  border-top: 1px solid var(--border-color);
  text-align: center;
}

/* 使文件树内容区域可滚动并占据剩余高度 */
.file-tree-wrapper {
  flex: 1;
  overflow-y: scroll; /* 始终显示滚动条 */
  overflow-x: hidden;
  /* 将滚动条放在左侧 */
  direction: rtl;
}

/* 还原文件树内容方向，避免文字颠倒 */
.file-tree-wrapper .el-tree {
  direction: ltr;
}

/* 自定义滚动条样式，确保在 macOS 上可见 */
.file-tree-wrapper::-webkit-scrollbar {
  width: 8px;
}

.file-tree-wrapper::-webkit-scrollbar-track {
  background: transparent;
}

.file-tree-wrapper::-webkit-scrollbar-thumb {
  background-color: rgba(0,0,0,0.25);
  border-radius: 4px;
}

/* Firefox */
.file-tree-wrapper {
  scrollbar-width: thin;
  scrollbar-color: rgba(0,0,0,0.25) transparent;
}

.editor-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.editor-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.editor-header {
  padding: 10px 15px;
  border-bottom: 1px solid var(--border-color);
  background-color: #f9f9f9;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.file-path {
  font-family: monospace;
  color: var(--text-color-secondary);
}

.editor-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.code-editor-wrapper {
  flex: 1;
  overflow: hidden;
}

.empty-editor {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  background-color: #f9f9f9;
}

.markdown-preview {
  padding: 20px;
  overflow: auto;
  height: 100%;
}

.loading-container {
  padding: 40px;
}

/* VS Code Web 全屏容器 */
.vscode-full-container {
  width: 100%;
  height: calc(100vh - 140px); /* 与 classic 编辑区保持一致高度 */
}

.new-editor-placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  background-color: #f9f9f9;
}

.vscode-loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.vscode-error {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.vscode-starting {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.loading-container {
  width: 100%;
  height: 200px;
}

.terminal-panel {
  transition: height .2s ease;
  position: relative; /* 为拖拽手柄定位 */
  border-top: 1px solid var(--border-color);
}

.terminal-resize-handle {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 6px;
  cursor: row-resize;
  background-color: var(--border-color);
  z-index: 5;
}

.terminal-collapse-container {
  border-top: 1px solid var(--border-color);
}

.terminal-collapse-header {
  padding: 10px;
  cursor: pointer;
  background-color: #f8f9fa;
  border-bottom: 1px solid var(--border-color);
  user-select: none;
}

.terminal-collapse-header:hover {
  background-color: #e9ecef;
}

.collapse-header-content {
  display: flex;
  align-items: center;
  gap: 10px;
}

.collapse-icon {
  transition: transform 0.3s ease;
}

.collapsed {
  transform: rotate(180deg);
}

.collapse-title {
  font-weight: 600;
}

.terminal-status {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 5px;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
}

.connected {
  background-color: #5cb85c;
}

.status-text {
  font-size: 12px;
  color: var(--text-color-secondary);
}

/* Mermaid HTML 预览 iframe */
.mermaid-html-preview {
  width: 100%;
  height: 100%;
  border: 0;
}

/* Mermaid 预览窄栏 */
.mermaid-toggle-bar {
  width: 10px;
  background-color: #f0f0f0;
  border-left: 1px solid var(--border-color);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s ease;
  position: relative;
}

.mermaid-toggle-bar:hover {
  background-color: #e0e0e0;
}

.mermaid-icon {
  transform: rotate(90deg);
  font-size: 12px;
  color: #666;
  transition: transform 0.3s ease;
}

.mermaid-icon.expanded {
  transform: rotate(270deg);
}

/* Mermaid 预览面板 */
.mermaid-preview-sidebar {
  position: relative; /* 为拖拽手柄定位 */
  transition: width .2s ease;
  width: 300px;
  border-left: 1px solid var(--border-color);
  background-color: #fff;
  display: flex;
  flex-direction: column;
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.1);
}

.mermaid-resize-handle {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  width: 6px;
  cursor: col-resize;
  background-color: var(--border-color);
  z-index: 5;
}

.mermaid-sidebar-header {
  padding: 10px 15px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f9f9f9;
}

.mermaid-sidebar-header h4 {
  margin: 0;
  font-size: 14px;
  color: var(--text-color);
}

.mermaid-file-selector {
  padding: 10px 15px;
  border-bottom: 1px solid var(--border-color);
}

.mermaid-preview-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: auto;
}

.mermaid-content-iframe {
  width: 100%;
  height: 100%;
  border: 0;
}

.mermaid-loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
  color: var(--text-color-secondary);
}

.mermaid-empty {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.yaml-preview-tabs, .yaml-preview-tabs > .el-tabs__content, .yaml-preview-tabs .el-tab-pane {
  height: 100%;
}

.yaml-preview-tabs .el-tab-pane {
  padding: 0;
}

.mermaid-toolbar .el-button {
  margin-left: 4px;
}

.mermaid-zoom-wrapper {
  overflow: auto;
  height: 100%;
}

/* 自定义按钮颜色 */
.custom-save-btn {
  background-color: #6DCACE !important;
  border-color: #6DCACE !important;
  color: white !important;
}

.custom-save-btn:hover {
  background-color: #5bb5b8 !important;
  border-color: #5bb5b8 !important;
  color: white !important;
}

.custom-save-btn:active,
.custom-save-btn:focus {
  background-color: #4da0a3 !important;
  border-color: #4da0a3 !important;
  color: white !important;
}

.custom-save-btn.is-disabled {
  background-color: #a8d8da !important;
  border-color: #a8d8da !important;
  color: white !important;
  opacity: 0.6;
}

.custom-run-btn {
  background-color: #FF5640 !important;
  border-color: #FF5640 !important;
  color: white !important;
}

.custom-run-btn:hover {
  background-color: #e6492e !important;
  border-color: #e6492e !important;
  color: white !important;
}

.custom-run-btn:active,
.custom-run-btn:focus {
  background-color: #cc3d1f !important;
  border-color: #cc3d1f !important;
  color: white !important;
}
</style>
