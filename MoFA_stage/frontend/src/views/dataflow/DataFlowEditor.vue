<template>
  <div class="dataflow-editor">
    <div class="editor-header">
      <h1>{{ dataFlow.name || $t('dataflow.editor') }}</h1>
      <div class="actions">
        <el-button class="action-button" type="success" @click="saveDataFlow">{{ $t('common.save') }}</el-button>
        <el-button class="action-button" type="primary" @click="runDataFlow">{{ $t('agent.run') }}</el-button>
        <el-button class="action-button" @click="goBack">{{ $t('common.back') }}</el-button>
      </div>
    </div>

    <div class="editor-container">
      <div class="sidebar">
        <h3>{{ $t('dataflow.availableAgents') }}</h3>
        <div class="search-box">
          <el-input
            v-model="searchQuery"
            :placeholder="$t('dataflow.searchAgent')"
            prefix-icon="el-icon-search"
            clearable
          />
        </div>
        <div class="agent-list">
          <div
            v-for="agent in filteredAgents"
            :key="agent.name"
            class="agent-item"
            draggable="true"
            @dragstart="onDragStart($event, agent)"
          >
            <div class="agent-name">{{ agent.name }}</div>
          </div>
          <div v-if="filteredAgents.length === 0" class="no-agents">
            {{ $t('dataflow.noAgentsFound') }}
          </div>
          <div v-if="isLoading" class="loading-agents">
            <el-skeleton :rows="5" animated />
          </div>
        </div>
      </div>

      <div class="canvas-container">
        <div
          class="canvas"
          @drop="onDrop($event)"
          @dragover="onDragOver($event)"
        >
          <div v-if="dataFlow.nodes.length === 0" class="empty-canvas">
            <p>{{ $t('dataflow.dragAgents') }}</p>
          </div>

          <div
            v-for="node in dataFlow.nodes"
            :key="node.id"
            class="node"
            :style="{ left: `${node.position.x}px`, top: `${node.position.y}px` }"
            @mousedown="startDrag($event, node)"
            :data-node-id="node.id"
          >
            <div class="node-header">
              <span>{{ getAgentName(node.agent_name) }}</span>
              <div class="node-actions">
                <el-dropdown trigger="click" @command="handleNodeCommand($event, node)">
                  <el-button type="info" size="small" icon="el-icon-more" circle></el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item command="copy">{{ $t('dataflow.copy') }}</el-dropdown-item>
                      <el-dropdown-item command="edit">{{ $t('common.edit') }}</el-dropdown-item>
                      <el-dropdown-item command="delete" divided>{{ $t('common.delete') }}</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </div>
            <div class="node-content">
              <!-- 输入表单 -->
              <div class="node-inputs">
                <div v-for="(input, index) in node.inputs" :key="`input-${index}`" class="input-group">
                  <label>{{ input.name }}:</label>
                  <div class="input-with-buttons">
                    <input 
                      v-if="input.type === 'text'" 
                      type="text" 
                      v-model="input.value" 
                      :placeholder="$t('dataflow.inputLabel') + ' ' + input.name"
                    />
                    <div v-if="input.type === 'file'" class="file-input-group">
                      <input type="text" v-model="input.value" :placeholder="$t('dataflow.selectFile')" readonly />
                      <el-button size="small" type="primary">{{ $t('dataflow.upload') }}</el-button>
                    </div>
                    <el-button 
                      v-if="input.type === 'text'" 
                      size="small" 
                      type="primary"
                    >{{ $t('dataflow.submit') }}</el-button>
                  </div>
                  <div class="port input-port" @mousedown="startConnection($event, node.id, input.name, 'target')">
                    <span class="port-dot"></span>
                  </div>
                </div>
                <!-- 添加输入按钮 -->
                <div class="add-port-button">
                  <el-button 
                    type="dashed" 
                    size="small" 
                    icon="el-icon-plus" 
                    @click="addInput(node.id)"
                  >{{ $t('dataflow.addInput') }}</el-button>
                </div>
              </div>
              
              <!-- 输出显示 -->
              <div class="node-outputs">
                <div v-for="(output, index) in node.outputs" :key="`output-${index}`" class="output-group">
                  <div class="output-label">
                    <label>{{ output.name }}:</label>
                    <div class="port output-port" @mousedown="startConnection($event, node.id, output.name, 'source')">
                      <span class="port-dot"></span>
                    </div>
                  </div>
                  <div class="output-value">
                    {{ output.value || '- - - - -' }}
                  </div>
                </div>
                <!-- 添加输出按钮 -->
                <div class="add-port-button">
                  <el-button 
                    type="dashed" 
                    size="small" 
                    icon="el-icon-plus" 
                    @click="addOutput(node.id)"
                  >{{ $t('dataflow.addOutput') }}</el-button>
                </div>
              </div>
            </div>
          </div>

          <!-- 连接线 -->
          <svg class="connections">
            <path
              v-for="conn in dataFlow.connections"
              :key="conn.id"
              :d="getConnectionPath(conn)"
              stroke="#409EFF"
              stroke-width="2"
              fill="none"
            />
          </svg>

          <!-- 正在创建的连接线 -->
          <svg class="temp-connection" v-if="tempConnection.active">
            <path
              :d="getTempConnectionPath()"
              stroke="#67C23A"
              stroke-width="2"
              stroke-dasharray="5,5"
              fill="none"
            />
          </svg>
        </div>
      </div>

      <div class="properties-panel">
        <h3>{{ $t('dataflow.propertiesPanel') }}</h3>
        <div v-if="selectedNode" class="node-properties">
          <h4>{{ $t('dataflow.nodeProperties') }}</h4>
          <el-form label-width="80px">
            <el-form-item label="Agent">
              <el-input v-model="selectedNode.agent_name" disabled />
            </el-form-item>
            <el-form-item :label="$t('dataflow.inputPorts')">
              <div v-for="(port, index) in ['input1', 'input2']" :key="`in-${index}`">
                <el-tag>{{ port }}</el-tag>
              </div>
            </el-form-item>
            <el-form-item :label="$t('dataflow.outputPorts')">
              <div v-for="(port, index) in ['output']" :key="`out-${index}`">
                <el-tag type="success">{{ port }}</el-tag>
              </div>
            </el-form-item>
          </el-form>
        </div>
        <div v-else-if="selectedConnection" class="connection-properties">
          <h4>{{ $t('dataflow.connectionProperties') }}</h4>
          <el-form label-width="80px">
            <el-form-item :label="$t('dataflow.source')">
              <el-input :value="getConnectionSourceLabel(selectedConnection)" disabled />
            </el-form-item>
            <el-form-item :label="$t('dataflow.target')">
              <el-input :value="getConnectionTargetLabel(selectedConnection)" disabled />
            </el-form-item>
            <el-form-item>
              <el-button type="danger" @click="removeConnection(selectedConnection.id)">{{ $t('dataflow.deleteConnection') }}</el-button>
            </el-form-item>
          </el-form>
        </div>
        <div v-else class="no-selection">
          <p>{{ $t('dataflow.selectToViewProperties') }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import dataflowApi from '@/api/dataflow'
import agentApi from '@/api/agent'

export default {
  name: 'DataFlowEditor',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const flowId = route.params.flowId

    // 加载状态
    const isLoading = ref(true)

    // 数据流数据
    const dataFlow = reactive({
      flow_id: flowId,
      name: '',
      description: '',
      nodes: [],
      connections: []
    })

    // Agents 列表
    const agents = ref([])
    const searchQuery = ref('')

    // 节点拖拽相关
    const isDragging = ref(false)
    const draggedNode = ref(null)
    const dragOffset = reactive({ x: 0, y: 0 })

    // 连接相关
    const tempConnection = reactive({
      active: false,
      sourceNodeId: null,
      sourcePort: null,
      targetNodeId: null,
      targetPort: null,
      startX: 0,
      startY: 0,
      endX: 0,
      endY: 0,
      type: null // 'source' 或 'target'
    })

    // 选中的元素
    const selectedNode = ref(null)
    const selectedConnection = ref(null)

    // 过滤后的 Agents 列表
    const filteredAgents = computed(() => {
      if (!searchQuery.value) return agents.value
      const query = searchQuery.value.toLowerCase()
      return agents.value.filter(agent => 
        agent.name.toLowerCase().includes(query) || 
        (agent.description && agent.description.toLowerCase().includes(query))
      )
    })

    // 获取数据流详情
    const fetchDataFlow = async () => {
      if (!flowId) return
      
      try {
        const response = await dataflowApi.getDataFlowDetails(flowId)
        if (response.data.success) {
          const flow = response.data.flow
          Object.assign(dataFlow, flow)
        } else {
          ElMessage.error(response.data.message || '获取数据流详情失败')
        }
      } catch (error) {
        console.error('Error fetching dataflow:', error)
        ElMessage.error('获取数据流详情失败')
      }
    }

    // 获取所有可用的 agents
    const fetchAgents = async () => {
      try {
        isLoading.value = true
        const response = await agentApi.getAllAgents()
        
        // 将字符串数组转换为对象数组，以便添加更多属性
        agents.value = (response.data.agents || []).map(agentName => ({
          name: agentName,
          description: ''
        }))
        
        // 获取每个agent的详细信息，包括输入输出参数
        for (const agent of agents.value) {
          try {
            const detailResponse = await agentApi.getAgentDetails(agent.name)
            if (detailResponse.data.agent) {
              agent.inputs = detailResponse.data.agent.inputs || []
              agent.outputs = detailResponse.data.agent.outputs || []
              agent.description = detailResponse.data.agent.description || '无描述'
            }
          } catch (detailError) {
            console.error(`Error fetching details for agent ${agent.name}:`, detailError)
          }
        }
      } catch (error) {
        console.error('Error fetching agents:', error)
        ElMessage.error('获取 Agents 失败')
      } finally {
        isLoading.value = false
      }
    }

    // 保存数据流
    const saveDataFlow = async () => {
      try {
        const response = await dataflowApi.updateDataFlow(flowId, dataFlow)
        if (response.data.success) {
          ElMessage.success('数据流保存成功')
        } else {
          ElMessage.error(response.data.message || '保存数据流失败')
        }
      } catch (error) {
        console.error('Error saving dataflow:', error)
        ElMessage.error('保存数据流失败')
      }
    }

    // 运行数据流
    const runDataFlow = async () => {
      try {
        const response = await dataflowApi.runDataFlow(flowId)
        if (response.data.success) {
          ElMessage.success('数据流已开始运行')
        } else {
          ElMessage.error(response.data.message || '运行数据流失败')
        }
      } catch (error) {
        console.error('Error running dataflow:', error)
        ElMessage.error('运行数据流失败')
      }
    }

    // 返回列表页
    const goBack = () => {
      router.push('/dataflows')
    }

    // 处理编辑器顶部下拉菜单命令
    const handleEditorCommand = (command) => {
      if (command === 'save') {
        saveDataFlow()
      } else if (command === 'run') {
        runDataFlow()
      } else if (command === 'back') {
        goBack()
      }
    }

    // 拖拽开始
    const onDragStart = (event, agent) => {
      console.log('Drag start with agent:', agent)
      // 设置拖拽数据
      event.dataTransfer.setData('text/plain', JSON.stringify(agent))
      event.dataTransfer.setData('agent', JSON.stringify(agent))
      // 设置拖拽效果
      event.dataTransfer.effectAllowed = 'copy'
      
      // 创建一个拖拽图像
      const dragImage = document.createElement('div')
      dragImage.textContent = agent.name
      dragImage.style.padding = '5px 10px'
      dragImage.style.background = '#409EFF'
      dragImage.style.color = 'white'
      dragImage.style.borderRadius = '4px'
      dragImage.style.position = 'absolute'
      dragImage.style.top = '-1000px'
      document.body.appendChild(dragImage)
      
      // 设置拖拽图像
      event.dataTransfer.setDragImage(dragImage, 0, 0)
      
      // 延迟移除拖拽图像
      setTimeout(() => {
        document.body.removeChild(dragImage)
      }, 0)
    }

    // 拖拽结束
    const onDrop = (event) => {
      event.preventDefault()
      try {
        // 尝试从多个可能的数据类型中获取数据
        let agentDataStr = event.dataTransfer.getData('agent')
        if (!agentDataStr) {
          agentDataStr = event.dataTransfer.getData('text/plain')
        }
        
        if (!agentDataStr) {
          console.error('No agent data found in drop event')
          return
        }
        
        const agentData = JSON.parse(agentDataStr)
        console.log('Dropped agent data:', agentData)
        
        // 计算放置位置
        const canvasRect = event.currentTarget.getBoundingClientRect()
        const x = event.clientX - canvasRect.left
        const y = event.clientY - canvasRect.top
        
        // 添加节点到画布
        const nodeId = addNode(agentData, { x, y })
      } catch (error) {
        console.error('Error processing drop event:', error)
      }
    }

    // 拖拽经过
    const onDragOver = (event) => {
      event.preventDefault()
    }

    // 开始拖拽节点
    const startDrag = (event, node) => {
      // 如果点击的是端口，不触发节点拖拽
      if (event.target.classList.contains('port')) return
      
      isDragging.value = true
      draggedNode.value = node
      
      const nodeElement = event.currentTarget
      const nodeRect = nodeElement.getBoundingClientRect()
      
      dragOffset.x = event.clientX - nodeRect.left
      dragOffset.y = event.clientY - nodeRect.top
      
      // 选中当前节点
      selectedNode.value = node
      selectedConnection.value = null
      
      document.addEventListener('mousemove', onMouseMove)
      document.addEventListener('mouseup', stopDrag)
    }

    // 鼠标移动
    const onMouseMove = (event) => {
      if (isDragging.value && draggedNode.value) {
        const canvasElement = document.querySelector('.canvas')
        const canvasRect = canvasElement.getBoundingClientRect()
        
        const x = event.clientX - canvasRect.left - dragOffset.x
        const y = event.clientY - canvasRect.top - dragOffset.y
        
        draggedNode.value.position.x = Math.max(0, x)
        draggedNode.value.position.y = Math.max(0, y)
      } else if (tempConnection.active) {
        const canvasElement = document.querySelector('.canvas')
        const canvasRect = canvasElement.getBoundingClientRect()
        
        if (tempConnection.type === 'source') {
          tempConnection.endX = event.clientX - canvasRect.left
          tempConnection.endY = event.clientY - canvasRect.top
        } else {
          tempConnection.startX = event.clientX - canvasRect.left
          tempConnection.startY = event.clientY - canvasRect.top
        }
      }
    }

    // 停止拖拽
    const stopDrag = () => {
      isDragging.value = false
      draggedNode.value = null
      
      document.removeEventListener('mousemove', onMouseMove)
      document.removeEventListener('mouseup', stopDrag)
    }

    // 开始创建连接
    const startConnection = (event, nodeId, port, type) => {
      event.stopPropagation()
      console.log(`Starting connection from node ${nodeId}, port ${port}, type ${type}`)
      
      tempConnection.active = true
      tempConnection.type = type
      
      const portElement = event.currentTarget
      const portRect = portElement.getBoundingClientRect()
      const canvasElement = document.querySelector('.canvas')
      const canvasRect = canvasElement.getBoundingClientRect()
      
      const portX = portRect.left + portRect.width / 2 - canvasRect.left
      const portY = portRect.top + portRect.height / 2 - canvasRect.top
      
      if (type === 'source') {
        tempConnection.sourceNodeId = nodeId
        tempConnection.sourcePort = port
        tempConnection.startX = portX
        tempConnection.startY = portY
        tempConnection.endX = portX
        tempConnection.endY = portY
      } else {
        tempConnection.targetNodeId = nodeId
        tempConnection.targetPort = port
        tempConnection.endX = portX
        tempConnection.endY = portY
        tempConnection.startX = portX
        tempConnection.startY = portY
      }
      
      document.addEventListener('mousemove', onMouseMove)
      document.addEventListener('mouseup', finishConnection)
    }

    // 完成连接创建
    const finishConnection = (event) => {
      document.removeEventListener('mousemove', onMouseMove)
      document.removeEventListener('mouseup', finishConnection)
      
      if (!tempConnection.active) return
      
      // 检查是否在端口上释放
      const portElement = event.target
      console.log('Finish connection on element:', portElement)
      
      if (portElement.classList.contains('port') || portElement.classList.contains('port-dot')) {
        // 如果点击的是端口内的圆点，获取父端口元素
        const actualPortElement = portElement.classList.contains('port-dot') 
          ? portElement.parentElement 
          : portElement
          
        const nodeElement = actualPortElement.closest('.node')
        if (!nodeElement) {
          console.error('Could not find parent node element')
          tempConnection.active = false
          return
        }
        
        const nodeId = nodeElement.getAttribute('data-node-id')
        console.log('Node ID:', nodeId)
        
        // 找到对应的输入/输出组
        let portName = ''
        if (actualPortElement.closest('.input-group')) {
          const inputGroup = actualPortElement.closest('.input-group')
          const label = inputGroup.querySelector('label')
          if (label) {
            portName = label.textContent.replace(':', '').trim()
          }
        } else if (actualPortElement.closest('.output-group')) {
          const outputGroup = actualPortElement.closest('.output-group')
          const label = outputGroup.querySelector('label')
          if (label) {
            portName = label.textContent.replace(':', '').trim()
          }
        }
        
        console.log('Port name:', portName)
        
        if (portName) {
          if (tempConnection.type === 'source' && actualPortElement.classList.contains('input-port')) {
            // 从输出连接到输入
            tempConnection.targetNodeId = nodeId
            tempConnection.targetPort = portName
            createConnection()
          } else if (tempConnection.type === 'target' && actualPortElement.classList.contains('output-port')) {
            // 从输入连接到输出
            tempConnection.sourceNodeId = nodeId
            tempConnection.sourcePort = portName
            createConnection()
          }
        }
      }
      
      // 重置临时连接
      tempConnection.active = false
    }

    // 创建连接
    const createConnection = () => {
      if (!tempConnection.sourceNodeId || !tempConnection.targetNodeId) return
      
      // 检查是否已存在相同的连接
      const exists = dataFlow.connections.some(conn => 
        conn.source_node_id === tempConnection.sourceNodeId &&
        conn.source_output === tempConnection.sourcePort &&
        conn.target_node_id === tempConnection.targetNodeId &&
        conn.target_input === tempConnection.targetPort
      )
      
      if (exists) {
        ElMessage.warning('连接已存在')
        return
      }
      
      // 添加新连接
      const connectionId = `conn-${Date.now()}`
      const connection = {
        id: connectionId,
        source_node_id: tempConnection.sourceNodeId,
        source_output: tempConnection.sourcePort,
        target_node_id: tempConnection.targetNodeId,
        target_input: tempConnection.targetPort
      }
      
      dataFlow.connections.push(connection)
    }

    // 获取连接路径
    const getConnectionPath = (connection) => {
      const sourceNode = dataFlow.nodes.find(node => node.id === connection.source_node_id)
      const targetNode = dataFlow.nodes.find(node => node.id === connection.target_node_id)
      
      if (!sourceNode || !targetNode) return ''
      
      // 计算输出端口位置
      // 找到源输出端口的索引
      const sourceOutputIndex = sourceNode.outputs.findIndex(output => output.name === connection.source_output)
      const outputPortY = 30 + (sourceNode.inputs.length * 40) + 40 + (sourceOutputIndex * 40) + 20
      
      // 计算输入端口位置
      // 找到目标输入端口的索引
      const targetInputIndex = targetNode.inputs.findIndex(input => input.name === connection.target_input)
      const inputPortY = 30 + (targetInputIndex * 40) + 20
      
      const startX = sourceNode.position.x + 400 // 节点宽度
      const startY = sourceNode.position.y + outputPortY
      const endX = targetNode.position.x
      const endY = targetNode.position.y + inputPortY
      
      // 贝塞尔曲线
      const controlX1 = startX + 80
      const controlX2 = endX - 80
      
      return `M ${startX} ${startY} C ${controlX1} ${startY}, ${controlX2} ${endY}, ${endX} ${endY}`
    }

    // 获取临时连接路径
    const getTempConnectionPath = () => {
      const { startX, startY, endX, endY } = tempConnection
      
      // 贝塞尔曲线
      const controlX1 = startX + 80
      const controlX2 = endX - 80
      
      return `M ${startX} ${startY} C ${controlX1} ${startY}, ${controlX2} ${endY}, ${endX} ${endY}`
    }

    // 移除节点
    const removeNode = (nodeId) => {
      // 移除与该节点相关的所有连接
      dataFlow.connections = dataFlow.connections.filter(conn => 
        conn.source_node_id !== nodeId && conn.target_node_id !== nodeId
      )
      
      // 移除节点
      dataFlow.nodes = dataFlow.nodes.filter(node => node.id !== nodeId)
      
      // 如果当前选中的是被删除的节点，清除选择
      if (selectedNode.value && selectedNode.value.id === nodeId) {
        selectedNode.value = null
      }
    }

    // 移除连接
    const removeConnection = (connectionId) => {
      dataFlow.connections = dataFlow.connections.filter(conn => conn.id !== connectionId)
      
      // 如果当前选中的是被删除的连接，清除选择
      if (selectedConnection.value && selectedConnection.value.id === connectionId) {
        selectedConnection.value = null
      }
    }

    // 获取 Agent 名称
    const getAgentName = (agentName) => {
      const agent = agents.value.find(a => a.name === agentName)
      return agent ? agent.name : agentName
    }

    // 获取连接源标签
    const getConnectionSourceLabel = (connection) => {
      const sourceNode = dataFlow.nodes.find(node => node.id === connection.source_node_id)
      return sourceNode ? `${getAgentName(sourceNode.agent_name)}.${connection.source_output}` : ''
    }

    // 获取连接目标标签
    const getConnectionTargetLabel = (connection) => {
      const targetNode = dataFlow.nodes.find(node => node.id === connection.target_node_id)
      return targetNode ? `${getAgentName(targetNode.agent_name)}.${connection.target_input}` : ''
    }

    // 添加输入端口
    const addInput = (nodeId) => {
      const node = dataFlow.nodes.find(n => n.id === nodeId)
      if (node) {
        const inputName = `input${node.inputs.length + 1}`
        node.inputs.push({ name: inputName, type: 'text', value: '' })
      }
    }
    
    // 添加输出端口
    const addOutput = (nodeId) => {
      const node = dataFlow.nodes.find(n => n.id === nodeId)
      if (node) {
        const outputName = `output${node.outputs.length + 1}`
        node.outputs.push({ name: outputName, value: '' })
      }
    }
    
    // 处理节点操作命令
    const handleNodeCommand = (command, node) => {
      if (command === 'copy') {
        duplicateNode(node)
      } else if (command === 'edit') {
        editNode(node)
      } else if (command === 'delete') {
        removeNode(node.id)
      }
    }
    
    // 复制节点
    const duplicateNode = (node) => {
      const newPosition = {
        x: node.position.x + 50,
        y: node.position.y + 50
      }
      
      const nodeId = `node-${Date.now()}`
      dataFlow.nodes.push({
        id: nodeId,
        agent_name: node.agent_name,
        position: newPosition,
        inputs: JSON.parse(JSON.stringify(node.inputs)),
        outputs: JSON.parse(JSON.stringify(node.outputs))
      })
    }
    
    // 编辑节点
    const editNode = (node) => {
      selectedNode.value = node
      // 这里可以添加打开编辑对话框的逻辑
    }

    // 添加节点到画布
    const addNode = (agent, position) => {
      const nodeId = `node-${Date.now()}`
      
      // 从agent定义中获取输入输出参数
      const inputs = agent.inputs && agent.inputs.length > 0 
        ? agent.inputs.map(input => ({ name: input.name, type: input.type || 'text', value: '' }))
        : [{ name: 'query', type: 'text', value: '' }]
      
      const outputs = agent.outputs && agent.outputs.length > 0
        ? agent.outputs.map(output => ({ name: output.name, value: '' }))
        : [{ name: 'agent_result', value: '' }]
      
      dataFlow.nodes.push({
        id: nodeId,
        agent_name: agent.name,
        position: { ...position },
        inputs: inputs,
        outputs: outputs
      })
      
      return nodeId
    }

    onMounted(() => {
      fetchDataFlow()
      fetchAgents()
    })

    onBeforeUnmount(() => {
      document.removeEventListener('mousemove', onMouseMove)
      document.removeEventListener('mouseup', stopDrag)
      document.removeEventListener('mouseup', finishConnection)
    })

    return {
      dataFlow,
      agents,
      searchQuery,
      filteredAgents,
      selectedNode,
      selectedConnection,
      isDragging,
      draggedNode,
      dragOffset,
      tempConnection,
      isLoading,
      onDragStart,
      onDragOver,
      onDrop,
      startDrag,
      onMouseMove,
      stopDrag,
      startConnection,
      getConnectionPath,
      getTempConnectionPath,
      saveDataFlow,
      runDataFlow,
      goBack,
      removeNode,
      removeConnection,
      getAgentName,
      getConnectionSourceLabel,
      getConnectionTargetLabel,
      addInput,
      addOutput,
      handleNodeCommand,
      handleEditorCommand,
      duplicateNode,
      editNode
    }
  }
}
</script>

<style scoped>
.dataflow-editor {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 25px;
  border-bottom: 1px solid #dcdfe6;
  background-color: #ffffff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.editor-container {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.sidebar {
  width: 250px;
  border-right: 1px solid #dcdfe6;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sidebar h3 {
  padding: 10px;
  margin: 0;
  border-bottom: 1px solid #dcdfe6;
}

.search-box {
  padding: 10px;
}

.agent-list {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
}

.agent-item {
  padding: 10px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  margin-bottom: 10px;
  cursor: move;
  background-color: #f5f7fa;
  transition: all 0.3s;
}

.agent-item:hover {
  background-color: #ecf5ff;
  border-color: #c6e2ff;
}

.agent-name {
  font-weight: bold;
  margin-bottom: 5px;
}

.agent-description {
  font-size: 12px;
  color: #606266;
}

.canvas-container {
  flex: 1;
  position: relative;
  overflow: hidden;
}

.canvas {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #f5f7fa;
  background-image: 
    linear-gradient(rgba(0, 0, 0, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 0, 0, 0.1) 1px, transparent 1px);
  background-size: 20px 20px;
  overflow: auto;
}

.empty-canvas {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #909399;
}

.node {
  position: absolute;
  width: 400px;
  background-color: white;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.node-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px;
  background-color: #409EFF;
  color: white;
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
}

.node-content {
  padding: 10px;
}

.node-inputs {
  margin-bottom: 15px;
  border-bottom: 1px dashed #dcdfe6;
  padding-bottom: 10px;
}

.input-group, .output-group {
  margin-bottom: 10px;
  display: flex;
  align-items: center;
}

.input-group {
  justify-content: space-between;
}

.input-group label, .output-label label {
  font-size: 14px;
  color: #606266;
  margin-right: 10px;
  width: 70px;
}

.input-with-buttons {
  display: flex;
  flex: 1;
  margin-right: 10px;
}

.input-with-buttons input {
  flex: 1;
  padding: 5px 10px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  margin-right: 5px;
}

.file-input-group {
  display: flex;
  flex: 1;
}

.file-input-group input {
  flex: 1;
  margin-right: 5px;
}

.output-group {
  flex-direction: column;
  align-items: flex-start;
}

.output-label {
  display: flex;
  justify-content: space-between;
  width: 100%;
  align-items: center;
}

.output-value {
  width: 100%;
  padding: 8px;
  background-color: #f5f7fa;
  border-radius: 4px;
  margin-top: 5px;
  color: #606266;
  font-family: monospace;
}

.port {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.port-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: white;
}

.input-port {
  background-color: #67c23a;
}

.output-port {
  background-color: #409eff;
}

.no-agents {
  padding: 20px;
  text-align: center;
  color: #909399;
}

.connections, .temp-connection {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 5;
}

.properties-panel {
  width: 300px;
  border-left: 1px solid #dcdfe6;
  overflow-y: auto;
}

.properties-panel h3 {
  padding: 10px;
  margin: 0;
  border-bottom: 1px solid #dcdfe6;
}

.node-properties, .connection-properties, .no-selection {
  padding: 10px;
}

.no-selection {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
  color: #909399;
}
.actions {
  display: flex;
}

.actions .action-button + .action-button {
  margin-left: 10px;
}

.action-button {
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: normal;
  border: 1px solid #dcdfe6;
  background-color: #ffffff;
  color: #606266;
  min-width: 60px;
  height: 32px;
  line-height: 1;
}

.action-button:hover {
  color: #409EFF;
  border-color: #c6e2ff;
  background-color: #ecf5ff;
}

.action-button:active {
  color: #3a8ee6;
  border-color: #3a8ee6;
  outline: none;
}


</style>
