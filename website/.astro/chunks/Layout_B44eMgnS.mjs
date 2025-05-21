import { c as createComponent, b as addAttribute, a as renderTemplate, g as defineScriptVars, d as createAstro, r as renderComponent, F as Fragment, u as unescapeHTML, s as spreadAttributes, f as renderScript, h as renderHead, e as renderSlot } from './astro/server_Ba4Od88w.mjs';
import 'kleur/colors';
/* empty css                                 */
import { f as getAsset, U as UI, d as getCanonical, I as I18N, S as SITE, M as METADATA } from './consts_C1AwyY78.mjs';
import 'clsx';
import { c as createSvgComponent } from './runtime_CFqD3Xvn.mjs';
import merge from 'lodash.merge';
import { escape } from 'html-escaper';
import { g as getImage } from './_astro_assets_CDPduv0g.mjs';
import { parseUrl, transformUrl } from 'unpic';

const $$CommonMeta = createComponent(($$result, $$props, $$slots) => {
  return renderTemplate`<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="sitemap"${addAttribute(getAsset("/sitemap-index.xml"), "href")}>`;
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/components/common/CommonMeta.astro", void 0);

const favIcon = "/_astro/favicon.CGiRCjPI.ico";

const favIconSvg = createSvgComponent({"meta":{"src":"/_astro/favicon.vp_fBu0c.svg","width":128,"height":128,"format":"svg"},"attributes":{"fill":"none","viewBox":"0 0 128 128"},"children":"\n    <path d=\"M50.4 78.5a75.1 75.1 0 0 0-28.5 6.9l24.2-65.7c.7-2 1.9-3.2 3.4-3.2h29c1.5 0 2.7 1.2 3.4 3.2l24.2 65.7s-11.6-7-28.5-7L67 45.5c-.4-1.7-1.6-2.8-2.9-2.8-1.3 0-2.5 1.1-2.9 2.7L50.4 78.5Zm-1.1 28.2Zm-4.2-20.2c-2 6.6-.6 15.8 4.2 20.2a17.5 17.5 0 0 1 .2-.7 5.5 5.5 0 0 1 5.7-4.5c2.8.1 4.3 1.5 4.7 4.7.2 1.1.2 2.3.2 3.5v.4c0 2.7.7 5.2 2.2 7.4a13 13 0 0 0 5.7 4.9v-.3l-.2-.3c-1.8-5.6-.5-9.5 4.4-12.8l1.5-1a73 73 0 0 0 3.2-2.2 16 16 0 0 0 6.8-11.4c.3-2 .1-4-.6-6l-.8.6-1.6 1a37 37 0 0 1-22.4 2.7c-5-.7-9.7-2-13.2-6.2Z\" />\n    <style>\n        path { fill: #000; }\n        @media (prefers-color-scheme: dark) {\n            path { fill: #FFF; }\n        }\n    </style>\n"});

const appleTouchIcon = new Proxy({"src":"/_astro/apple-touch-icon.DHIlG7dp.png","width":180,"height":180,"format":"png"}, {
						get(target, name, receiver) {
							if (name === 'clone') {
								return structuredClone(target);
							}
							if (name === 'fsPath') {
								return "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/assets/favicons/apple-touch-icon.png";
							}
							if (target[name] !== undefined && globalThis.astroAsset) globalThis.astroAsset?.referencedImages.add("/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/assets/favicons/apple-touch-icon.png");
							return target[name];
						}
					});

const $$Favicons = createComponent(($$result, $$props, $$slots) => {
  return renderTemplate`<link rel="shortcut icon"${addAttribute(favIcon, "href")}><link rel="icon" type="image/svg+xml"${addAttribute(favIconSvg.src, "href")}><link rel="mask-icon"${addAttribute(favIconSvg.src, "href")} color="#8D46E7"><link rel="apple-touch-icon" sizes="180x180"${addAttribute(appleTouchIcon.src, "href")}>`;
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/components/Favicons.astro", void 0);

const $$CustomStyles = createComponent(($$result, $$props, $$slots) => {
  return renderTemplate`<style>
  :root {
    --aw-font-sans: 'Noto Sans SC', 'Inter Variable', sans-serif;
    --aw-font-serif: 'Noto Sans SC', 'Inter Variable', serif;
    --aw-font-heading: 'Noto Sans SC', 'Inter Variable', sans-serif;

    --mondrian-red: rgb(220, 36, 31);
    --mondrian-blue: rgb(0, 57, 166);
    --mondrian-yellow: rgb(254, 213, 0);
    --mondrian-black: rgb(0, 0, 0);
    --mondrian-white: rgb(255, 255, 255);

    --aw-color-primary: var(--mondrian-red);
    --aw-color-secondary: var(--mondrian-blue);
    --aw-color-accent: var(--mondrian-yellow);

    --aw-color-text-heading: var(--mondrian-black);
    --aw-color-text-default: rgb(16 16 16);
    --aw-color-text-muted: rgb(16 16 16 / 66%);
    --aw-color-bg-page: var(--mondrian-white);

    --aw-color-bg-page-dark: rgb(16 16 24);

    ::selection {
      background-color: var(--mondrian-yellow);
      color: var(--mondrian-black);
    }
  }

  .dark {
    --aw-font-sans: 'Noto Sans SC', 'Inter Variable', sans-serif;
    --aw-font-serif: 'Noto Sans SC', 'Inter Variable', serif;
    --aw-font-heading: 'Noto Sans SC', 'Inter Variable', sans-serif;

    --aw-color-primary: var(--mondrian-red);
    --aw-color-secondary: var(--mondrian-blue);
    --aw-color-accent: var(--mondrian-yellow);

    --aw-color-text-heading: rgb(247, 248, 248);
    --aw-color-text-default: rgb(229 236 246);
    --aw-color-text-muted: rgb(229 236 246 / 66%);
    --aw-color-bg-page: rgb(16 16 24);

    ::selection {
      background-color: var(--mondrian-blue);
      color: var(--mondrian-white);
    }
  }
</style>`;
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/components/CustomStyles.astro", void 0);

var __freeze$2 = Object.freeze;
var __defProp$2 = Object.defineProperty;
var __template$2 = (cooked, raw) => __freeze$2(__defProp$2(cooked, "raw", { value: __freeze$2(cooked.slice()) }));
var _a$2;
const $$ApplyColorMode = createComponent(($$result, $$props, $$slots) => {
  return renderTemplate(_a$2 || (_a$2 = __template$2(["<script>(function(){", "\n  function applyTheme(theme) {\n    if (theme === 'dark') {\n      document.documentElement.classList.add('dark');\n    } else {\n      document.documentElement.classList.remove('dark');\n    }\n    const matches = document.querySelectorAll('[data-aw-toggle-color-scheme] > input');\n\n    if (matches && matches.length) {\n      matches.forEach((elem) => {\n        elem.checked = theme !== 'dark';\n      });\n    }\n  }\n\n  if ((defaultTheme && defaultTheme.endsWith(':only')) || (!localStorage.theme && defaultTheme !== 'system')) {\n    applyTheme(defaultTheme.replace(':only', ''));\n  } else if (\n    localStorage.theme === 'dark' ||\n    (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)\n  ) {\n    applyTheme('dark');\n  } else {\n    applyTheme('light');\n  }\n})();<\/script>"])), defineScriptVars({ defaultTheme: UI.theme }));
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/components/common/ApplyColorMode.astro", void 0);

const createMetaTag = (attributes) => {
  const attrs = Object.entries(attributes).map(([key, value]) => `${key}="${escape(value)}"`).join(" ");
  return `<meta ${attrs}>`;
};
const createLinkTag = (attributes) => {
  const attrs = Object.entries(attributes).map(([key, value]) => `${key}="${escape(value)}"`).join(" ");
  return `<link ${attrs}>`;
};
const createOpenGraphTag = (property, content) => {
  return createMetaTag({ property: `og:${property}`, content });
};
const buildOpenGraphMediaTags = (mediaType, media) => {
  let tags = "";
  const addTag = (tag) => {
    tags += tag + "\n";
  };
  media.forEach((medium) => {
    addTag(createOpenGraphTag(mediaType, medium.url));
    if (medium.alt) {
      addTag(createOpenGraphTag(`${mediaType}:alt`, medium.alt));
    }
    if (medium.secureUrl) {
      addTag(createOpenGraphTag(`${mediaType}:secure_url`, medium.secureUrl));
    }
    if (medium.type) {
      addTag(createOpenGraphTag(`${mediaType}:type`, medium.type));
    }
    if (medium.width) {
      addTag(createOpenGraphTag(`${mediaType}:width`, medium.width.toString()));
    }
    if (medium.height) {
      addTag(
        createOpenGraphTag(`${mediaType}:height`, medium.height.toString())
      );
    }
  });
  return tags;
};
const buildTags = (config) => {
  let tagsToRender = "";
  const addTag = (tag) => {
    tagsToRender += tag + "\n";
  };
  if (config.title) {
    const formattedTitle = config.titleTemplate ? config.titleTemplate.replace("%s", config.title) : config.title;
    addTag(`<title>${escape(formattedTitle)}</title>`);
  }
  if (config.description) {
    addTag(createMetaTag({ name: "description", content: config.description }));
  }
  let robotsContent = [];
  if (typeof config.noindex !== "undefined") {
    robotsContent.push(config.noindex ? "noindex" : "index");
  }
  if (typeof config.nofollow !== "undefined") {
    robotsContent.push(config.nofollow ? "nofollow" : "follow");
  }
  if (config.robotsProps) {
    const {
      nosnippet,
      maxSnippet,
      maxImagePreview,
      noarchive,
      unavailableAfter,
      noimageindex,
      notranslate
    } = config.robotsProps;
    if (nosnippet) robotsContent.push("nosnippet");
    if (typeof maxSnippet === "number") robotsContent.push(`max-snippet:${maxSnippet}`);
    if (maxImagePreview)
      robotsContent.push(`max-image-preview:${maxImagePreview}`);
    if (noarchive) robotsContent.push("noarchive");
    if (unavailableAfter)
      robotsContent.push(`unavailable_after:${unavailableAfter}`);
    if (noimageindex) robotsContent.push("noimageindex");
    if (notranslate) robotsContent.push("notranslate");
  }
  if (robotsContent.length > 0) {
    addTag(createMetaTag({ name: "robots", content: robotsContent.join(",") }));
  }
  if (config.canonical) {
    addTag(createLinkTag({ rel: "canonical", href: config.canonical }));
  }
  if (config.mobileAlternate) {
    addTag(
      createLinkTag({
        rel: "alternate",
        media: config.mobileAlternate.media,
        href: config.mobileAlternate.href
      })
    );
  }
  if (config.languageAlternates && config.languageAlternates.length > 0) {
    config.languageAlternates.forEach((languageAlternate) => {
      addTag(
        createLinkTag({
          rel: "alternate",
          hreflang: languageAlternate.hreflang,
          href: languageAlternate.href
        })
      );
    });
  }
  if (config.openGraph) {
    const title = config.openGraph?.title || config.title;
    if (title) {
      addTag(createOpenGraphTag("title", title));
    }
    const description = config.openGraph?.description || config.description;
    if (description) {
      addTag(createOpenGraphTag("description", description));
    }
    if (config.openGraph.url) {
      addTag(createOpenGraphTag("url", config.openGraph.url));
    }
    if (config.openGraph.type) {
      addTag(createOpenGraphTag("type", config.openGraph.type));
    }
    if (config.openGraph.images && config.openGraph.images.length) {
      addTag(buildOpenGraphMediaTags("image", config.openGraph.images));
    }
    if (config.openGraph.videos && config.openGraph.videos.length) {
      addTag(buildOpenGraphMediaTags("video", config.openGraph.videos));
    }
    if (config.openGraph.locale) {
      addTag(createOpenGraphTag("locale", config.openGraph.locale));
    }
    if (config.openGraph.site_name) {
      addTag(createOpenGraphTag("site_name", config.openGraph.site_name));
    }
    if (config.openGraph.profile) {
      if (config.openGraph.profile.firstName) {
        addTag(
          createOpenGraphTag(
            "profile:first_name",
            config.openGraph.profile.firstName
          )
        );
      }
      if (config.openGraph.profile.lastName) {
        addTag(
          createOpenGraphTag(
            "profile:last_name",
            config.openGraph.profile.lastName
          )
        );
      }
      if (config.openGraph.profile.username) {
        addTag(
          createOpenGraphTag(
            "profile:username",
            config.openGraph.profile.username
          )
        );
      }
      if (config.openGraph.profile.gender) {
        addTag(
          createOpenGraphTag("profile:gender", config.openGraph.profile.gender)
        );
      }
    }
    if (config.openGraph.book) {
      if (config.openGraph.book.authors && config.openGraph.book.authors.length) {
        config.openGraph.book.authors.forEach((author) => {
          addTag(createOpenGraphTag("book:author", author));
        });
      }
      if (config.openGraph.book.isbn) {
        addTag(createOpenGraphTag("book:isbn", config.openGraph.book.isbn));
      }
      if (config.openGraph.book.releaseDate) {
        addTag(
          createOpenGraphTag(
            "book:release_date",
            config.openGraph.book.releaseDate
          )
        );
      }
      if (config.openGraph.book.tags && config.openGraph.book.tags.length) {
        config.openGraph.book.tags.forEach((tag) => {
          addTag(createOpenGraphTag("book:tag", tag));
        });
      }
    }
    if (config.openGraph.article) {
      if (config.openGraph.article.publishedTime) {
        addTag(
          createOpenGraphTag(
            "article:published_time",
            config.openGraph.article.publishedTime
          )
        );
      }
      if (config.openGraph.article.modifiedTime) {
        addTag(
          createOpenGraphTag(
            "article:modified_time",
            config.openGraph.article.modifiedTime
          )
        );
      }
      if (config.openGraph.article.expirationTime) {
        addTag(
          createOpenGraphTag(
            "article:expiration_time",
            config.openGraph.article.expirationTime
          )
        );
      }
      if (config.openGraph.article.authors && config.openGraph.article.authors.length) {
        config.openGraph.article.authors.forEach((author) => {
          addTag(createOpenGraphTag("article:author", author));
        });
      }
      if (config.openGraph.article.section) {
        addTag(
          createOpenGraphTag(
            "article:section",
            config.openGraph.article.section
          )
        );
      }
      if (config.openGraph.article.tags && config.openGraph.article.tags.length) {
        config.openGraph.article.tags.forEach((tag) => {
          addTag(createOpenGraphTag("article:tag", tag));
        });
      }
    }
    if (config.openGraph.video) {
      if (config.openGraph.video.actors && config.openGraph.video.actors.length) {
        config.openGraph.video.actors.forEach((actor) => {
          addTag(createOpenGraphTag("video:actor", actor.profile));
          if (actor.role) {
            addTag(createOpenGraphTag("video:actor:role", actor.role));
          }
        });
      }
      if (config.openGraph.video.directors && config.openGraph.video.directors.length) {
        config.openGraph.video.directors.forEach((director) => {
          addTag(createOpenGraphTag("video:director", director));
        });
      }
      if (config.openGraph.video.writers && config.openGraph.video.writers.length) {
        config.openGraph.video.writers.forEach((writer) => {
          addTag(createOpenGraphTag("video:writer", writer));
        });
      }
      if (config.openGraph.video.duration) {
        addTag(
          createOpenGraphTag(
            "video:duration",
            config.openGraph.video.duration.toString()
          )
        );
      }
      if (config.openGraph.video.releaseDate) {
        addTag(
          createOpenGraphTag(
            "video:release_date",
            config.openGraph.video.releaseDate
          )
        );
      }
      if (config.openGraph.video.tags && config.openGraph.video.tags.length) {
        config.openGraph.video.tags.forEach((tag) => {
          addTag(createOpenGraphTag("video:tag", tag));
        });
      }
      if (config.openGraph.video.series) {
        addTag(
          createOpenGraphTag("video:series", config.openGraph.video.series)
        );
      }
    }
  }
  if (config.facebook && config.facebook.appId) {
    addTag(
      createMetaTag({ property: "fb:app_id", content: config.facebook.appId })
    );
  }
  if (config.twitter) {
    if (config.twitter.cardType) {
      addTag(
        createMetaTag({
          name: "twitter:card",
          content: config.twitter.cardType
        })
      );
    }
    if (config.twitter.site) {
      addTag(
        createMetaTag({ name: "twitter:site", content: config.twitter.site })
      );
    }
    if (config.twitter.handle) {
      addTag(
        createMetaTag({
          name: "twitter:creator",
          content: config.twitter.handle
        })
      );
    }
  }
  if (config.additionalMetaTags && config.additionalMetaTags.length > 0) {
    config.additionalMetaTags.forEach((metaTag) => {
      const attributes = {
        content: metaTag.content
      };
      if ("name" in metaTag && metaTag.name) {
        attributes.name = metaTag.name;
      } else if ("property" in metaTag && metaTag.property) {
        attributes.property = metaTag.property;
      } else if ("httpEquiv" in metaTag && metaTag.httpEquiv) {
        attributes["http-equiv"] = metaTag.httpEquiv;
      }
      addTag(createMetaTag(attributes));
    });
  }
  if (config.additionalLinkTags && config.additionalLinkTags.length > 0) {
    config.additionalLinkTags.forEach((linkTag) => {
      const attributes = {
        rel: linkTag.rel,
        href: linkTag.href
      };
      if (linkTag.sizes) {
        attributes.sizes = linkTag.sizes;
      }
      if (linkTag.media) {
        attributes.media = linkTag.media;
      }
      if (linkTag.type) {
        attributes.type = linkTag.type;
      }
      if (linkTag.color) {
        attributes.color = linkTag.color;
      }
      if (linkTag.as) {
        attributes.as = linkTag.as;
      }
      if (linkTag.crossOrigin) {
        attributes.crossorigin = linkTag.crossOrigin;
      }
      addTag(createLinkTag(attributes));
    });
  }
  return tagsToRender.trim();
};

const $$Astro$4 = createAstro("https://mofa.ai");
const $$AstroSeo = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro$4, $$props, $$slots);
  Astro2.self = $$AstroSeo;
  const {
    title,
    titleTemplate,
    noindex,
    nofollow,
    robotsProps,
    description,
    canonical,
    mobileAlternate,
    languageAlternates,
    openGraph,
    facebook,
    twitter,
    additionalMetaTags,
    additionalLinkTags
  } = Astro2.props;
  return renderTemplate`${renderComponent($$result, "Fragment", Fragment, {}, { "default": ($$result2) => renderTemplate`${unescapeHTML(buildTags({
    title,
    titleTemplate,
    noindex,
    nofollow,
    robotsProps,
    description,
    canonical,
    mobileAlternate,
    languageAlternates,
    openGraph,
    facebook,
    twitter,
    additionalMetaTags,
    additionalLinkTags
  }))}` })}`;
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/node_modules/@astrolib/seo/src/AstroSeo.astro", void 0);

const config = {
  deviceSizes: [
    640,
    // older and lower-end phones
    750,
    // iPhone 6-8
    828,
    // iPhone XR/11
    960,
    // older horizontal phones
    1080,
    // iPhone 6-8 Plus
    1280,
    // 720p
    1668,
    // Various iPads
    1920,
    // 1080p
    2048,
    // QXGA
    2560,
    // WQXGA
    3200,
    // QHD+
    3840,
    // 4K
    4480,
    // 4.5K
    5120,
    // 5K
    6016
    // 6K
  ]};
const computeHeight = (width, aspectRatio) => {
  return Math.floor(width / aspectRatio);
};
const parseAspectRatio = (aspectRatio) => {
  if (typeof aspectRatio === "number") return aspectRatio;
  if (typeof aspectRatio === "string") {
    const match = aspectRatio.match(/(\d+)\s*[/:]\s*(\d+)/);
    if (match) {
      const [, num, den] = match.map(Number);
      if (den && !isNaN(num)) return num / den;
    } else {
      const numericValue = parseFloat(aspectRatio);
      if (!isNaN(numericValue)) return numericValue;
    }
  }
  return void 0;
};
const getSizes = (width, layout) => {
  if (!width || !layout) {
    return void 0;
  }
  switch (layout) {
    // If screen is wider than the max size, image width is the max size,
    // otherwise it's the width of the screen
    case `constrained`:
      return `(min-width: ${width}px) ${width}px, 100vw`;
    // Image is always the same width, whatever the size of the screen
    case `fixed`:
      return `${width}px`;
    // Image is always the width of the screen
    case `fullWidth`:
      return `100vw`;
    default:
      return void 0;
  }
};
const pixelate = (value) => value || value === 0 ? `${value}px` : void 0;
const getStyle = ({
  width,
  height,
  aspectRatio,
  layout,
  objectFit = "cover",
  objectPosition = "center",
  background
}) => {
  const styleEntries = [
    ["object-fit", objectFit],
    ["object-position", objectPosition]
  ];
  if (background?.startsWith("https:") || background?.startsWith("http:") || background?.startsWith("data:")) {
    styleEntries.push(["background-image", `url(${background})`]);
    styleEntries.push(["background-size", "cover"]);
    styleEntries.push(["background-repeat", "no-repeat"]);
  } else {
    styleEntries.push(["background", background]);
  }
  if (layout === "fixed") {
    styleEntries.push(["width", pixelate(width)]);
    styleEntries.push(["height", pixelate(height)]);
    styleEntries.push(["object-position", "top left"]);
  }
  if (layout === "constrained") {
    styleEntries.push(["max-width", pixelate(width)]);
    styleEntries.push(["max-height", pixelate(height)]);
    styleEntries.push(["aspect-ratio", aspectRatio ? `${aspectRatio}` : void 0]);
    styleEntries.push(["width", "100%"]);
  }
  if (layout === "fullWidth") {
    styleEntries.push(["width", "100%"]);
    styleEntries.push(["aspect-ratio", aspectRatio ? `${aspectRatio}` : void 0]);
    styleEntries.push(["height", pixelate(height)]);
  }
  if (layout === "responsive") {
    styleEntries.push(["width", "100%"]);
    styleEntries.push(["height", "auto"]);
    styleEntries.push(["aspect-ratio", aspectRatio ? `${aspectRatio}` : void 0]);
  }
  if (layout === "contained") {
    styleEntries.push(["max-width", "100%"]);
    styleEntries.push(["max-height", "100%"]);
    styleEntries.push(["object-fit", "contain"]);
    styleEntries.push(["aspect-ratio", aspectRatio ? `${aspectRatio}` : void 0]);
  }
  if (layout === "cover") {
    styleEntries.push(["max-width", "100%"]);
    styleEntries.push(["max-height", "100%"]);
  }
  const styles = Object.fromEntries(styleEntries.filter(([, value]) => value));
  return Object.entries(styles).map(([key, value]) => `${key}: ${value};`).join(" ");
};
const getBreakpoints = ({
  width,
  breakpoints,
  layout
}) => {
  if (layout === "fullWidth" || layout === "cover" || layout === "responsive" || layout === "contained") {
    return breakpoints || config.deviceSizes;
  }
  if (!width) {
    return [];
  }
  const doubleWidth = width * 2;
  if (layout === "fixed") {
    return [width, doubleWidth];
  }
  if (layout === "constrained") {
    return [
      // Always include the image at 1x and 2x the specified width
      width,
      doubleWidth,
      // Filter out any resolutions that are larger than the double-res image
      ...(breakpoints || config.deviceSizes).filter((w) => w < doubleWidth)
    ];
  }
  return [];
};
const astroAssetsOptimizer = async (image, breakpoints, _width, _height, format = void 0) => {
  if (!image) {
    return [];
  }
  return Promise.all(
    breakpoints.map(async (w) => {
      const result = await getImage({ src: image, width: w, inferSize: true, ...format ? { format } : {} });
      return {
        src: result?.src,
        width: result?.attributes?.width ?? w,
        height: result?.attributes?.height
      };
    })
  );
};
const isUnpicCompatible = (image) => {
  return typeof parseUrl(image) !== "undefined";
};
const unpicOptimizer = async (image, breakpoints, width, height, format = void 0) => {
  if (!image || typeof image !== "string") {
    return [];
  }
  const urlParsed = parseUrl(image);
  if (!urlParsed) {
    return [];
  }
  return Promise.all(
    breakpoints.map(async (w) => {
      const _height = width && height ? computeHeight(w, width / height) : height;
      const url = transformUrl({
        url: image,
        width: w,
        height: _height,
        cdn: urlParsed.cdn,
        ...format ? { format } : {}
      }) || image;
      return {
        src: String(url),
        width: w,
        height: _height
      };
    })
  );
};
async function getImagesOptimized(image, {
  src: _,
  width,
  height,
  sizes,
  aspectRatio,
  objectPosition,
  widths,
  layout = "constrained",
  style = "",
  format,
  ...rest
}, transform = () => Promise.resolve([])) {
  if (typeof image !== "string") {
    width ||= Number(image.width) || void 0;
    height ||= typeof width === "number" ? computeHeight(width, image.width / image.height) : void 0;
  }
  width = width && Number(width) || void 0;
  height = height && Number(height) || void 0;
  widths ||= config.deviceSizes;
  sizes ||= getSizes(Number(width) || void 0, layout);
  aspectRatio = parseAspectRatio(aspectRatio);
  if (aspectRatio) {
    if (width) {
      if (height) ; else {
        height = width / aspectRatio;
      }
    } else if (height) {
      width = Number(height * aspectRatio);
    } else if (layout !== "fullWidth") {
      console.error("When aspectRatio is set, either width or height must also be set");
      console.error("Image", image);
    }
  } else if (width && height) {
    aspectRatio = width / height;
  } else if (layout !== "fullWidth") {
    console.error("Either aspectRatio or both width and height must be set");
    console.error("Image", image);
  }
  let breakpoints = getBreakpoints({ width, breakpoints: widths, layout });
  breakpoints = [...new Set(breakpoints)].sort((a, b) => a - b);
  const srcset = (await transform(image, breakpoints, Number(width) || void 0, Number(height) || void 0, format)).map(({ src, width: width2 }) => `${src} ${width2}w`).join(", ");
  return {
    src: typeof image === "string" ? image : image.src,
    attributes: {
      width,
      height,
      srcset: srcset || void 0,
      sizes,
      style: `${getStyle({
        width,
        height,
        aspectRatio,
        objectPosition,
        layout
      })}${style ?? ""}`,
      ...rest
    }
  };
}

const load = async function() {
  let images = void 0;
  try {
    images = /* #__PURE__ */ Object.assign({"/src/assets/images/app-store.png": () => import('./app-store_2sLqBTyh.mjs'),"/src/assets/images/default.png": () => import('./default_DJDofbum.mjs'),"/src/assets/images/google-play.png": () => import('./google-play_C0IgyUw3.mjs'),"/src/assets/images/hero-image.png": () => import('./hero-image_DZGB_yXB.mjs'),"/src/assets/images/mofa-logo.png": () => import('./mofa-logo_CGO6teq5.mjs'),"/src/assets/images/mondrian.jpg": () => import('./mondrian_C4RTRcEv.mjs')});
  } catch (error) {
  }
  return images;
};
let _images = void 0;
const fetchLocalImages = async () => {
  _images = _images || await load();
  return _images;
};
const findImage = async (imagePath) => {
  if (typeof imagePath !== "string") {
    return imagePath;
  }
  if (imagePath.startsWith("http://") || imagePath.startsWith("https://") || imagePath.startsWith("/")) {
    return imagePath;
  }
  if (!imagePath.startsWith("~/assets/images")) {
    return imagePath;
  }
  const images = await fetchLocalImages();
  const key = imagePath.replace("~/", "/src/");
  return images && typeof images[key] === "function" ? (await images[key]())["default"] : null;
};
const adaptOpenGraphImages = async (openGraph = {}, astroSite = new URL("")) => {
  if (!openGraph?.images?.length) {
    return openGraph;
  }
  const images = openGraph.images;
  const defaultWidth = 1200;
  const defaultHeight = 626;
  const adaptedImages = await Promise.all(
    images.map(async (image) => {
      if (image?.url) {
        const resolvedImage = await findImage(image.url);
        if (!resolvedImage) {
          return {
            url: ""
          };
        }
        let _image;
        if (typeof resolvedImage === "string" && (resolvedImage.startsWith("http://") || resolvedImage.startsWith("https://")) && isUnpicCompatible(resolvedImage)) {
          _image = (await unpicOptimizer(resolvedImage, [defaultWidth], defaultWidth, defaultHeight, "jpg"))[0];
        } else if (resolvedImage) {
          const dimensions = typeof resolvedImage !== "string" && resolvedImage?.width <= defaultWidth ? [resolvedImage?.width, resolvedImage?.height] : [defaultWidth, defaultHeight];
          _image = (await astroAssetsOptimizer(resolvedImage, [dimensions[0]], dimensions[0], dimensions[1], "jpg"))[0];
        }
        if (typeof _image === "object") {
          return {
            url: "src" in _image && typeof _image.src === "string" ? String(new URL(_image.src, astroSite)) : "",
            width: "width" in _image && typeof _image.width === "number" ? _image.width : void 0,
            height: "height" in _image && typeof _image.height === "number" ? _image.height : void 0
          };
        }
        return {
          url: ""
        };
      }
      return {
        url: ""
      };
    })
  );
  return { ...openGraph, ...adaptedImages ? { images: adaptedImages } : {} };
};

const $$Astro$3 = createAstro("https://mofa.ai");
const $$Metadata = createComponent(async ($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro$3, $$props, $$slots);
  Astro2.self = $$Metadata;
  const {
    title,
    ignoreTitleTemplate = false,
    canonical = String(getCanonical(String(Astro2.url.pathname))),
    robots = {},
    description,
    openGraph = {},
    twitter = {}
  } = Astro2.props;
  const seoProps = merge(
    {
      title: "",
      titleTemplate: "%s",
      canonical,
      noindex: true,
      nofollow: true,
      description: void 0,
      openGraph: {
        url: canonical,
        site_name: SITE?.name,
        images: [],
        locale: I18N?.language,
        type: "website"
      },
      twitter: {
        cardType: openGraph?.images?.length ? "summary_large_image" : "summary"
      }
    },
    {
      title: METADATA?.title?.default,
      titleTemplate: METADATA?.title?.template,
      noindex: false ,
      nofollow: false ,
      description: METADATA?.description,
      openGraph: METADATA?.openGraph,
      twitter: METADATA?.twitter
    },
    {
      title,
      titleTemplate: ignoreTitleTemplate ? "%s" : void 0,
      canonical,
      noindex: typeof robots?.index !== "undefined" ? !robots.index : void 0,
      nofollow: typeof robots?.follow !== "undefined" ? !robots.follow : void 0,
      description,
      openGraph: { url: canonical, ...openGraph },
      twitter
    }
  );
  return renderTemplate`${renderComponent($$result, "AstroSeo", $$AstroSeo, { ...{ ...seoProps, openGraph: await adaptOpenGraphImages(seoProps?.openGraph, Astro2.site) } })}`;
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/components/common/Metadata.astro", void 0);

const $$SiteVerification = createComponent(($$result, $$props, $$slots) => {
  return renderTemplate`${SITE.googleSiteVerificationId}`;
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/components/common/SiteVerification.astro", void 0);

var __freeze$1 = Object.freeze;
var __defProp$1 = Object.defineProperty;
var __template$1 = (cooked, raw) => __freeze$1(__defProp$1(cooked, "raw", { value: __freeze$1(cooked.slice()) }));
var _a$1;
const $$Astro$2 = createAstro("https://mofa.ai");
const $$GoogleAnalytics = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro$2, $$props, $$slots);
  Astro2.self = $$GoogleAnalytics;
  const { id = "GA_MEASUREMENT_ID", partytown = false } = Astro2.props;
  const attrs = partytown ? { type: "text/partytown" } : {};
  return renderTemplate(_a$1 || (_a$1 = __template$1(["<script async", "", "><\/script><script", ">(function(){", '\n  window.dataLayer = window.dataLayer || [];\n  function gtag() {\n    window.dataLayer.push(arguments);\n  }\n  gtag("js", new Date());\n  gtag("config", id);\n})();<\/script>'])), addAttribute(`https://www.googletagmanager.com/gtag/js?id=${id}`, "src"), spreadAttributes(attrs), spreadAttributes(attrs), defineScriptVars({ id }));
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/node_modules/@astrolib/analytics/src/GoogleAnalytics.astro", void 0);

const $$Analytics = createComponent(($$result, $$props, $$slots) => {
  return renderTemplate`${null}`;
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/components/common/Analytics.astro", void 0);

var __freeze = Object.freeze;
var __defProp = Object.defineProperty;
var __template = (cooked, raw) => __freeze(__defProp(cooked, "raw", { value: __freeze(raw || cooked.slice()) }));
var _a;
const $$BasicScripts = createComponent(($$result, $$props, $$slots) => {
  return renderTemplate(_a || (_a = __template(["<script>(function(){", "\n  if (window.basic_script) {\n    return;\n  }\n\n  window.basic_script = true;\n\n  // Handle language switching\n  function initLanguage() {\n    // Check URL parameters for language\n    const urlParams = new URLSearchParams(window.location.search);\n    const langParam = urlParams.get('lang');\n    \n    // If lang parameter exists in URL, use it\n    if (langParam && (langParam === 'en' || langParam === 'zh')) {\n      localStorage.setItem('language', langParam);\n      document.documentElement.setAttribute('lang', langParam);\n    }\n    // Otherwise use localStorage or default\n    else {\n      const storedLang = localStorage.getItem('language');\n      if (storedLang && (storedLang === 'en' || storedLang === 'zh')) {\n        document.documentElement.setAttribute('lang', storedLang);\n      } else {\n        // Use default language from config\n        localStorage.setItem('language', defaultLanguage);\n      }\n    }\n  }\n  \n  // Initialize language\n  initLanguage();\n\n  function applyTheme(theme) {\n    if (theme === 'dark') {\n      document.documentElement.classList.add('dark');\n    } else {\n      document.documentElement.classList.remove('dark');\n    }\n  }\n\n  const initTheme = function () {\n    if ((defaultTheme && defaultTheme.endsWith(':only')) || (!localStorage.theme && defaultTheme !== 'system')) {\n      applyTheme(defaultTheme.replace(':only', ''));\n    } else if (\n      localStorage.theme === 'dark' ||\n      (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)\n    ) {\n      applyTheme('dark');\n    } else {\n      applyTheme('light');\n    }\n  };\n  initTheme();\n\n  function attachEvent(selector, event, fn) {\n    const matches = typeof selector === 'string' ? document.querySelectorAll(selector) : selector;\n    if (matches && matches.length) {\n      matches.forEach((elem) => {\n        elem.addEventListener(event, (e) => fn(e, elem), false);\n      });\n    }\n  }\n\n  const onLoad = function () {\n    let lastKnownScrollPosition = window.scrollY;\n    let ticking = true;\n\n    attachEvent('#header nav', 'click', function () {\n      document.querySelector('[data-aw-toggle-menu]')?.classList.remove('expanded');\n      document.body.classList.remove('overflow-hidden');\n      document.getElementById('header')?.classList.remove('h-screen');\n      document.getElementById('header')?.classList.remove('expanded');\n      document.getElementById('header')?.classList.remove('bg-page');\n      document.querySelector('#header nav')?.classList.add('hidden');\n      document.querySelector('#header > div > div:last-child')?.classList.add('hidden');\n    });\n\n    attachEvent('[data-aw-toggle-menu]', 'click', function (_, elem) {\n      elem.classList.toggle('expanded');\n      document.body.classList.toggle('overflow-hidden');\n      document.getElementById('header')?.classList.toggle('h-screen');\n      document.getElementById('header')?.classList.toggle('expanded');\n      document.getElementById('header')?.classList.toggle('bg-page');\n      document.querySelector('#header nav')?.classList.toggle('hidden');\n      document.querySelector('#header > div > div:last-child')?.classList.toggle('hidden');\n    });\n\n    attachEvent('[data-aw-toggle-color-scheme]', 'click', function () {\n      if (defaultTheme.endsWith(':only')) {\n        return;\n      }\n      document.documentElement.classList.toggle('dark');\n      localStorage.theme = document.documentElement.classList.contains('dark') ? 'dark' : 'light';\n    });\n\n    attachEvent('[data-aw-social-share]', 'click', function (_, elem) {\n      const network = elem.getAttribute('data-aw-social-share');\n      const url = encodeURIComponent(elem.getAttribute('data-aw-url'));\n      const text = encodeURIComponent(elem.getAttribute('data-aw-text'));\n\n      let href;\n      switch (network) {\n        case 'facebook':\n          href = `https://www.facebook.com/sharer.php?u=${url}`;\n          break;\n        case 'twitter':\n          href = `https://twitter.com/intent/tweet?url=${url}&text=${text}`;\n          break;\n        case 'linkedin':\n          href = `https://www.linkedin.com/shareArticle?mini=true&url=${url}&title=${text}`;\n          break;\n        case 'whatsapp':\n          href = `https://wa.me/?text=${text}%20${url}`;\n          break;\n        case 'mail':\n          href = `mailto:?subject=%22${text}%22&body=${text}%20${url}`;\n          break;\n\n        default:\n          return;\n      }\n\n      const newlink = document.createElement('a');\n      newlink.target = '_blank';\n      newlink.href = href;\n      newlink.click();\n    });\n\n    const screenSize = window.matchMedia('(max-width: 767px)');\n    screenSize.addEventListener('change', function () {\n      document.querySelector('[data-aw-toggle-menu]')?.classList.remove('expanded');\n      document.body.classList.remove('overflow-hidden');\n      document.getElementById('header')?.classList.remove('h-screen');\n      document.getElementById('header')?.classList.remove('expanded');\n      document.getElementById('header')?.classList.remove('bg-page');\n      document.querySelector('#header nav')?.classList.add('hidden');\n      document.querySelector('#header > div > div:last-child')?.classList.add('hidden');\n    });\n\n    function applyHeaderStylesOnScroll() {\n      const header = document.querySelector('#header[data-aw-sticky-header]');\n      if (!header) return;\n      if (lastKnownScrollPosition > 60 && !header.classList.contains('scroll')) {\n        header.classList.add('scroll');\n      } else if (lastKnownScrollPosition <= 60 && header.classList.contains('scroll')) {\n        header.classList.remove('scroll');\n      }\n      ticking = false;\n    }\n    applyHeaderStylesOnScroll();\n\n    attachEvent([document], 'scroll', function () {\n      lastKnownScrollPosition = window.scrollY;\n\n      if (!ticking) {\n        window.requestAnimationFrame(() => {\n          applyHeaderStylesOnScroll();\n        });\n        ticking = true;\n      }\n    });\n  };\n  const onPageShow = function () {\n    document.documentElement.classList.add('motion-safe:scroll-smooth');\n    const elem = document.querySelector('[data-aw-toggle-menu]');\n    if (elem) {\n      elem.classList.remove('expanded');\n    }\n    document.body.classList.remove('overflow-hidden');\n    document.getElementById('header')?.classList.remove('h-screen');\n    document.getElementById('header')?.classList.remove('expanded');\n    document.querySelector('#header nav')?.classList.add('hidden');\n  };\n\n  window.onload = onLoad;\n  window.onpageshow = onPageShow;\n\n  document.addEventListener('astro:after-swap', () => {\n    initTheme();\n    onLoad();\n    onPageShow();\n  });\n})();<\/script> <script>\n  /* Inspired by: https://github.com/heidkaemper/tailwindcss-intersect */\n  const Observer = {\n    observer: null,\n    delayBetweenAnimations: 100,\n    animationCounter: 0,\n\n    start() {\n      const selectors = [\n        '[class*=\" intersect:\"]',\n        '[class*=\":intersect:\"]',\n        '[class^=\"intersect:\"]',\n        '[class=\"intersect\"]',\n        '[class*=\" intersect \"]',\n        '[class^=\"intersect \"]',\n        '[class$=\" intersect\"]',\n      ];\n\n      const elements = Array.from(document.querySelectorAll(selectors.join(',')));\n\n      const getThreshold = (element) => {\n        if (element.classList.contains('intersect-full')) return 0.99;\n        if (element.classList.contains('intersect-half')) return 0.5;\n        if (element.classList.contains('intersect-quarter')) return 0.25;\n        return 0;\n      };\n\n      elements.forEach((el) => {\n        el.setAttribute('no-intersect', '');\n        el._intersectionThreshold = getThreshold(el);\n      });\n\n      const callback = (entries) => {\n        entries.forEach((entry) => {\n          requestAnimationFrame(() => {\n            const target = entry.target;\n            const intersectionRatio = entry.intersectionRatio;\n            const threshold = target._intersectionThreshold;\n\n            if (target.classList.contains('intersect-no-queue')) {\n              if (entry.isIntersecting) {\n                target.removeAttribute('no-intersect');\n                if (target.classList.contains('intersect-once')) {\n                  this.observer.unobserve(target);\n                }\n              } else {\n                target.setAttribute('no-intersect', '');\n              }\n              return;\n            }\n\n            if (intersectionRatio >= threshold) {\n              if (!target.hasAttribute('data-animated')) {\n                target.removeAttribute('no-intersect');\n                target.setAttribute('data-animated', 'true');\n\n                const delay = this.animationCounter * this.delayBetweenAnimations;\n                this.animationCounter++;\n\n                target.style.transitionDelay = `${delay}ms`;\n                target.style.animationDelay = `${delay}ms`;\n\n                if (target.classList.contains('intersect-once')) {\n                  this.observer.unobserve(target);\n                }\n              }\n            } else {\n              target.setAttribute('no-intersect', '');\n              target.removeAttribute('data-animated');\n              target.style.transitionDelay = '';\n              target.style.animationDelay = '';\n\n              this.animationCounter = 0;\n            }\n          });\n        });\n      };\n\n      this.observer = new IntersectionObserver(callback.bind(this), { threshold: [0, 0.25, 0.5, 0.99] });\n\n      elements.forEach((el) => {\n        this.observer.observe(el);\n      });\n    },\n  };\n\n  Observer.start();\n\n  document.addEventListener('astro:after-swap', () => {\n    Observer.start();\n  });\n<\/script>"], ["<script>(function(){", "\n  if (window.basic_script) {\n    return;\n  }\n\n  window.basic_script = true;\n\n  // Handle language switching\n  function initLanguage() {\n    // Check URL parameters for language\n    const urlParams = new URLSearchParams(window.location.search);\n    const langParam = urlParams.get('lang');\n    \n    // If lang parameter exists in URL, use it\n    if (langParam && (langParam === 'en' || langParam === 'zh')) {\n      localStorage.setItem('language', langParam);\n      document.documentElement.setAttribute('lang', langParam);\n    }\n    // Otherwise use localStorage or default\n    else {\n      const storedLang = localStorage.getItem('language');\n      if (storedLang && (storedLang === 'en' || storedLang === 'zh')) {\n        document.documentElement.setAttribute('lang', storedLang);\n      } else {\n        // Use default language from config\n        localStorage.setItem('language', defaultLanguage);\n      }\n    }\n  }\n  \n  // Initialize language\n  initLanguage();\n\n  function applyTheme(theme) {\n    if (theme === 'dark') {\n      document.documentElement.classList.add('dark');\n    } else {\n      document.documentElement.classList.remove('dark');\n    }\n  }\n\n  const initTheme = function () {\n    if ((defaultTheme && defaultTheme.endsWith(':only')) || (!localStorage.theme && defaultTheme !== 'system')) {\n      applyTheme(defaultTheme.replace(':only', ''));\n    } else if (\n      localStorage.theme === 'dark' ||\n      (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)\n    ) {\n      applyTheme('dark');\n    } else {\n      applyTheme('light');\n    }\n  };\n  initTheme();\n\n  function attachEvent(selector, event, fn) {\n    const matches = typeof selector === 'string' ? document.querySelectorAll(selector) : selector;\n    if (matches && matches.length) {\n      matches.forEach((elem) => {\n        elem.addEventListener(event, (e) => fn(e, elem), false);\n      });\n    }\n  }\n\n  const onLoad = function () {\n    let lastKnownScrollPosition = window.scrollY;\n    let ticking = true;\n\n    attachEvent('#header nav', 'click', function () {\n      document.querySelector('[data-aw-toggle-menu]')?.classList.remove('expanded');\n      document.body.classList.remove('overflow-hidden');\n      document.getElementById('header')?.classList.remove('h-screen');\n      document.getElementById('header')?.classList.remove('expanded');\n      document.getElementById('header')?.classList.remove('bg-page');\n      document.querySelector('#header nav')?.classList.add('hidden');\n      document.querySelector('#header > div > div:last-child')?.classList.add('hidden');\n    });\n\n    attachEvent('[data-aw-toggle-menu]', 'click', function (_, elem) {\n      elem.classList.toggle('expanded');\n      document.body.classList.toggle('overflow-hidden');\n      document.getElementById('header')?.classList.toggle('h-screen');\n      document.getElementById('header')?.classList.toggle('expanded');\n      document.getElementById('header')?.classList.toggle('bg-page');\n      document.querySelector('#header nav')?.classList.toggle('hidden');\n      document.querySelector('#header > div > div:last-child')?.classList.toggle('hidden');\n    });\n\n    attachEvent('[data-aw-toggle-color-scheme]', 'click', function () {\n      if (defaultTheme.endsWith(':only')) {\n        return;\n      }\n      document.documentElement.classList.toggle('dark');\n      localStorage.theme = document.documentElement.classList.contains('dark') ? 'dark' : 'light';\n    });\n\n    attachEvent('[data-aw-social-share]', 'click', function (_, elem) {\n      const network = elem.getAttribute('data-aw-social-share');\n      const url = encodeURIComponent(elem.getAttribute('data-aw-url'));\n      const text = encodeURIComponent(elem.getAttribute('data-aw-text'));\n\n      let href;\n      switch (network) {\n        case 'facebook':\n          href = \\`https://www.facebook.com/sharer.php?u=\\${url}\\`;\n          break;\n        case 'twitter':\n          href = \\`https://twitter.com/intent/tweet?url=\\${url}&text=\\${text}\\`;\n          break;\n        case 'linkedin':\n          href = \\`https://www.linkedin.com/shareArticle?mini=true&url=\\${url}&title=\\${text}\\`;\n          break;\n        case 'whatsapp':\n          href = \\`https://wa.me/?text=\\${text}%20\\${url}\\`;\n          break;\n        case 'mail':\n          href = \\`mailto:?subject=%22\\${text}%22&body=\\${text}%20\\${url}\\`;\n          break;\n\n        default:\n          return;\n      }\n\n      const newlink = document.createElement('a');\n      newlink.target = '_blank';\n      newlink.href = href;\n      newlink.click();\n    });\n\n    const screenSize = window.matchMedia('(max-width: 767px)');\n    screenSize.addEventListener('change', function () {\n      document.querySelector('[data-aw-toggle-menu]')?.classList.remove('expanded');\n      document.body.classList.remove('overflow-hidden');\n      document.getElementById('header')?.classList.remove('h-screen');\n      document.getElementById('header')?.classList.remove('expanded');\n      document.getElementById('header')?.classList.remove('bg-page');\n      document.querySelector('#header nav')?.classList.add('hidden');\n      document.querySelector('#header > div > div:last-child')?.classList.add('hidden');\n    });\n\n    function applyHeaderStylesOnScroll() {\n      const header = document.querySelector('#header[data-aw-sticky-header]');\n      if (!header) return;\n      if (lastKnownScrollPosition > 60 && !header.classList.contains('scroll')) {\n        header.classList.add('scroll');\n      } else if (lastKnownScrollPosition <= 60 && header.classList.contains('scroll')) {\n        header.classList.remove('scroll');\n      }\n      ticking = false;\n    }\n    applyHeaderStylesOnScroll();\n\n    attachEvent([document], 'scroll', function () {\n      lastKnownScrollPosition = window.scrollY;\n\n      if (!ticking) {\n        window.requestAnimationFrame(() => {\n          applyHeaderStylesOnScroll();\n        });\n        ticking = true;\n      }\n    });\n  };\n  const onPageShow = function () {\n    document.documentElement.classList.add('motion-safe:scroll-smooth');\n    const elem = document.querySelector('[data-aw-toggle-menu]');\n    if (elem) {\n      elem.classList.remove('expanded');\n    }\n    document.body.classList.remove('overflow-hidden');\n    document.getElementById('header')?.classList.remove('h-screen');\n    document.getElementById('header')?.classList.remove('expanded');\n    document.querySelector('#header nav')?.classList.add('hidden');\n  };\n\n  window.onload = onLoad;\n  window.onpageshow = onPageShow;\n\n  document.addEventListener('astro:after-swap', () => {\n    initTheme();\n    onLoad();\n    onPageShow();\n  });\n})();<\/script> <script>\n  /* Inspired by: https://github.com/heidkaemper/tailwindcss-intersect */\n  const Observer = {\n    observer: null,\n    delayBetweenAnimations: 100,\n    animationCounter: 0,\n\n    start() {\n      const selectors = [\n        '[class*=\" intersect:\"]',\n        '[class*=\":intersect:\"]',\n        '[class^=\"intersect:\"]',\n        '[class=\"intersect\"]',\n        '[class*=\" intersect \"]',\n        '[class^=\"intersect \"]',\n        '[class$=\" intersect\"]',\n      ];\n\n      const elements = Array.from(document.querySelectorAll(selectors.join(',')));\n\n      const getThreshold = (element) => {\n        if (element.classList.contains('intersect-full')) return 0.99;\n        if (element.classList.contains('intersect-half')) return 0.5;\n        if (element.classList.contains('intersect-quarter')) return 0.25;\n        return 0;\n      };\n\n      elements.forEach((el) => {\n        el.setAttribute('no-intersect', '');\n        el._intersectionThreshold = getThreshold(el);\n      });\n\n      const callback = (entries) => {\n        entries.forEach((entry) => {\n          requestAnimationFrame(() => {\n            const target = entry.target;\n            const intersectionRatio = entry.intersectionRatio;\n            const threshold = target._intersectionThreshold;\n\n            if (target.classList.contains('intersect-no-queue')) {\n              if (entry.isIntersecting) {\n                target.removeAttribute('no-intersect');\n                if (target.classList.contains('intersect-once')) {\n                  this.observer.unobserve(target);\n                }\n              } else {\n                target.setAttribute('no-intersect', '');\n              }\n              return;\n            }\n\n            if (intersectionRatio >= threshold) {\n              if (!target.hasAttribute('data-animated')) {\n                target.removeAttribute('no-intersect');\n                target.setAttribute('data-animated', 'true');\n\n                const delay = this.animationCounter * this.delayBetweenAnimations;\n                this.animationCounter++;\n\n                target.style.transitionDelay = \\`\\${delay}ms\\`;\n                target.style.animationDelay = \\`\\${delay}ms\\`;\n\n                if (target.classList.contains('intersect-once')) {\n                  this.observer.unobserve(target);\n                }\n              }\n            } else {\n              target.setAttribute('no-intersect', '');\n              target.removeAttribute('data-animated');\n              target.style.transitionDelay = '';\n              target.style.animationDelay = '';\n\n              this.animationCounter = 0;\n            }\n          });\n        });\n      };\n\n      this.observer = new IntersectionObserver(callback.bind(this), { threshold: [0, 0.25, 0.5, 0.99] });\n\n      elements.forEach((el) => {\n        this.observer.observe(el);\n      });\n    },\n  };\n\n  Observer.start();\n\n  document.addEventListener('astro:after-swap', () => {\n    Observer.start();\n  });\n<\/script>"])), defineScriptVars({ defaultTheme: UI.theme, defaultLanguage: I18N.language }));
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/components/common/BasicScripts.astro", void 0);

const $$Astro$1 = createAstro("https://mofa.ai");
const $$ClientRouter = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro$1, $$props, $$slots);
  Astro2.self = $$ClientRouter;
  const { fallback = "animate" } = Astro2.props;
  return renderTemplate`<meta name="astro-view-transitions-enabled" content="true"><meta name="astro-view-transitions-fallback"${addAttribute(fallback, "content")}>${renderScript($$result, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/node_modules/astro/components/ClientRouter.astro?astro&type=script&index=0&lang.ts")}`;
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/node_modules/astro/components/ClientRouter.astro", void 0);

const $$Astro = createAstro("https://mofa.ai");
const $$Layout = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$Layout;
  const { metadata = {} } = Astro2.props;
  const { language, textDirection } = I18N;
  return renderTemplate`<html${addAttribute(language, "lang")}${addAttribute(textDirection, "dir")} class="2xl:text-[20px]"> <head>${renderComponent($$result, "CommonMeta", $$CommonMeta, {})}${renderComponent($$result, "Favicons", $$Favicons, {})}${renderComponent($$result, "CustomStyles", $$CustomStyles, {})}${renderComponent($$result, "ApplyColorMode", $$ApplyColorMode, {})}${renderComponent($$result, "Metadata", $$Metadata, { ...metadata })}${renderComponent($$result, "SiteVerification", $$SiteVerification, {})}${renderComponent($$result, "Analytics", $$Analytics, {})}<!-- Comment the line below to disable View Transitions -->${renderComponent($$result, "ClientRouter", $$ClientRouter, { "fallback": "swap" })}${renderHead()}</head> <body class="antialiased text-default bg-page tracking-tight"> ${renderSlot($$result, $$slots["default"])} ${renderComponent($$result, "BasicScripts", $$BasicScripts, {})} </body></html>`;
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/website/src/layouts/Layout.astro", void 0);

export { $$Layout as $, astroAssetsOptimizer as a, findImage as f, getImagesOptimized as g, isUnpicCompatible as i, unpicOptimizer as u };
