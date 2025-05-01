/**
 * 设置状态管理
 */
import { defineStore } from 'pinia'
import settingsApi from '../api/settings'

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    settings: {
      mofa_env_path: '',
      mofa_dir: '',
      theme: 'light',
      editor_font_size: 14,
      editor_tab_size: 4
    },
    isLoading: false,
    error: null
  }),
  
  actions: {
    async fetchSettings() {
      this.isLoading = true
      this.error = null
      try {
        const response = await settingsApi.getSettings()
        if (response.data && response.data.success) {
          this.settings = response.data.settings
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
