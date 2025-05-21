import { defineMiddleware } from 'astro:middleware';

export const onRequest = defineMiddleware((context, next) => {
  // Check if the URL path is /docs/getting-started
  if (context.url.pathname === '/docs/getting-started') {
    // Redirect to GitHub documentation
    return Response.redirect('https://github.com/moxin-org/mofa/blob/main/README.md', 302);
  }
  
  // Continue with the request for all other paths
  return next();
}); 