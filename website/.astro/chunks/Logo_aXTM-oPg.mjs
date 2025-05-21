import { c as createComponent, m as maybeRenderHead, r as renderComponent, a as renderTemplate } from './astro/server_Ba4Od88w.mjs';
import 'kleur/colors';
import { S as SITE } from './consts_C1AwyY78.mjs';
import '@astrojs/internal-helpers/path';
import '@astrojs/internal-helpers/remote';
import { $ as $$Image } from './_astro_assets_CDPduv0g.mjs';
import logoImage from './mofa-logo_CGO6teq5.mjs';

const $$Logo = createComponent(($$result, $$props, $$slots) => {
  return renderTemplate`${maybeRenderHead()}<div class="flex items-center"> ${renderComponent($$result, "Image", $$Image, { "src": logoImage, "alt": "MoFA Logo", "width": 32, "height": 32, "class": "w-8 h-8" })} <span class="self-center ml-2 rtl:ml-0 rtl:mr-2 text-2xl md:text-xl font-bold text-gray-900 whitespace-nowrap dark:text-white"> ${SITE?.name} </span> </div>`;
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/components/Logo.astro", void 0);

export { $$Logo as $ };
