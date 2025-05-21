import { I18N as DefaultI18N } from 'astrowind:config';

// Define supported languages
export const LANGUAGES = ['en', 'zh'] as const;
export type Language = typeof LANGUAGES[number];

// Check if a language is supported
export function isValidLanguage(lang: string | null): lang is Language {
  return Boolean(lang && LANGUAGES.includes(lang as Language));
}

// Get language from URL path (for future /en/ or /zh/ style paths)
function getLangFromPath(pathname: string): Language | null {
  const pathSegments = pathname.split('/').filter(Boolean);
  const firstSegment = pathSegments[0];
  return isValidLanguage(firstSegment) ? firstSegment : null;
}

// Get language from URL search params
function getLangFromSearchParams(url: URL | null): Language | null {
  if (!url) return null;
  const urlLang = url.searchParams.get('lang');
  return isValidLanguage(urlLang) ? urlLang : null;
}

// Get language from browser
function getBrowserLanguage(): Language {
  if (typeof navigator === 'undefined') return 'en';
  
  const browserLang = navigator.language.split('-')[0];
  return isValidLanguage(browserLang) ? browserLang : 'en';
}

// Get language from localStorage
function getStoredLanguage(): Language | null {
  if (typeof localStorage === 'undefined') return null;
  
  const storedLang = localStorage.getItem('language');
  return isValidLanguage(storedLang) ? storedLang : null;
}

// Create a function to get the current language with proper fallbacks
export function getCurrentLanguage(url: URL | null = null): Language {
  // Priority:
  // 1. URL search parameter (?lang=xx)
  // 2. URL path (/xx/page) - for future use
  // 3. localStorage
  // 4. Browser language
  // 5. Default language from config
  
  // Check URL search params first (highest priority)
  const urlLang = getLangFromSearchParams(url);
  if (urlLang) return urlLang;
  
  // Check URL path (for future implementation)
  if (url) {
    const pathLang = getLangFromPath(url.pathname);
    if (pathLang) return pathLang;
  }
  
  // Check localStorage
  const storedLang = getStoredLanguage();
  if (storedLang) return storedLang;
  
  // Check browser language
  if (typeof window !== 'undefined') {
    const browserLang = getBrowserLanguage();
    if (browserLang) return browserLang;
  }
  
  // Fall back to default language
  return DefaultI18N.language as Language;
}

// Create an I18N configuration object based on the current URL
export function getI18N(url: URL | null = null) {
  const language = getCurrentLanguage(url);
  
  return {
    ...DefaultI18N,
    language,
    textDirection: 'ltr', // Both English and Chinese use left-to-right
  };
}

// Default export for use in client-side scripts
export default {
  ...DefaultI18N,
  language: 'en', // This will be overridden by client-side logic
}; 