<template>
  <div class="code-editor-container" ref="editorContainer"></div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import * as monaco from 'monaco-editor'

export default {
  name: 'CodeEditor',
  props: {
    modelValue: {
      type: String,
      default: ''
    },
    language: {
      type: String,
      default: 'python'
    },
    readOnly: {
      type: Boolean,
      default: false
    },
    theme: {
      type: String,
      default: 'vs'
    }
  },
  emits: ['update:modelValue', 'save'],
  setup(props, { emit }) {
    const editorContainer = ref(null)
    let editor = null
    
    // 初始化编辑器
    const initMonaco = () => {
      if (editorContainer.value) {
        // 创建编辑器实例
        editor = monaco.editor.create(editorContainer.value, {
          value: props.modelValue,
          language: props.language,
          theme: props.theme,
          automaticLayout: true, // 自动调整布局
          fontSize: 14,
          tabSize: 4,
          minimap: { enabled: true },
          scrollBeyondLastLine: false,
          readOnly: props.readOnly,
          scrollbar: {
            useShadows: false,
            vertical: 'visible',
            horizontal: 'visible',
            verticalScrollbarSize: 10,
            horizontalScrollbarSize: 10
          }
        })
        
        // 监听内容变化事件
        editor.onDidChangeModelContent(() => {
          const value = editor.getValue()
          emit('update:modelValue', value)
        })
        
        // 添加快捷键: Ctrl+S 或 Cmd+S 保存
        editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyS, () => {
          emit('save')
        })
      }
    }
    
    // 清理编辑器
    const disposeEditor = () => {
      if (editor) {
        editor.dispose()
        editor = null
      }
    }
    
    // 当组件挂载时初始化编辑器
    onMounted(() => {
      initMonaco()
    })
    
    // 当组件销毁前清理编辑器
    onBeforeUnmount(() => {
      disposeEditor()
    })
    
    // 监听 modelValue 变化，更新编辑器内容
    watch(() => props.modelValue, (newValue) => {
      if (editor && newValue !== editor.getValue()) {
        editor.setValue(newValue)
      }
    })
    
    // 监听语言变化，更新编辑器语言模式
    watch(() => props.language, (newLanguage) => {
      if (editor) {
        monaco.editor.setModelLanguage(editor.getModel(), newLanguage)
      }
    })
    
    // 监听主题变化
    watch(() => props.theme, (newTheme) => {
      if (editor) {
        monaco.editor.setTheme(newTheme)
      }
    })
    
    // 监听只读状态变化
    watch(() => props.readOnly, (isReadOnly) => {
      if (editor) {
        editor.updateOptions({ readOnly: isReadOnly })
      }
    })
    
    return {
      editorContainer
    }
  }
}
</script>

<style scoped>
.code-editor-container {
  width: 100%;
  height: 100%;
  min-height: 300px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  overflow: hidden;
}
</style>
