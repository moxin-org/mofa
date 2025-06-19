<template>
  <div class="ssh-terminal-container">
    <div class="terminal-header">
      <h3>{{ title || 'SSH Terminal' }}</h3>
      <div class="terminal-controls">
        <el-button type="primary" size="small" @click="connectSSH" :disabled="isConnected">
          <el-icon><Connection /></el-icon> Connect
        </el-button>
        <el-button type="danger" size="small" @click="disconnectSSH" :disabled="!isConnected">
          <el-icon><Close /></el-icon> Disconnect
        </el-button>
      </div>
    </div>
    
    <div class="terminal-config" v-if="!isConnected">
      <el-form :model="sshConfig" label-width="100px">
        <el-form-item label="Host">
          <el-input v-model="sshConfig.host" placeholder="例如: localhost 或 127.0.0.1" />
        </el-form-item>
        <el-form-item label="Port">
          <el-input v-model="sshConfig.port" placeholder="例如: 22" />
        </el-form-item>
        <el-form-item label="Username">
          <el-input v-model="sshConfig.username" placeholder="SSH 用户名" />
        </el-form-item>
        <el-form-item label="Password">
          <el-input v-model="sshConfig.password" type="password" placeholder="SSH 密码" />
        </el-form-item>
        <el-form-item label="Command">
          <el-input v-model="sshConfig.command" type="textarea" :rows="3" placeholder="要执行的命令" />
        </el-form-item>
      </el-form>
    </div>
    
    <div class="terminal-output" v-if="isConnected || terminalOutput.length > 0">
      <div class="output-header">
        <span>Command Output</span>
        <el-button type="primary" size="small" plain @click="clearOutput">
          Clear Output
        </el-button>
      </div>
      <pre class="output-content" ref="outputContent">{{ terminalOutput }}</pre>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { Connection, Close } from '@element-plus/icons-vue'

export default {
  name: 'SshTerminal',
  components: {
    Connection,
    Close
  },
  props: {
    title: {
      type: String,
      default: 'SSH Terminal'
    },
    initialCommand: {
      type: String,
      default: ''
    },
    autoConnect: {
      type: Boolean,
      default: false
    },
    agentPath: {
      type: String,
      default: ''
    }
  },
  setup(props, { emit }) {
    const isConnected = ref(false)
    const terminalOutput = ref('')
    const outputContent = ref(null)
    const sshConfig = reactive({
      host: 'localhost',
      port: '22',
      username: '',
      password: '',
      command: props.initialCommand || ''
    })
    
    // 模拟 SSH 连接
    // 在实际应用中，这里应该使用 WebSocket 或其他方式与后端通信
    const connectSSH = async () => {
      if (!sshConfig.host || !sshConfig.port || !sshConfig.username || !sshConfig.password) {
        ElMessage.warning('Please fill in the complete SSH connection information')
        return
      }
      
      if (!sshConfig.command.trim()) {
        ElMessage.warning('Please enter the command to execute')
        return
      }
      
      try {
        isConnected.value = true
        appendOutput(`Connecting to ${sshConfig.host}:${sshConfig.port} as ${sshConfig.username}...\n`)
        
        // 模拟连接延迟
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        appendOutput('Connection successful!\n')
        appendOutput(`Executing command: ${sshConfig.command}\n`)
        
        // 模拟命令执行
        await new Promise(resolve => setTimeout(resolve, 500))
        
        // 这里应该是实际的命令输出
        // 在实际应用中，这里应该从 WebSocket 或其他方式获取实时输出
        appendOutput('Command execution in progress...\n')
        
        // 模拟命令输出
        const interval = setInterval(() => {
          appendOutput('.')
        }, 300)
        
        // 模拟命令完成
        setTimeout(() => {
          clearInterval(interval)
          appendOutput('\nCommand execution completed!\n')
        }, 5000)
        
        emit('connected')
      } catch (error) {
        appendOutput(`Connection error: ${error.message}\n`)
        isConnected.value = false
        emit('error', error)
      }
    }
    
    const disconnectSSH = () => {
      appendOutput('Disconnecting...\n')
      isConnected.value = false
      emit('disconnected')
    }
    
    const appendOutput = (text) => {
      terminalOutput.value += text
      nextTick(() => {
        if (outputContent.value) {
          outputContent.value.scrollTop = outputContent.value.scrollHeight
        }
      })
    }
    
    const clearOutput = () => {
      terminalOutput.value = ''
    }
    
    onMounted(() => {
      if (props.autoConnect && sshConfig.command) {
        // 如果设置了自动连接且有命令，则自动连接
        if (props.agentPath) {
          sshConfig.command = `cd ${props.agentPath} && dora up && dora build *.yml && dora start *.yml`
        }
        connectSSH()
      }
    })
    
    onBeforeUnmount(() => {
      if (isConnected.value) {
        disconnectSSH()
      }
    })
    
    return {
      isConnected,
      sshConfig,
      terminalOutput,
      outputContent,
      connectSSH,
      disconnectSSH,
      clearOutput
    }
  }
}
</script>

<style scoped>
.ssh-terminal-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 10px;
}

.terminal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.terminal-header h3 {
  margin: 0;
}

.terminal-controls {
  display: flex;
  gap: 10px;
}

.terminal-config {
  margin-bottom: 20px;
}

.terminal-output {
  flex: 1;
  display: flex;
  flex-direction: column;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
}

.output-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background-color: #f5f7fa;
  border-bottom: 1px solid #dcdfe6;
}

.output-content {
  flex: 1;
  padding: 10px;
  margin: 0;
  background-color: #1e1e1e;
  color: #d4d4d4;
  font-family: monospace;
  white-space: pre-wrap;
  overflow: auto;
  min-height: 300px;
}

[data-theme="light"] .output-content {
  background-color: #f5f5f5;
  color: #333;
}
</style>
