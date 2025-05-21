import { d as createAstro, c as createComponent, m as maybeRenderHead, b as addAttribute, s as spreadAttributes, r as renderComponent, F as Fragment, a as renderTemplate, u as unescapeHTML, e as renderSlot, f as renderScript } from './astro/server_Ba4Od88w.mjs';
import 'kleur/colors';
import { $ as $$Layout } from './Layout_B44eMgnS.mjs';
import { $ as $$Icon, a as $$ToggleTheme } from './ToggleTheme_FEZIKbSa.mjs';
import { $ as $$Logo } from './Logo_aXTM-oPg.mjs';
import 'clsx';
import { twMerge } from 'tailwind-merge';
import { t as trimSlash, g as getHomePermalink, f as getAsset, S as SITE, I as I18N$1, a as getPermalink, b as getBlogPermalink } from './consts_C1AwyY78.mjs';
import './_astro_content_DFSiQrT2.mjs';

const $$Astro$5 = createAstro("https://mofa.ai");
const $$Button = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro$5, $$props, $$slots);
  Astro2.self = $$Button;
  const {
    variant = "secondary",
    target,
    text = Astro2.slots.render("default"),
    icon = "",
    class: className = "",
    type,
    ...rest
  } = Astro2.props;
  const variants = {
    primary: "btn-primary",
    secondary: "btn-secondary",
    tertiary: "btn btn-tertiary",
    link: "cursor-pointer hover:text-primary"
  };
  return renderTemplate`${type === "button" || type === "submit" || type === "reset" ? renderTemplate`${maybeRenderHead()}<button${addAttribute(type, "type")}${addAttribute(twMerge(variants[variant] || "", className), "class")}${spreadAttributes(rest)}>${renderComponent($$result, "Fragment", Fragment, {}, { "default": ($$result2) => renderTemplate`${unescapeHTML(text)}` })}${icon && renderTemplate`${renderComponent($$result, "Icon", $$Icon, { "name": icon, "class": "w-5 h-5 ml-1 -mr-1.5 rtl:mr-1 rtl:-ml-1.5 inline-block" })}`}</button>` : renderTemplate`<a${addAttribute(twMerge(variants[variant] || "", className), "class")}${spreadAttributes(target ? { target, rel: "noopener noreferrer" } : {})}${spreadAttributes(rest)}>${renderComponent($$result, "Fragment", Fragment, {}, { "default": ($$result2) => renderTemplate`${unescapeHTML(text)}` })}${icon && renderTemplate`${renderComponent($$result, "Icon", $$Icon, { "name": icon, "class": "w-5 h-5 ml-1 -mr-1.5 rtl:mr-1 rtl:-ml-1.5 inline-block" })}`}</a>`}`;
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/components/ui/Button.astro", void 0);

const $$Astro$4 = createAstro("https://mofa.ai");
const $$ToggleMenu = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro$4, $$props, $$slots);
  Astro2.self = $$ToggleMenu;
  const {
    label = "Toggle Menu",
    class: className = "flex flex-col h-12 w-12 rounded justify-center items-center cursor-pointer group"
  } = Astro2.props;
  return renderTemplate`${maybeRenderHead()}<button type="button"${addAttribute(className, "class")}${addAttribute(label, "aria-label")} data-aw-toggle-menu> <span class="sr-only">${label}</span> ${renderSlot($$result, $$slots["default"], renderTemplate` <span aria-hidden="true" class="h-0.5 w-6 my-1 rounded-full bg-black dark:bg-white transition ease transform duration-200 opacity-80 group-[.expanded]:rotate-45 group-[.expanded]:translate-y-2.5"></span> <span aria-hidden="true" class="h-0.5 w-6 my-1 rounded-full bg-black dark:bg-white transition ease transform duration-200 opacity-80 group-[.expanded]:opacity-0"></span> <span aria-hidden="true" class="h-0.5 w-6 my-1 rounded-full bg-black dark:bg-white transition ease transform duration-200 opacity-80 group-[.expanded]:-rotate-45 group-[.expanded]:-translate-y-2.5"></span> `)} </button>`;
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/components/common/ToggleMenu.astro", void 0);

const $$LanguageSwitcher = createComponent(($$result, $$props, $$slots) => {
  return renderTemplate`import ${Icon} from 'astro-icon/components';
import ${I18N} from 'astrowind:config';

const ${language} = I18N;
${maybeRenderHead()}<button id="language-switcher" type="button" class="text-muted dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 rounded-lg text-sm p-2.5 inline-flex items-center" aria-label="Switch Language"> ${renderComponent($$result, "Icon", Icon, { "name": language === "en" ? "tabler:language" : "tabler:language", "class": "w-5 h-5" })} <span class="ml-1 rtl:mr-1 rtl:ml-0 font-semibold">${language === "en" ? "\u4E2D\u6587" : "EN"}</span> </button> ${renderScript($$result, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/components/common/LanguageSwitcher.astro?astro&type=script&index=0&lang.ts")}`;
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/components/common/LanguageSwitcher.astro", void 0);

const $$Astro$3 = createAstro("https://mofa.ai");
const $$Header = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro$3, $$props, $$slots);
  Astro2.self = $$Header;
  const {
    id = "header",
    links = [],
    actions = [],
    isSticky = false,
    isDark = false,
    isFullWidth = false,
    showToggleTheme = false,
    showRssFeed = false,
    position = "center"
  } = Astro2.props;
  const currentPath = `/${trimSlash(new URL(Astro2.url).pathname)}`;
  return renderTemplate`${maybeRenderHead()}<header${addAttribute([
    { sticky: isSticky, relative: !isSticky, dark: isDark },
    "top-0 z-40 flex-none mx-auto w-full border-b border-gray-50/0 transition-[opacity] ease-in-out"
  ], "class:list")}${spreadAttributes(isSticky ? { "data-aw-sticky-header": true } : {})}${spreadAttributes(id ? { id } : {})}> <div class="absolute inset-0"></div> <div${addAttribute([
    "relative text-default py-3 px-3 md:px-6 mx-auto w-full",
    {
      "md:flex md:justify-between": position !== "center"
    },
    {
      "md:grid md:grid-cols-3 md:items-center": position === "center"
    },
    {
      "max-w-7xl": !isFullWidth
    }
  ], "class:list")}> <div${addAttribute([{ "mr-auto rtl:mr-0 rtl:ml-auto": position === "right" }, "flex justify-between"], "class:list")}> <a class="flex items-center"${addAttribute(getHomePermalink(), "href")}> ${renderComponent($$result, "Logo", $$Logo, {})} </a> <div class="flex items-center md:hidden"> ${renderComponent($$result, "ToggleMenu", $$ToggleMenu, {})} </div> </div> <nav class="items-center w-full md:w-auto hidden md:flex md:mx-5 text-default overflow-y-auto overflow-x-hidden md:overflow-y-visible md:overflow-x-auto md:justify-self-center" aria-label="Main navigation"> <ul class="flex flex-col md:flex-row md:self-center w-full md:w-auto text-xl md:text-[0.9375rem] tracking-[0.01rem] font-medium md:justify-center"> ${links.map(({ text, href, links: links2 }) => renderTemplate`<li${addAttribute(links2?.length ? "dropdown" : "", "class")}> ${links2?.length ? renderTemplate`${renderComponent($$result, "Fragment", Fragment, {}, { "default": ($$result2) => renderTemplate` <button type="button" class="hover:text-link dark:hover:text-white px-4 py-3 flex items-center whitespace-nowrap"> ${text}${" "} ${renderComponent($$result2, "Icon", $$Icon, { "name": "tabler:chevron-down", "class": "w-3.5 h-3.5 ml-0.5 rtl:ml-0 rtl:mr-0.5 hidden md:inline" })} </button> <ul class="dropdown-menu md:backdrop-blur-md dark:md:bg-dark rounded md:absolute pl-4 md:pl-0 md:hidden font-medium md:bg-white/90 md:min-w-[200px] drop-shadow-xl"> ${links2.map(({ text: text2, href: href2 }) => renderTemplate`<li> <a${addAttribute([
    "first:rounded-t last:rounded-b md:hover:bg-gray-100 hover:text-link dark:hover:text-white dark:hover:bg-gray-700 py-2 px-5 block whitespace-no-wrap",
    { "aw-link-active": href2 === currentPath }
  ], "class:list")}${addAttribute(href2, "href")}> ${text2} </a> </li>`)} </ul> ` })}` : renderTemplate`<a${addAttribute([
    "hover:text-link dark:hover:text-white px-4 py-3 flex items-center whitespace-nowrap",
    { "aw-link-active": href === currentPath }
  ], "class:list")}${addAttribute(href, "href")}> ${text} </a>`} </li>`)} </ul> </nav> <div${addAttribute([
    { "ml-auto rtl:ml-0 rtl:mr-auto": position === "left" },
    "hidden md:self-center md:flex items-center md:mb-0 fixed w-full md:w-auto md:static justify-end left-0 rtl:left-auto rtl:right-0 bottom-0 p-3 md:p-0 md:justify-self-end"
  ], "class:list")}> <div class="items-center flex justify-between w-full md:w-auto"> <div class="flex"> ${showToggleTheme && renderTemplate`${renderComponent($$result, "ToggleTheme", $$ToggleTheme, { "iconClass": "w-6 h-6 md:w-5 md:h-5 md:inline-block" })}`} ${renderComponent($$result, "LanguageSwitcher", $$LanguageSwitcher, {})} ${showRssFeed && renderTemplate`<a class="text-muted dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 rounded-lg text-sm p-2.5 inline-flex items-center" aria-label="RSS Feed"${addAttribute(getAsset("/rss.xml"), "href")}> ${renderComponent($$result, "Icon", $$Icon, { "name": "tabler:rss", "class": "w-5 h-5" })} </a>`} </div> ${actions?.length ? renderTemplate`<span class="ml-4 rtl:ml-0 rtl:mr-4"> ${actions.map((btnProps) => renderTemplate`${renderComponent($$result, "Button", $$Button, { ...btnProps, "class": "ml-2 py-2.5 px-5.5 md:px-6 font-semibold shadow-none text-sm w-auto" })}`)} </span>` : ""} </div> </div> </div> </header>`;
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/components/widgets/Header.astro", void 0);

const $$Astro$2 = createAstro("https://mofa.ai");
const $$Footer = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro$2, $$props, $$slots);
  Astro2.self = $$Footer;
  const { socialLinks = [], secondaryLinks = [], links = [], footNote = "", theme = "light" } = Astro2.props;
  return renderTemplate`${maybeRenderHead()}<footer${addAttribute([{ dark: theme === "dark" }, "relative border-t border-gray-200 dark:border-slate-800 not-prose"], "class:list")}> <div class="dark:bg-dark absolute inset-0 pointer-events-none" aria-hidden="true"></div> <div class="relative max-w-7xl mx-auto px-4 sm:px-6 dark:text-slate-300 intersect-once intersect-quarter intercept-no-queue motion-safe:md:opacity-0 motion-safe:md:intersect:animate-fade"> <div class="grid grid-cols-12 gap-4 gap-y-8 sm:gap-8 py-8 md:py-12"> <div class="col-span-12 lg:col-span-4"> <div class="mb-2"> <a class="inline-block font-bold text-xl"${addAttribute(getHomePermalink(), "href")}>${SITE?.name}</a> </div> <div class="text-sm text-muted flex gap-1"> ${secondaryLinks.map(({ text, href }, index) => renderTemplate`${renderComponent($$result, "Fragment", Fragment, {}, { "default": ($$result2) => renderTemplate`${index !== 0 ? " \xB7 " : ""}<a class="text-muted hover:text-gray-700 dark:text-gray-400 hover:underline transition duration-150 ease-in-out"${addAttribute(href, "href")}>${unescapeHTML(text)}</a> ` })}`)} </div> </div> ${links.map(({ title, links: links2 }) => renderTemplate`<div class="col-span-6 md:col-span-3 lg:col-span-2"> <div class="dark:text-gray-300 font-medium mb-2">${title}</div> ${links2 && Array.isArray(links2) && links2.length > 0 && renderTemplate`<ul class="text-sm"> ${links2.map(({ text, href, ariaLabel }) => renderTemplate`<li class="mb-2"> <a class="text-muted hover:text-gray-700 hover:underline dark:text-gray-400 transition duration-150 ease-in-out"${addAttribute(href, "href")}${addAttribute(ariaLabel, "aria-label")}> ${renderComponent($$result, "Fragment", Fragment, {}, { "default": ($$result2) => renderTemplate`${unescapeHTML(text)}` })} </a> </li>`)} </ul>`} </div>`)} </div> <div class="md:flex md:items-center md:justify-between py-6 md:py-8"> ${socialLinks?.length ? renderTemplate`<ul class="flex mb-4 md:order-1 -ml-2 md:ml-4 md:mb-0 rtl:ml-0 rtl:-mr-2 rtl:md:ml-0 rtl:md:mr-4"> ${socialLinks.map(({ ariaLabel, href, text, icon }) => renderTemplate`<li> <a class="text-muted dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 rounded-lg text-sm p-2.5 inline-flex items-center"${addAttribute(ariaLabel, "aria-label")}${addAttribute(href, "href")}> ${icon && renderTemplate`${renderComponent($$result, "Icon", $$Icon, { "name": icon, "class": "w-5 h-5" })}`} ${renderComponent($$result, "Fragment", Fragment, {}, { "default": ($$result2) => renderTemplate`${unescapeHTML(text)}` })} </a> </li>`)} </ul>` : ""} <div class="text-sm mr-4 dark:text-muted"> ${renderComponent($$result, "Fragment", Fragment, {}, { "default": ($$result2) => renderTemplate`${unescapeHTML(footNote)}` })} </div> </div> </div> </footer>`;
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/components/widgets/Footer.astro", void 0);

const $$Astro$1 = createAstro("https://mofa.ai");
const $$Announcement = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro$1, $$props, $$slots);
  Astro2.self = $$Announcement;
  return renderTemplate`${maybeRenderHead()}<div class="dark text-muted text-sm bg-black dark:bg-transparent dark:border-b dark:border-slate-800 dark:text-slate-400 hidden md:flex gap-1 overflow-hidden px-3 py-2 relative text-ellipsis whitespace-nowrap"> <span class="dark:bg-slate-700 bg-white/40 dark:text-slate-300 font-semibold px-1 py-0.5 text-xs mr-0.5 rtl:mr-0 rtl:ml-0.5 inline-block">NEW</span> <a href="https://astro.build/blog/astro-570/" class="text-muted hover:underline dark:text-slate-400 font-medium">Astro v5.7 is now available! »</a> <a target="_blank" rel="noopener" class="ltr:ml-auto rtl:mr-auto w-[5.6rem] h-[1.25rem] ml-auto bg-contain inline-block bg-[url(https://img.shields.io/github/stars/onwidget/astrowind.svg?style=social&label=Stars&maxAge=86400)]" title="If you like AstroWind, give us a star." href="https://github.com/onwidget/astrowind"></a> </div>`;
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/components/widgets/Announcement.astro", void 0);

const translations = {
  en: {
    // Navigation
    "nav.home": "Home",
    "nav.docs": "Documentation",
    "nav.quickStart": "Quick Start",
    "nav.coreConcepts": "Core Concepts",
    "nav.tutorials": "Tutorials",
    "nav.api": "API Reference",
    "nav.installation": "Installation & CLI",
    "nav.examples": "Examples",
    "nav.helloWorld": "Hello World",
    "nav.rag": "RAG QA",
    "nav.arxiv": "Arxiv Paper Analysis",
    "nav.reflection": "Reflection Agent",
    "nav.multiAgent": "Multi-Agent Collaboration",
    "nav.community": "Community",
    "nav.discord": "Discord",
    "nav.wechat": "WeChat Group",
    "nav.contributing": "Contributing Guide",
    "nav.contributors": "Contributors",
    "nav.blog": "Blog",
    "nav.about": "About",
    "nav.github": "GitHub",
    // Hero section
    "hero.title": "MoFA: Modular Framework for Agent",
    "hero.subtitle": "MoFA is a software framework for building AI agents through composition. With MoFA, AI agents can be built using templates and combined in layers to form more powerful super-agents.",
    "hero.cta.github": "GitHub",
    "hero.cta.learnMore": "Learn More",
    // Core Philosophy
    "core.title": "Core Philosophy:",
    "core.values": "Modularity, Clarity, Composability, Simplicity",
    // Features
    "features.tagline": "Features",
    "features.title": "MoFA Advantages",
    "features.subtitle": "MoFA offers a new way to build AI agents, creating more powerful and flexible intelligent applications through modularization and composition.",
    "features.modularity.title": "Modularity",
    "features.modularity.description": "Modular agent templates and agent services; simple configuration and clear interfaces between modules.",
    "features.clarity.title": "Clarity",
    "features.clarity.description": '"Lego-like" logic for assembling complex systems.',
    "features.composability.title": "Composability",
    "features.composability.description": "Agent applications gain more powerful capabilities and extended functionality through agent composition.",
    "features.simplicity.title": "Simplicity",
    "features.simplicity.description": "Building complex agents becomes a zero-code process.",
    "features.performance.title": "High Performance",
    "features.performance.description": "Agents run in the high-performance, low-latency distributed AI and robotics compute environment DORA-RS, outperforming Python-based environments.",
    "features.diversity.title": "Diversity",
    "features.diversity.description": "MoFA's agent compositions organically combine various capabilities to create more powerful, more comprehensive composite agents.",
    // Design section
    "design.tagline": "Towards AIOS",
    "design.title": "Design Inspired by Unix Philosophy",
    "design.content.title": "Built on Modern Foundations",
    "design.content.description": "Gain a competitive edge by combining cutting-edge AI technology with classic software design principles",
    "design.aios.title": "AIOS Core",
    "design.aios.description": "MoFA provides services such as task planning, memory, action, and Retrieval Augmented Generation (RAG).",
    "design.tools.title": "Practical Tools and Applications",
    "design.tools.description": "Provides common and basic functionality through agent templates.",
    "design.shell.title": "Shell",
    "design.shell.description": "Environment for running agents and automating their processes.",
    // Design Patterns
    "patterns.tagline": "Design Patterns",
    "patterns.title": "Nested Design Patterns for AI Agents",
    "patterns.subtitle": "AI agents are intelligent software applications. Similar to design patterns in object-oriented programming, AI agents have various design patterns, including but not limited to:",
    "patterns.llm.title": "LLM Reasoning",
    "patterns.llm.description": "Using Large Language Models (LLMs) for reasoning is the simplest design pattern.",
    "patterns.prompt.title": "Custom Prompts",
    "patterns.prompt.description": "Customizing system prompts for agents.",
    "patterns.reflection.title": "Reflection Pattern",
    "patterns.reflection.description": "Agents capable of self-examination and improvement.",
    "patterns.actor.title": "Actor Pattern",
    "patterns.actor.description": "Agents capable of using external tools and resources, such as generating code or searching the web.",
    "patterns.react.title": "ReAct Pattern",
    "patterns.react.description": "Combining reflection and tool use to improve output quality.",
    "patterns.multiagent.title": "Multi-Agent Collaboration",
    "patterns.multiagent.description": "Agents assume specialized roles and collaborate to complete complex tasks.",
    // Quick Start
    "quickstart.title": "Quick Start Using MoFA to Build Your AI Agent",
    "quickstart.step1.title": 'Step 1: <span class="font-medium">Installation</span>',
    "quickstart.step1.description": "Clone the MoFA repository from GitHub and follow the installation guide to set up your environment.",
    "quickstart.step2.title": 'Step 2: <span class="font-medium">Choose a Template</span>',
    "quickstart.step2.description": "Select the base template that best fits your needs from MoFA's agent templates.",
    "quickstart.step3.title": 'Step 3: <span class="font-medium">Configure Your Agent</span>',
    "quickstart.step3.description": "Customize your agent's capabilities, behaviors, and interaction style according to your needs.",
    "quickstart.step4.title": 'Step 4: <span class="font-medium">Compose Agents</span>',
    "quickstart.step4.description": "Combine multiple agents together to create more powerful super-agents.",
    "quickstart.complete": "Complete!",
    // FAQ
    "faq.tagline": "FAQ",
    "faq.title": "Frequently Asked Questions",
    "faq.subtitle": "Have questions about MoFA? Here are answers to some common questions.",
    "faq.difference.title": "How is MoFA different from other agent frameworks?",
    "faq.difference.description": "MoFA's uniqueness lies in its modular and compositional approach. It allows developers to build AI agents like Lego blocks without needing to understand complex underlying technologies. Additionally, MoFA is based on the high-performance DORA-RS framework, offering better performance than traditional Python frameworks.",
    "faq.knowledge.title": "How much programming knowledge do I need to use MoFA?",
    "faq.knowledge.description": "MoFA is designed to lower the barrier to building AI agents. While basic programming knowledge is helpful, MoFA's template system and compositional approach make it possible for users with limited programming experience to create powerful agents.",
    "faq.models.title": "What types of AI models does MoFA support?",
    "faq.models.description": "MoFA is designed to be model-agnostic, supporting various Large Language Models (LLMs) and other AI models. It can be used with popular models like the GPT series, Claude, Llama, etc., and can be easily extended to support new models.",
    "faq.contribute.title": "How can I contribute to the MoFA project?",
    "faq.contribute.description": "MoFA is an open-source project, and community contributions are welcome. You can submit issues and pull requests through GitHub or join our Discord community to participate in discussions. We especially welcome new agent templates, core functionality improvements, and documentation contributions.",
    "faq.applications.title": "What types of applications is MoFA suitable for?",
    "faq.applications.description": "MoFA is suitable for a wide range of applications, including but not limited to: customer service automation, content creation and management, data analysis, personal assistants, educational tools, game AI, etc. Any application requiring intelligent interaction and decision-making can benefit from MoFA.",
    // Call to action
    "cta.title": "Ready to build the next generation of AI agents?",
    "cta.subtitle": "Join the MoFA community and start your journey in modular agent building.",
    "cta.getStarted": "Get Started",
    "cta.github": "GitHub",
    // Footer
    "footer.docs": "Documentation",
    "footer.examples": "Examples",
    "footer.community": "Community",
    "footer.about": "About",
    "footer.origins": "Project Origins",
    "footer.team": "Team Background",
    "footer.moxin": "Moxin Community",
    "footer.contact": "Contact Us",
    "footer.terms": "Terms",
    "footer.privacy": "Privacy Policy",
    "footer.rights": "All rights reserved"
  },
  zh: {
    // Navigation
    "nav.home": "首页",
    "nav.docs": "文档",
    "nav.quickStart": "快速开始",
    "nav.coreConcepts": "核心概念",
    "nav.tutorials": "教程指南",
    "nav.api": "API参考",
    "nav.installation": "安装与CLI",
    "nav.examples": "示例项目",
    "nav.helloWorld": "Hello World",
    "nav.rag": "RAG文档问答",
    "nav.arxiv": "Arxiv Paper分析",
    "nav.reflection": "反思Agent",
    "nav.multiAgent": "多智能体协作",
    "nav.community": "社区",
    "nav.discord": "Discord",
    "nav.wechat": "微信群",
    "nav.contributing": "贡献指南",
    "nav.contributors": "贡献者榜",
    "nav.blog": "博客",
    "nav.about": "关于",
    "nav.github": "GitHub",
    // Hero section
    "hero.title": "MoFA: 模块化代理框架",
    "hero.subtitle": "MoFA (Modular Framework for Agent) 是一个通过组合方式构建AI代理的软件框架。使用MoFA，AI代理可以通过模板构建并分层组合，形成更强大的超级代理。",
    "hero.cta.github": "GitHub",
    "hero.cta.learnMore": "了解更多",
    // Core Philosophy
    "core.title": "核心理念:",
    "core.values": "模块化、清晰性、组合性、简单性",
    // Features
    "features.tagline": "特点",
    "features.title": "MoFA的优势",
    "features.subtitle": "MoFA提供了构建AI代理的全新方式，通过模块化和组合方式创建更强大、更灵活的智能应用。",
    "features.modularity.title": "模块化",
    "features.modularity.description": "模块化的代理模板和代理服务；模块之间简单配置和清晰的接口。",
    "features.clarity.title": "清晰性",
    "features.clarity.description": '类似"乐高积木"的逻辑，用于组装复杂系统。',
    "features.composability.title": "组合性",
    "features.composability.description": "代理应用通过组合代理获得更强大的能力和扩展功能。",
    "features.simplicity.title": "简单性",
    "features.simplicity.description": "构建复杂代理变成零代码过程。",
    "features.performance.title": "高性能",
    "features.performance.description": "代理在高性能、低延迟的分布式AI和机器人计算环境DORA-RS中运行，性能优于基于Python的环境。",
    "features.diversity.title": "多样性",
    "features.diversity.description": "MoFA的代理组合有机地结合各种能力，创造更强大、更全面的复合代理。",
    // Design section
    "design.tagline": "走向AIOS",
    "design.title": "受Unix哲学启发的设计",
    "design.content.title": "构建在现代基础上",
    "design.content.description": "通过结合前沿AI技术和经典软件设计原则，获得竞争优势",
    "design.aios.title": "AIOS核心",
    "design.aios.description": "MoFA提供任务规划、记忆、行动和检索增强生成（RAG）等服务。",
    "design.tools.title": "实用工具和应用",
    "design.tools.description": "通过代理模板提供通用和基础功能。",
    "design.shell.title": "Shell",
    "design.shell.description": "运行代理和自动化其流程的环境。",
    // Design Patterns
    "patterns.tagline": "设计模式",
    "patterns.title": "AI代理的嵌套设计模式",
    "patterns.subtitle": "AI代理是智能软件应用。类似于面向对象编程中的设计模式，AI代理有各种设计模式，包括但不限于：",
    "patterns.llm.title": "LLM推理",
    "patterns.llm.description": "使用大型语言模型(LLMs)进行推理是最简单的设计模式。",
    "patterns.prompt.title": "自定义提示",
    "patterns.prompt.description": "为代理定制系统提示。",
    "patterns.reflection.title": "反思模式",
    "patterns.reflection.description": "能够自我审查和改进的代理。",
    "patterns.actor.title": "行动者模式",
    "patterns.actor.description": "能够使用外部工具和资源的代理，如生成代码或搜索网络。",
    "patterns.react.title": "ReAct模式",
    "patterns.react.description": "结合反思和工具使用，提高输出质量。",
    "patterns.multiagent.title": "多代理协作",
    "patterns.multiagent.description": "代理承担专门角色并协作完成复杂任务。",
    // Quick Start
    "quickstart.title": "快速开始使用MoFA构建你的AI代理",
    "quickstart.step1.title": '步骤 1: <span class="font-medium">安装</span>',
    "quickstart.step1.description": "从GitHub克隆MoFA仓库，并按照安装指南设置环境。",
    "quickstart.step2.title": '步骤 2: <span class="font-medium">选择模板</span>',
    "quickstart.step2.description": "从MoFA提供的代理模板中选择最适合你需求的基础模板。",
    "quickstart.step3.title": '步骤 3: <span class="font-medium">配置代理</span>',
    "quickstart.step3.description": "根据你的需求自定义代理的能力、行为和交互方式。",
    "quickstart.step4.title": '步骤 4: <span class="font-medium">组合代理</span>',
    "quickstart.step4.description": "将多个代理组合在一起，创建功能更强大的超级代理。",
    "quickstart.complete": "完成!",
    // FAQ
    "faq.tagline": "FAQ",
    "faq.title": "常见问题",
    "faq.subtitle": "对MoFA有疑问？这里是一些常见问题的解答。",
    "faq.difference.title": "MoFA与其他代理框架有什么不同？",
    "faq.difference.description": "MoFA的独特之处在于其模块化和组合方法。它允许开发者像搭建乐高积木一样构建AI代理，无需深入了解复杂的底层技术。此外，MoFA基于高性能的DORA-RS框架，提供比传统Python框架更好的性能。",
    "faq.knowledge.title": "我需要多少编程知识才能使用MoFA？",
    "faq.knowledge.description": "MoFA旨在降低构建AI代理的门槛。虽然基本的编程知识会有所帮助，但MoFA的模板系统和组合方法使得即使是编程经验有限的用户也能创建功能强大的代理。",
    "faq.models.title": "MoFA支持哪些类型的AI模型？",
    "faq.models.description": "MoFA设计为模型不可知的，支持各种大型语言模型（LLM）和其他AI模型。它可以与流行的模型如GPT系列、Claude、Llama等一起使用，并且可以轻松扩展以支持新的模型。",
    "faq.contribute.title": "如何为MoFA项目做贡献？",
    "faq.contribute.description": "MoFA是一个开源项目，欢迎社区贡献。你可以通过GitHub提交问题和拉取请求，或者加入我们的Discord社区参与讨论。我们特别欢迎新的代理模板、核心功能改进和文档贡献。",
    "faq.applications.title": "MoFA适合什么类型的应用？",
    "faq.applications.description": "MoFA适用于广泛的应用场景，包括但不限于：客户服务自动化、内容创建和管理、数据分析、个人助手、教育工具、游戏AI等。任何需要智能交互和决策的应用都可以从MoFA中受益。",
    // Call to action
    "cta.title": "准备好构建下一代AI代理了吗？",
    "cta.subtitle": "加入MoFA社区，开始你的模块化代理构建之旅。",
    "cta.getStarted": "开始使用",
    "cta.github": "GitHub",
    // Footer
    "footer.docs": "文档",
    "footer.examples": "示例项目",
    "footer.community": "社区",
    "footer.about": "关于",
    "footer.origins": "项目缘起",
    "footer.team": "团队背景",
    "footer.moxin": "Moxin社区",
    "footer.contact": "联系我们",
    "footer.terms": "条款",
    "footer.privacy": "隐私政策",
    "footer.rights": "保留所有权利"
  }
};

function t(key) {
  const { language } = I18N$1;
  const currentLang = language;
  if (translations[currentLang] && translations[currentLang][key]) {
    return translations[currentLang][key];
  }
  return key;
}
function getCurrentLanguage() {
  if (typeof document !== "undefined") {
    return document.documentElement.lang || I18N$1.language;
  }
  return I18N$1.language;
}

const headerData = {
  links: [
    {
      text: t("nav.home"),
      href: getPermalink("/")
    },
    {
      text: t("nav.docs"),
      links: [
        {
          text: t("nav.quickStart"),
          href: getPermalink("/docs/getting-started")
        },
        {
          text: t("nav.coreConcepts"),
          href: getPermalink("/docs/core-concepts")
        },
        {
          text: t("nav.tutorials"),
          href: getPermalink("/docs/tutorials")
        },
        {
          text: t("nav.api"),
          href: getPermalink("/docs/api")
        },
        {
          text: t("nav.installation"),
          href: getPermalink("/docs/installation")
        }
      ]
    },
    {
      text: t("nav.examples"),
      links: [
        {
          text: t("nav.helloWorld"),
          href: getPermalink("/examples/hello-world")
        },
        {
          text: t("nav.rag"),
          href: getPermalink("/examples/rag")
        },
        {
          text: t("nav.arxiv"),
          href: getPermalink("/examples/arxiv")
        },
        {
          text: t("nav.reflection"),
          href: getPermalink("/examples/reflection")
        },
        {
          text: t("nav.multiAgent"),
          href: getPermalink("/examples/multi-agent")
        }
      ]
    },
    {
      text: t("nav.community"),
      links: [
        {
          text: t("nav.discord"),
          href: "https://discord.gg/mofa",
          target: "_blank"
        },
        {
          text: t("nav.wechat"),
          href: getPermalink("/community/wechat")
        },
        {
          text: t("nav.contributing"),
          href: getPermalink("/community/contributing")
        },
        {
          text: t("nav.contributors"),
          href: getPermalink("/community/contributors")
        },
        {
          text: t("nav.blog"),
          href: getBlogPermalink()
        }
      ]
    },
    {
      text: t("nav.about"),
      href: getPermalink("/about")
    }
  ],
  actions: [{ text: t("nav.github"), href: "https://github.com/moxin-org/mofa", target: "_blank" }]
};
const footerData = {
  links: [
    {
      title: t("footer.docs"),
      links: [
        { text: t("nav.quickStart"), href: getPermalink("/docs/getting-started") },
        { text: t("nav.coreConcepts"), href: getPermalink("/docs/core-concepts") },
        { text: t("nav.tutorials"), href: getPermalink("/docs/tutorials") },
        { text: t("nav.api"), href: getPermalink("/docs/api") },
        { text: t("nav.installation"), href: getPermalink("/docs/installation") }
      ]
    },
    {
      title: t("footer.examples"),
      links: [
        { text: t("nav.helloWorld"), href: getPermalink("/examples/hello-world") },
        { text: t("nav.rag"), href: getPermalink("/examples/rag") },
        { text: t("nav.arxiv"), href: getPermalink("/examples/arxiv") },
        { text: t("nav.reflection"), href: getPermalink("/examples/reflection") },
        { text: t("nav.multiAgent"), href: getPermalink("/examples/multi-agent") }
      ]
    },
    {
      title: t("footer.community"),
      links: [
        { text: t("nav.discord"), href: "https://discord.gg/mofa", target: "_blank" },
        { text: t("nav.wechat"), href: getPermalink("/community/wechat") },
        { text: t("nav.contributing"), href: getPermalink("/community/contributing") },
        { text: t("nav.contributors"), href: getPermalink("/community/contributors") },
        { text: t("nav.blog"), href: getBlogPermalink() }
      ]
    },
    {
      title: t("footer.about"),
      links: [
        { text: t("footer.origins"), href: getPermalink("/about") },
        { text: t("footer.team"), href: getPermalink("/about#team") },
        { text: t("footer.moxin"), href: "https://moxin.ai", target: "_blank" },
        { text: t("footer.contact"), href: getPermalink("/contact") }
      ]
    }
  ],
  secondaryLinks: [
    { text: t("footer.terms"), href: getPermalink("/terms") },
    { text: t("footer.privacy"), href: getPermalink("/privacy") }
  ],
  socialLinks: [
    { ariaLabel: "GitHub", icon: "tabler:brand-github", href: "https://github.com/moxin-org/mofa" },
    { ariaLabel: "Discord", icon: "tabler:brand-discord", href: "https://discord.gg/mofa" },
    { ariaLabel: "RSS", icon: "tabler:rss", href: getAsset("/rss.xml") }
  ],
  footNote: `
    <div class="flex items-center">
      <img class="w-5 h-5 md:w-6 md:h-6 md:-mt-0.5 bg-cover mr-1.5 rtl:mr-0 rtl:ml-1.5 float-left rtl:float-right rounded-sm" src="/mofa-logo.png" alt="MoFA logo" loading="lazy"></img>
      <span>© ${(/* @__PURE__ */ new Date()).getFullYear()} MoFA.AI · ${t("footer.rights")}</span>
    </div>
  `
};

const $$Astro = createAstro("https://mofa.ai");
const $$PageLayout = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$PageLayout;
  const { metadata } = Astro2.props;
  return renderTemplate`${renderComponent($$result, "Layout", $$Layout, { "metadata": metadata }, { "default": ($$result2) => renderTemplate` ${renderSlot($$result2, $$slots["announcement"], renderTemplate` ${renderComponent($$result2, "Announcement", $$Announcement, {})} `)} ${renderSlot($$result2, $$slots["header"], renderTemplate` ${renderComponent($$result2, "Header", $$Header, { ...headerData, "isSticky": true, "showRssFeed": true, "showToggleTheme": true })} `)} ${maybeRenderHead()}<main> ${renderSlot($$result2, $$slots["default"])} </main> ${renderSlot($$result2, $$slots["footer"], renderTemplate` ${renderComponent($$result2, "Footer", $$Footer, { ...footerData })} `)} ` })}`;
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/layouts/PageLayout.astro", void 0);

export { $$PageLayout as $, $$Button as a, $$Header as b, getCurrentLanguage as g, headerData as h, t };
