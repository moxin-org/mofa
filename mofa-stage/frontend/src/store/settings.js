/**
 * 设置状态管理
 */
import { defineStore } from 'pinia'
import settingsApi from '../api/settings'

export const useSettingsStore = defineStore('settings', {
  state: () => {
    // 从localStorage获取备份的路径
    const defaultPaths = {
      mofa_dir: localStorage.getItem('mofa_dir') || '/mnt/c/Users/Yao/Desktop/code/mofa/mofa',
      agent_hub_path: localStorage.getItem('agent_hub_path') || '',
      examples_path: localStorage.getItem('examples_path') || '',
      custom_agent_hub_path: localStorage.getItem('custom_agent_hub_path') || '',
      custom_examples_path: localStorage.getItem('custom_examples_path') || '',
    };
    
    return {
      settings: {
        mofa_env_path: '',
        mofa_dir: defaultPaths.mofa_dir,
        mofa_mode: 'system',
        docker_container_name: '',
        use_system_mofa: true,
        use_default_agent_hub_path: true,
        use_default_examples_path: true,
        use_relative_paths: true,
        agent_hub_path: defaultPaths.agent_hub_path,
        examples_path: defaultPaths.examples_path, 
        custom_agent_hub_path: defaultPaths.custom_agent_hub_path,
        custom_examples_path: defaultPaths.custom_examples_path,
        theme: 'light',
        editor_font_size: 14,
        editor_tab_size: 4,
        editor_version: 'classic',
        language: localStorage.getItem('language') || 'zh',
        ssh: {
          hostname: '127.0.0.1',
          port: 22,
          username: '',
          password: '',
          auto_connect: true
        },
        // 添加终端显示模式设置
        terminal_display_mode: 'both', // 'terminal', 'webssh', 'both'
        // ---- AI API Settings ----
        openai_api_key: '',
        openai_base_url: 'https://api.openai.com/v1',
        azure_openai_api_key: '',
        azure_openai_endpoint: '',
        azure_openai_api_version: '2023-05-15-preview',
        gemini_api_key: '',
        gemini_api_endpoint: 'https://generativelanguage.googleapis.com/v1beta'
      },
      isLoading: false,
      error: null
    }
  },
  
  actions: {
    async fetchSettings() {
      this.isLoading = true
      this.error = null
      try {
        const response = await settingsApi.getSettings()
        if (response.data && response.data.success) {
          // 保留默认值，如果服务器没有返回这些字段
          const defaultPaths = {
            mofa_dir: this.settings.mofa_dir,
            agent_hub_path: this.settings.agent_hub_path,
            examples_path: this.settings.examples_path,
            custom_agent_hub_path: this.settings.custom_agent_hub_path,
            custom_examples_path: this.settings.custom_examples_path,
          };
          
          // 更新设置
          this.settings = response.data.settings
          
          // 确保路径字段不会丢失
          if (!this.settings.mofa_dir) {
            this.settings.mofa_dir = defaultPaths.mofa_dir;
          } else {
            localStorage.setItem('mofa_dir', this.settings.mofa_dir);
          }
          
          // 保存和恢复Agent Hub相关路径
          if (!this.settings.agent_hub_path) {
            this.settings.agent_hub_path = defaultPaths.agent_hub_path;
          } else {
            localStorage.setItem('agent_hub_path', this.settings.agent_hub_path);
          }
          
          if (!this.settings.examples_path) {
            this.settings.examples_path = defaultPaths.examples_path;
          } else {
            localStorage.setItem('examples_path', this.settings.examples_path);
          }
          
          if (!this.settings.custom_agent_hub_path) {
            this.settings.custom_agent_hub_path = defaultPaths.custom_agent_hub_path;
          } else {
            localStorage.setItem('custom_agent_hub_path', this.settings.custom_agent_hub_path);
          }
          
          if (!this.settings.custom_examples_path) {
            this.settings.custom_examples_path = defaultPaths.custom_examples_path;
          } else {
            localStorage.setItem('custom_examples_path', this.settings.custom_examples_path);
          }
          
          // 确保use_default路径相关字段存在
          if (this.settings.use_default_agent_hub_path === undefined) {
            this.settings.use_default_agent_hub_path = true;
          }
          
          if (this.settings.use_default_examples_path === undefined) {
            this.settings.use_default_examples_path = true;
          }
          
          // 确保use_relative_paths字段存在
          if (this.settings.use_relative_paths === undefined) {
            this.settings.use_relative_paths = true;
          }
          
          // 确保终端显示模式有默认值
          if (this.settings.terminal_display_mode === undefined) {
            this.settings.terminal_display_mode = 'both';
          }
          
          // 确保编辑器版本有默认值
          if (this.settings.editor_version === undefined) {
            this.settings.editor_version = 'classic'
          }
          
          // 确保ssh对象总是存在
          if (!this.settings.ssh) {
            this.settings.ssh = {
              hostname: '127.0.0.1',
              port: 22,
              username: '',
              password: '',
              auto_connect: true
            }
          }
          
          // 确保新字段mofa_mode存在
          if (!this.settings.mofa_mode) {
            // 根据旧字段use_system_mofa推断
            this.settings.mofa_mode = this.settings.use_system_mofa ? 'system' : 'venv'
          }
          
          // 如果mofa_mode存在，但use_system_mofa丢失，做向后兼容
          if (this.settings.use_system_mofa === undefined) {
            this.settings.use_system_mofa = this.settings.mofa_mode === 'system'
          }
          
          if (this.settings.docker_container_name === undefined) {
            this.settings.docker_container_name = ''
          }
          
          return this.settings
        } else {
          throw new Error('Failed to fetch settings')
        }
      } catch (error) {
        this.error = error.message || 'Failed to fetch settings'
        console.error(error)
        return null
      } finally {
        this.isLoading = false
      }
    },
    
    async saveSettings(settings) {
      this.isLoading = true
      this.error = null
      try {
        // 保存所有路径到localStorage作为备份
        localStorage.setItem('mofa_dir', settings.mofa_dir || '');
        localStorage.setItem('agent_hub_path', settings.agent_hub_path || '');
        localStorage.setItem('examples_path', settings.examples_path || '');
        localStorage.setItem('custom_agent_hub_path', settings.custom_agent_hub_path || '');
        localStorage.setItem('custom_examples_path', settings.custom_examples_path || '');
        
        const response = await settingsApi.updateSettings(settings)
        if (response.data && response.data.success) {
          this.settings = response.data.settings
          return true
        } else {
          throw new Error('Failed to save settings')
        }
      } catch (error) {
        this.error = error.message || 'Failed to save settings'
        console.error(error)
        return false
      } finally {
        this.isLoading = false
      }
    },
    
    async resetSettings() {
      this.isLoading = true
      this.error = null
      try {
        const response = await settingsApi.resetSettings()
        if (response.data && response.data.success) {
          this.settings = response.data.settings
          return true
        } else {
          throw new Error('Failed to reset settings')
        }
      } catch (error) {
        this.error = error.message || 'Failed to reset settings'
        console.error(error)
        return false
      } finally {
        this.isLoading = false
      }
    }
  }
})
