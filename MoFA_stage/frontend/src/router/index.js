import { createRouter, createWebHistory } from 'vue-router'

// 导入页面组件
import AgentList from '../views/AgentList.vue'
import AgentEdit from '../views/AgentEdit.vue'
import AgentCreate from '../views/AgentCreate.vue'
import Settings from '../views/Settings.vue'
import Terminal from '../views/Terminal.vue'
// 注释掉这两行，因为现在这两个组件在App.vue中直接使用
// import WebSSH from '../views/WebSSH.vue'
// import TtydTerminal from '../views/TtydTerminal.vue'
import NotFound from '../views/NotFound.vue'
import DataFlowList from '../views/dataflow/DataFlowList.vue'
import DataFlowEditor from '../views/dataflow/DataFlowEditor.vue'

// 创建空组件替代直接加载的终端组件
const EmptyComponent = { render: () => null }

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      redirect: '/agents'
    },
    {
      path: '/agents',
      name: 'agents',
      component: AgentList
    },
    {
      path: '/agents/create',
      name: 'agent-create',
      component: AgentCreate
    },
    {
      path: '/agents/:agentName/edit',
      name: 'agent-edit',
      component: AgentEdit,
      props: true
    },
    {
      path: '/settings',
      name: 'settings',
      component: Settings
    },
    {
      path: '/terminal',
      name: 'terminal',
      component: Terminal
    },
    {
      path: '/webssh',
      name: 'webssh',
      component: EmptyComponent, // 使用空组件
      meta: { keepAlive: true }
    },
    {
      path: '/ttyd',
      name: 'ttyd',
      component: EmptyComponent, // 使用空组件
      meta: { keepAlive: true }
    },
    {
      path: '/dataflows',
      name: 'dataflows',
      component: DataFlowList
    },
    {
      path: '/dataflows/:flowId/edit',
      name: 'dataflow-edit',
      component: DataFlowEditor,
      props: true
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: NotFound
    }
  ]
})

export default router
