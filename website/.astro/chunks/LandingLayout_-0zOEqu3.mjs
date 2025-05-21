import { d as createAstro, c as createComponent, r as renderComponent, a as renderTemplate, F as Fragment, e as renderSlot } from './astro/server_Ba4Od88w.mjs';
import 'kleur/colors';
import { $ as $$PageLayout, b as $$Header, h as headerData } from './PageLayout_DlB73lxi.mjs';

const $$Astro = createAstro("https://mofa.ai");
const $$LandingLayout = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$LandingLayout;
  const { metadata } = Astro2.props;
  return renderTemplate`${renderComponent($$result, "PageLayout", $$PageLayout, { "metadata": metadata }, { "announcement": ($$result2) => renderTemplate`${renderComponent($$result2, "Fragment", Fragment, { "slot": "announcement" }, { "default": ($$result3) => renderTemplate` ${renderSlot($$result3, $$slots["announcement"])} ` })}`, "default": ($$result2) => renderTemplate`   ${renderSlot($$result2, $$slots["default"])} `, "header": ($$result2) => renderTemplate`${renderComponent($$result2, "Fragment", Fragment, { "slot": "header" }, { "default": ($$result3) => renderTemplate` ${renderSlot($$result3, $$slots["header"], renderTemplate` ${renderComponent($$result3, "Header", $$Header, { "links": headerData?.links[2] ? [headerData.links[2]] : void 0, "actions": [
    {
      text: "Download",
      href: "https://github.com/onwidget/astrowind"
    }
  ], "showToggleTheme": true, "position": "right" })} `)} ` })}` })}`;
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/layouts/LandingLayout.astro", void 0);

export { $$LandingLayout as $ };
