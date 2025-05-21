import { translations } from './translations';
import { I18N } from 'astrowind:config';

/**
 * Get a translation string based on the key and current language
 * @param key The translation key
 * @returns The translated string or the key if not found
 */
export function t(key: string): string {
  // 获取当前语言 - 在服务器端，尝试从Astro.url获取
  let currentLang: string;
  
  // 检查是否在浏览器环境
  if (typeof document !== 'undefined') {
    // 客户端：优先从URL获取，其次从localStorage，最后从HTML或配置获取
    const urlParams = new URLSearchParams(window.location.search);
    currentLang = urlParams.get('lang') || localStorage.getItem('language') || document.documentElement.lang || I18N.language;
  } else {
    // 服务器端：使用配置的默认语言
    currentLang = I18N.language;
  }
  
  // 确保currentLang是translations中的有效键
  const langKey = currentLang as keyof typeof translations;
  
  // 尝试获取当前语言的翻译
  if (translations[langKey] && translations[langKey][key]) {
    return translations[langKey][key];
  }
  
  // 回退到英语
  if (langKey !== 'en' && translations.en && translations.en[key]) {
    return translations.en[key];
  }
  
  // 如果找不到翻译，返回键名
  return key;
}

/**
 * Get the current language from HTML or config
 * @returns The current language code
 */
export function getCurrentLanguage(): string {
  if (typeof document !== 'undefined') {
    // 客户端：优先从URL获取，其次从localStorage，最后从HTML或配置获取
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('lang') || localStorage.getItem('language') || document.documentElement.lang || I18N.language;
  }
  return I18N.language;
}

/**
 * Check if the current language is the specified language
 * @param lang Language code to check
 * @returns True if current language matches
 */
export function isCurrentLanguage(lang: string): boolean {
  return getCurrentLanguage() === lang;
} 