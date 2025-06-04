import { prependForwardSlash } from '@astrojs/internal-helpers/path';
import { c as createAstro, a as createComponent, r as renderTemplate, m as maybeRenderHead, b as addAttribute, d as renderHead, e as renderComponent, f as renderSlot, A as AstroError, U as UnknownContentCollectionError, g as renderUniqueStylesheet, h as renderScriptElement, i as createHeadAndContent, u as unescapeHTML } from '../astro.7f8fc68a.js';
import 'clsx';
/* empty css                           */
const $$Astro$4 = createAstro("https://moxin-org.github.io");
const $$Header = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro$4, $$props, $$slots);
  Astro2.self = $$Header;
  const navItems = [
    { name: "\u6587\u6863", href: "/docs" },
    { name: "\u793A\u4F8B", href: "/examples" },
    { name: "\u535A\u5BA2", href: "/blog" },
    { name: "\u793E\u533A", href: "/community" },
    { name: "\u5173\u4E8E", href: "/about" }
  ];
  const { base } = (Object.assign({"BASE_URL":"/mofa","MODE":"production","DEV":false,"PROD":true,"SSR":true,"SITE":"https://moxin-org.github.io","ASSETS_PREFIX":undefined},{_:process.env._,}));
  const currentPath = Astro2.url.pathname.replace(base, "");
  return renderTemplate`${maybeRenderHead()}<header class="sticky top-0 z-50 bg-white border-b-4 border-mondrian-black shadow-sm"> <nav class="container mx-auto px-4 py-4"> <div class="flex items-center justify-between"> <!-- Logo with Mondrian-style blocks --> <a${addAttribute(`${base}/`, "href")} class="flex items-center space-x-2 group"> <div class="w-10 h-10 relative overflow-hidden rounded-md transition-all duration-300 group-hover:scale-110 group-hover:shadow-lg"> <img${addAttribute(`${base}/mofa-logo.png`, "src")} alt="MoFA Logo" class="w-full h-full object-cover rounded-md"> <!-- 保留悬浮效果 --> <div class="absolute inset-0 bg-gradient-to-br from-transparent via-white/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div> </div> <span class="text-2xl font-bold gradient-text">MoFA</span> </a> <!-- Navigation Menu --> <div class="hidden md:flex items-center space-x-8"> ${navItems.map((item) => renderTemplate`<a${addAttribute(`${base}${item.href}`, "href")}${addAttribute(currentPath.startsWith(item.href) ? "nav-link-active" : "nav-link", "class")}> ${item.name} </a>`)} <a href="https://github.com/moxin-org/mofa" target="_blank" rel="noopener noreferrer" class="btn-primary text-sm"> <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24"> <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"></path> </svg>
GitHub
</a> </div> <!-- Mobile menu button --> <button class="md:hidden p-2 rounded-md hover:bg-mondrian-gray"> <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"> <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path> </svg> </button> </div> </nav> </header>`;
}, "/Users/liyao/Code/mofa/mofa-website/src/components/Header.astro", void 0);

const $$Footer = createComponent(($$result, $$props, $$slots) => {
  const currentYear = (/* @__PURE__ */ new Date()).getFullYear();
  const { base } = (Object.assign({"BASE_URL":"/mofa","MODE":"production","DEV":false,"PROD":true,"SSR":true,"SITE":"https://moxin-org.github.io","ASSETS_PREFIX":undefined},{_:process.env._,}));
  const footerLinks = {
    \u4EA7\u54C1: [
      { name: "\u6587\u6863", href: "/docs" },
      { name: "\u793A\u4F8B", href: "/examples" },
      { name: "API \u53C2\u8003", href: "/docs/api" },
      { name: "\u5FEB\u901F\u5F00\u59CB", href: "/docs/quick-start" }
    ],
    \u793E\u533A: [
      { name: "GitHub", href: "https://github.com/moxin-org/mofa", external: true },
      { name: "Discord", href: "https://discord.gg/mofatesttesttesttesttsets", external: true },
      { name: "\u8D21\u732E\u6307\u5357", href: "/community/contributing" },
      { name: "\u535A\u5BA2", href: "/blog" }
    ],
    \u516C\u53F8: [
      { name: "\u5173\u4E8E\u6211\u4EEC", href: "/about" },
      { name: "Moxin", href: "https://moxin.io", external: true },
      { name: "\u62DB\u8058", href: "/about#careers" },
      { name: "\u8054\u7CFB\u6211\u4EEC", href: "/about#contact" }
    ]
  };
  return renderTemplate`${maybeRenderHead()}<footer class="bg-mondrian-black text-white mt-16"> <div class="container mx-auto px-4 py-12"> <!-- Footer Grid with Mondrian-inspired layout --> <div class="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8"> <!-- Company Info --> <div class="md:col-span-1"> <div class="flex items-center space-x-2 mb-4"> <div class="w-8 h-8 rounded-md overflow-hidden"> <img${addAttribute(`${base}/mofa-logo.png`, "src")} alt="MoFA Logo" class="w-full h-full object-cover"> </div> <span class="text-xl font-bold">MoFA</span> </div> <p class="text-gray-400 text-sm">
让普通开发者成为全栈 AI 工程师
</p> <p class="text-gray-400 text-sm mt-2">
Make Ordinary Developers Full-stack AI Engineers
</p> </div> <!-- Footer Links --> ${Object.entries(footerLinks).map(([category, links]) => renderTemplate`<div> <h4 class="font-semibold mb-4 text-mondrian-yellow">${category}</h4> <ul class="space-y-2"> ${links.map((link) => renderTemplate`<li> <a${addAttribute(link.external ? link.href : `${base}${link.href}`, "href")}${addAttribute(link.external ? "_blank" : void 0, "target")}${addAttribute(link.external ? "noopener noreferrer" : void 0, "rel")} class="text-gray-400 hover:text-white transition-colors duration-200 text-sm"> ${link.name} </a> </li>`)} </ul> </div>`)} </div> <!-- Bottom Bar --> <div class="border-t border-gray-800 pt-8"> <div class="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0"> <p class="text-gray-400 text-sm">
&copy; ${currentYear} MoFA. All rights reserved. | Powered by <a href="https://moxin.io" target="_blank" rel="noopener noreferrer" class="hover:text-mondrian-yellow transition-colors">Moxin</a> </p> <div class="flex space-x-6"> <a href="https://github.com/moxin-org/mofa" target="_blank" rel="noopener noreferrer" class="text-gray-400 hover:text-white transition-colors"> <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"> <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"></path> </svg> </a> <a href="https://discord.gg/mofa" target="_blank" rel="noopener noreferrer" class="text-gray-400 hover:text-white transition-colors"> <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"> <path d="M20.317 4.3698a19.7913 19.7913 0 00-4.8851-1.5152.0741.0741 0 00-.0785.0371c-.211.3753-.4447.8648-.6083 1.2495-1.8447-.2762-3.68-.2762-5.4868 0-.1636-.3933-.4058-.8742-.6177-1.2495a.077.077 0 00-.0785-.037 19.7363 19.7363 0 00-4.8852 1.515.0699.0699 0 00-.0321.0277C.5334 9.0458-.319 13.5799.0992 18.0578a.0824.0824 0 00.0312.0561c2.0528 1.5076 4.0413 2.4228 5.9929 3.0294a.0777.0777 0 00.0842-.0276c.4616-.6304.8731-1.2952 1.226-1.9942a.076.076 0 00-.0416-.1057c-.6528-.2476-1.2743-.5495-1.8722-.8923a.077.077 0 01-.0076-.1277c.1258-.0943.2517-.1923.3718-.2914a.0743.0743 0 01.0776-.0105c3.9278 1.7933 8.18 1.7933 12.0614 0a.0739.0739 0 01.0785.0095c.1202.099.246.1981.3728.2924a.077.077 0 01-.0066.1276 12.2986 12.2986 0 01-1.873.8914.0766.0766 0 00-.0407.1067c.3604.698.7719 1.3628 1.225 1.9932a.076.076 0 00.0842.0286c1.961-.6067 3.9495-1.5219 6.0023-3.0294a.077.077 0 00.0313-.0552c.5004-5.177-.8382-9.6739-3.5485-13.6604a.061.061 0 00-.0312-.0286zM8.02 15.3312c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9555-2.4189 2.157-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.9555 2.4189-2.1569 2.4189zm7.9748 0c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9554-2.4189 2.1569-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.946 2.4189-2.1568 2.4189z"></path> </svg> </a> </div> </div> </div> </div> </footer>`;
}, "/Users/liyao/Code/mofa/mofa-website/src/components/Footer.astro", void 0);

const $$Astro$3 = createAstro("https://moxin-org.github.io");
const $$BaseLayout = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro$3, $$props, $$slots);
  Astro2.self = $$BaseLayout;
  const { title, description = "MoFA - Make Ordinary Developers Full-stack AI Engineers" } = Astro2.props;
  const { base } = (Object.assign({"BASE_URL":"/mofa","MODE":"production","DEV":false,"PROD":true,"SSR":true,"SITE":"https://moxin-org.github.io","ASSETS_PREFIX":undefined},{}));
  return renderTemplate`<html lang="zh-CN"> <head><meta charset="UTF-8"><meta name="description"${addAttribute(description, "content")}><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="icon" type="image/png"${addAttribute(`${base}/favicon-32x32.png`, "href")}><link rel="shortcut icon"${addAttribute(`${base}/favicon-32x32.png`, "href")}><link rel="apple-touch-icon"${addAttribute(`${base}/apple-touch-icon.png`, "href")}><link rel="icon" type="image/png" sizes="16x16"${addAttribute(`${base}/favicon-16x16.png`, "href")}><link rel="icon" type="image/png" sizes="32x32"${addAttribute(`${base}/favicon-32x32.png`, "href")}><link rel="icon" type="image/png" sizes="48x48"${addAttribute(`${base}/favicon-48x48.png`, "href")}><meta name="generator"${addAttribute(Astro2.generator, "content")}><title>${title} | MoFA</title>${renderHead()}</head> <body> ${renderComponent($$result, "Header", $$Header, {})} <main class="flex-grow"> ${renderSlot($$result, $$slots["default"])} </main> ${renderComponent($$result, "Footer", $$Footer, {})} </body></html>`;
}, "/Users/liyao/Code/mofa/mofa-website/src/layouts/BaseLayout.astro", void 0);

function createCollectionToGlobResultMap({
  globResult,
  contentDir
}) {
  const collectionToGlobResultMap = {};
  for (const key in globResult) {
    const keyRelativeToContentDir = key.replace(new RegExp(`^${contentDir}`), "");
    const segments = keyRelativeToContentDir.split("/");
    if (segments.length <= 1)
      continue;
    const collection = segments[0];
    collectionToGlobResultMap[collection] ??= {};
    collectionToGlobResultMap[collection][key] = globResult[key];
  }
  return collectionToGlobResultMap;
}
const cacheEntriesByCollection = /* @__PURE__ */ new Map();
function createGetCollection({
  contentCollectionToEntryMap,
  dataCollectionToEntryMap,
  getRenderEntryImport
}) {
  return async function getCollection(collection, filter) {
    let type;
    if (collection in contentCollectionToEntryMap) {
      type = "content";
    } else if (collection in dataCollectionToEntryMap) {
      type = "data";
    } else {
      console.warn(
        `The collection **${collection}** does not exist or is empty. Ensure a collection directory with this name exists.`
      );
      return;
    }
    const lazyImports = Object.values(
      type === "content" ? contentCollectionToEntryMap[collection] : dataCollectionToEntryMap[collection]
    );
    let entries = [];
    if (!(Object.assign({"BASE_URL":"/mofa","MODE":"production","DEV":false,"PROD":true,"SSR":true,"SITE":"https://moxin-org.github.io","ASSETS_PREFIX":undefined},{_:process.env._,}))?.DEV && cacheEntriesByCollection.has(collection)) {
      entries = [...cacheEntriesByCollection.get(collection)];
    } else {
      entries = await Promise.all(
        lazyImports.map(async (lazyImport) => {
          const entry = await lazyImport();
          return type === "content" ? {
            id: entry.id,
            slug: entry.slug,
            body: entry.body,
            collection: entry.collection,
            data: entry.data,
            async render() {
              return render({
                collection: entry.collection,
                id: entry.id,
                renderEntryImport: await getRenderEntryImport(collection, entry.slug)
              });
            }
          } : {
            id: entry.id,
            collection: entry.collection,
            data: entry.data
          };
        })
      );
      cacheEntriesByCollection.set(collection, entries);
    }
    if (typeof filter === "function") {
      return entries.filter(filter);
    } else {
      return entries;
    }
  };
}
async function render({
  collection,
  id,
  renderEntryImport
}) {
  const UnexpectedRenderError = new AstroError({
    ...UnknownContentCollectionError,
    message: `Unexpected error while rendering ${String(collection)} \u2192 ${String(id)}.`
  });
  if (typeof renderEntryImport !== "function")
    throw UnexpectedRenderError;
  const baseMod = await renderEntryImport();
  if (baseMod == null || typeof baseMod !== "object")
    throw UnexpectedRenderError;
  const { default: defaultMod } = baseMod;
  if (isPropagatedAssetsModule(defaultMod)) {
    const { collectedStyles, collectedLinks, collectedScripts, getMod } = defaultMod;
    if (typeof getMod !== "function")
      throw UnexpectedRenderError;
    const propagationMod = await getMod();
    if (propagationMod == null || typeof propagationMod !== "object")
      throw UnexpectedRenderError;
    const Content = createComponent({
      factory(result, baseProps, slots) {
        let styles = "", links = "", scripts = "";
        if (Array.isArray(collectedStyles)) {
          styles = collectedStyles.map((style) => {
            return renderUniqueStylesheet(result, {
              type: "inline",
              content: style
            });
          }).join("");
        }
        if (Array.isArray(collectedLinks)) {
          links = collectedLinks.map((link) => {
            return renderUniqueStylesheet(result, {
              type: "external",
              src: prependForwardSlash(link)
            });
          }).join("");
        }
        if (Array.isArray(collectedScripts)) {
          scripts = collectedScripts.map((script) => renderScriptElement(script)).join("");
        }
        let props = baseProps;
        if (id.endsWith("mdx")) {
          props = {
            components: propagationMod.components ?? {},
            ...baseProps
          };
        }
        return createHeadAndContent(
          unescapeHTML(styles + links + scripts),
          renderTemplate`${renderComponent(
            result,
            "Content",
            propagationMod.Content,
            props,
            slots
          )}`
        );
      },
      propagation: "self"
    });
    return {
      Content,
      headings: propagationMod.getHeadings?.() ?? [],
      remarkPluginFrontmatter: propagationMod.frontmatter ?? {}
    };
  } else if (baseMod.Content && typeof baseMod.Content === "function") {
    return {
      Content: baseMod.Content,
      headings: baseMod.getHeadings?.() ?? [],
      remarkPluginFrontmatter: baseMod.frontmatter ?? {}
    };
  } else {
    throw UnexpectedRenderError;
  }
}
function isPropagatedAssetsModule(module) {
  return typeof module === "object" && module != null && "__astroPropagation" in module;
}

// astro-head-inject

const contentDir = '/src/content/';

const contentEntryGlob = /* #__PURE__ */ Object.assign({"/src/content/blog/introducing-mofa.md": () => import('../introducing-mofa.4c354880.js'),"/src/content/docs/quick-start.md": () => import('../quick-start.eaddd0f2.js')});
const contentCollectionToEntryMap = createCollectionToGlobResultMap({
	globResult: contentEntryGlob,
	contentDir,
});

const dataEntryGlob = /* #__PURE__ */ Object.assign({});
const dataCollectionToEntryMap = createCollectionToGlobResultMap({
	globResult: dataEntryGlob,
	contentDir,
});
createCollectionToGlobResultMap({
	globResult: { ...contentEntryGlob, ...dataEntryGlob },
	contentDir,
});

let lookupMap = {};
lookupMap = {"blog":{"type":"content","entries":{"introducing-mofa":"/src/content/blog/introducing-mofa.md"}},"docs":{"type":"content","entries":{"quick-start":"/src/content/docs/quick-start.md"}}};

function createGlobLookup(glob) {
	return async (collection, lookupId) => {
		const filePath = lookupMap[collection]?.entries[lookupId];

		if (!filePath) return undefined;
		return glob[collection][filePath];
	};
}

const renderEntryGlob = /* #__PURE__ */ Object.assign({"/src/content/blog/introducing-mofa.md": () => import('../introducing-mofa.da19adf4.js'),"/src/content/docs/quick-start.md": () => import('../quick-start.d57f25a3.js')});
const collectionToRenderEntryMap = createCollectionToGlobResultMap({
	globResult: renderEntryGlob,
	contentDir,
});

const getCollection = createGetCollection({
	contentCollectionToEntryMap,
	dataCollectionToEntryMap,
	getRenderEntryImport: createGlobLookup(collectionToRenderEntryMap),
});

const $$Astro$2 = createAstro("https://moxin-org.github.io");
async function getStaticPaths$1() {
  const posts = await getCollection("blog");
  return posts.map((post) => ({
    params: { slug: post.slug },
    props: { post }
  }));
}
const $$$1 = createComponent(async ($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro$2, $$props, $$slots);
  Astro2.self = $$$1;
  const { post } = Astro2.props;
  const { Content } = await post.render();
  const { base } = (Object.assign({"BASE_URL":"/mofa","MODE":"production","DEV":false,"PROD":true,"SSR":true,"SITE":"https://moxin-org.github.io","ASSETS_PREFIX":undefined},{_:process.env._,}));
  return renderTemplate`${renderComponent($$result, "BaseLayout", $$BaseLayout, { "title": post.data.title, "description": post.data.description }, { "default": async ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="container mx-auto px-4 py-16"> <div class="max-w-4xl mx-auto"> <!-- Back to blog --> <div class="mb-8"> <a${addAttribute(`${base}/blog`, "href")} class="inline-flex items-center text-mondrian-blue hover:text-mondrian-red transition-colors"> <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"> <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path> </svg>
返回博客
</a> </div> <!-- Article Header --> <header class="mb-12"> <div class="flex items-center mb-4"> <time class="text-gray-500 mr-4"> ${post.data.date.toLocaleDateString("zh-CN")} </time> ${post.data.tags && renderTemplate`<div class="flex gap-2"> ${post.data.tags.map((tag) => renderTemplate`<span class="text-sm bg-mondrian-yellow text-gray-900 px-3 py-1 rounded-md"> ${tag} </span>`)} </div>`} </div> <h1 class="text-4xl md:text-5xl font-bold mb-4 leading-tight"> ${post.data.title} </h1> <p class="text-xl text-gray-600 mb-6"> ${post.data.description} </p> <div class="flex items-center text-gray-500"> <span>作者：${post.data.author}</span> </div> </header> <!-- Article Content --> <article class="prose prose-lg max-w-none"> ${renderComponent($$result2, "Content", Content, {})} </article> <!-- Footer with navigation --> <footer class="mt-16 pt-8 border-t border-mondrian-gray"> <div class="flex flex-col sm:flex-row justify-between items-center gap-4"> <div class="text-center sm:text-left"> <p class="text-gray-600 mb-2">喜欢这篇文章？</p> <div class="flex space-x-4"> <a href="https://github.com/moxin-org/mofa" target="_blank" rel="noopener noreferrer" class="btn-outline text-sm">
GitHub 上关注我们
</a> <a href="https://discord.gg/mofatesttesttest" target="_blank" rel="noopener noreferrer" class="btn-secondary text-sm">
加入讨论
</a> </div> </div> <div class="text-center sm:text-right"> <p class="text-gray-600 mb-2">发现问题？</p> <a${addAttribute(`https://github.com/moxin-org/mofa-website/edit/main/src/content/blog/${post.slug}.md`, "href")} target="_blank" rel="noopener noreferrer" class="text-mondrian-blue hover:text-mondrian-red transition-colors text-sm">
在 GitHub 上编辑此页面
</a> </div> </div> </footer> </div> </div> ` })}`;
}, "/Users/liyao/Code/mofa/mofa-website/src/pages/blog/[...slug].astro", void 0);

const $$file$1 = "/Users/liyao/Code/mofa/mofa-website/src/pages/blog/[...slug].astro";
const $$url$1 = "/mofa/blog/[...slug]";

const ____slug_$1 = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$$1,
  file: $$file$1,
  getStaticPaths: getStaticPaths$1,
  url: $$url$1
}, Symbol.toStringTag, { value: 'Module' }));

const $$Astro$1 = createAstro("https://moxin-org.github.io");
const $$DocsLayout = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro$1, $$props, $$slots);
  Astro2.self = $$DocsLayout;
  const { title, description } = Astro2.props;
  const { base } = (Object.assign({"BASE_URL":"/mofa","MODE":"production","DEV":false,"PROD":true,"SSR":true,"SITE":"https://moxin-org.github.io","ASSETS_PREFIX":undefined},{}));
  const docNav = [
    {
      title: "\u5FEB\u901F\u5F00\u59CB",
      items: [
        { title: "\u5B89\u88C5", href: "/docs/quick-start" },
        { title: "\u7B2C\u4E00\u4E2A\u4EE3\u7406", href: "/docs/first-agent" }
      ]
    },
    {
      title: "\u6838\u5FC3\u6982\u5FF5",
      items: [
        { title: "\u4EE3\u7406 (Agent)", href: "/docs/concepts/agent" },
        { title: "\u7BA1\u9053 (Pipeline)", href: "/docs/concepts/pipeline" }
      ]
    }
  ];
  return renderTemplate`${renderComponent($$result, "BaseLayout", $$BaseLayout, { "title": title, "description": description }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="container mx-auto px-4 py-8"> <div class="flex gap-8"> <!-- 左侧导航 --> <aside class="w-64 flex-shrink-0 hidden lg:block"> <nav class="sticky top-20"> ${docNav.map((section) => renderTemplate`<div class="mb-6"> <h3 class="font-semibold text-gray-900 mb-2">${section.title}</h3> <ul class="space-y-1"> ${section.items.map((item) => renderTemplate`<li> <a${addAttribute(`${base}${item.href}`, "href")} class="block px-3 py-2 text-sm text-gray-600 hover:text-mondrian-red hover:bg-gray-50 rounded transition-colors"> ${item.title} </a> </li>`)} </ul> </div>`)} </nav> </aside> <!-- 主内容区 --> <main class="flex-1 max-w-4xl"> <article class="prose prose-lg max-w-none"> ${renderSlot($$result2, $$slots["default"])} </article> </main> </div> </div> ` })}`;
}, "/Users/liyao/Code/mofa/mofa-website/src/layouts/DocsLayout.astro", void 0);

const $$Astro = createAstro("https://moxin-org.github.io");
async function getStaticPaths() {
  const docs = await getCollection("docs");
  return docs.map((doc) => ({
    params: { slug: doc.slug },
    props: { doc }
  }));
}
const $$ = createComponent(async ($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$;
  const { doc } = Astro2.props;
  const { Content } = await doc.render();
  return renderTemplate`${renderComponent($$result, "DocsLayout", $$DocsLayout, { "title": doc.data.title, "description": doc.data.description }, { "default": async ($$result2) => renderTemplate` ${renderComponent($$result2, "Content", Content, {})} ` })}`;
}, "/Users/liyao/Code/mofa/mofa-website/src/pages/docs/[...slug].astro", void 0);

const $$file = "/Users/liyao/Code/mofa/mofa-website/src/pages/docs/[...slug].astro";
const $$url = "/mofa/docs/[...slug]";

const ____slug_ = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$,
  file: $$file,
  getStaticPaths,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

export { $$BaseLayout as $, ____slug_$1 as _, $$DocsLayout as a, ____slug_ as b, getCollection as g };
