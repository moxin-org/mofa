<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <el-button @click="goBack" icon="ArrowLeft"></el-button>
        <h1 class="page-title">{{ agentName }}</h1>
        <el-tag v-if="isAgentRunning" type="success">运行中</el-tag>
      </div>
      
      <div class="header-actions">
        <el-button-group>
          <el-button type="primary" @click="saveCurrentFile" :disabled="!hasChanges" :loading="isSaving">
            <el-icon><Document /></el-icon>
            保存
          </el-button>
          <el-button v-if="!isAgentRunning" type="success" @click="runAgent">
            <el-icon><VideoPlay /></el-icon>
            运行
          </el-button>
          <el-button v-else type="danger" @click="stopAgent">
            <el-icon><VideoPause /></el-icon>
            停止
          </el-button>
        </el-button-group>
      </div>
    </div>

    <!-- 加载中 -->
    <el-card v-if="isLoading" class="loading-container">
      <el-skeleton :rows="10" animated />
    </el-card>

    <!-- 主编辑区 -->
    <div v-else class="edit-container">
      <!-- 文件树侧边栏 -->
      <div class="file-tree-sidebar">
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
        
        <el-tree
          :data="fileTreeData"
          :props="defaultProps"
          :filter-node-method="filterNode"
          @node-click="handleFileClick"
          ref="fileTree"
          default-expand-all
          highlight-current
        />

        <div class="sidebar-footer">
          <el-button size="small" @click="addNewFile" icon="Plus">新建文件</el-button>
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
                <el-button 
                  v-if="isMarkdownFile" 
                  size="small" 
                  :type="previewMode ? 'primary' : 'default'"
                  @click="togglePreviewMode">
                  预览
                </el-button>
              </el-button-group>
            </div>
          </div>

          <!-- 代码编辑器/Markdown预览 -->
          <div class="editor-content">
            <template v-if="isMarkdownFile && previewMode">
              <div class="markdown-preview" v-html="renderedMarkdown"></div>
            </template>
            <template v-else>
              <CodeEditor
                v-model="editorContent"
                :language="editorLanguage"
                @save="saveCurrentFile"
              />
            </template>
          </div>
        </div>

        <div v-else class="empty-editor">
          <el-empty description="请从左侧选择文件或创建新文件">
            <el-button @click="addNewFile" type="primary">新建文件</el-button>
          </el-empty>
        </div>
      </div>
    </div>

    <!-- 新建文件对话框 -->
    <el-dialog v-model="newFileDialogVisible" title="新建文件" width="30%">
      <el-form :model="newFileForm" label-width="80px">
        <el-form-item label="文件名" required>
          <el-input v-model="newFileForm.name" placeholder="例如: helper.py">
            <template #append>
              <el-select v-model="newFileForm.ext" style="width: 80px;">
                <el-option label=".py" value="py" />
                <el-option label=".md" value="md" />
                <el-option label=".yml" value="yml" />
                <el-option label=".env" value="env" />
                <el-option label=".txt" value="txt" />
              </el-select>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item label="目录">
          <el-input v-model="newFileForm.path" placeholder="留空表示根目录" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="newFileDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="createNewFile" :loading="isCreatingFile">
            创建
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAgentStore } from '../store/agent'
import CodeEditor from '../components/editor/CodeEditor.vue'
import { Document, ArrowLeft, VideoPlay, VideoPause, Search, Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import MarkdownIt from 'markdown-it'

export default {
  name: 'AgentEdit',
  components: {
    CodeEditor,
    Document,
    ArrowLeft,
    VideoPlay,
    VideoPause,
    Search,
    Plus
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
    const isAgentRunning = computed(() => agentStore.isAgentRunning(props.agentName))
    
    // 新建文件相关
    const newFileDialogVisible = ref(false)
    const newFileForm = ref({
      name: '',
      ext: 'py',
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
        ElMessage.error(`加载 Agent 文件失败: ${err.message}`)
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
      
      loadFileContent(data.path)
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
          previewMode.value = false
        }
      } catch (err) {
        ElMessage.error(`加载文件内容失败: ${err.message}`)
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
          ElMessage.success('文件已保存')
        } else {
          ElMessage.error(`保存失败: ${error.value}`)
        }
      } catch (err) {
        ElMessage.error(`保存失败: ${err.message}`)
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
        name: '',
        ext: 'py',
        path: ''
      }
      newFileDialogVisible.value = true
    }

    const createNewFile = async () => {
      if (!newFileForm.value.name) {
        ElMessage.warning('请输入文件名')
        return
      }
      
      isCreatingFile.value = true
      try {
        const filePath = newFileForm.value.path 
          ? `${newFileForm.value.path}/${newFileForm.value.name}.${newFileForm.value.ext}`
          : `${newFileForm.value.name}.${newFileForm.value.ext}`
        
        // 创建默认内容
        let defaultContent = ''
        switch (newFileForm.value.ext) {
          case 'py':
            defaultContent = `# ${newFileForm.value.name}.py\n# Created in MoFA_Stage\n\ndef main():\n    print("Hello from ${newFileForm.value.name}")\n\nif __name__ == "__main__":\n    main()\n`
            break
          case 'md':
            defaultContent = `# ${newFileForm.value.name}\n\n## Overview\n\nThis is a new file created in MoFA_Stage.\n`
            break
          case 'yml':
          case 'yaml':
            defaultContent = `# ${newFileForm.value.name}.${newFileForm.value.ext}\n# Configuration file\n\nname: ${props.agentName}\n`
            break
          case 'env':
            defaultContent = `# Environment variables for ${props.agentName}\n\nDEBUG=True\n`
            break
        }
        
        const result = await agentStore.saveFileContent(
          props.agentName,
          filePath,
          defaultContent
        )
        
        if (result) {
          ElMessage.success('文件已创建')
          newFileDialogVisible.value = false
          
          // 重新加载文件列表并打开新文件
          await loadAgentFiles()
          loadFileContent(filePath)
        } else {
          ElMessage.error(`创建文件失败: ${error.value}`)
        }
      } catch (err) {
        ElMessage.error(`创建文件失败: ${err.message}`)
      } finally {
        isCreatingFile.value = false
      }
    }

    const runAgent = async () => {
      const result = await agentStore.runAgent(props.agentName)
      if (result.success) {
        ElMessage.success(`Agent ${props.agentName} 已启动`)
      } else {
        ElMessage.error(`启动 Agent 失败: ${result.error}`)
      }
    }

    const stopAgent = async () => {
      const result = await agentStore.stopAgent(props.agentName)
      if (result.success) {
        ElMessage.success(`Agent ${props.agentName} 已停止`)
      } else {
        ElMessage.error(`停止 Agent 失败: ${result.error}`)
      }
    }

    // 监听搜索词变化
    watch(fileSearchQuery, (val) => {
      fileTree.value?.filter(val)
    })

    onMounted(async () => {
      await loadAgentFiles()
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
      stopAgent
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
  height: 100%;
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
</style>
