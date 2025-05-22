# MoFA 官方网站

基于 Astro 构建的 MoFA (Modular Framework for AI Agents) 官方网站，采用蒙德里安设计风格，支持通过 Markdown 文件管理内容。

## 🎨 设计特色

- **蒙德里安风格**：采用经典的红、蓝、黄、黑、白配色方案
- **响应式设计**：完美适配桌面端、平板和移动设备
- **模块化组件**：组件化开发，易于维护和扩展
- **高性能**：基于 Astro 的静态站点生成

## 📁 项目结构

```
mofa-website/
├── src/
│   ├── components/          # 可复用组件
│   │   ├── Header.astro    # 网站头部导航
│   │   ├── Footer.astro    # 网站底部
│   │   ├── Hero.astro      # 首页英雄区域
│   │   ├── Features.astro  # 功能特色展示
│   │   └── ...
│   ├── layouts/            # 页面布局
│   │   ├── BaseLayout.astro
│   │   └── DocsLayout.astro
│   ├── pages/              # 页面路由
│   │   ├── index.astro     # 首页
│   │   ├── blog/           # 博客页面
│   │   ├── docs/           # 文档页面
│   │   └── examples/       # 示例页面
│   ├── content/            # 内容文件（Markdown）
│   │   ├── blog/           # 博客文章
│   │   └── docs/           # 文档内容
│   ├── styles/             # 样式文件
│   └── assets/             # 静态资源
├── public/                 # 公共资源
└── .github/workflows/      # GitHub Actions 部署配置
```

## 🚀 快速开始

### 本地开发

```bash
# 克隆项目
git clone https://github.com/moxin-org/mofa-website.git
cd mofa-website

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 浏览器访问 http://localhost:4321
```

### 构建部署

```bash
# 构建静态站点
npm run build

# 预览构建结果
npm run preview
```

## ✏️ 内容管理

### 📝 添加博客文章

1. 在 `src/content/blog/` 目录下创建新的 `.md` 文件
2. 文件名格式：`your-post-title.md`
3. 文件开头需要包含 frontmatter：

```markdown
---
title: 文章标题
description: 文章描述
date: 2024-01-15
author: 作者名称
tags: [标签1, 标签2]
---

# 文章标题

你的文章内容...
```

### 📚 添加文档

1. 在 `src/content/docs/` 目录下创建新的 `.md` 文件
2. 文件开头包含 frontmatter：

```markdown
---
title: 文档标题
description: 文档描述
---

# 文档标题

你的文档内容...
```

3. 更新导航：在 `src/layouts/DocsLayout.astro` 中的 `docNav` 数组添加新文档链接

### 🎯 修改示例

编辑 `src/pages/examples/index.astro` 文件中的 `examples` 数组，添加或修改示例内容。

### 🎨 样式自定义

- **全局样式**：编辑 `src/styles/global.css`
- **Tailwind 配置**：修改 `tailwind.config.mjs`
- **蒙德里安配色**：在 Tailwind 配置中的 `colors` 部分自定义

## 🔧 高级配置

### GitHub Pages 部署

网站配置了自动部署到 GitHub Pages，当推送到 `main` 分支时自动触发。

确保在 GitHub 仓库设置中：
1. 启用 GitHub Pages
2. 选择 "GitHub Actions" 作为源

### 自定义域名

在 `astro.config.mjs` 中修改 `site` 和 `base` 配置：

```javascript
export default defineConfig({
  site: 'https://your-domain.com',
  base: '/', // 如果使用子路径，修改为如 '/mofa'
  // ...
});
```

### 添加新页面

1. 在 `src/pages/` 目录下创建 `.astro` 文件
2. 使用适当的布局：

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
---

<BaseLayout title="页面标题">
  <!-- 页面内容 -->
</BaseLayout>
```

## 🛠️ 开发指南

### 组件开发

创建新组件时：

1. 在 `src/components/` 目录下创建 `.astro` 文件
2. 使用 TypeScript 定义 Props 接口
3. 遵循蒙德里安设计风格
4. 确保响应式设计

示例：

```astro
---
export interface Props {
  title: string;
  description?: string;
}

const { title, description } = Astro.props;
---

<div class="card">
  <h2 class="text-xl font-semibold">{title}</h2>
  {description && <p class="text-gray-600">{description}</p>}
</div>
```

### 样式规范

- 使用 Tailwind CSS 类名
- 遵循蒙德里安配色方案：
  - 主色：`mondrian-red` (#E31E24)
  - 次要色：`mondrian-blue` (#0C5DA5)
  - 强调色：`mondrian-yellow` (#FFD500)
  - 中性色：`mondrian-black`、`mondrian-white`、`mondrian-gray`

### 响应式设计

确保所有组件在不同屏幕尺寸下都能正常显示：

- 移动端：`sm:` (640px+)
- 平板：`md:` (768px+)
- 桌面：`lg:` (1024px+)

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

我们欢迎所有形式的贡献！请查看 [贡献指南](CONTRIBUTING.md) 了解详情。

## 📞 联系我们

- GitHub: [moxin-org/mofa](https://github.com/moxin-org/mofa)
- Discord: [加入我们的社区](https://discord.gg/mofa)
- Email: contact@moxin.io

---

Made with ❤️ by the MoFA Team

```sh
npm create astro@latest -- --template minimal
```

[![Open in StackBlitz](https://developer.stackblitz.com/img/open_in_stackblitz.svg)](https://stackblitz.com/github/withastro/astro/tree/latest/examples/minimal)
[![Open with CodeSandbox](https://assets.codesandbox.io/github/button-edit-lime.svg)](https://codesandbox.io/p/sandbox/github/withastro/astro/tree/latest/examples/minimal)
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/withastro/astro?devcontainer_path=.devcontainer/minimal/devcontainer.json)

> 🧑‍🚀 **Seasoned astronaut?** Delete this file. Have fun!

## 🚀 Project Structure

Inside of your Astro project, you'll see the following folders and files:

```text
/
├── public/
├── src/
│   └── pages/
│       └── index.astro
└── package.json
```

Astro looks for `.astro` or `.md` files in the `src/pages/` directory. Each page is exposed as a route based on its file name.

There's nothing special about `src/components/`, but that's where we like to put any Astro/React/Vue/Svelte/Preact components.

Any static assets, like images, can be placed in the `public/` directory.

## 🧞 Commands

All commands are run from the root of the project, from a terminal:

| Command                   | Action                                           |
| :------------------------ | :----------------------------------------------- |
| `npm install`             | Installs dependencies                            |
| `npm run dev`             | Starts local dev server at `localhost:4321`      |
| `npm run build`           | Build your production site to `./dist/`          |
| `npm run preview`         | Preview your build locally, before deploying     |
| `npm run astro ...`       | Run CLI commands like `astro add`, `astro check` |
| `npm run astro -- --help` | Get help using the Astro CLI                     |

## 👀 Want to learn more?

Feel free to check [our documentation](https://docs.astro.build) or jump into our [Discord server](https://astro.build/chat).
