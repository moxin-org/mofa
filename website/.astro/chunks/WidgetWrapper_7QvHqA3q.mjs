import { d as createAstro, c as createComponent, m as maybeRenderHead, b as addAttribute, e as renderSlot, a as renderTemplate, r as renderComponent, F as Fragment, u as unescapeHTML } from './astro/server_Ba4Od88w.mjs';
import 'kleur/colors';
import { twMerge } from 'tailwind-merge';
import 'clsx';

const $$Astro$1 = createAstro("https://mofa.ai");
const $$Background = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro$1, $$props, $$slots);
  Astro2.self = $$Background;
  const { isDark = false } = Astro2.props;
  return renderTemplate`${maybeRenderHead()}<div${addAttribute(["absolute inset-0", { "bg-dark dark:bg-transparent": isDark }], "class:list")}> ${renderSlot($$result, $$slots["default"])} </div>`;
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/components/ui/Background.astro", void 0);

const $$Astro = createAstro("https://mofa.ai");
const $$WidgetWrapper = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$WidgetWrapper;
  const { id, isDark = false, containerClass = "", bg, as = "section" } = Astro2.props;
  const WrapperTag = as;
  return renderTemplate`${renderComponent($$result, "WrapperTag", WrapperTag, { "class": "relative not-prose scroll-mt-[72px]", ...id ? { id } : {} }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="absolute inset-0 pointer-events-none -z-[1]" aria-hidden="true"> ${renderSlot($$result2, $$slots["bg"], renderTemplate` ${bg ? renderTemplate`${renderComponent($$result2, "Fragment", Fragment, {}, { "default": ($$result3) => renderTemplate`${unescapeHTML(bg)}` })}` : renderTemplate`${renderComponent($$result2, "Background", $$Background, { "isDark": isDark })}`} `)} </div> <div${addAttribute([
    twMerge(
      "relative mx-auto max-w-7xl px-4 md:px-6 py-12 md:py-16 lg:py-20 text-default intersect-once intersect-quarter intercept-no-queue motion-safe:md:opacity-0 motion-safe:md:intersect:animate-fade",
      containerClass
    ),
    { dark: isDark }
  ], "class:list")}> ${renderSlot($$result2, $$slots["default"])} </div> ` })}`;
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/components/ui/WidgetWrapper.astro", void 0);

export { $$WidgetWrapper as $ };
