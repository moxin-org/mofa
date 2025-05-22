import '@astrojs/internal-helpers/path';
import 'cookie';
import 'kleur/colors';
import 'string-width';
import 'mime';
import './chunks/astro_7f8fc68a.mjs';
import 'clsx';
import { compile } from 'path-to-regexp';

if (typeof process !== "undefined") {
  let proc = process;
  if ("argv" in proc && Array.isArray(proc.argv)) {
    if (proc.argv.includes("--verbose")) ; else if (proc.argv.includes("--silent")) ; else ;
  }
}

new TextEncoder();

function getRouteGenerator(segments, addTrailingSlash) {
  const template = segments.map((segment) => {
    return "/" + segment.map((part) => {
      if (part.spread) {
        return `:${part.content.slice(3)}(.*)?`;
      } else if (part.dynamic) {
        return `:${part.content}`;
      } else {
        return part.content.normalize().replace(/\?/g, "%3F").replace(/#/g, "%23").replace(/%5B/g, "[").replace(/%5D/g, "]").replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      }
    }).join("");
  }).join("");
  let trailing = "";
  if (addTrailingSlash === "always" && segments.length) {
    trailing = "/";
  }
  const toPath = compile(template + trailing);
  return toPath;
}

function deserializeRouteData(rawRouteData) {
  return {
    route: rawRouteData.route,
    type: rawRouteData.type,
    pattern: new RegExp(rawRouteData.pattern),
    params: rawRouteData.params,
    component: rawRouteData.component,
    generate: getRouteGenerator(rawRouteData.segments, rawRouteData._meta.trailingSlash),
    pathname: rawRouteData.pathname || void 0,
    segments: rawRouteData.segments,
    prerender: rawRouteData.prerender,
    redirect: rawRouteData.redirect,
    redirectRoute: rawRouteData.redirectRoute ? deserializeRouteData(rawRouteData.redirectRoute) : void 0,
    fallbackRoutes: rawRouteData.fallbackRoutes.map((fallback) => {
      return deserializeRouteData(fallback);
    })
  };
}

function deserializeManifest(serializedManifest) {
  const routes = [];
  for (const serializedRoute of serializedManifest.routes) {
    routes.push({
      ...serializedRoute,
      routeData: deserializeRouteData(serializedRoute.routeData)
    });
    const route = serializedRoute;
    route.routeData = deserializeRouteData(serializedRoute.routeData);
  }
  const assets = new Set(serializedManifest.assets);
  const componentMetadata = new Map(serializedManifest.componentMetadata);
  const clientDirectives = new Map(serializedManifest.clientDirectives);
  return {
    ...serializedManifest,
    assets,
    componentMetadata,
    clientDirectives,
    routes
  };
}

const manifest = deserializeManifest({"adapterName":"","routes":[{"file":"","links":[],"scripts":[],"styles":[{"type":"external","src":"/mofa/_astro/_slug_.c35bd949.css"}],"routeData":{"route":"/","type":"page","pattern":"^\\/$","segments":[],"params":[],"component":"src/pages/index.astro","pathname":"/","prerender":false,"fallbackRoutes":[],"_meta":{"trailingSlash":"ignore"}}},{"file":"","links":[],"scripts":[],"styles":[{"type":"external","src":"/mofa/_astro/_slug_.c35bd949.css"}],"routeData":{"route":"/examples","type":"page","pattern":"^\\/examples\\/?$","segments":[[{"content":"examples","dynamic":false,"spread":false}]],"params":[],"component":"src/pages/examples/index.astro","pathname":"/examples","prerender":false,"fallbackRoutes":[],"_meta":{"trailingSlash":"ignore"}}},{"file":"","links":[],"scripts":[],"styles":[{"type":"external","src":"/mofa/_astro/_slug_.c35bd949.css"}],"routeData":{"route":"/blog","type":"page","pattern":"^\\/blog\\/?$","segments":[[{"content":"blog","dynamic":false,"spread":false}]],"params":[],"component":"src/pages/blog/index.astro","pathname":"/blog","prerender":false,"fallbackRoutes":[],"_meta":{"trailingSlash":"ignore"}}},{"file":"","links":[],"scripts":[],"styles":[{"type":"external","src":"/mofa/_astro/_slug_.c35bd949.css"}],"routeData":{"route":"/blog/[...slug]","type":"page","pattern":"^\\/blog(?:\\/(.*?))?\\/?$","segments":[[{"content":"blog","dynamic":false,"spread":false}],[{"content":"...slug","dynamic":true,"spread":true}]],"params":["...slug"],"component":"src/pages/blog/[...slug].astro","prerender":false,"fallbackRoutes":[],"_meta":{"trailingSlash":"ignore"}}},{"file":"","links":[],"scripts":[],"styles":[{"type":"external","src":"/mofa/_astro/_slug_.c35bd949.css"}],"routeData":{"route":"/docs","type":"page","pattern":"^\\/docs\\/?$","segments":[[{"content":"docs","dynamic":false,"spread":false}]],"params":[],"component":"src/pages/docs/index.astro","pathname":"/docs","prerender":false,"fallbackRoutes":[],"_meta":{"trailingSlash":"ignore"}}},{"file":"","links":[],"scripts":[],"styles":[{"type":"external","src":"/mofa/_astro/_slug_.c35bd949.css"}],"routeData":{"route":"/docs/[...slug]","type":"page","pattern":"^\\/docs(?:\\/(.*?))?\\/?$","segments":[[{"content":"docs","dynamic":false,"spread":false}],[{"content":"...slug","dynamic":true,"spread":true}]],"params":["...slug"],"component":"src/pages/docs/[...slug].astro","prerender":false,"fallbackRoutes":[],"_meta":{"trailingSlash":"ignore"}}}],"site":"https://moxin-org.github.io","base":"/mofa","trailingSlash":"ignore","compressHTML":true,"componentMetadata":[["/mnt/c/Users/Yao/Desktop/code/mofa/mofa-website/src/pages/docs/[...slug].astro",{"propagation":"in-tree","containsHead":true}],["/mnt/c/Users/Yao/Desktop/code/mofa/mofa-website/src/pages/docs/index.astro",{"propagation":"none","containsHead":true}],["/mnt/c/Users/Yao/Desktop/code/mofa/mofa-website/src/pages/blog/[...slug].astro",{"propagation":"in-tree","containsHead":true}],["/mnt/c/Users/Yao/Desktop/code/mofa/mofa-website/src/pages/blog/index.astro",{"propagation":"in-tree","containsHead":true}],["/mnt/c/Users/Yao/Desktop/code/mofa/mofa-website/src/pages/examples/index.astro",{"propagation":"none","containsHead":true}],["\u0000astro:content",{"propagation":"in-tree","containsHead":false}],["\u0000@astro-page:src/pages/blog/[...slug]@_@astro",{"propagation":"in-tree","containsHead":false}],["\u0000@astro-page:src/pages/blog/index@_@astro",{"propagation":"in-tree","containsHead":false}],["\u0000@astro-page:src/pages/docs/[...slug]@_@astro",{"propagation":"in-tree","containsHead":false}],["/mnt/c/Users/Yao/Desktop/code/mofa/mofa-website/src/pages/index.astro",{"propagation":"none","containsHead":true}]],"renderers":[],"clientDirectives":[["idle","(()=>{var i=t=>{let e=async()=>{await(await t())()};\"requestIdleCallback\"in window?window.requestIdleCallback(e):setTimeout(e,200)};(self.Astro||(self.Astro={})).idle=i;window.dispatchEvent(new Event(\"astro:idle\"));})();"],["load","(()=>{var e=async t=>{await(await t())()};(self.Astro||(self.Astro={})).load=e;window.dispatchEvent(new Event(\"astro:load\"));})();"],["media","(()=>{var s=(i,t)=>{let a=async()=>{await(await i())()};if(t.value){let e=matchMedia(t.value);e.matches?a():e.addEventListener(\"change\",a,{once:!0})}};(self.Astro||(self.Astro={})).media=s;window.dispatchEvent(new Event(\"astro:media\"));})();"],["only","(()=>{var e=async t=>{await(await t())()};(self.Astro||(self.Astro={})).only=e;window.dispatchEvent(new Event(\"astro:only\"));})();"],["visible","(()=>{var r=(i,c,s)=>{let n=async()=>{await(await i())()},t=new IntersectionObserver(e=>{for(let o of e)if(o.isIntersecting){t.disconnect(),n();break}});for(let e of s.children)t.observe(e)};(self.Astro||(self.Astro={})).visible=r;window.dispatchEvent(new Event(\"astro:visible\"));})();"]],"entryModules":{"\u0000@astro-page:src/pages/index@_@astro":"pages/index.astro.mjs","\u0000@astro-page:src/pages/examples/index@_@astro":"pages/examples.astro.mjs","\u0000@astro-page:src/pages/blog/index@_@astro":"pages/blog.astro.mjs","\u0000@astro-page:src/pages/blog/[...slug]@_@astro":"pages/blog/_---slug_.astro.mjs","\u0000@astro-page:src/pages/docs/index@_@astro":"pages/docs.astro.mjs","\u0000@astro-page:src/pages/docs/[...slug]@_@astro":"pages/docs/_---slug_.astro.mjs","\u0000@astro-renderers":"renderers.mjs","\u0000empty-middleware":"_empty-middleware.mjs","\u0000@astrojs-manifest":"manifest_0cae7378.mjs","/mnt/c/Users/Yao/Desktop/code/mofa/mofa-website/src/content/blog/introducing-mofa.md?astroContentCollectionEntry=true":"chunks/introducing-mofa_c31a09e2.mjs","/mnt/c/Users/Yao/Desktop/code/mofa/mofa-website/src/content/docs/quick-start.md?astroContentCollectionEntry=true":"chunks/quick-start_e66ff828.mjs","/mnt/c/Users/Yao/Desktop/code/mofa/mofa-website/src/content/blog/introducing-mofa.md?astroPropagatedAssets":"chunks/introducing-mofa_25ef78e1.mjs","/mnt/c/Users/Yao/Desktop/code/mofa/mofa-website/src/content/docs/quick-start.md?astroPropagatedAssets":"chunks/quick-start_be04ad1e.mjs","/mnt/c/Users/Yao/Desktop/code/mofa/mofa-website/src/content/blog/introducing-mofa.md":"chunks/introducing-mofa_fffda481.mjs","/mnt/c/Users/Yao/Desktop/code/mofa/mofa-website/src/content/docs/quick-start.md":"chunks/quick-start_42ebc9d4.mjs","astro:scripts/before-hydration.js":""},"assets":[]});

export { manifest };
