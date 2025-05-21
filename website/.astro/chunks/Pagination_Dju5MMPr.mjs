import { d as createAstro, c as createComponent, m as maybeRenderHead, b as addAttribute, r as renderComponent, a as renderTemplate, F as Fragment, u as unescapeHTML } from './astro/server_Ba4Od88w.mjs';
import 'kleur/colors';
import { $ as $$Icon } from './ToggleTheme_FEZIKbSa.mjs';
import { $ as $$Image } from './Image_Dln13ko0.mjs';
import { $ as $$Tags } from './Tags_BjkFnEDi.mjs';
import { a as getPermalink, c as getFormattedDate } from './consts_C1AwyY78.mjs';
import { f as findImage } from './Layout_B44eMgnS.mjs';
import 'clsx';
import { a as $$Button } from './PageLayout_DlB73lxi.mjs';

const $$Astro$3 = createAstro("https://mofa.ai");
const $$ListItem = createComponent(async ($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro$3, $$props, $$slots);
  Astro2.self = $$ListItem;
  const { post } = Astro2.props;
  const image = await findImage(post.image);
  const link = getPermalink(post.permalink, "post") ;
  return renderTemplate`${maybeRenderHead()}<article${addAttribute(`max-w-md mx-auto md:max-w-none grid gap-6 md:gap-8 intersect-once intersect-quarter motion-safe:md:opacity-0 motion-safe:md:intersect:animate-fade ${image ? "md:grid-cols-2" : ""}`, "class")}> ${image && (link ? renderTemplate`<a class="relative block group"${addAttribute(link ?? "javascript:void(0)", "href")}> <div class="relative h-0 pb-[56.25%] md:pb-[75%] md:h-72 lg:pb-[56.25%] overflow-hidden bg-gray-400 dark:bg-slate-700 rounded shadow-lg"> ${image && renderTemplate`${renderComponent($$result, "Image", $$Image, { "src": image, "class": "absolute inset-0 object-cover w-full h-full mb-6 rounded shadow-lg bg-gray-400 dark:bg-slate-700", "widths": [400, 900], "width": 900, "sizes": "(max-width: 900px) 400px, 900px", "alt": post.title, "aspectRatio": "16:9", "loading": "lazy", "decoding": "async" })}`} </div> </a>` : renderTemplate`<div class="relative h-0 pb-[56.25%] md:pb-[75%] md:h-72 lg:pb-[56.25%] overflow-hidden bg-gray-400 dark:bg-slate-700 rounded shadow-lg"> ${image && renderTemplate`${renderComponent($$result, "Image", $$Image, { "src": image, "class": "absolute inset-0 object-cover w-full h-full mb-6 rounded shadow-lg bg-gray-400 dark:bg-slate-700", "widths": [400, 900], "width": 900, "sizes": "(max-width: 900px) 400px, 900px", "alt": post.title, "aspectRatio": "16:9", "loading": "lazy", "decoding": "async" })}`} </div>`)} <div class="mt-2"> <header> <div class="mb-1"> <span class="text-sm"> ${renderComponent($$result, "Icon", $$Icon, { "name": "tabler:clock", "class": "w-3.5 h-3.5 inline-block -mt-0.5 dark:text-gray-400" })} <time${addAttribute(String(post.publishDate), "datetime")} class="inline-block">${getFormattedDate(post.publishDate)}</time> ${post.author && renderTemplate`${renderComponent($$result, "Fragment", Fragment, {}, { "default": async ($$result2) => renderTemplate`${" "}
· ${renderComponent($$result2, "Icon", $$Icon, { "name": "tabler:user", "class": "w-3.5 h-3.5 inline-block -mt-0.5 dark:text-gray-400" })} <span>${post.author.replaceAll("-", " ")}</span> ` })}`} ${post.category && renderTemplate`${renderComponent($$result, "Fragment", Fragment, {}, { "default": async ($$result2) => renderTemplate`${" "}
·${" "}<a class="hover:underline"${addAttribute(getPermalink(post.category.slug, "category"), "href")}> ${post.category.title} </a> ` })}`} </span> </div> <h2 class="text-xl sm:text-2xl font-bold leading-tight mb-2 font-heading dark:text-slate-300"> ${link ? renderTemplate`<a class="inline-block hover:text-primary dark:hover:text-blue-700 transition ease-in duration-200"${addAttribute(link, "href")}> ${post.title} </a>` : post.title} </h2> </header> ${post.excerpt && renderTemplate`<p class="flex-grow text-muted dark:text-slate-400 text-lg">${post.excerpt}</p>`} ${post.tags && Array.isArray(post.tags) ? renderTemplate`<footer class="mt-5"> ${renderComponent($$result, "PostTags", $$Tags, { "tags": post.tags })} </footer>` : renderTemplate`${renderComponent($$result, "Fragment", Fragment, {})}`} </div> </article>`;
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/components/blog/ListItem.astro", void 0);

const $$Astro$2 = createAstro("https://mofa.ai");
const $$List = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro$2, $$props, $$slots);
  Astro2.self = $$List;
  const { posts } = Astro2.props;
  return renderTemplate`${maybeRenderHead()}<ul> ${posts.map((post) => renderTemplate`<li class="mb-12 md:mb-20"> ${renderComponent($$result, "Item", $$ListItem, { "post": post })} </li>`)} </ul>`;
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/components/blog/List.astro", void 0);

const $$Astro$1 = createAstro("https://mofa.ai");
const $$Headline = createComponent(async ($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro$1, $$props, $$slots);
  Astro2.self = $$Headline;
  const { title = await Astro2.slots.render("default"), subtitle = await Astro2.slots.render("subtitle") } = Astro2.props;
  return renderTemplate`${maybeRenderHead()}<header class="mb-8 md:mb-16 text-center max-w-3xl mx-auto"> <h1 class="text-4xl md:text-5xl font-bold leading-tighter tracking-tighter font-heading">${unescapeHTML(title)}</h1> ${subtitle && renderTemplate`<div class="mt-2 md:mt-3 mx-auto text-xl text-gray-500 dark:text-slate-400 font-medium">${unescapeHTML(subtitle)}</div>`} </header>`;
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/components/blog/Headline.astro", void 0);

const $$Astro = createAstro("https://mofa.ai");
const $$Pagination = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$Pagination;
  const { prevUrl, nextUrl, prevText = "Newer posts", nextText = "Older posts" } = Astro2.props;
  return renderTemplate`${(prevUrl || nextUrl) && renderTemplate`${maybeRenderHead()}<div class="container flex"><div class="flex flex-row mx-auto container justify-between">${renderComponent($$result, "Button", $$Button, { "variant": "tertiary", "class": `md:px-3 px-3 mr-2 ${!prevUrl ? "invisible" : ""}`, "href": getPermalink(prevUrl) }, { "default": ($$result2) => renderTemplate`${renderComponent($$result2, "Icon", $$Icon, { "name": "tabler:chevron-left", "class": "w-6 h-6" })}<p class="ml-2">${prevText}</p>` })}${renderComponent($$result, "Button", $$Button, { "variant": "tertiary", "class": `md:px-3 px-3 ${!nextUrl ? "invisible" : ""}`, "href": getPermalink(nextUrl) }, { "default": ($$result2) => renderTemplate`<span class="mr-2">${nextText}</span>${renderComponent($$result2, "Icon", $$Icon, { "name": "tabler:chevron-right", "class": "w-6 h-6" })}` })}</div></div>`}`;
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/components/blog/Pagination.astro", void 0);

export { $$Headline as $, $$List as a, $$Pagination as b };
