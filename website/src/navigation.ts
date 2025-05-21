import { getPermalink, getBlogPermalink, getAsset } from './utils/permalinks';
import { translations } from './i18n/translations';
import { getCurrentLanguage } from './utils/i18nConfig';

export function getHeaderData(lang = 'en') {
  function serverT(key: string): string {
    const langKey = lang as keyof typeof translations;
    
    if (translations[langKey] && translations[langKey][key]) {
      return translations[langKey][key];
    }
    
    if (langKey !== 'en' && translations.en && translations.en[key]) {
      return translations.en[key];
    }
    
    return key;
  }

  return {
    links: [
      {
        text: serverT('nav.docs'),
        href: 'https://github.com/moxin-org/mofa/blob/main/README.md',
        target: '_blank',
      },
    ],
    actions: [{ 
      text: serverT('nav.github'), 
      href: 'https://github.com/moxin-org/mofa', 
      target: '_blank',
      icon: 'tabler:brand-github' 
    }],
  };
}

export function getFooterData(lang = 'en') {
  function serverT(key: string): string {
    const langKey = lang as keyof typeof translations;
    
    if (translations[langKey] && translations[langKey][key]) {
      return translations[langKey][key];
    }
    
    if (langKey !== 'en' && translations.en && translations.en[key]) {
      return translations.en[key];
    }
    
    return key;
  }

  return {
    links: [
      {
        title: serverT('footer.docs'),
        links: [
          { text: serverT('nav.quickStart'), href: 'https://github.com/moxin-org/mofa/blob/main/README.md', target: '_blank' },
          { text: serverT('nav.coreConcepts'), href: 'https://github.com/moxin-org/mofa/blob/main/README.md', target: '_blank' },
          { text: serverT('nav.tutorials'), href: 'https://github.com/moxin-org/mofa/blob/main/README.md', target: '_blank' },
          { text: serverT('nav.api'), href: 'https://github.com/moxin-org/mofa/blob/main/README.md', target: '_blank' },
          { text: serverT('nav.installation'), href: 'https://github.com/moxin-org/mofa/blob/main/README.md', target: '_blank' },
        ],
      },
    ],
    secondaryLinks: [
      { text: serverT('footer.terms'), href: 'https://github.com/moxin-org/mofa', target: '_blank' },
      { text: serverT('footer.privacy'), href: 'https://github.com/moxin-org/mofa', target: '_blank' },
    ],
    socialLinks: [
      { ariaLabel: 'GitHub', icon: 'tabler:brand-github', href: 'https://github.com/moxin-org/mofa', target: '_blank' },
    ],
    footNote: `
      <div class="flex items-center">
        <img class="w-5 h-5 md:w-6 md:h-6 md:-mt-0.5 bg-cover mr-1.5 rtl:mr-0 rtl:ml-1.5 float-left rtl:float-right rounded-sm" src="/mofa-logo.png" alt="MoFA logo" loading="lazy"></img>
        <span>© ${new Date().getFullYear()} MoFA.AI · ${serverT('footer.rights')}</span>
      </div>
    `,
  };
}

let currentLang = 'en';
if (typeof window !== 'undefined') {
  const urlParams = new URLSearchParams(window.location.search);
  currentLang = urlParams.get('lang') || localStorage.getItem('language') || 'en';
}

export const headerData = getHeaderData(currentLang);
export const footerData = getFooterData(currentLang);
