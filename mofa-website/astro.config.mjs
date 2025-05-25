// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  site: 'https://moxin-org.github.io',
  base: '/mofa',
  outDir: '../docs',
  build: {
    inlineStylesheets: 'always',  // 强制内联CSS
    format: 'directory'           // 确保正确的目录结构
  },
  vite: {
    build: {
      rollupOptions: {
        output: {
          manualChunks: undefined,     // 避免代码分割
          entryFileNames: 'assets/[name].[hash].js',
          chunkFileNames: 'assets/[name].[hash].js',
          assetFileNames: 'assets/[name].[hash].[ext]'
        }
      }
    }
  }
});
