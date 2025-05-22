// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  site: 'https://moxin-org.github.io',
  base: '/mofa',
  outDir: '../docs',
  build: {
    inlineStylesheets: 'always'  // 强制内联CSS
  }
});
