import { d as createAstro, c as createComponent, r as renderComponent, F as Fragment, a as renderTemplate, b as addAttribute, m as maybeRenderHead } from './astro/server_Ba4Od88w.mjs';
import 'kleur/colors';
import { a as getPermalink } from './consts_C1AwyY78.mjs';

const $$Astro = createAstro("https://mofa.ai");
const $$Tags = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$Tags;
  const { tags, class: className = "text-sm", title = void 0, isCategory = false } = Astro2.props;
  return renderTemplate`${tags && Array.isArray(tags) && renderTemplate`${renderComponent($$result, "Fragment", Fragment, {}, { "default": ($$result2) => renderTemplate`${title !== void 0 && renderTemplate`${maybeRenderHead()}<span class="align-super font-normal underline underline-offset-4 decoration-2 dark:text-slate-400">${title}</span>`}<ul${addAttribute(className, "class")}>${tags.map((tag) => renderTemplate`<li class="bg-gray-100 dark:bg-slate-700 inline-block mr-2 rtl:mr-0 rtl:ml-2 mb-2 py-0.5 px-2 lowercase font-medium">${renderTemplate`<a${addAttribute(getPermalink(tag.slug, isCategory ? "category" : "tag"), "href")} class="text-muted dark:text-slate-300 hover:text-primary dark:hover:text-gray-200">${tag.title}</a>`}</li>`)}</ul>` })}`}`;
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/components/blog/Tags.astro", void 0);

export { $$Tags as $ };
