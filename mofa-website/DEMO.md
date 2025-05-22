# MoFA 网站演示

## 🎨 设计特色展示

这个 MoFA 网站采用了蒙德里安艺术风格，体现了"组合"的核心理念：

### 视觉设计
- **配色方案**：经典的红(#E31E24)、蓝(#0C5DA5)、黄(#FFD500)、黑、白配色
- **几何元素**：网格布局体现模块化思想
- **动态效果**：悬浮动画和过渡效果

### 页面结构

1. **首页 (index.astro)**
   - Hero 区域：展示 MoFA 品牌和核心价值
   - Features：四大核心优势
   - QuickStart：三步快速上手
   - Examples：示例项目预览
   - Community：社区统计和加入方式

2. **文档系统 (/docs)**
   - 基于 Markdown 的文档管理
   - 左侧导航栏
   - 支持代码高亮

3. **博客系统 (/blog)**
   - 文章列表页面
   - 文章详情页面
   - 标签和分类支持

4. **示例页面 (/examples)**
   - 从入门到专家级的示例
   - 在线代码展示
   - 难度星级评估

## 🔧 内容管理

### 添加博客文章
只需在 `src/content/blog/` 目录下添加 Markdown 文件：

```markdown
---
title: 新文章标题
description: 文章描述
date: 2024-01-20
author: 作者名
tags: [AI, MoFA]
---

# 文章内容

这里是文章正文...
```

### 添加文档
在 `src/content/docs/` 目录下添加 Markdown 文件：

```markdown
---
title: 新文档
description: 文档描述
---

# 文档内容

这里是文档正文...
```

### 修改示例
编辑 `src/pages/examples/index.astro` 中的 `examples` 数组即可。

## 🚀 部署方式

### GitHub Pages
- 推送到 main 分支自动部署
- 使用 GitHub Actions
- 静态站点生成

### 本地开发
```bash
npm install
npm run dev
```

### 构建生产版本
```bash
npm run build
npm run preview
```

## 🎯 技术栈

- **框架**：Astro 5.8.0
- **样式**：Tailwind CSS 3.4.0
- **内容**：Markdown + Frontmatter
- **部署**：GitHub Pages
- **语言**：TypeScript

## 📱 响应式设计

网站完全响应式，支持：
- 📱 移动设备 (320px+)
- 📱 平板设备 (768px+)
- 💻 桌面设备 (1024px+)

## 🎨 设计理念

### 蒙德里安风格应用
1. **几何网格**：体现模块化组合
2. **经典配色**：传达专业和创新
3. **平衡布局**：简洁而不失动感
4. **线条分割**：清晰的信息层次

### 用户体验
- 直观的导航结构
- 快速加载的静态站点
- 无障碍访问支持
- SEO 友好的页面结构

这个网站完美体现了 MoFA "让普通开发者成为全栈 AI 工程师"的使命，通过简洁的设计和强大的功能，为用户提供最佳的浏览体验。 