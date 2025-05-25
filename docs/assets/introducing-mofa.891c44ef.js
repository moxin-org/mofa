import { a as createComponent, r as renderTemplate, m as maybeRenderHead, u as unescapeHTML } from './astro.7f8fc68a.js';
import 'clsx';

const html = "<h1 id=\"mofa-正式发布让每个开发者都能成为-ai-工程师\">MoFA 正式发布：让每个开发者都能成为 AI 工程师</h1>\n<p>今天，我们非常激动地宣布 <strong>MoFA (Modular Framework for AI Agents)</strong> 正式发布！经过数月的开发和测试，我们终于推出了这个革命性的 AI 开发框架。</p>\n<h2 id=\"为什么创建-mofa\">为什么创建 MoFA？</h2>\n<p>在 AI 技术飞速发展的今天，构建 AI 应用的门槛依然很高。我们发现：</p>\n<ul>\n<li>🚧 <strong>技术门槛高</strong>：需要深厚的机器学习背景</li>\n<li>🔧 <strong>工具链复杂</strong>：各种框架和库让人眼花缭乱</li>\n<li>💰 <strong>成本高昂</strong>：从零开始构建需要大量时间和资源</li>\n<li>🧩 <strong>缺乏模块化</strong>：难以复用已有的 AI 能力</li>\n</ul>\n<p>MoFA 的诞生就是为了解决这些问题。</p>\n<h2 id=\"mofa-的核心理念\">MoFA 的核心理念</h2>\n<h3 id=\"1-像搭积木一样构建-ai\">1. 像搭积木一样构建 AI</h3>\n<pre class=\"astro-code github-dark\" style=\"background-color:#24292e;color:#e1e4e8; overflow-x: auto;\" tabindex=\"0\"><code><span class=\"line\"><span style=\"color:#6A737D\"># 简单的组合就能实现复杂功能</span></span>\n<span class=\"line\"><span style=\"color:#E1E4E8\">agent1 </span><span style=\"color:#F97583\">=</span><span style=\"color:#E1E4E8\"> Agent(</span><span style=\"color:#9ECBFF\">\"analyzer\"</span><span style=\"color:#E1E4E8\">)</span></span>\n<span class=\"line\"><span style=\"color:#E1E4E8\">agent2 </span><span style=\"color:#F97583\">=</span><span style=\"color:#E1E4E8\"> Agent(</span><span style=\"color:#9ECBFF\">\"summarizer\"</span><span style=\"color:#E1E4E8\">)</span></span>\n<span class=\"line\"><span style=\"color:#E1E4E8\">pipeline </span><span style=\"color:#F97583\">=</span><span style=\"color:#E1E4E8\"> Pipeline()</span></span>\n<span class=\"line\"><span style=\"color:#E1E4E8\">pipeline.add(agent1).add(agent2)</span></span></code></pre>\n<h3 id=\"2-开箱即用的预设代理\">2. 开箱即用的预设代理</h3>\n<p>我们提供了 100+ 预设代理，涵盖：</p>\n<ul>\n<li>文本处理</li>\n<li>数据分析</li>\n<li>代码生成</li>\n<li>图像理解</li>\n<li>多模态交互</li>\n</ul>\n<h3 id=\"3-简单但强大\">3. 简单但强大</h3>\n<p>5 分钟上手，但功能强大到足以构建企业级应用。</p>\n<h2 id=\"社区驱动的开发\">社区驱动的开发</h2>\n<p>MoFA 是一个开源项目，我们相信社区的力量：</p>\n<ul>\n<li>🌟 完全开源，MIT 许可证</li>\n<li>🤝 欢迎贡献代码和想法</li>\n<li>📚 详细的文档和教程</li>\n<li>💬 活跃的社区支持</li>\n</ul>\n<h2 id=\"加入我们\">加入我们</h2>\n<p>无论你是：</p>\n<ul>\n<li>刚接触 AI 的新手开发者</li>\n<li>想要提高效率的资深工程师</li>\n<li>希望快速验证想法的创业者</li>\n<li>对 AI 充满好奇的学生</li>\n</ul>\n<p>MoFA 都能帮助你快速实现 AI 应用的梦想。</p>\n<h2 id=\"下一步\">下一步</h2>\n<ul>\n<li>📖 查看<a href=\"/docs/quick-start\">快速开始指南</a></li>\n<li>🚀 探索<a href=\"/examples\">示例项目</a></li>\n<li>💬 加入 <a href=\"https://discord.gg/mofa\">Discord 社区</a></li>\n<li>⭐ 在 <a href=\"https://github.com/moxin-org/mofa\">GitHub</a> 上给我们 Star</li>\n</ul>\n<p>让我们一起，让 AI 开发变得简单、高效、有趣！</p>\n<hr>\n<p><em>MoFA Team</em>\n<em>2024年1月15日</em></p>";

				const frontmatter = {"title":"MoFA 正式发布：让每个开发者都能成为 AI 工程师","description":"我们很高兴地宣布 MoFA 正式发布，这是一个让普通开发者能够轻松构建 AI 应用的框架","date":"2024-01-15T00:00:00.000Z","author":"MoFA Team","tags":["发布","公告"]};
				const file = "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/mofa-website/src/content/blog/introducing-mofa.md";
				const url = undefined;
				function rawContent() {
					return "\n# MoFA 正式发布：让每个开发者都能成为 AI 工程师\n\n今天，我们非常激动地宣布 **MoFA (Modular Framework for AI Agents)** 正式发布！经过数月的开发和测试，我们终于推出了这个革命性的 AI 开发框架。\n\n## 为什么创建 MoFA？\n\n在 AI 技术飞速发展的今天，构建 AI 应用的门槛依然很高。我们发现：\n\n- 🚧 **技术门槛高**：需要深厚的机器学习背景\n- 🔧 **工具链复杂**：各种框架和库让人眼花缭乱\n- 💰 **成本高昂**：从零开始构建需要大量时间和资源\n- 🧩 **缺乏模块化**：难以复用已有的 AI 能力\n\nMoFA 的诞生就是为了解决这些问题。\n\n## MoFA 的核心理念\n\n### 1. 像搭积木一样构建 AI\n\n```python\n# 简单的组合就能实现复杂功能\nagent1 = Agent(\"analyzer\")\nagent2 = Agent(\"summarizer\")\npipeline = Pipeline()\npipeline.add(agent1).add(agent2)\n```\n\n### 2. 开箱即用的预设代理\n\n我们提供了 100+ 预设代理，涵盖：\n- 文本处理\n- 数据分析\n- 代码生成\n- 图像理解\n- 多模态交互\n\n### 3. 简单但强大\n\n5 分钟上手，但功能强大到足以构建企业级应用。\n\n## 社区驱动的开发\n\nMoFA 是一个开源项目，我们相信社区的力量：\n\n- 🌟 完全开源，MIT 许可证\n- 🤝 欢迎贡献代码和想法\n- 📚 详细的文档和教程\n- 💬 活跃的社区支持\n\n## 加入我们\n\n无论你是：\n- 刚接触 AI 的新手开发者\n- 想要提高效率的资深工程师\n- 希望快速验证想法的创业者\n- 对 AI 充满好奇的学生\n\nMoFA 都能帮助你快速实现 AI 应用的梦想。\n\n## 下一步\n\n- 📖 查看[快速开始指南](/docs/quick-start)\n- 🚀 探索[示例项目](/examples)\n- 💬 加入 [Discord 社区](https://discord.gg/mofa)\n- ⭐ 在 [GitHub](https://github.com/moxin-org/mofa) 上给我们 Star\n\n让我们一起，让 AI 开发变得简单、高效、有趣！\n\n---\n\n*MoFA Team*\n*2024年1月15日* ";
				}
				function compiledContent() {
					return html;
				}
				function getHeadings() {
					return [{"depth":1,"slug":"mofa-正式发布让每个开发者都能成为-ai-工程师","text":"MoFA 正式发布：让每个开发者都能成为 AI 工程师"},{"depth":2,"slug":"为什么创建-mofa","text":"为什么创建 MoFA？"},{"depth":2,"slug":"mofa-的核心理念","text":"MoFA 的核心理念"},{"depth":3,"slug":"1-像搭积木一样构建-ai","text":"1. 像搭积木一样构建 AI"},{"depth":3,"slug":"2-开箱即用的预设代理","text":"2. 开箱即用的预设代理"},{"depth":3,"slug":"3-简单但强大","text":"3. 简单但强大"},{"depth":2,"slug":"社区驱动的开发","text":"社区驱动的开发"},{"depth":2,"slug":"加入我们","text":"加入我们"},{"depth":2,"slug":"下一步","text":"下一步"}];
				}

				const Content = createComponent((result, _props, slots) => {
					const { layout, ...content } = frontmatter;
					content.file = file;
					content.url = url;

					return renderTemplate`${maybeRenderHead()}${unescapeHTML(html)}`;
				});

export { Content, compiledContent, Content as default, file, frontmatter, getHeadings, rawContent, url };
