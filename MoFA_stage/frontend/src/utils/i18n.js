import { createI18n } from 'vue-i18n'
import { messages } from '../locales'

// Create i18n instance with default locale
export const i18n = createI18n({
  legacy: false,
  locale: localStorage.getItem('language') || 'zh',
  fallbackLocale: 'zh',
  messages
})

// Set language and ensure it's stored in both localStorage and applies immediately
export function setLanguage(lang) {
  // Update i18n locale immediately
  i18n.global.locale.value = lang
  
  // Store in localStorage for persistence
  localStorage.setItem('language', lang)
  
  // Apply language change to document for any CSS-based changes
  document.documentElement.setAttribute('lang', lang)
  
  // Log language change for debugging
  console.log(`Language changed to: ${lang}`)
}

export function getLanguage() {
  return i18n.global.locale.value
}
