import { a as createComponent, r as renderTemplate, d as renderHead, e as renderComponent, m as maybeRenderHead, b as addAttribute } from '../astro.7f8fc68a.js';
import 'clsx';
/* empty css                           */import { $ as $$BaseLayout, g as getCollection, a as $$DocsLayout } from './_...slug_.astro.43fe2e96.js';

var __freeze = Object.freeze;
var __defProp = Object.defineProperty;
var __template = (cooked, raw) => __freeze(__defProp(cooked, "raw", { value: __freeze(raw || cooked.slice()) }));
var _a;
const $$Index$3 = createComponent(($$result, $$props, $$slots) => {
  return renderTemplate(_a || (_a = __template(['<html lang="en" id="html-root" style="scroll-behavior: smooth;"> <head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title id="page-title">MoFA - Make Ordinary Developers Full-stack AI Engineers</title><!-- Favicon --><link rel="icon" type="image/png" href="https://avatars.githubusercontent.com/u/167464495?s=32"><link rel="shortcut icon" href="https://avatars.githubusercontent.com/u/167464495?s=32"><link rel="apple-touch-icon" href="https://avatars.githubusercontent.com/u/167464495?s=180"><link rel="icon" type="image/png" sizes="16x16" href="https://avatars.githubusercontent.com/u/167464495?s=16"><link rel="icon" type="image/png" sizes="32x32" href="https://avatars.githubusercontent.com/u/167464495?s=32"><link rel="icon" type="image/png" sizes="48x48" href="https://avatars.githubusercontent.com/u/167464495?s=48"><meta name="theme-color" content="#6366F1">', `</head> <body> <header style="position: sticky; top: 0; background: white; border-bottom: 4px solid var(--mondrian-black); box-shadow: 0 2px 4px rgba(0,0,0,0.1); z-index: 50;"> <nav class="container" style="padding: 16px; display: flex; align-items: center; justify-content: space-between;"> <a href="https://mofa.ai" style="display: flex; align-items: center; gap: 8px; text-decoration: none;" target="_blank" rel="noopener noreferrer"> <img src="https://avatars.githubusercontent.com/u/167464495" alt="MoFA Logo" style="width: 40px; height: 40px; border-radius: 8px;"> <span style="font-size: 1.5rem; font-weight: 700; color: var(--mondrian-black);">MoFA</span> </a> <div style="display: flex; align-items: center; gap: 32px;"> <a href="https://github.com/moxin-org/mofa/tree/main/Gosim_2024_Hackathon/documents" class="nav-link" target="_blank" rel="noopener noreferrer" data-en="Docs" data-zh="\u6587\u6863">Docs</a> <a href="https://demo.mofa.ai" class="nav-link" target="_blank" rel="noopener noreferrer" data-en="Examples" data-zh="\u793A\u4F8B">Examples</a> <a href="http://blog.mofa.ai/" class="nav-link" target="_blank" rel="noopener noreferrer" data-en="Blog" data-zh="\u535A\u5BA2">Blog</a> <!-- \u8BED\u8A00\u5207\u6362\u6309\u94AE --> <div style="display: flex; align-items: center; gap: 8px;"> <button id="lang-toggle" style="
            display: flex;
            align-items: center;
            gap: 4px;
            padding: 8px 12px;
            background: transparent;
            border: 2px solid var(--mondrian-gray);
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.2s ease;
            font-size: 0.875rem;
            font-weight: 500;
            color: var(--mondrian-black);
          " onmouseover="this.style.borderColor='var(--mondrian-red)'" onmouseout="this.style.borderColor='var(--mondrian-gray)'"> <span id="current-lang">\u{1F1FA}\u{1F1F8} EN</span> <span style="font-size: 0.75rem; opacity: 0.6;">\u25BC</span> </button> </div> <a href="https://github.com/moxin-org/mofa" class="btn-primary" target="_blank" rel="noopener noreferrer" style="display: flex; align-items: center; gap: 8px;"> <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" style="flex-shrink: 0;"> <path d="M12 0C5.374 0 0 5.373 0 12 0 17.302 3.438 21.8 8.207 23.387c.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"></path> </svg>
GitHub
</a> </div> </nav> </header> <!-- \u4E3B\u8981\u5185\u5BB9 --> <main style="flex: 1;"> <!-- Hero \u533A\u57DF --> <section class="py-20" style="position: relative; overflow: hidden;"> <!-- \u8499\u5FB7\u91CC\u5B89\u80CC\u666F --> <div style="position: absolute; inset: 0; opacity: 0.1;"> <div class="mondrian-grid" style="grid-template-columns: repeat(12, 1fr); grid-template-rows: repeat(8, 1fr); height: 100%;"> <div class="mondrian-block animate-grid-float" style="background-color: var(--mondrian-red); grid-column: span 3; grid-row: span 2;"></div> <div class="mondrian-block animate-grid-float" style="background-color: var(--mondrian-yellow); grid-column: span 2; grid-row: span 3; animation-delay: 0.5s;"></div> <div class="mondrian-block animate-grid-float" style="background-color: var(--mondrian-blue); grid-column: span 4; grid-row: span 2; animation-delay: 1s;"></div> <div class="mondrian-block" style="background-color: var(--mondrian-white); grid-column: span 3; grid-row: span 3;"></div> </div> </div> <div class="container" style="position: relative; z-index: 10;"> <div class="max-w-4xl mx-auto text-center"> <!-- Logo --> <div style="display: flex; justify-content: center; margin-bottom: 32px;"> <div class="mondrian-grid" style="grid-template-columns: repeat(3, 1fr); grid-template-rows: repeat(3, 1fr); width: 96px; height: 96px; transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'"> <div class="mondrian-block animate-pulse-slow" style="background-color: var(--mondrian-red); min-height: auto;"></div> <div class="mondrian-block" style="background-color: var(--mondrian-white); min-height: auto; grid-column: span 2;"></div> <div class="mondrian-block animate-pulse-slow" style="background-color: var(--mondrian-yellow); min-height: auto; grid-row: span 2; animation-delay: 0.5s;"></div> <div class="mondrian-block animate-pulse-slow" style="background-color: var(--mondrian-blue); min-height: auto; animation-delay: 1s;"></div> <div class="mondrian-block" style="background-color: var(--mondrian-white); min-height: auto;"></div> <div class="mondrian-block animate-pulse-slow" style="background-color: var(--mondrian-red); min-height: auto; animation-delay: 1.5s;"></div> </div> </div> <!-- \u4E3B\u6807\u9898 --> <h1 style="font-size: 3rem; font-weight: 700; margin-bottom: 24px;"> <span class="gradient-text">MoFA</span> </h1> <!-- \u526F\u6807\u9898 --> <p class="text-2xl font-medium mb-4" style="color: var(--mondrian-black);" data-en="Make Ordinary Developers Full-stack AI Engineers" data-zh="\u8BA9\u666E\u901A\u5F00\u53D1\u8005\u6210\u4E3A\u5168\u6808 AI \u5DE5\u7A0B\u5E08">
Make Ordinary Developers Full-stack AI Engineers
</p> <p class="text-xl mb-8 text-gray-600" data-en="Modular Framework for AI Agents" data-zh="\u6A21\u5757\u5316 AI \u4EE3\u7406\u6846\u67B6">
Modular Framework for AI Agents
</p> <!-- \u63CF\u8FF0 --> <p class="text-xl text-gray-700 mb-12 max-w-2xl mx-auto" data-en="A composable AI agent framework that enables every developer to easily build, debug, and deploy complex AI applications" data-zh="\u901A\u8FC7\u53EF\u7EC4\u5408\u7684 AI \u4EE3\u7406\u6846\u67B6\uFF0C\u8BA9\u6BCF\u4E2A\u5F00\u53D1\u8005\u90FD\u80FD\u8F7B\u677E\u6784\u5EFA\u3001\u8C03\u8BD5\u548C\u90E8\u7F72\u590D\u6742\u7684 AI \u5E94\u7528">
A composable AI agent framework that enables every developer to easily build, debug, and deploy complex AI applications
</p> <!-- CTA \u6309\u94AE --> <div style="display: flex; flex-direction: column; gap: 16px; justify-content: center; margin-bottom: 64px;"> <div style="display: flex; flex-wrap: wrap; gap: 16px; justify-content: center;"> <a href="https://github.com/moxin-org/mofa/blob/main/python/README.md#2-quick-start-guide" target="_blank" rel="noopener noreferrer" class="btn-primary" style="font-size: 1.125rem; padding: 16px 32px;" data-en="\u{1F680} Quick Start" data-zh="\u{1F680} \u5FEB\u901F\u5F00\u59CB">
\u{1F680} Quick Start
</a> <a href="#why-mofa" rel="noopener noreferrer" class="btn-outline" style="font-size: 1.125rem; padding: 16px 32px;" data-en="\u{1F4A1} Learn More" data-zh="\u{1F4A1} \u4E86\u89E3\u66F4\u591A">
\u{1F4A1} Learn More
</a> </div> </div> <!-- \u5FEB\u901F\u7EDF\u8BA1 --> <div class="grid grid-cols-3 gap-8 max-w-2xl mx-auto"> <div class="text-center"> <div class="text-3xl font-bold" style="color: var(--mondrian-red);" data-en="5 min" data-zh="5\u5206\u949F">5 min</div> <div class="text-sm text-gray-600" data-en="Quick Setup" data-zh="\u5FEB\u901F\u4E0A\u624B">Quick Setup</div> </div> <div class="text-center"> <div class="text-3xl font-bold" style="color: var(--mondrian-blue);">100+</div> <div class="text-sm text-gray-600" data-en="Built-in Agents" data-zh="\u5185\u7F6E\u4EE3\u7406">Built-in Agents</div> </div> <div class="text-center"> <div class="text-3xl font-bold" style="color: var(--mondrian-yellow);">\u221E</div> <div class="text-sm text-gray-600" data-en="Combinations" data-zh="\u7EC4\u5408\u53EF\u80FD">Combinations</div> </div> </div> </div> </div> </section> <!-- \u5C0F\u578B\u5206\u9694\u7EBF --> <div class="mini-divider"> <div class="mini-line red-line"></div> <div class="mini-line blue-line"></div> <div class="mini-line yellow-line"></div> </div> <!-- \u6838\u5FC3\u4F18\u52BF --> <section id="why-mofa" class="py-20" style="background-color: #f9fafb;"> <div class="container"> <div class="text-center mb-16"> <h2 class="text-4xl font-bold mb-4" data-en="Why Choose <span class='gradient-text'>MoFA</span>" data-zh="\u4E3A\u4EC0\u4E48\u9009\u62E9 <span class='gradient-text'>MoFA</span>">
Why Choose <span class="gradient-text">MoFA</span> </h2> <p class="text-xl text-gray-600 max-w-2xl mx-auto" data-en="Making AI development simple, efficient, and enjoyable" data-zh="\u8BA9 AI \u5F00\u53D1\u53D8\u5F97\u7B80\u5355\u3001\u9AD8\u6548\u3001\u6709\u8DA3">
Making AI development simple, efficient, and enjoyable
</p> </div> <div class="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto"> <div class="card" style="border: 2px solid var(--mondrian-black); transition: border-width 0.2s ease;" onmouseover="this.style.borderWidth='4px'" onmouseout="this.style.borderWidth='2px'"> <div style="display: flex; align-items: flex-start; gap: 16px;"> <div style="padding: 12px; border-radius: 8px; background-color: var(--mondrian-red); color: white; flex-shrink: 0;">
\u{1F9E9}
</div> <div> <h3 class="text-xl font-semibold mb-2" data-en="Composable Agent Architecture" data-zh="\u53EF\u7EC4\u5408\u7684\u4EE3\u7406\u67B6\u6784">Composable Agent Architecture</h3> <p class="text-gray-600" data-en="Build complex AI applications by connecting agents via YAML-defined flows. Leverage a core kernel with modules for RAG (embedding, splitting, vector stores), planning, and tool integration. Easily orchestrate data flow between agents." data-zh="\u901A\u8FC7 YAML \u5B9A\u4E49\u7684\u5DE5\u4F5C\u6D41\u8FDE\u63A5\u4EE3\u7406\uFF0C\u6784\u5EFA\u590D\u6742\u7684 AI \u5E94\u7528\u3002\u5229\u7528\u5305\u542B RAG\uFF08\u5D4C\u5165\u3001\u5206\u5272\u3001\u5411\u91CF\u5B58\u50A8\uFF09\u3001\u89C4\u5212\u548C\u5DE5\u5177\u96C6\u6210\u7B49\u6A21\u5757\u7684\u6838\u5FC3\u5185\u6838\u3002\u8F7B\u677E\u7F16\u6392\u4EE3\u7406\u95F4\u7684\u6570\u636E\u6D41\u52A8\u3002">
Build complex AI applications by connecting agents via YAML-defined flows. Leverage a core kernel with modules for RAG (embedding, splitting, vector stores), planning, and tool integration. Easily orchestrate data flow between agents.
</p> </div> </div> </div> <div class="card" style="border: 2px solid var(--mondrian-black); transition: border-width 0.2s ease;" onmouseover="this.style.borderWidth='4px'" onmouseout="this.style.borderWidth='2px'"> <div style="display: flex; align-items: flex-start; gap: 16px;"> <div style="padding: 12px; border-radius: 8px; background-color: var(--mondrian-blue); color: white; flex-shrink: 0;">
\u26A1
</div> <div> <h3 class="text-xl font-semibold mb-2" data-en="Rapid Agent Development" data-zh="\u5FEB\u901F\u4EE3\u7406\u5F00\u53D1">Rapid Agent Development</h3> <p class="text-gray-600" data-en="MoFA offers a clear structure for agent development, significantly reducing boilerplate and letting you focus on core logic. The MoFA Stage visual IDE further accelerates the entire development cycle, from creation to debugging. Get started in just 5 minutes." data-zh="MoFA \u63D0\u4F9B\u6E05\u6670\u7684\u4EE3\u7406\u5F00\u53D1\u7ED3\u6784\uFF0C\u5927\u5E45\u51CF\u5C11\u6837\u677F\u4EE3\u7801\uFF0C\u8BA9\u60A8\u4E13\u6CE8\u4E8E\u6838\u5FC3\u4E1A\u52A1\u903B\u8F91\u3002\u7ED3\u5408 MoFA Stage \u53EF\u89C6\u5316 IDE\uFF0C\u53EF\u8FDB\u4E00\u6B65\u52A0\u901F\u4ECE\u521B\u5EFA\u5230\u8C03\u8BD5\u7684\u5B8C\u6574\u5F00\u53D1\u5468\u671F\u30025\u5206\u949F\u5373\u53EF\u5FEB\u901F\u4E0A\u624B\u3002">
MoFA offers a clear structure for agent development, significantly reducing boilerplate and letting you focus on core logic. The MoFA Stage visual IDE further accelerates the entire development cycle, from creation to debugging. Get started in just 5 minutes.
</p> </div> </div> </div> <div class="card" style="border: 2px solid var(--mondrian-black); transition: border-width 0.2s ease;" onmouseover="this.style.borderWidth='4px'" onmouseout="this.style.borderWidth='2px'"> <div style="display: flex; align-items: flex-start; gap: 16px;"> <div style="padding: 12px; border-radius: 8px; background-color: var(--mondrian-yellow); color: var(--mondrian-black); flex-shrink: 0;">
\u{1F680}
</div> <div> <h3 class="text-xl font-semibold mb-2" data-en="Rich Agent Hub & Dev Tools" data-zh="\u4E30\u5BCC\u4EE3\u7406\u4E2D\u5FC3\u4E0E\u5F00\u53D1\u5DE5\u5177">Rich Agent Hub &amp; Dev Tools</h3> <p class="text-gray-600" data-en="Access 100+ pre-built agents from our Agent Hub, covering data connectors, LLM integrations, and specialized tools. MoFA Stage further enhances development with visual agent management, an integrated terminal, and an advanced code editor." data-zh="\u4ECE\u6211\u4EEC\u7684\u4EE3\u7406\u4E2D\u5FC3\u83B7\u53D6100+\u9884\u6784\u5EFA\u4EE3\u7406\uFF0C\u6DB5\u76D6\u6570\u636E\u8FDE\u63A5\u5668\u3001LLM \u96C6\u6210\u548C\u4E13\u7528\u5DE5\u5177\u3002MoFA Stage \u901A\u8FC7\u53EF\u89C6\u5316\u4EE3\u7406\u7BA1\u7406\u3001\u96C6\u6210\u7EC8\u7AEF\u548C\u9AD8\u7EA7\u4EE3\u7801\u7F16\u8F91\u5668\u8FDB\u4E00\u6B65\u589E\u5F3A\u5F00\u53D1\u4F53\u9A8C\u3002">
Access 100+ pre-built agents from our Agent Hub, covering data connectors, LLM integrations, and specialized tools. MoFA Stage further enhances development with visual agent management, an integrated terminal, and an advanced code editor.
</p> </div> </div> </div> <div class="card" style="border: 2px solid var(--mondrian-black); transition: border-width 0.2s ease;" onmouseover="this.style.borderWidth='4px'" onmouseout="this.style.borderWidth='2px'"> <div style="display: flex; align-items: flex-start; gap: 16px;"> <div style="padding: 12px; border-radius: 8px; background-color: var(--mondrian-black); color: white; flex-shrink: 0;">
\u{1F527}
</div> <div> <h3 class="text-xl font-semibold mb-2" data-en="Highly Extensible Framework" data-zh="\u9AD8\u5EA6\u53EF\u6269\u5C55\u6846\u67B6">Highly Extensible Framework</h3> <p class="text-gray-600" data-en="Easily write custom Python agents. Integrate third-party tools, models, and data sources through well-defined interfaces. Extend core functionalities like memory (e.g., Mem0 integration) or RAG strategies by implementing custom components." data-zh="\u8F7B\u677E\u7F16\u5199\u81EA\u5B9A\u4E49 Python \u4EE3\u7406\u3002\u901A\u8FC7\u5B9A\u4E49\u826F\u597D\u7684\u63A5\u53E3\u96C6\u6210\u7B2C\u4E09\u65B9\u5DE5\u5177\u3001\u6A21\u578B\u548C\u6570\u636E\u6E90\u3002\u901A\u8FC7\u5B9E\u73B0\u81EA\u5B9A\u4E49\u7EC4\u4EF6\u6765\u6269\u5C55\u6838\u5FC3\u529F\u80FD\uFF0C\u5982\u8BB0\u5FC6\uFF08\u4F8B\u5982 Mem0 \u96C6\u6210\uFF09\u6216 RAG \u7B56\u7565\u3002">
Easily write custom Python agents. Integrate third-party tools, models, and data sources through well-defined interfaces. Extend core functionalities like memory (e.g., Mem0 integration) or RAG strategies by implementing custom components.
</p> </div> </div> </div> </div> <div class="text-center mt-16 mb-8" style="display: none;"> <h3 class="text-3xl font-bold" data-en="Highlight: Your AI Agent IDE - <span class='gradient-text'>MoFA Stage</span>" data-zh="\u6838\u5FC3\u529F\u80FD\uFF1A\u4F60\u7684 AI Agent IDE - <span class='gradient-text'>MoFA Stage</span>">
Highlight: Your AI Agent IDE - <span class="gradient-text">MoFA Stage</span> </h3> </div> <p class="text-xl text-gray-600 max-w-3xl mx-auto text-center mb-12" style="display: none;" data-en="A visual management platform for MoFA - your web-based IDE for AI agents." data-zh="MoFA \u7684\u53EF\u89C6\u5316\u7BA1\u7406\u5E73\u53F0 - \u4F60\u7684Agent\u4E13\u5C5E Web IDE.">
A visual management platform for MoFA - your web-based IDE.
</p> <div class="max-w-6xl mx-auto" style="display: none;"> <!-- \u5E73\u53F0\u7279\u8272\u5C55\u793A --> <div class="grid md:grid-cols-3 gap-8 mb-16"> <div class="card" style="border: 2px solid var(--mondrian-black); transition: all 0.3s ease; padding: 16px;" onmouseover="this.style.borderWidth='4px'; this.style.transform='translateY(-8px)'" onmouseout="this.style.borderWidth='2px'; this.style.transform='translateY(0)'"> <div style="text-align: center;"> <div style="
                   width: 48px;
                   height: 48px;
                   margin: 0 auto 12px;
                   background: linear-gradient(135deg, var(--mondrian-red), #8B5CF6);
                   border-radius: 12px;
                   display: flex;
                   align-items: center;
                   justify-content: center;
                   font-size: 1.5rem;
                   color: white;
                   box-shadow: 0 6px 18px rgba(99, 102, 241, 0.3);
                 ">\u{1F4BB}</div> <h3 class="text-base font-semibold mb-1" data-en="Visual Agent Management" data-zh="\u53EF\u89C6\u5316\u4EE3\u7406\u7BA1\u7406">Visual Agent Management</h3> <p class="text-gray-600 text-xs leading-snug" data-en="Create, edit, and manage AI agents through an intuitive web interface" data-zh="\u901A\u8FC7\u76F4\u89C2\u7684\u7F51\u9875\u754C\u9762\u521B\u5EFA\u3001\u7F16\u8F91\u548C\u7BA1\u7406 AI \u4EE3\u7406">
Create, edit, and manage AI agents through an intuitive web interface - no command line expertise required
</p> </div> </div> <div class="card" style="border: 2px solid var(--mondrian-black); transition: all 0.3s ease; padding: 16px;" onmouseover="this.style.borderWidth='4px'; this.style.transform='translateY(-8px)'" onmouseout="this.style.borderWidth='2px'; this.style.transform='translateY(0)'"> <div style="text-align: center;"> <div style="
                   width: 48px;
                   height: 48px;
                   margin: 0 auto 12px;
                   background: linear-gradient(135deg, var(--mondrian-blue), #06B6D4);
                   border-radius: 12px;
                   display: flex;
                   align-items: center;
                   justify-content: center;
                   font-size: 1.5rem;
                   color: white;
                   box-shadow: 0 6px 18px rgba(14, 165, 233, 0.3);
                 ">\u{1F5A5}\uFE0F</div> <h3 class="text-base font-semibold mb-1" data-en="Integrated Terminal" data-zh="\u96C6\u6210\u7EC8\u7AEF">Integrated Terminal</h3> <p class="text-gray-600 text-xs leading-snug" data-en="Built-in web terminal with SSH access - execute commands and monitor agents directly from your browser" data-zh="\u5185\u7F6E\u7F51\u9875\u7EC8\u7AEF\u652F\u6301 SSH \u8BBF\u95EE - \u76F4\u63A5\u5728\u6D4F\u89C8\u5668\u4E2D\u6267\u884C\u547D\u4EE4\u548C\u76D1\u63A7\u4EE3\u7406">
Built-in web terminal with SSH access - execute commands and monitor agents directly from your browser
</p> </div> </div> <div class="card" style="border: 2px solid var(--mondrian-black); transition: all 0.3s ease; padding: 16px;" onmouseover="this.style.borderWidth='4px'; this.style.transform='translateY(-8px)'" onmouseout="this.style.borderWidth='2px'; this.style.transform='translateY(0)'"> <div style="text-align: center;"> <div style="
                   width: 48px;
                   height: 48px;
                   margin: 0 auto 12px;
                   background: linear-gradient(135deg, var(--mondrian-yellow), #FBBF24);
                   border-radius: 12px;
                   display: flex;
                   align-items: center;
                   justify-content: center;
                   font-size: 1.5rem;
                   color: var(--mondrian-black);
                   box-shadow: 0 6px 18px rgba(245, 158, 11, 0.3);
                 ">\u{1F4DD}</div> <h3 class="text-base font-semibold mb-1" data-en="Advanced Code Editor" data-zh="\u4EE3\u7801\u7F16\u8F91\u5668">Code Editor</h3> <p class="text-gray-600 text-xs leading-snug" data-en="Monaco-powered editor with syntax highlighting, auto-completion, and instant Markdown preview" data-zh="\u57FA\u4E8E Monaco \u7684\u7F16\u8F91\u5668\uFF0C\u652F\u6301\u8BED\u6CD5\u9AD8\u4EAE\u3001\u81EA\u52A8\u8865\u5168\u548C Markdown \u5373\u65F6\u9884\u89C8">
Monaco-powered editor with syntax highlighting, auto-completion, and instant Markdown preview - just like VS Code
</p> </div> </div> </div> <!-- \u5E73\u53F0\u67B6\u6784\u5C55\u793A --> <div class="bg-white rounded-lg shadow-lg p-8" style="border: 2px solid var(--mondrian-black); display: none;"> <div class="text-center mb-8"> <h3 class="text-2xl font-bold mb-4" data-en="Full-Stack Architecture" data-zh="\u5168\u6808\u67B6\u6784">Full-Stack Architecture</h3> <p class="text-gray-600" data-en="Built with modern technologies for optimal performance and developer experience" data-zh="\u4F7F\u7528\u73B0\u4EE3\u6280\u672F\u6784\u5EFA\uFF0C\u786E\u4FDD\u6700\u4F73\u6027\u80FD\u548C\u5F00\u53D1\u4F53\u9A8C">
Built with modern technologies for optimal performance and developer experience
</p> </div> <div class="grid md:grid-cols-2 gap-12"> <!-- \u524D\u7AEF\u6280\u672F\u6808 --> <div> <h4 class="text-lg font-semibold mb-4 flex items-center gap-2" data-en="\u{1F3A8} Frontend Stack" data-zh="\u{1F3A8} \u524D\u7AEF\u6280\u672F\u6808">
\u{1F3A8} Frontend Stack
</h4> <div class="space-y-3"> <div class="flex items-center gap-3"> <div style="width: 12px; height: 12px; background: #42b883; border-radius: 50%;"></div> <span class="font-medium">Vue 3</span> <span class="text-sm text-gray-500" data-en="Progressive Framework" data-zh="\u6E10\u8FDB\u5F0F\u6846\u67B6">Progressive Framework</span> </div> <div class="flex items-center gap-3"> <div style="width: 12px; height: 12px; background: #409eff; border-radius: 50%;"></div> <span class="font-medium">Element Plus</span> <span class="text-sm text-gray-500" data-en="UI Components" data-zh="UI \u7EC4\u4EF6\u5E93">UI Components</span> </div> <div class="flex items-center gap-3"> <div style="width: 12px; height: 12px; background: var(--mondrian-blue); border-radius: 50%;"></div> <span class="font-medium">Monaco Editor</span> <span class="text-sm text-gray-500" data-en="VS Code Engine" data-zh="VS Code \u5F15\u64CE">VS Code Engine</span> </div> <div class="flex items-center gap-3"> <div style="width: 12px; height: 12px; background: #000; border-radius: 50%;"></div> <span class="font-medium">XTerm.js</span> <span class="text-sm text-gray-500" data-en="Terminal Emulation" data-zh="\u7EC8\u7AEF\u6A21\u62DF">Terminal Emulation</span> </div> </div> </div> <!-- \u540E\u7AEF\u6280\u672F\u6808 --> <div> <h4 class="text-lg font-semibold mb-4 flex items-center gap-2" data-en="\u2699\uFE0F Backend Stack" data-zh="\u2699\uFE0F \u540E\u7AEF\u6280\u672F\u6808">
\u2699\uFE0F Backend Stack
</h4> <div class="space-y-3"> <div class="flex items-center gap-3"> <div style="width: 12px; height: 12px; background: #306998; border-radius: 50%;"></div> <span class="font-medium">Python + Flask</span> <span class="text-sm text-gray-500" data-en="RESTful API" data-zh="RESTful API">RESTful API</span> </div> <div class="flex items-center gap-3"> <div style="width: 12px; height: 12px; background: var(--mondrian-red); border-radius: 50%;"></div> <span class="font-medium">WebSocket</span> <span class="text-sm text-gray-500" data-en="Real-time Communication" data-zh="\u5B9E\u65F6\u901A\u4FE1">Real-time Communication</span> </div> <div class="flex items-center gap-3"> <div style="width: 12px; height: 12px; background: #ff6b35; border-radius: 50%;"></div> <span class="font-medium">SSH Integration</span> <span class="text-sm text-gray-500" data-en="Terminal Access" data-zh="\u7EC8\u7AEF\u8BBF\u95EE">Terminal Access</span> </div> <div class="flex items-center gap-3"> <div style="width: 12px; height: 12px; background: var(--mondrian-yellow); border-radius: 50%;"></div> <span class="font-medium">ttyd Service</span> <span class="text-sm text-gray-500" data-en="Web Terminal" data-zh="\u7F51\u9875\u7EC8\u7AEF">Web Terminal</span> </div> </div> </div> </div> </div> <!-- \u5FEB\u901F\u5F00\u59CB\u6309\u94AE --> <div class="text-center mt-12"> <a href="https://github.com/moxin-org/mofa/tree/main/MoFA_stage" target="_blank" rel="noopener noreferrer" class="btn-primary" style="font-size: 1.125rem; padding: 16px 32px; margin-right: 16px;" data-en="\u{1F680} Explore MoFA_Stage" data-zh="\u{1F680} \u63A2\u7D22 MoFA_Stage">
\u{1F680} Explore MoFA_Stage
</a> <a href="https://github.com/moxin-org/mofa/tree/main/MoFA_stage#quick-start" target="_blank" rel="noopener noreferrer" class="btn-outline" style="font-size: 1.125rem; padding: 16px 32px;" data-en="\u{1F4D6} Quick Start Guide" data-zh="\u{1F4D6} \u5FEB\u901F\u5F00\u59CB\u6307\u5357">
\u{1F4D6} Quick Start Guide
</a> </div> </div> </div> </section> <!-- \u5C0F\u578B\u5206\u9694\u7EBF --> <div class="mini-divider"> <div class="mini-line blue-line"></div> <div class="mini-line yellow-line"></div> <div class="mini-line red-line"></div> </div> <!-- Agent & Flow \u6982\u5FF5\u4ECB\u7ECD --> <section class="py-20" style="background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);"> <div class="container"> <div class="text-center mb-16"> <h2 class="text-4xl font-bold mb-4" data-en="From Agents to <span class='gradient-text'>Flows</span>" data-zh="\u4ECE\u4EE3\u7406\u5230<span class='gradient-text'>\u5DE5\u4F5C\u6D41</span>">
From Agents to <span class="gradient-text">Flows</span> </h2> <p class="text-xl text-gray-600 max-w-3xl mx-auto" data-en="MoFA transforms individual AI agents into powerful workflows through intelligent composition and data flow orchestration" data-zh="MoFA \u901A\u8FC7\u667A\u80FD\u7EC4\u5408\u548C\u6570\u636E\u6D41\u7F16\u6392\uFF0C\u5C06\u72EC\u7ACB\u7684 AI \u4EE3\u7406\u8F6C\u5316\u4E3A\u5F3A\u5927\u7684\u5DE5\u4F5C\u6D41">
MoFA transforms individual AI agents into powerful workflows through intelligent composition and data flow orchestration
</p> </div> <!-- \u6982\u5FF5\u89E3\u91CA --> <div class="grid md:grid-cols-2 gap-12 mb-20" style="display: none;"> <div class="space-y-8"> <div class="card" style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(14, 165, 233, 0.05) 100%); border: 2px solid rgba(99, 102, 241, 0.2);"> <h3 class="text-2xl font-bold mb-4 flex items-center gap-3" data-en="\u{1F916} What is an Agent?" data-zh="\u{1F916} \u4EC0\u4E48\u662F\u4EE3\u7406\uFF1F">
\u{1F916} What is an Agent?
</h3> <p class="text-gray-700 mb-4" data-en="An agent is a self-contained AI component that performs a specific task - like extracting keywords, analyzing documents, or generating reports. Each agent has clear inputs and outputs." data-zh="\u4EE3\u7406\u662F\u4E00\u4E2A\u72EC\u7ACB\u7684 AI \u7EC4\u4EF6\uFF0C\u6267\u884C\u7279\u5B9A\u4EFB\u52A1 - \u5982\u63D0\u53D6\u5173\u952E\u8BCD\u3001\u5206\u6790\u6587\u6863\u6216\u751F\u6210\u62A5\u544A\u3002\u6BCF\u4E2A\u4EE3\u7406\u90FD\u6709\u660E\u786E\u7684\u8F93\u5165\u548C\u8F93\u51FA\u3002">
An agent is a self-contained AI component that performs a specific task - like extracting keywords, analyzing documents, or generating reports. Each agent has clear inputs and outputs.
</p> <div class="agent-demo" style="
                padding: 16px;
                background: white;
                border-radius: 8px;
                border: 1px solid rgba(99, 102, 241, 0.2);
                display: flex;
                align-items: center;
                gap: 12px;
              "> <div style="
                  padding: 8px 12px;
                  background: linear-gradient(135deg, var(--mondrian-red), #8B5CF6);
                  color: white;
                  border-radius: 6px;
                  font-size: 0.875rem;
                  font-weight: 500;
                ">Input</div> <div style="color: var(--mondrian-red); font-weight: bold;">\u2192</div> <div style="
                  padding: 8px 12px;
                  background: var(--mondrian-gray);
                  border-radius: 6px;
                  font-size: 0.875rem;
                  font-weight: 500;
                ">Agent</div> <div style="color: var(--mondrian-red); font-weight: bold;">\u2192</div> <div style="
                  padding: 8px 12px;
                  background: linear-gradient(135deg, var(--mondrian-blue), #06B6D4);
                  color: white;
                  border-radius: 6px;
                  font-size: 0.875rem;
                  font-weight: 500;
                ">Output</div> </div> </div> </div> <div class="space-y-8"> <div class="card" style="background: linear-gradient(135deg, rgba(14, 165, 233, 0.05) 0%, rgba(245, 158, 11, 0.05) 100%); border: 2px solid rgba(14, 165, 233, 0.2);"> <h3 class="text-2xl font-bold mb-4 flex items-center gap-3" data-en="\u{1F504} What is a Flow?" data-zh="\u{1F504} \u4EC0\u4E48\u662F\u5DE5\u4F5C\u6D41\uFF1F">
\u{1F504} What is a Flow?
</h3> <p class="text-gray-700 mb-4" data-en="A flow connects multiple agents together, where the output of one agent becomes the input of another. This creates powerful, multi-step AI pipelines that can solve complex problems." data-zh="\u5DE5\u4F5C\u6D41\u5C06\u591A\u4E2A\u4EE3\u7406\u8FDE\u63A5\u5728\u4E00\u8D77\uFF0C\u5176\u4E2D\u4E00\u4E2A\u4EE3\u7406\u7684\u8F93\u51FA\u6210\u4E3A\u53E6\u4E00\u4E2A\u4EE3\u7406\u7684\u8F93\u5165\u3002\u8FD9\u521B\u5EFA\u4E86\u5F3A\u5927\u7684\u591A\u6B65\u9AA4 AI \u7BA1\u9053\uFF0C\u53EF\u4EE5\u89E3\u51B3\u590D\u6742\u95EE\u9898\u3002">
A flow connects multiple agents together, where the output of one agent becomes the input of another. This creates powerful, multi-step AI pipelines that can solve complex problems.
</p> <div class="flow-demo" style="
                padding: 16px;
                background: white;
                border-radius: 8px;
                border: 1px solid rgba(14, 165, 233, 0.2);
              "> <div style="display: flex; flex-direction: column; gap: 8px;"> <div style="display: flex; align-items: center; gap: 8px;"> <div class="agent-box">Agent A</div> <div class="arrow">\u2192</div> <div class="agent-box">Agent B</div> </div> <div style="display: flex; align-items: center; gap: 8px; margin-left: 80px;"> <div class="arrow">\u2193</div> </div> <div style="display: flex; align-items: center; gap: 8px; margin-left: 80px;"> <div class="agent-box">Agent C</div> </div> </div> </div> </div> </div> </div> <!-- \u5B9E\u9645\u6848\u4F8B\u5C55\u793A\uFF1AMultiple Flow Examples --> <div class="bg-white rounded-lg shadow-lg p-8 mb-16"> <h3 class="text-3xl font-bold text-center mb-8" data-en="Real Examples: Agent Flows in Action" data-zh="\u5B9E\u9645\u6848\u4F8B\uFF1A\u4EE3\u7406\u5DE5\u4F5C\u6D41\u5B9E\u6218">
Real Examples: Agent Flows in Action
</h3> <p class="text-center text-gray-600 mb-12 max-w-3xl mx-auto" data-en="Explore different types of AI workflows - from research automation to weather prediction and web scraping" data-zh="\u63A2\u7D22\u4E0D\u540C\u7C7B\u578B\u7684 AI \u5DE5\u4F5C\u6D41 - \u4ECE\u7814\u7A76\u81EA\u52A8\u5316\u5230\u5929\u6C14\u9884\u6D4B\u548C\u7F51\u9875\u6293\u53D6">
Explore different types of AI workflows - from research automation to weather prediction and web scraping
</p> <!-- Demo Carousel Controls --> <div class="demo-carousel-container" style="position: relative; max-width: 100%; margin: 0 auto 32px;"> <!-- Left Arrow --> <button class="carousel-arrow carousel-arrow-left" style="
              position: absolute;
              left: 0px;
              top: 50%;
              transform: translateY(-50%);
              width: 40px;
              height: 40px;
              border-radius: 50%;
              border: 2px solid var(--mondrian-gray);
              background: white;
              box-shadow: 0 2px 10px rgba(0,0,0,0.2);
              color: var(--mondrian-black);
              font-size: 18px;
              cursor: pointer;
              transition: all 0.2s ease;
              z-index: 10;
              display: flex;
              align-items: center;
              justify-content: center;
            " onmouseover="this.style.borderColor='var(--mondrian-red)'; this.style.background='var(--mondrian-red)'; this.style.color='white'" onmouseout="this.style.borderColor='var(--mondrian-gray)'; this.style.background='white'; this.style.color='var(--mondrian-black)'">
\u2190
</button> <!-- Demo Selector --> <div class="text-center mb-4"> <div class="demo-tabs-container" style="
                display: flex;
                justify-content: center;
                gap: 4px;
                padding: 8px 40px;
                background: linear-gradient(to right, rgba(240,240,240,0.9), rgba(240,240,240,0.9) 10%, rgba(240,240,240,0.9) 90%, rgba(240,240,240,0.9));
                border-radius: 12px;
                overflow-x: auto;
                white-space: nowrap;
                max-width: 100%;
                width: 950px;
                margin: 0 auto;
                scrollbar-width: none; /* Firefox */
                -ms-overflow-style: none; /* IE and Edge */
              "> <style>
                .demo-tabs-container::-webkit-scrollbar {
                  display: none; /* Chrome, Safari and Opera */
                }
                .demo-tab {
                  padding: 6px 8px;
                  border-radius: 8px;
                  background: white;
                  border: none;
                  font-size: 0.8rem;
                  font-weight: 500;
                  color: var(--mondrian-black);
                  cursor: pointer;
                  transition: all 0.2s ease;
                  display: inline-flex;
                  align-items: center;
                  gap: 4px;
                  min-width: 100px;
                  justify-content: center;
                  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                }
                .demo-tab:hover {
                  background-color: #e2e8f0;
                  transform: translateY(-2px);
                }
                .demo-tab.active {
                  background: var(--mondrian-blue);
                  color: white;
                  box-shadow: 0 2px 6px rgba(37, 99, 235, 0.4);
                }
                .demo-emoji {
                  font-size: 1rem;
                }
              </style> <button class="demo-tab active" data-demo="hello-world"> <span class="demo-emoji">\u{1F44B}</span> <span class="demo-name" data-en="Hello World" data-zh="Hello World">Hello World</span> </button> <button class="demo-tab" data-demo="browser-use"> <span class="demo-emoji">\u{1F310}</span> <span class="demo-name" data-en="Browser Use" data-zh="\u6D4F\u89C8\u5668\u8C03\u7528">Browser Use</span> </button> <button class="demo-tab" data-demo="deep-research"> <span class="demo-emoji">\u{1F52C}</span> <span class="demo-name" data-en="Deep Research" data-zh="\u6DF1\u5EA6\u7814\u7A76">Deep Research</span> </button> <button class="demo-tab" data-demo="firecrawl"> <span class="demo-emoji">\u{1F577}\uFE0F</span> <span class="demo-name" data-en="Web Scraping" data-zh="\u7F51\u9875\u6293\u53D6">Web Scraping</span> </button> <button class="demo-tab" data-demo="weather"> <span class="demo-emoji">\u{1F324}\uFE0F</span> <span class="demo-name" data-en="Weather" data-zh="\u5929\u6C14\u83B7\u53D6">Weather</span> </button> <button class="demo-tab" data-demo="arxiv"> <span class="demo-emoji">\u{1F4DA}</span> <span class="demo-name" data-en="arXiv Research" data-zh="arXiv\u7814\u7A76">arXiv Research</span> </button> <button class="demo-tab" data-demo="moly-client"> <span class="demo-emoji">\u{1F916}</span> <span class="demo-name" data-en="Moly Client" data-zh="Moly\u5BA2\u6237\u7AEF">Moly Client</span> </button> <button class="demo-tab" data-demo="mem0-dataflow"> <span class="demo-emoji">\u{1F9E0}</span> <span class="demo-name" data-en="Mem0 Flow" data-zh="Mem0\u6D41\u7A0B">Mem0 Flow</span> </button> <button class="demo-tab" data-demo="camera-screenshot"> <span class="demo-emoji">\u{1F4F8}</span> <span class="demo-name" data-en="Camera Screenshot" data-zh="\u76F8\u673A\u622A\u56FE">Camera Screenshot</span> </button> </div> </div> <!-- Right Arrow --> <button class="carousel-arrow carousel-arrow-right" style="
              position: absolute;
              right: 0px;
              top: 50%;
              transform: translateY(-50%);
              width: 40px;
              height: 40px;
              border-radius: 50%;
              border: 2px solid var(--mondrian-gray);
              background: white;
              box-shadow: 0 2px 10px rgba(0,0,0,0.2);
              color: var(--mondrian-black);
              font-size: 18px;
              cursor: pointer;
              transition: all 0.2s ease;
              z-index: 10;
              display: flex;
              align-items: center;
              justify-content: center;
            " onmouseover="this.style.borderColor='var(--mondrian-red)'; this.style.background='var(--mondrian-red)'; this.style.color='white'" onmouseout="this.style.borderColor='var(--mondrian-gray)'; this.style.background='white'; this.style.color='var(--mondrian-black)'">
\u2192
</button> </div> <!-- Script to dynamically generate flow components --> <script>
            // Define all demos and their node configurations
            const demoConfigs = {
              'hello-world': {
                nodes: [
                  { emoji: '\u{1F4AC}', title: { en: 'Terminal Input', zh: '\u7EC8\u7AEF\u8F93\u5165' }, subtitle: { en: 'User query input', zh: '\u7528\u6237\u67E5\u8BE2\u8F93\u5165' } },
                  { emoji: '\u{1F916}', title: { en: 'Hello Agent', zh: '\u95EE\u5019\u4EE3\u7406' }, subtitle: { en: 'Process & respond', zh: '\u5904\u7406\u5E76\u54CD\u5E94' } }
                ],
                id: 'hello-world-demo',
                isActive: true
              },
              'browser-use': {
                nodes: [
                  { emoji: '\u2328\uFE0F', title: { en: 'Terminal Input', zh: '\u7EC8\u7AEF\u8F93\u5165' }, subtitle: { en: 'Browser task input', zh: '\u6D4F\u89C8\u5668\u4EFB\u52A1\u8F93\u5165' } },
                  { emoji: '\u{1F310}', title: { en: 'Browser Agent', zh: '\u6D4F\u89C8\u5668\u4EE3\u7406' }, subtitle: { en: 'Automate browser', zh: '\u81EA\u52A8\u5316\u6D4F\u89C8\u5668' } }
                ],
                id: 'browser-use-demo'
              },
              'deep-research': {
                nodes: [
                  { emoji: '\u{1F5A5}\uFE0F', title: { en: 'OpenAI Server', zh: 'OpenAI\u670D\u52A1\u5668' }, subtitle: { en: 'Chat interface', zh: '\u804A\u5929\u63A5\u53E3' } },
                  { emoji: '\u{1F52C}', title: { en: 'Research Planner', zh: '\u7814\u7A76\u89C4\u5212\u5668' }, subtitle: { en: 'Deep analysis', zh: '\u6DF1\u5EA6\u5206\u6790' } }
                ],
                id: 'deep-research-demo'
              },
              'firecrawl': {
                nodes: [
                  { emoji: '\u{1F517}', title: { en: 'URL Input', zh: 'URL\u8F93\u5165' }, subtitle: { en: 'Receive target URL', zh: '\u63A5\u6536\u76EE\u6807URL' } },
                  { emoji: '\u{1F577}\uFE0F', title: { en: 'Firecrawl Agent', zh: 'Firecrawl\u4EE3\u7406' }, subtitle: { en: 'Scrape & extract', zh: '\u6293\u53D6\u548C\u63D0\u53D6' } },
                  { emoji: '\u{1F4CB}', title: { en: 'Structured Data', zh: '\u7ED3\u6784\u5316\u6570\u636E' }, subtitle: { en: 'Clean content output', zh: '\u6E05\u6D01\u5185\u5BB9\u8F93\u51FA' } }
                ],
                id: 'firecrawl-demo'
              },
              'weather': {
                nodes: [
                  { emoji: '\u{1F4CD}', title: { en: 'Geolocation Agent', zh: '\u5730\u7406\u5B9A\u4F4D\u4EE3\u7406' }, subtitle: { en: 'Find coordinates', zh: '\u67E5\u627E\u5750\u6807' } },
                  { emoji: '\u{1F30A}', title: { en: 'Windy Crawler', zh: 'Windy\u722C\u866B' }, subtitle: { en: 'Scrape weather data', zh: '\u6293\u53D6\u5929\u6C14\u6570\u636E' } },
                  { emoji: '\u{1F9E0}', title: { en: 'Weather Predictor', zh: '\u5929\u6C14\u9884\u6D4B\u5668' }, subtitle: { en: 'Analyze & predict', zh: '\u5206\u6790\u548C\u9884\u6D4B' } },
                  { emoji: '\u{1F4CA}', title: { en: 'Weather Report', zh: '\u5929\u6C14\u62A5\u544A' }, subtitle: { en: 'Final forecast', zh: '\u6700\u7EC8\u9884\u62A5' } }
                ],
                id: 'weather-demo',
                nodeWidth: 140 // narrower for 4 nodes
              },
              'arxiv': {
                nodes: [
                  { emoji: '\u{1F50D}', title: { en: 'Keyword Extractor', zh: '\u5173\u952E\u8BCD\u63D0\u53D6\u5668' }, subtitle: { en: 'Extract keywords', zh: '\u63D0\u53D6\u5173\u952E\u8BCD' } },
                  { emoji: '\u{1F4E5}', title: { en: 'Paper Downloader', zh: '\u8BBA\u6587\u4E0B\u8F7D\u5668' }, subtitle: { en: 'Download papers', zh: '\u4E0B\u8F7D\u8BBA\u6587' } },
                  { emoji: '\u{1F52C}', title: { en: 'Paper Analyzer', zh: '\u8BBA\u6587\u5206\u6790\u5668' }, subtitle: { en: 'Analyze content', zh: '\u5206\u6790\u5185\u5BB9' } },
                  { emoji: '\u270D\uFE0F', title: { en: 'Report Writer', zh: '\u62A5\u544A\u64B0\u5199\u5668' }, subtitle: { en: 'Generate report', zh: '\u751F\u6210\u62A5\u544A' } },
                  { emoji: '\u{1F4AC}', title: { en: 'Feedback Agent', zh: '\u53CD\u9988\u4EE3\u7406' }, subtitle: { en: 'Suggest changes', zh: '\u63D0\u4F9B\u5EFA\u8BAE' } },
                  { emoji: '\u{1F527}', title: { en: 'Refinement Agent', zh: '\u4F18\u5316\u4EE3\u7406' }, subtitle: { en: 'Improve report', zh: '\u4F18\u5316\u62A5\u544A' } }
                ],
                id: 'arxiv-demo',
                nodeWidth: 120,
                nodePadding: 12,
                fontSize: {
                  emoji: '1.2rem',
                  title: '0.8rem',
                  subtitle: '0.65rem'
                },
                arrowWidth: 15,
                gap: 16
              },
              'moly-client': {
                nodes: [
                  { emoji: '\u{1F916}', title: { en: 'OpenAI Server', zh: 'OpenAI\u670D\u52A1\u5668' }, subtitle: { en: 'Chat completions', zh: '\u5BF9\u8BDD\u8865\u5168' } },
                  { emoji: '\u{1F9E0}', title: { en: 'Reasoner Agent', zh: '\u63A8\u7406\u4EE3\u7406' }, subtitle: { en: 'Process & reason', zh: '\u5904\u7406\u4E0E\u63A8\u7406' } }
                ],
                id: 'moly-client-demo',
                nodeWidth: 140
              },
              'mem0-dataflow': {
                nodes: [
                  { emoji: '\u2328\uFE0F', title: { en: 'Terminal Input', zh: '\u7EC8\u7AEF\u8F93\u5165' }, subtitle: { en: 'User input', zh: '\u7528\u6237\u8F93\u5165' } },
                  { emoji: '\u{1F9E0}', title: { en: 'Memory Agent', zh: '\u8BB0\u5FC6\u4EE3\u7406' }, subtitle: { en: 'Memory operations', zh: '\u8BB0\u5FC6\u64CD\u4F5C' } },
                  { emoji: '\u{1F914}', title: { en: 'Reasoner', zh: '\u63A8\u7406\u5668' }, subtitle: { en: 'Process & analyze', zh: '\u5904\u7406\u4E0E\u5206\u6790' } }
                ],
                id: 'mem0-dataflow-demo',
                nodeWidth: 140
              },
              'camera-screenshot': {
                nodes: [
                  { emoji: '\u2328\uFE0F', title: { en: 'Terminal Input', zh: '\u7EC8\u7AEF\u8F93\u5165' }, subtitle: { en: 'Command input', zh: '\u547D\u4EE4\u8F93\u5165' } },
                  { emoji: '\u{1F4F8}', title: { en: 'Camera Screenshot', zh: '\u76F8\u673A\u622A\u56FE' }, subtitle: { en: 'Capture screen', zh: '\u6355\u83B7\u5C4F\u5E55' } }
                ],
                id: 'camera-screenshot-demo',
                nodeWidth: 140
              }
            };

            // Function to generate a flow node HTML
            function generateNode(node, config) {
              const width = config.nodeWidth || 160;
              const padding = config.nodePadding || 16;
              const fontSize = config.fontSize || {
                emoji: '1.5rem',
                title: '0.9rem',
                subtitle: '0.7rem'
              };
              
              return \`
                <div class="flow-step">
                  <div class="agent-card interactive-agent" style="
                    padding: \${padding}px;
                    text-align: center;
                    transition: all 0.3s ease;
                    color: #333;
                    width: \${width}px;
                    background: rgba(245, 247, 250, 0.8);
                    border-radius: 4px;
                  ">
                    <div style="font-size: \${fontSize.emoji}; margin-bottom: 8px;">\${node.emoji}</div>
                    <h4 style="font-weight: bold; margin-bottom: 4px; font-size: \${fontSize.title};" 
                        data-en="\${node.title.en}"
                        data-zh="\${node.title.zh}">\${node.title.en}</h4>
                    <p style="font-size: \${fontSize.subtitle}; opacity: 0.9;" 
                       data-en="\${node.subtitle.en}"
                       data-zh="\${node.subtitle.zh}">\${node.subtitle.en}</p>
                  </div>
                </div>
              \`;
            }

            // Function to generate arrow between nodes
            function generateArrow(config) {
              const arrowWidth = config.arrowWidth || 40;
              
              return \`
                <div style="display: flex; align-items: center; color: var(--mondrian-black); position: relative;">
                  <div style="width: \${arrowWidth}px; height: 2px; background-color: var(--mondrian-black);"></div>
                  <div style="position: absolute; right: -5px; width: 0; height: 0; border-top: 5px solid transparent; border-bottom: 5px solid transparent; border-left: 5px solid var(--mondrian-black);"></div>
              </div>
              \`;
            }

            // Function to generate a complete flow container
            function generateFlowContainer(demoKey, config) {
              const { nodes, id, isActive } = config;
              const gap = config.gap || 40;
              
              let nodesHtml = '';
              
              nodes.forEach((node, index) => {
                nodesHtml += generateNode(node, config);
                
                // Add arrow if not the last node
                if (index < nodes.length - 1) {
                  nodesHtml += generateArrow(config);
                }
              });
              
              return \`
                <div class="demo-content \${isActive ? 'active' : ''}" id="\${id}" style="\${!isActive ? 'display: none;' : ''}">
              <div class="flow-container" style="
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    gap: \${gap}px;
                max-width: 1000px;
                margin: 0 auto;
                position: relative;
                    padding: 20px 0;
                    flex-wrap: nowrap;
                    overflow-x: auto;
                  ">
                    \${nodesHtml}
                <svg style="
                  position: absolute;
                  top: 0;
                  left: 0;
                  width: 100%;
                  height: 100%;
                  pointer-events: none;
                  z-index: -1;
                      display: none;
                " class="flow-connections">
                </svg>
              </div>
            </div>
              \`;
            }

            // Function to generate all demos
            function generateAllDemos() {
              let demosHtml = '';
              
              Object.keys(demoConfigs).forEach(demoKey => {
                demosHtml += generateFlowContainer(demoKey, demoConfigs[demoKey]);
              });
              
              return demosHtml;
            }
          <\/script> <!-- Interactive Flow Visualization --> <div class="flow-visualization"> <script>
              document.write(generateAllDemos());
            <\/script> </div> </div> </div> </section> <!-- \u5C0F\u578B\u5206\u9694\u7EBF --> <div class="mini-divider"> <div class="mini-line yellow-line"></div> <div class="mini-line red-line"></div> <div class="mini-line blue-line"></div> </div> <!-- Demo Video Section --> <section class="py-20" style="background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);"> <div class="container"> <div class="text-center mb-16"> <h2 class="text-4xl font-bold mb-4" data-en="See MoFA in <span class='gradient-text'>Action</span>" data-zh="\u89C2\u770B MoFA <span class='gradient-text'>\u5B9E\u6218\u6F14\u793A</span>">
See MoFA in <span class="gradient-text">Action</span> </h2> <p class="text-xl text-gray-600 max-w-2xl mx-auto" data-en="Watch how developers use MoFA to build sophisticated AI applications in minutes" data-zh="\u89C2\u770B\u5F00\u53D1\u8005\u5982\u4F55\u5728\u51E0\u5206\u949F\u5185\u4F7F\u7528 MoFA \u6784\u5EFA\u590D\u6742\u7684\u4EBA\u5DE5\u667A\u80FD\u5E94\u7528">Watch how developers use MoFA to build sophisticated AI applications in minutes</p> <!-- Video Embed --> <div class="video-container rounded-lg shadow-2xl overflow-hidden mx-auto" style="max-width: 800px; background-color: #2d3748;"> <iframe id="demo-video-iframe" width="100%" style="aspect-ratio: 16/9; display: block;" src="https://www.youtube.com/embed/YOUR_PLACEHOLDER_VIDEO_ID" title="MoFA in Action Demo Video" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen>
          </iframe> </div> </div> </div> <!-- \u5C0F\u578B\u5206\u9694\u7EBF --> <div class="mini-divider"> <div class="mini-line red-line"></div> <div class="mini-line blue-line"></div> <div class="mini-line yellow-line"></div> </div> </section></main> <footer style="background-color: var(--mondrian-black); color: white;"> <div class="container py-12"> <div class="text-center"> <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin-bottom: 16px;"> <img src="https://avatars.githubusercontent.com/u/167464495" alt="MoFA Logo" style="width: 32px; height: 32px; border-radius: 6px;"> <span style="font-size: 1.25rem; font-weight: 700;">MoFA</span> </div> <p style="color: #9ca3af; margin-bottom: 8px;" data-en="Make Ordinary Developers Full-stack AI Engineers" data-zh="\u8BA9\u666E\u901A\u5F00\u53D1\u8005\u6210\u4E3A\u5168\u6808 AI \u5DE5\u7A0B\u5E08">
Make Ordinary Developers Full-stack AI Engineers
</p> <p style="color: #9ca3af; margin-bottom: 24px;" data-en="Modular Framework for AI Agents" data-zh="\u6A21\u5757\u5316 AI \u4EE3\u7406\u6846\u67B6">
Modular Framework for AI Agents
</p> <div style="display: flex; justify-content: center; gap: 32px; margin-bottom: 16px;"> <a href="https://github.com/moxin-org/mofa" target="_blank" rel="noopener noreferrer" style="color: #9ca3af; text-decoration: none; transition: color 0.2s ease;" onmouseover="this.style.color='white'" onmouseout="this.style.color='#9ca3af'">GitHub</a> <a href="https://discord.gg/mofatesttesttesttse" target="_blank" rel="noopener noreferrer" style="color: #9ca3af; text-decoration: none; transition: color 0.2s ease;" onmouseover="this.style.color='white'" onmouseout="this.style.color='#9ca3af'">Discord</a> <a href="https://github.com/moxin-org/mofa/tree/main/Gosim_2024_Hackathon/documents" target="_blank" rel="noopener noreferrer" style="color: #9ca3af; text-decoration: none; transition: color 0.2s ease;" onmouseover="this.style.color='white'" onmouseout="this.style.color='#9ca3af'" data-en="Docs" data-zh="\u6587\u6863">Docs</a> </div> <p style="color: #6b7280; font-size: 0.875rem;" data-en="\xA9 2025 MoFA. All rights reserved. | Made with \u2764\uFE0F by MoFA Team" data-zh="\xA9 2025 MoFA. \u4FDD\u7559\u6240\u6709\u6743\u5229. | Made with \u2764\uFE0F by MoFA Team">
&copy; 2024 MoFA. All rights reserved. | Made with \u2764\uFE0F by MoFA Team
</p> </div> </div> </footer> <!-- \u8FD4\u56DE\u9876\u90E8\u6309\u94AE --> <button id="back-to-top" title="Go to top" style="
    display: none; /* Hidden by default */
    position: fixed;
    bottom: 30px;
    right: 30px;
    z-index: 99;
    border: none;
    outline: none;
    background-color: var(--mondrian-red);
    color: white;
    cursor: pointer;
    padding: 15px;
    border-radius: 50%;
    font-size: 18px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    transition: background-color 0.3s, opacity 0.3s, visibility 0.3s;
  ">
\u2191
</button> <!-- \u8BED\u8A00\u5207\u6362\u811A\u672C --> <script>
    // \u8FD4\u56DE\u9876\u90E8\u6309\u94AE\u903B\u8F91
    const backToTopButton = document.getElementById('back-to-top');

    window.onscroll = function() {
      if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
        backToTopButton.style.display = "block";
      } else {
        backToTopButton.style.display = "none";
      }
    };

    backToTopButton.addEventListener('click', function(){
      window.scrollTo({top: 0, behavior: 'smooth'});
    });

    // \u8BED\u8A00\u6570\u636E\u548C\u5207\u6362\u903B\u8F91
    const languages = {
      en: {
        flag: '\u{1F1FA}\u{1F1F8}',
        name: 'EN',
        title: 'MoFA - Make Ordinary Developers Full-stack AI Engineers'
      },
      zh: {
        flag: '\u{1F1E8}\u{1F1F3}',
        name: '\u4E2D\u6587',
        title: 'MoFA - \u8BA9\u666E\u901A\u5F00\u53D1\u8005\u6210\u4E3A\u5168\u6808 AI \u5DE5\u7A0B\u5E08'
      }
    };

    let currentLang = 'en'; // \u9ED8\u8BA4\u82F1\u6587

    function updateLanguage(lang) {
      currentLang = lang;
      
      // \u66F4\u65B0\u9875\u9762title
      document.getElementById('page-title').textContent = languages[lang].title;
      
      // \u66F4\u65B0html lang\u5C5E\u6027
      document.getElementById('html-root').setAttribute('lang', lang === 'zh' ? 'zh-CN' : 'en');
      
      // \u66F4\u65B0\u8BED\u8A00\u5207\u6362\u6309\u94AE\u663E\u793A
      const currentLangEl = document.getElementById('current-lang');
      const otherLang = lang === 'en' ? 'zh' : 'en';
      currentLangEl.textContent = \`\${languages[otherLang].flag} \${languages[otherLang].name}\`;
      
      // \u66F4\u65B0\u6240\u6709\u5E26\u6709data-en\u548Cdata-zh\u5C5E\u6027\u7684\u5143\u7D20
      const elements = document.querySelectorAll('[data-en][data-zh]');
      elements.forEach(element => {
        const text = element.getAttribute(\`data-\${lang}\`);
        if (text) {
          element.innerHTML = text;
        }
      });

      // \u66F4\u65B0\u89C6\u9891iframe\u7684src
      const videoIframe = document.getElementById('demo-video-iframe');
      if (videoIframe) {
        if (lang === 'zh') {
          videoIframe.src = "//player.bilibili.com/player.html?bvid=BV15fQPY6EnD&page=1&high_quality=1&danmaku=0";
        } else { // 'en' or default
          videoIframe.src = "https://www.youtube.com/embed/YOUR_PLACEHOLDER_VIDEO_ID"; // TODO: Replace with actual English video when ready
        }
      }
      
      // \u4FDD\u5B58\u8BED\u8A00\u8BBE\u7F6E\u5230localStorage
      localStorage.setItem('mofa-language', lang);
    }

    // \u521D\u59CB\u5316\u8BED\u8A00
    function initLanguage() {
      // \u4ECElocalStorage\u8BFB\u53D6\u4FDD\u5B58\u7684\u8BED\u8A00\u8BBE\u7F6E
      const savedLang = localStorage.getItem('mofa-language');
      
      if (savedLang && languages[savedLang]) {
        updateLanguage(savedLang);
      } else {
        // \u9ED8\u8BA4\u82F1\u6587
        updateLanguage('en');
      }
    }

    // \u8BED\u8A00\u5207\u6362\u4E8B\u4EF6
    document.getElementById('lang-toggle').addEventListener('click', () => {
      const newLang = currentLang === 'en' ? 'zh' : 'en';
      updateLanguage(newLang);
    });

    // \u9875\u9762\u52A0\u8F7D\u65F6\u521D\u59CB\u5316\u8BED\u8A00
    document.addEventListener('DOMContentLoaded', initLanguage);

    // \u4EA4\u4E92\u5F0F\u6D41\u7A0B\u53EF\u89C6\u5316
    let currentDemo = 'arxiv';
    let currentStep = 0;
    let isPlaying = false;
    let flowInterval;
    let demoSwitchInterval;

    // \u4E0D\u540Cdemo\u7684\u6D41\u7A0B\u914D\u7F6E
    const flowConfigs = {
      'hello-world': {
        steps: 2,
        connections: [
          { from: 1, to: 2 },
          { from: 2, to: 1 } // \u5FAA\u73AF
        ]
      },
      'browser-use': {
        steps: 2,
        connections: [
          { from: 1, to: 2 }
        ]
      },
      'deep-research': {
        steps: 2,
        connections: [
          { from: 1, to: 2 },
          { from: 2, to: 1 } // \u5FAA\u73AF
        ]
      },
      'firecrawl': {
        steps: 3,
        connections: [
          { from: 1, to: 2 },
          { from: 2, to: 3 }
        ]
      },
      'weather': {
        steps: 4,
        connections: [
          { from: 1, to: 2 },
          { from: 2, to: 3 },
          { from: 3, to: 4 }
        ]
      },
      'arxiv': {
        steps: 6,
        connections: [
          { from: 1, to: 2 },
          { from: 2, to: 3 },
          { from: 3, to: 4 },
          { from: 4, to: 5 },
          { from: 5, to: 6 },
          { from: 6, to: 1 } // cycle back for demonstration
        ]
      },
      'moly-client': {
        steps: 2,
        connections: [
          { from: 1, to: 2 },
          { from: 2, to: 1 } // bidirectional flow
        ]
      },
      'mem0-dataflow': {
        steps: 3,
        connections: [
          { from: 1, to: 2 },
          { from: 2, to: 3 },
          { from: 3, to: 2 }, // memory feedback loop
          { from: 2, to: 1 } // result feedback
        ]
      },
      'camera-screenshot': {
        steps: 2,
        connections: [
          { from: 1, to: 2 },
          { from: 2, to: 1 } // result feedback
        ]
      }
    };

    // \u6D41\u7A0B\u53EF\u89C6\u5316\u51FD\u6570
    function initFlowVisualization() {
      try {
        // \u7ED1\u5B9Ademo\u5207\u6362\u4E8B\u4EF6
        const demoTabs = document.querySelectorAll('.demo-tab');
        console.log('Found demo tabs:', demoTabs.length);
        
        demoTabs.forEach(tab => {
          tab.addEventListener('click', () => {
            console.log('Demo tab clicked:', tab.dataset.demo);
            switchDemo(tab.dataset.demo);
          });
        });
        
        // \u7ED1\u5B9A\u8F6E\u64AD\u7BAD\u5934\u4E8B\u4EF6
        const leftArrow = document.querySelector('.carousel-arrow-left');
        const rightArrow = document.querySelector('.carousel-arrow-right');
        
        if (leftArrow && rightArrow) {
          leftArrow.addEventListener('click', () => {
            const demos = ['hello-world', 'browser-use', 'deep-research', 'firecrawl', 'weather', 'arxiv', 'moly-client', 'mem0-dataflow', 'camera-screenshot'];
            const currentIndex = demos.indexOf(currentDemo);
            const prevIndex = (currentIndex - 1 + demos.length) % demos.length;
            switchDemo(demos[prevIndex]);
          });
          
          rightArrow.addEventListener('click', () => {
            const demos = ['hello-world', 'browser-use', 'deep-research', 'firecrawl', 'weather', 'arxiv', 'moly-client', 'mem0-dataflow', 'camera-screenshot'];
            const currentIndex = demos.indexOf(currentDemo);
            const nextIndex = (currentIndex + 1) % demos.length;
            switchDemo(demos[nextIndex]);
          });
        }
        
        // Set step attributes for all flow steps
        document.querySelectorAll('.demo-content').forEach(demo => {
          const steps = demo.querySelectorAll('.flow-step');
          steps.forEach((step, index) => {
            step.setAttribute('data-step', index + 1);
          });
        });
        
        // \u521D\u59CB\u5316\u5F53\u524Ddemo
        console.log('Initializing with hello-world demo');
        switchDemo('hello-world');
        
        // \u5F00\u59CB\u81EA\u52A8\u5FAA\u73AF\u64AD\u653E
        startAutoFlow();
        
        // \u6BCF60\u79D2\u81EA\u52A8\u5207\u6362demo
        demoSwitchInterval = setInterval(() => {
          const demos = ['hello-world', 'browser-use', 'deep-research', 'firecrawl', 'weather', 'arxiv', 'moly-client', 'mem0-dataflow', 'camera-screenshot'];
          const currentIndex = demos.indexOf(currentDemo);
          const nextIndex = (currentIndex + 1) % demos.length;
          switchDemo(demos[nextIndex]);
        }, 60000);
        
        console.log('Flow visualization initialized successfully');
      } catch (error) {
        console.error('Error initializing flow visualization:', error);
      }
    }

    function switchDemo(demoType) {
      try {
        console.log('Switching to demo:', demoType);
        if (demoType === currentDemo) return;
        
        // \u505C\u6B62\u5F53\u524D\u6D41\u7A0B
        stopFlow();
        
        // \u5207\u6362demo\u663E\u793A
        const allDemos = document.querySelectorAll('.demo-content');
        console.log('Found demo contents:', allDemos.length);
        
        allDemos.forEach(demo => {
          demo.style.display = 'none';
          demo.classList.remove('active');
        });
        
        const targetDemo = document.getElementById(\`\${demoType}-demo\`);
        console.log('Target demo element:', targetDemo);
        
        if (targetDemo) {
          targetDemo.style.display = 'block';
          targetDemo.classList.add('active');
        } else {
          console.error('Target demo not found:', \`\${demoType}-demo\`);
          return;
        }
        
        // \u66F4\u65B0tab\u72B6\u6001
        const allTabs = document.querySelectorAll('.demo-tab');
        allTabs.forEach(tab => {
          if (tab.dataset.demo === demoType) {
            tab.classList.add('active');
          } else {
            tab.classList.remove('active');
          }
        });
        
        currentDemo = demoType;
        currentStep = 0;
        
        // \u91CD\u65B0\u7ED8\u5236\u8FDE\u63A5\u7EBF\u5E76\u5F00\u59CB\u6D41\u7A0B
        setTimeout(() => {
          try {
            drawConnections();
            resetFlow();
            startAutoFlow();
            console.log('Demo switched successfully to:', demoType);
          } catch (error) {
            console.error('Error in demo switch timeout:', error);
          }
        }, 100);
      } catch (error) {
        console.error('Error switching demo:', error);
      }
    }

    function drawConnections() {
      const activeDemo = document.querySelector('.demo-content.active');
      if (!activeDemo) return;
      
      const svg = activeDemo.querySelector('.flow-connections');
      if (!svg) return;

      svg.innerHTML = '';
      
      const config = flowConfigs[currentDemo];
      if (!config) return;
      
      config.connections.forEach((connection, index) => {
        const fromElement = activeDemo.querySelector(\`[data-step="\${connection.from}"] .agent-card\`);
        const toElement = activeDemo.querySelector(\`[data-step="\${connection.to}"] .agent-card\`);
        
        if (fromElement && toElement) {
          const fromRect = fromElement.getBoundingClientRect();
          const toRect = toElement.getBoundingClientRect();
          const containerRect = activeDemo.querySelector('.flow-container').getBoundingClientRect();
          
          const fromX = fromRect.left - containerRect.left + fromRect.width / 2;
          const fromY = fromRect.top - containerRect.top + fromRect.height / 2;
          const toX = toRect.left - containerRect.left + toRect.width / 2;
          const toY = toRect.top - containerRect.top + toRect.height / 2;
          
          const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
          
          // \u521B\u5EFA\u8D1D\u585E\u5C14\u66F2\u7EBF\u8DEF\u5F84
          const controlX1 = fromX + (toX - fromX) * 0.5;
          const controlY1 = fromY;
          const controlX2 = toX - (toX - fromX) * 0.5;
          const controlY2 = toY;
          
          const pathData = \`M \${fromX} \${fromY} C \${controlX1} \${controlY1}, \${controlX2} \${controlY2}, \${toX} \${toY}\`;
          
          path.setAttribute('d', pathData);
          path.setAttribute('class', 'flow-path');
          path.setAttribute('data-connection', index);
          
          svg.appendChild(path);
        }
      });
    }

    function startAutoFlow() {
      if (isPlaying) return;
      
      isPlaying = true;
      currentStep = 0;
      
      const config = flowConfigs[currentDemo];
      if (!config) return;
      
      flowInterval = setInterval(() => {
        if (currentStep < config.steps) {
          activateStep(currentStep + 1);
          currentStep++;
        } else {
          // \u6D41\u7A0B\u5B8C\u6210\uFF0C\u91CD\u65B0\u5F00\u59CB
          setTimeout(() => {
            resetFlow();
            currentStep = 0;
          }, 2000);
        }
      }, 1500);
    }

    function stopFlow() {
      isPlaying = false;
      if (flowInterval) {
        clearInterval(flowInterval);
        flowInterval = null;
      }
    }

    function activateStep(step) {
      const activeDemo = document.querySelector('.demo-content.active');
      if (!activeDemo) return;
      
      // \u6FC0\u6D3B\u5F53\u524D\u6B65\u9AA4
      const stepElement = activeDemo.querySelector(\`[data-step="\${step}"] .agent-card\`);
      if (stepElement) {
        stepElement.classList.remove('pending', 'completed');
        stepElement.classList.add('active', 'processing');
        stepElement.style.transform = 'scale(1)';
        stepElement.style.opacity = '1';
        stepElement.style.boxShadow = '0 10px 30px rgba(99, 102, 241, 0.3)';
        
        // 1.2\u79D2\u540E\u6807\u8BB0\u4E3A\u5B8C\u6210
        setTimeout(() => {
          stepElement.classList.remove('active', 'processing');
          stepElement.classList.add('completed');
          stepElement.style.boxShadow = 'none';
        }, 1200);
      }
      
      // \u6FC0\u6D3B\u76F8\u5173\u8FDE\u63A5\u7EBF
      const config = flowConfigs[currentDemo];
      if (config) {
        config.connections.forEach((connection, index) => {
          if (connection.from === step) {
            setTimeout(() => {
              const path = activeDemo.querySelector(\`[data-connection="\${index}"]\`);
              if (path) {
                path.classList.add('active');
              }
            }, 600);
          }
        });
      }
    }

    function resetFlow() {
      stopFlow();
      currentStep = 0;
      
      const activeDemo = document.querySelector('.demo-content.active');
      if (!activeDemo) return;
      
      // \u91CD\u7F6E\u6240\u6709\u4EE3\u7406\u72B6\u6001
      const agents = activeDemo.querySelectorAll('.interactive-agent');
      agents.forEach(agent => {
        agent.classList.remove('active', 'completed', 'processing');
        agent.classList.add('pending');
        agent.style.transform = 'scale(0.95)';
        agent.style.opacity = '0.7';
        agent.style.boxShadow = 'none';
      });
      
      // \u91CD\u7F6E\u8FDE\u63A5\u7EBF
      const paths = activeDemo.querySelectorAll('.flow-path');
      paths.forEach(path => {
        path.classList.remove('active');
      });
    }

    // \u7A97\u53E3\u5927\u5C0F\u6539\u53D8\u65F6\u91CD\u65B0\u7ED8\u5236\u8FDE\u63A5\u7EBF
    window.addEventListener('resize', () => {
      setTimeout(drawConnections, 100);
    });

    // \u9875\u9762\u52A0\u8F7D\u65F6\u521D\u59CB\u5316\u6D41\u7A0B\u53EF\u89C6\u5316
    function initPage() {
      try {
        console.log('Page initialization started');
        initLanguage();
        setTimeout(() => {
          console.log('Starting flow visualization initialization');
          initFlowVisualization();
        }, 100);
      } catch (error) {
        console.error('Error during page initialization:', error);
      }
    }

    // \u786E\u4FDDDOM\u5B8C\u5168\u52A0\u8F7D\u540E\u518D\u521D\u59CB\u5316
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initPage);
    } else {
      // DOM\u5DF2\u7ECF\u52A0\u8F7D\u5B8C\u6210\uFF0C\u76F4\u63A5\u521D\u59CB\u5316
      initPage();
    }
  <\/script> </body> </html>`], ['<html lang="en" id="html-root" style="scroll-behavior: smooth;"> <head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title id="page-title">MoFA - Make Ordinary Developers Full-stack AI Engineers</title><!-- Favicon --><link rel="icon" type="image/png" href="https://avatars.githubusercontent.com/u/167464495?s=32"><link rel="shortcut icon" href="https://avatars.githubusercontent.com/u/167464495?s=32"><link rel="apple-touch-icon" href="https://avatars.githubusercontent.com/u/167464495?s=180"><link rel="icon" type="image/png" sizes="16x16" href="https://avatars.githubusercontent.com/u/167464495?s=16"><link rel="icon" type="image/png" sizes="32x32" href="https://avatars.githubusercontent.com/u/167464495?s=32"><link rel="icon" type="image/png" sizes="48x48" href="https://avatars.githubusercontent.com/u/167464495?s=48"><meta name="theme-color" content="#6366F1">', `</head> <body> <header style="position: sticky; top: 0; background: white; border-bottom: 4px solid var(--mondrian-black); box-shadow: 0 2px 4px rgba(0,0,0,0.1); z-index: 50;"> <nav class="container" style="padding: 16px; display: flex; align-items: center; justify-content: space-between;"> <a href="https://mofa.ai" style="display: flex; align-items: center; gap: 8px; text-decoration: none;" target="_blank" rel="noopener noreferrer"> <img src="https://avatars.githubusercontent.com/u/167464495" alt="MoFA Logo" style="width: 40px; height: 40px; border-radius: 8px;"> <span style="font-size: 1.5rem; font-weight: 700; color: var(--mondrian-black);">MoFA</span> </a> <div style="display: flex; align-items: center; gap: 32px;"> <a href="https://github.com/moxin-org/mofa/tree/main/Gosim_2024_Hackathon/documents" class="nav-link" target="_blank" rel="noopener noreferrer" data-en="Docs" data-zh="\u6587\u6863">Docs</a> <a href="https://demo.mofa.ai" class="nav-link" target="_blank" rel="noopener noreferrer" data-en="Examples" data-zh="\u793A\u4F8B">Examples</a> <a href="http://blog.mofa.ai/" class="nav-link" target="_blank" rel="noopener noreferrer" data-en="Blog" data-zh="\u535A\u5BA2">Blog</a> <!-- \u8BED\u8A00\u5207\u6362\u6309\u94AE --> <div style="display: flex; align-items: center; gap: 8px;"> <button id="lang-toggle" style="
            display: flex;
            align-items: center;
            gap: 4px;
            padding: 8px 12px;
            background: transparent;
            border: 2px solid var(--mondrian-gray);
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.2s ease;
            font-size: 0.875rem;
            font-weight: 500;
            color: var(--mondrian-black);
          " onmouseover="this.style.borderColor='var(--mondrian-red)'" onmouseout="this.style.borderColor='var(--mondrian-gray)'"> <span id="current-lang">\u{1F1FA}\u{1F1F8} EN</span> <span style="font-size: 0.75rem; opacity: 0.6;">\u25BC</span> </button> </div> <a href="https://github.com/moxin-org/mofa" class="btn-primary" target="_blank" rel="noopener noreferrer" style="display: flex; align-items: center; gap: 8px;"> <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" style="flex-shrink: 0;"> <path d="M12 0C5.374 0 0 5.373 0 12 0 17.302 3.438 21.8 8.207 23.387c.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"></path> </svg>
GitHub
</a> </div> </nav> </header> <!-- \u4E3B\u8981\u5185\u5BB9 --> <main style="flex: 1;"> <!-- Hero \u533A\u57DF --> <section class="py-20" style="position: relative; overflow: hidden;"> <!-- \u8499\u5FB7\u91CC\u5B89\u80CC\u666F --> <div style="position: absolute; inset: 0; opacity: 0.1;"> <div class="mondrian-grid" style="grid-template-columns: repeat(12, 1fr); grid-template-rows: repeat(8, 1fr); height: 100%;"> <div class="mondrian-block animate-grid-float" style="background-color: var(--mondrian-red); grid-column: span 3; grid-row: span 2;"></div> <div class="mondrian-block animate-grid-float" style="background-color: var(--mondrian-yellow); grid-column: span 2; grid-row: span 3; animation-delay: 0.5s;"></div> <div class="mondrian-block animate-grid-float" style="background-color: var(--mondrian-blue); grid-column: span 4; grid-row: span 2; animation-delay: 1s;"></div> <div class="mondrian-block" style="background-color: var(--mondrian-white); grid-column: span 3; grid-row: span 3;"></div> </div> </div> <div class="container" style="position: relative; z-index: 10;"> <div class="max-w-4xl mx-auto text-center"> <!-- Logo --> <div style="display: flex; justify-content: center; margin-bottom: 32px;"> <div class="mondrian-grid" style="grid-template-columns: repeat(3, 1fr); grid-template-rows: repeat(3, 1fr); width: 96px; height: 96px; transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'"> <div class="mondrian-block animate-pulse-slow" style="background-color: var(--mondrian-red); min-height: auto;"></div> <div class="mondrian-block" style="background-color: var(--mondrian-white); min-height: auto; grid-column: span 2;"></div> <div class="mondrian-block animate-pulse-slow" style="background-color: var(--mondrian-yellow); min-height: auto; grid-row: span 2; animation-delay: 0.5s;"></div> <div class="mondrian-block animate-pulse-slow" style="background-color: var(--mondrian-blue); min-height: auto; animation-delay: 1s;"></div> <div class="mondrian-block" style="background-color: var(--mondrian-white); min-height: auto;"></div> <div class="mondrian-block animate-pulse-slow" style="background-color: var(--mondrian-red); min-height: auto; animation-delay: 1.5s;"></div> </div> </div> <!-- \u4E3B\u6807\u9898 --> <h1 style="font-size: 3rem; font-weight: 700; margin-bottom: 24px;"> <span class="gradient-text">MoFA</span> </h1> <!-- \u526F\u6807\u9898 --> <p class="text-2xl font-medium mb-4" style="color: var(--mondrian-black);" data-en="Make Ordinary Developers Full-stack AI Engineers" data-zh="\u8BA9\u666E\u901A\u5F00\u53D1\u8005\u6210\u4E3A\u5168\u6808 AI \u5DE5\u7A0B\u5E08">
Make Ordinary Developers Full-stack AI Engineers
</p> <p class="text-xl mb-8 text-gray-600" data-en="Modular Framework for AI Agents" data-zh="\u6A21\u5757\u5316 AI \u4EE3\u7406\u6846\u67B6">
Modular Framework for AI Agents
</p> <!-- \u63CF\u8FF0 --> <p class="text-xl text-gray-700 mb-12 max-w-2xl mx-auto" data-en="A composable AI agent framework that enables every developer to easily build, debug, and deploy complex AI applications" data-zh="\u901A\u8FC7\u53EF\u7EC4\u5408\u7684 AI \u4EE3\u7406\u6846\u67B6\uFF0C\u8BA9\u6BCF\u4E2A\u5F00\u53D1\u8005\u90FD\u80FD\u8F7B\u677E\u6784\u5EFA\u3001\u8C03\u8BD5\u548C\u90E8\u7F72\u590D\u6742\u7684 AI \u5E94\u7528">
A composable AI agent framework that enables every developer to easily build, debug, and deploy complex AI applications
</p> <!-- CTA \u6309\u94AE --> <div style="display: flex; flex-direction: column; gap: 16px; justify-content: center; margin-bottom: 64px;"> <div style="display: flex; flex-wrap: wrap; gap: 16px; justify-content: center;"> <a href="https://github.com/moxin-org/mofa/blob/main/python/README.md#2-quick-start-guide" target="_blank" rel="noopener noreferrer" class="btn-primary" style="font-size: 1.125rem; padding: 16px 32px;" data-en="\u{1F680} Quick Start" data-zh="\u{1F680} \u5FEB\u901F\u5F00\u59CB">
\u{1F680} Quick Start
</a> <a href="#why-mofa" rel="noopener noreferrer" class="btn-outline" style="font-size: 1.125rem; padding: 16px 32px;" data-en="\u{1F4A1} Learn More" data-zh="\u{1F4A1} \u4E86\u89E3\u66F4\u591A">
\u{1F4A1} Learn More
</a> </div> </div> <!-- \u5FEB\u901F\u7EDF\u8BA1 --> <div class="grid grid-cols-3 gap-8 max-w-2xl mx-auto"> <div class="text-center"> <div class="text-3xl font-bold" style="color: var(--mondrian-red);" data-en="5 min" data-zh="5\u5206\u949F">5 min</div> <div class="text-sm text-gray-600" data-en="Quick Setup" data-zh="\u5FEB\u901F\u4E0A\u624B">Quick Setup</div> </div> <div class="text-center"> <div class="text-3xl font-bold" style="color: var(--mondrian-blue);">100+</div> <div class="text-sm text-gray-600" data-en="Built-in Agents" data-zh="\u5185\u7F6E\u4EE3\u7406">Built-in Agents</div> </div> <div class="text-center"> <div class="text-3xl font-bold" style="color: var(--mondrian-yellow);">\u221E</div> <div class="text-sm text-gray-600" data-en="Combinations" data-zh="\u7EC4\u5408\u53EF\u80FD">Combinations</div> </div> </div> </div> </div> </section> <!-- \u5C0F\u578B\u5206\u9694\u7EBF --> <div class="mini-divider"> <div class="mini-line red-line"></div> <div class="mini-line blue-line"></div> <div class="mini-line yellow-line"></div> </div> <!-- \u6838\u5FC3\u4F18\u52BF --> <section id="why-mofa" class="py-20" style="background-color: #f9fafb;"> <div class="container"> <div class="text-center mb-16"> <h2 class="text-4xl font-bold mb-4" data-en="Why Choose <span class='gradient-text'>MoFA</span>" data-zh="\u4E3A\u4EC0\u4E48\u9009\u62E9 <span class='gradient-text'>MoFA</span>">
Why Choose <span class="gradient-text">MoFA</span> </h2> <p class="text-xl text-gray-600 max-w-2xl mx-auto" data-en="Making AI development simple, efficient, and enjoyable" data-zh="\u8BA9 AI \u5F00\u53D1\u53D8\u5F97\u7B80\u5355\u3001\u9AD8\u6548\u3001\u6709\u8DA3">
Making AI development simple, efficient, and enjoyable
</p> </div> <div class="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto"> <div class="card" style="border: 2px solid var(--mondrian-black); transition: border-width 0.2s ease;" onmouseover="this.style.borderWidth='4px'" onmouseout="this.style.borderWidth='2px'"> <div style="display: flex; align-items: flex-start; gap: 16px;"> <div style="padding: 12px; border-radius: 8px; background-color: var(--mondrian-red); color: white; flex-shrink: 0;">
\u{1F9E9}
</div> <div> <h3 class="text-xl font-semibold mb-2" data-en="Composable Agent Architecture" data-zh="\u53EF\u7EC4\u5408\u7684\u4EE3\u7406\u67B6\u6784">Composable Agent Architecture</h3> <p class="text-gray-600" data-en="Build complex AI applications by connecting agents via YAML-defined flows. Leverage a core kernel with modules for RAG (embedding, splitting, vector stores), planning, and tool integration. Easily orchestrate data flow between agents." data-zh="\u901A\u8FC7 YAML \u5B9A\u4E49\u7684\u5DE5\u4F5C\u6D41\u8FDE\u63A5\u4EE3\u7406\uFF0C\u6784\u5EFA\u590D\u6742\u7684 AI \u5E94\u7528\u3002\u5229\u7528\u5305\u542B RAG\uFF08\u5D4C\u5165\u3001\u5206\u5272\u3001\u5411\u91CF\u5B58\u50A8\uFF09\u3001\u89C4\u5212\u548C\u5DE5\u5177\u96C6\u6210\u7B49\u6A21\u5757\u7684\u6838\u5FC3\u5185\u6838\u3002\u8F7B\u677E\u7F16\u6392\u4EE3\u7406\u95F4\u7684\u6570\u636E\u6D41\u52A8\u3002">
Build complex AI applications by connecting agents via YAML-defined flows. Leverage a core kernel with modules for RAG (embedding, splitting, vector stores), planning, and tool integration. Easily orchestrate data flow between agents.
</p> </div> </div> </div> <div class="card" style="border: 2px solid var(--mondrian-black); transition: border-width 0.2s ease;" onmouseover="this.style.borderWidth='4px'" onmouseout="this.style.borderWidth='2px'"> <div style="display: flex; align-items: flex-start; gap: 16px;"> <div style="padding: 12px; border-radius: 8px; background-color: var(--mondrian-blue); color: white; flex-shrink: 0;">
\u26A1
</div> <div> <h3 class="text-xl font-semibold mb-2" data-en="Rapid Agent Development" data-zh="\u5FEB\u901F\u4EE3\u7406\u5F00\u53D1">Rapid Agent Development</h3> <p class="text-gray-600" data-en="MoFA offers a clear structure for agent development, significantly reducing boilerplate and letting you focus on core logic. The MoFA Stage visual IDE further accelerates the entire development cycle, from creation to debugging. Get started in just 5 minutes." data-zh="MoFA \u63D0\u4F9B\u6E05\u6670\u7684\u4EE3\u7406\u5F00\u53D1\u7ED3\u6784\uFF0C\u5927\u5E45\u51CF\u5C11\u6837\u677F\u4EE3\u7801\uFF0C\u8BA9\u60A8\u4E13\u6CE8\u4E8E\u6838\u5FC3\u4E1A\u52A1\u903B\u8F91\u3002\u7ED3\u5408 MoFA Stage \u53EF\u89C6\u5316 IDE\uFF0C\u53EF\u8FDB\u4E00\u6B65\u52A0\u901F\u4ECE\u521B\u5EFA\u5230\u8C03\u8BD5\u7684\u5B8C\u6574\u5F00\u53D1\u5468\u671F\u30025\u5206\u949F\u5373\u53EF\u5FEB\u901F\u4E0A\u624B\u3002">
MoFA offers a clear structure for agent development, significantly reducing boilerplate and letting you focus on core logic. The MoFA Stage visual IDE further accelerates the entire development cycle, from creation to debugging. Get started in just 5 minutes.
</p> </div> </div> </div> <div class="card" style="border: 2px solid var(--mondrian-black); transition: border-width 0.2s ease;" onmouseover="this.style.borderWidth='4px'" onmouseout="this.style.borderWidth='2px'"> <div style="display: flex; align-items: flex-start; gap: 16px;"> <div style="padding: 12px; border-radius: 8px; background-color: var(--mondrian-yellow); color: var(--mondrian-black); flex-shrink: 0;">
\u{1F680}
</div> <div> <h3 class="text-xl font-semibold mb-2" data-en="Rich Agent Hub & Dev Tools" data-zh="\u4E30\u5BCC\u4EE3\u7406\u4E2D\u5FC3\u4E0E\u5F00\u53D1\u5DE5\u5177">Rich Agent Hub &amp; Dev Tools</h3> <p class="text-gray-600" data-en="Access 100+ pre-built agents from our Agent Hub, covering data connectors, LLM integrations, and specialized tools. MoFA Stage further enhances development with visual agent management, an integrated terminal, and an advanced code editor." data-zh="\u4ECE\u6211\u4EEC\u7684\u4EE3\u7406\u4E2D\u5FC3\u83B7\u53D6100+\u9884\u6784\u5EFA\u4EE3\u7406\uFF0C\u6DB5\u76D6\u6570\u636E\u8FDE\u63A5\u5668\u3001LLM \u96C6\u6210\u548C\u4E13\u7528\u5DE5\u5177\u3002MoFA Stage \u901A\u8FC7\u53EF\u89C6\u5316\u4EE3\u7406\u7BA1\u7406\u3001\u96C6\u6210\u7EC8\u7AEF\u548C\u9AD8\u7EA7\u4EE3\u7801\u7F16\u8F91\u5668\u8FDB\u4E00\u6B65\u589E\u5F3A\u5F00\u53D1\u4F53\u9A8C\u3002">
Access 100+ pre-built agents from our Agent Hub, covering data connectors, LLM integrations, and specialized tools. MoFA Stage further enhances development with visual agent management, an integrated terminal, and an advanced code editor.
</p> </div> </div> </div> <div class="card" style="border: 2px solid var(--mondrian-black); transition: border-width 0.2s ease;" onmouseover="this.style.borderWidth='4px'" onmouseout="this.style.borderWidth='2px'"> <div style="display: flex; align-items: flex-start; gap: 16px;"> <div style="padding: 12px; border-radius: 8px; background-color: var(--mondrian-black); color: white; flex-shrink: 0;">
\u{1F527}
</div> <div> <h3 class="text-xl font-semibold mb-2" data-en="Highly Extensible Framework" data-zh="\u9AD8\u5EA6\u53EF\u6269\u5C55\u6846\u67B6">Highly Extensible Framework</h3> <p class="text-gray-600" data-en="Easily write custom Python agents. Integrate third-party tools, models, and data sources through well-defined interfaces. Extend core functionalities like memory (e.g., Mem0 integration) or RAG strategies by implementing custom components." data-zh="\u8F7B\u677E\u7F16\u5199\u81EA\u5B9A\u4E49 Python \u4EE3\u7406\u3002\u901A\u8FC7\u5B9A\u4E49\u826F\u597D\u7684\u63A5\u53E3\u96C6\u6210\u7B2C\u4E09\u65B9\u5DE5\u5177\u3001\u6A21\u578B\u548C\u6570\u636E\u6E90\u3002\u901A\u8FC7\u5B9E\u73B0\u81EA\u5B9A\u4E49\u7EC4\u4EF6\u6765\u6269\u5C55\u6838\u5FC3\u529F\u80FD\uFF0C\u5982\u8BB0\u5FC6\uFF08\u4F8B\u5982 Mem0 \u96C6\u6210\uFF09\u6216 RAG \u7B56\u7565\u3002">
Easily write custom Python agents. Integrate third-party tools, models, and data sources through well-defined interfaces. Extend core functionalities like memory (e.g., Mem0 integration) or RAG strategies by implementing custom components.
</p> </div> </div> </div> </div> <div class="text-center mt-16 mb-8" style="display: none;"> <h3 class="text-3xl font-bold" data-en="Highlight: Your AI Agent IDE - <span class='gradient-text'>MoFA Stage</span>" data-zh="\u6838\u5FC3\u529F\u80FD\uFF1A\u4F60\u7684 AI Agent IDE - <span class='gradient-text'>MoFA Stage</span>">
Highlight: Your AI Agent IDE - <span class="gradient-text">MoFA Stage</span> </h3> </div> <p class="text-xl text-gray-600 max-w-3xl mx-auto text-center mb-12" style="display: none;" data-en="A visual management platform for MoFA - your web-based IDE for AI agents." data-zh="MoFA \u7684\u53EF\u89C6\u5316\u7BA1\u7406\u5E73\u53F0 - \u4F60\u7684Agent\u4E13\u5C5E Web IDE.">
A visual management platform for MoFA - your web-based IDE.
</p> <div class="max-w-6xl mx-auto" style="display: none;"> <!-- \u5E73\u53F0\u7279\u8272\u5C55\u793A --> <div class="grid md:grid-cols-3 gap-8 mb-16"> <div class="card" style="border: 2px solid var(--mondrian-black); transition: all 0.3s ease; padding: 16px;" onmouseover="this.style.borderWidth='4px'; this.style.transform='translateY(-8px)'" onmouseout="this.style.borderWidth='2px'; this.style.transform='translateY(0)'"> <div style="text-align: center;"> <div style="
                   width: 48px;
                   height: 48px;
                   margin: 0 auto 12px;
                   background: linear-gradient(135deg, var(--mondrian-red), #8B5CF6);
                   border-radius: 12px;
                   display: flex;
                   align-items: center;
                   justify-content: center;
                   font-size: 1.5rem;
                   color: white;
                   box-shadow: 0 6px 18px rgba(99, 102, 241, 0.3);
                 ">\u{1F4BB}</div> <h3 class="text-base font-semibold mb-1" data-en="Visual Agent Management" data-zh="\u53EF\u89C6\u5316\u4EE3\u7406\u7BA1\u7406">Visual Agent Management</h3> <p class="text-gray-600 text-xs leading-snug" data-en="Create, edit, and manage AI agents through an intuitive web interface" data-zh="\u901A\u8FC7\u76F4\u89C2\u7684\u7F51\u9875\u754C\u9762\u521B\u5EFA\u3001\u7F16\u8F91\u548C\u7BA1\u7406 AI \u4EE3\u7406">
Create, edit, and manage AI agents through an intuitive web interface - no command line expertise required
</p> </div> </div> <div class="card" style="border: 2px solid var(--mondrian-black); transition: all 0.3s ease; padding: 16px;" onmouseover="this.style.borderWidth='4px'; this.style.transform='translateY(-8px)'" onmouseout="this.style.borderWidth='2px'; this.style.transform='translateY(0)'"> <div style="text-align: center;"> <div style="
                   width: 48px;
                   height: 48px;
                   margin: 0 auto 12px;
                   background: linear-gradient(135deg, var(--mondrian-blue), #06B6D4);
                   border-radius: 12px;
                   display: flex;
                   align-items: center;
                   justify-content: center;
                   font-size: 1.5rem;
                   color: white;
                   box-shadow: 0 6px 18px rgba(14, 165, 233, 0.3);
                 ">\u{1F5A5}\uFE0F</div> <h3 class="text-base font-semibold mb-1" data-en="Integrated Terminal" data-zh="\u96C6\u6210\u7EC8\u7AEF">Integrated Terminal</h3> <p class="text-gray-600 text-xs leading-snug" data-en="Built-in web terminal with SSH access - execute commands and monitor agents directly from your browser" data-zh="\u5185\u7F6E\u7F51\u9875\u7EC8\u7AEF\u652F\u6301 SSH \u8BBF\u95EE - \u76F4\u63A5\u5728\u6D4F\u89C8\u5668\u4E2D\u6267\u884C\u547D\u4EE4\u548C\u76D1\u63A7\u4EE3\u7406">
Built-in web terminal with SSH access - execute commands and monitor agents directly from your browser
</p> </div> </div> <div class="card" style="border: 2px solid var(--mondrian-black); transition: all 0.3s ease; padding: 16px;" onmouseover="this.style.borderWidth='4px'; this.style.transform='translateY(-8px)'" onmouseout="this.style.borderWidth='2px'; this.style.transform='translateY(0)'"> <div style="text-align: center;"> <div style="
                   width: 48px;
                   height: 48px;
                   margin: 0 auto 12px;
                   background: linear-gradient(135deg, var(--mondrian-yellow), #FBBF24);
                   border-radius: 12px;
                   display: flex;
                   align-items: center;
                   justify-content: center;
                   font-size: 1.5rem;
                   color: var(--mondrian-black);
                   box-shadow: 0 6px 18px rgba(245, 158, 11, 0.3);
                 ">\u{1F4DD}</div> <h3 class="text-base font-semibold mb-1" data-en="Advanced Code Editor" data-zh="\u4EE3\u7801\u7F16\u8F91\u5668">Code Editor</h3> <p class="text-gray-600 text-xs leading-snug" data-en="Monaco-powered editor with syntax highlighting, auto-completion, and instant Markdown preview" data-zh="\u57FA\u4E8E Monaco \u7684\u7F16\u8F91\u5668\uFF0C\u652F\u6301\u8BED\u6CD5\u9AD8\u4EAE\u3001\u81EA\u52A8\u8865\u5168\u548C Markdown \u5373\u65F6\u9884\u89C8">
Monaco-powered editor with syntax highlighting, auto-completion, and instant Markdown preview - just like VS Code
</p> </div> </div> </div> <!-- \u5E73\u53F0\u67B6\u6784\u5C55\u793A --> <div class="bg-white rounded-lg shadow-lg p-8" style="border: 2px solid var(--mondrian-black); display: none;"> <div class="text-center mb-8"> <h3 class="text-2xl font-bold mb-4" data-en="Full-Stack Architecture" data-zh="\u5168\u6808\u67B6\u6784">Full-Stack Architecture</h3> <p class="text-gray-600" data-en="Built with modern technologies for optimal performance and developer experience" data-zh="\u4F7F\u7528\u73B0\u4EE3\u6280\u672F\u6784\u5EFA\uFF0C\u786E\u4FDD\u6700\u4F73\u6027\u80FD\u548C\u5F00\u53D1\u4F53\u9A8C">
Built with modern technologies for optimal performance and developer experience
</p> </div> <div class="grid md:grid-cols-2 gap-12"> <!-- \u524D\u7AEF\u6280\u672F\u6808 --> <div> <h4 class="text-lg font-semibold mb-4 flex items-center gap-2" data-en="\u{1F3A8} Frontend Stack" data-zh="\u{1F3A8} \u524D\u7AEF\u6280\u672F\u6808">
\u{1F3A8} Frontend Stack
</h4> <div class="space-y-3"> <div class="flex items-center gap-3"> <div style="width: 12px; height: 12px; background: #42b883; border-radius: 50%;"></div> <span class="font-medium">Vue 3</span> <span class="text-sm text-gray-500" data-en="Progressive Framework" data-zh="\u6E10\u8FDB\u5F0F\u6846\u67B6">Progressive Framework</span> </div> <div class="flex items-center gap-3"> <div style="width: 12px; height: 12px; background: #409eff; border-radius: 50%;"></div> <span class="font-medium">Element Plus</span> <span class="text-sm text-gray-500" data-en="UI Components" data-zh="UI \u7EC4\u4EF6\u5E93">UI Components</span> </div> <div class="flex items-center gap-3"> <div style="width: 12px; height: 12px; background: var(--mondrian-blue); border-radius: 50%;"></div> <span class="font-medium">Monaco Editor</span> <span class="text-sm text-gray-500" data-en="VS Code Engine" data-zh="VS Code \u5F15\u64CE">VS Code Engine</span> </div> <div class="flex items-center gap-3"> <div style="width: 12px; height: 12px; background: #000; border-radius: 50%;"></div> <span class="font-medium">XTerm.js</span> <span class="text-sm text-gray-500" data-en="Terminal Emulation" data-zh="\u7EC8\u7AEF\u6A21\u62DF">Terminal Emulation</span> </div> </div> </div> <!-- \u540E\u7AEF\u6280\u672F\u6808 --> <div> <h4 class="text-lg font-semibold mb-4 flex items-center gap-2" data-en="\u2699\uFE0F Backend Stack" data-zh="\u2699\uFE0F \u540E\u7AEF\u6280\u672F\u6808">
\u2699\uFE0F Backend Stack
</h4> <div class="space-y-3"> <div class="flex items-center gap-3"> <div style="width: 12px; height: 12px; background: #306998; border-radius: 50%;"></div> <span class="font-medium">Python + Flask</span> <span class="text-sm text-gray-500" data-en="RESTful API" data-zh="RESTful API">RESTful API</span> </div> <div class="flex items-center gap-3"> <div style="width: 12px; height: 12px; background: var(--mondrian-red); border-radius: 50%;"></div> <span class="font-medium">WebSocket</span> <span class="text-sm text-gray-500" data-en="Real-time Communication" data-zh="\u5B9E\u65F6\u901A\u4FE1">Real-time Communication</span> </div> <div class="flex items-center gap-3"> <div style="width: 12px; height: 12px; background: #ff6b35; border-radius: 50%;"></div> <span class="font-medium">SSH Integration</span> <span class="text-sm text-gray-500" data-en="Terminal Access" data-zh="\u7EC8\u7AEF\u8BBF\u95EE">Terminal Access</span> </div> <div class="flex items-center gap-3"> <div style="width: 12px; height: 12px; background: var(--mondrian-yellow); border-radius: 50%;"></div> <span class="font-medium">ttyd Service</span> <span class="text-sm text-gray-500" data-en="Web Terminal" data-zh="\u7F51\u9875\u7EC8\u7AEF">Web Terminal</span> </div> </div> </div> </div> </div> <!-- \u5FEB\u901F\u5F00\u59CB\u6309\u94AE --> <div class="text-center mt-12"> <a href="https://github.com/moxin-org/mofa/tree/main/MoFA_stage" target="_blank" rel="noopener noreferrer" class="btn-primary" style="font-size: 1.125rem; padding: 16px 32px; margin-right: 16px;" data-en="\u{1F680} Explore MoFA_Stage" data-zh="\u{1F680} \u63A2\u7D22 MoFA_Stage">
\u{1F680} Explore MoFA_Stage
</a> <a href="https://github.com/moxin-org/mofa/tree/main/MoFA_stage#quick-start" target="_blank" rel="noopener noreferrer" class="btn-outline" style="font-size: 1.125rem; padding: 16px 32px;" data-en="\u{1F4D6} Quick Start Guide" data-zh="\u{1F4D6} \u5FEB\u901F\u5F00\u59CB\u6307\u5357">
\u{1F4D6} Quick Start Guide
</a> </div> </div> </div> </section> <!-- \u5C0F\u578B\u5206\u9694\u7EBF --> <div class="mini-divider"> <div class="mini-line blue-line"></div> <div class="mini-line yellow-line"></div> <div class="mini-line red-line"></div> </div> <!-- Agent & Flow \u6982\u5FF5\u4ECB\u7ECD --> <section class="py-20" style="background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);"> <div class="container"> <div class="text-center mb-16"> <h2 class="text-4xl font-bold mb-4" data-en="From Agents to <span class='gradient-text'>Flows</span>" data-zh="\u4ECE\u4EE3\u7406\u5230<span class='gradient-text'>\u5DE5\u4F5C\u6D41</span>">
From Agents to <span class="gradient-text">Flows</span> </h2> <p class="text-xl text-gray-600 max-w-3xl mx-auto" data-en="MoFA transforms individual AI agents into powerful workflows through intelligent composition and data flow orchestration" data-zh="MoFA \u901A\u8FC7\u667A\u80FD\u7EC4\u5408\u548C\u6570\u636E\u6D41\u7F16\u6392\uFF0C\u5C06\u72EC\u7ACB\u7684 AI \u4EE3\u7406\u8F6C\u5316\u4E3A\u5F3A\u5927\u7684\u5DE5\u4F5C\u6D41">
MoFA transforms individual AI agents into powerful workflows through intelligent composition and data flow orchestration
</p> </div> <!-- \u6982\u5FF5\u89E3\u91CA --> <div class="grid md:grid-cols-2 gap-12 mb-20" style="display: none;"> <div class="space-y-8"> <div class="card" style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(14, 165, 233, 0.05) 100%); border: 2px solid rgba(99, 102, 241, 0.2);"> <h3 class="text-2xl font-bold mb-4 flex items-center gap-3" data-en="\u{1F916} What is an Agent?" data-zh="\u{1F916} \u4EC0\u4E48\u662F\u4EE3\u7406\uFF1F">
\u{1F916} What is an Agent?
</h3> <p class="text-gray-700 mb-4" data-en="An agent is a self-contained AI component that performs a specific task - like extracting keywords, analyzing documents, or generating reports. Each agent has clear inputs and outputs." data-zh="\u4EE3\u7406\u662F\u4E00\u4E2A\u72EC\u7ACB\u7684 AI \u7EC4\u4EF6\uFF0C\u6267\u884C\u7279\u5B9A\u4EFB\u52A1 - \u5982\u63D0\u53D6\u5173\u952E\u8BCD\u3001\u5206\u6790\u6587\u6863\u6216\u751F\u6210\u62A5\u544A\u3002\u6BCF\u4E2A\u4EE3\u7406\u90FD\u6709\u660E\u786E\u7684\u8F93\u5165\u548C\u8F93\u51FA\u3002">
An agent is a self-contained AI component that performs a specific task - like extracting keywords, analyzing documents, or generating reports. Each agent has clear inputs and outputs.
</p> <div class="agent-demo" style="
                padding: 16px;
                background: white;
                border-radius: 8px;
                border: 1px solid rgba(99, 102, 241, 0.2);
                display: flex;
                align-items: center;
                gap: 12px;
              "> <div style="
                  padding: 8px 12px;
                  background: linear-gradient(135deg, var(--mondrian-red), #8B5CF6);
                  color: white;
                  border-radius: 6px;
                  font-size: 0.875rem;
                  font-weight: 500;
                ">Input</div> <div style="color: var(--mondrian-red); font-weight: bold;">\u2192</div> <div style="
                  padding: 8px 12px;
                  background: var(--mondrian-gray);
                  border-radius: 6px;
                  font-size: 0.875rem;
                  font-weight: 500;
                ">Agent</div> <div style="color: var(--mondrian-red); font-weight: bold;">\u2192</div> <div style="
                  padding: 8px 12px;
                  background: linear-gradient(135deg, var(--mondrian-blue), #06B6D4);
                  color: white;
                  border-radius: 6px;
                  font-size: 0.875rem;
                  font-weight: 500;
                ">Output</div> </div> </div> </div> <div class="space-y-8"> <div class="card" style="background: linear-gradient(135deg, rgba(14, 165, 233, 0.05) 0%, rgba(245, 158, 11, 0.05) 100%); border: 2px solid rgba(14, 165, 233, 0.2);"> <h3 class="text-2xl font-bold mb-4 flex items-center gap-3" data-en="\u{1F504} What is a Flow?" data-zh="\u{1F504} \u4EC0\u4E48\u662F\u5DE5\u4F5C\u6D41\uFF1F">
\u{1F504} What is a Flow?
</h3> <p class="text-gray-700 mb-4" data-en="A flow connects multiple agents together, where the output of one agent becomes the input of another. This creates powerful, multi-step AI pipelines that can solve complex problems." data-zh="\u5DE5\u4F5C\u6D41\u5C06\u591A\u4E2A\u4EE3\u7406\u8FDE\u63A5\u5728\u4E00\u8D77\uFF0C\u5176\u4E2D\u4E00\u4E2A\u4EE3\u7406\u7684\u8F93\u51FA\u6210\u4E3A\u53E6\u4E00\u4E2A\u4EE3\u7406\u7684\u8F93\u5165\u3002\u8FD9\u521B\u5EFA\u4E86\u5F3A\u5927\u7684\u591A\u6B65\u9AA4 AI \u7BA1\u9053\uFF0C\u53EF\u4EE5\u89E3\u51B3\u590D\u6742\u95EE\u9898\u3002">
A flow connects multiple agents together, where the output of one agent becomes the input of another. This creates powerful, multi-step AI pipelines that can solve complex problems.
</p> <div class="flow-demo" style="
                padding: 16px;
                background: white;
                border-radius: 8px;
                border: 1px solid rgba(14, 165, 233, 0.2);
              "> <div style="display: flex; flex-direction: column; gap: 8px;"> <div style="display: flex; align-items: center; gap: 8px;"> <div class="agent-box">Agent A</div> <div class="arrow">\u2192</div> <div class="agent-box">Agent B</div> </div> <div style="display: flex; align-items: center; gap: 8px; margin-left: 80px;"> <div class="arrow">\u2193</div> </div> <div style="display: flex; align-items: center; gap: 8px; margin-left: 80px;"> <div class="agent-box">Agent C</div> </div> </div> </div> </div> </div> </div> <!-- \u5B9E\u9645\u6848\u4F8B\u5C55\u793A\uFF1AMultiple Flow Examples --> <div class="bg-white rounded-lg shadow-lg p-8 mb-16"> <h3 class="text-3xl font-bold text-center mb-8" data-en="Real Examples: Agent Flows in Action" data-zh="\u5B9E\u9645\u6848\u4F8B\uFF1A\u4EE3\u7406\u5DE5\u4F5C\u6D41\u5B9E\u6218">
Real Examples: Agent Flows in Action
</h3> <p class="text-center text-gray-600 mb-12 max-w-3xl mx-auto" data-en="Explore different types of AI workflows - from research automation to weather prediction and web scraping" data-zh="\u63A2\u7D22\u4E0D\u540C\u7C7B\u578B\u7684 AI \u5DE5\u4F5C\u6D41 - \u4ECE\u7814\u7A76\u81EA\u52A8\u5316\u5230\u5929\u6C14\u9884\u6D4B\u548C\u7F51\u9875\u6293\u53D6">
Explore different types of AI workflows - from research automation to weather prediction and web scraping
</p> <!-- Demo Carousel Controls --> <div class="demo-carousel-container" style="position: relative; max-width: 100%; margin: 0 auto 32px;"> <!-- Left Arrow --> <button class="carousel-arrow carousel-arrow-left" style="
              position: absolute;
              left: 0px;
              top: 50%;
              transform: translateY(-50%);
              width: 40px;
              height: 40px;
              border-radius: 50%;
              border: 2px solid var(--mondrian-gray);
              background: white;
              box-shadow: 0 2px 10px rgba(0,0,0,0.2);
              color: var(--mondrian-black);
              font-size: 18px;
              cursor: pointer;
              transition: all 0.2s ease;
              z-index: 10;
              display: flex;
              align-items: center;
              justify-content: center;
            " onmouseover="this.style.borderColor='var(--mondrian-red)'; this.style.background='var(--mondrian-red)'; this.style.color='white'" onmouseout="this.style.borderColor='var(--mondrian-gray)'; this.style.background='white'; this.style.color='var(--mondrian-black)'">
\u2190
</button> <!-- Demo Selector --> <div class="text-center mb-4"> <div class="demo-tabs-container" style="
                display: flex;
                justify-content: center;
                gap: 4px;
                padding: 8px 40px;
                background: linear-gradient(to right, rgba(240,240,240,0.9), rgba(240,240,240,0.9) 10%, rgba(240,240,240,0.9) 90%, rgba(240,240,240,0.9));
                border-radius: 12px;
                overflow-x: auto;
                white-space: nowrap;
                max-width: 100%;
                width: 950px;
                margin: 0 auto;
                scrollbar-width: none; /* Firefox */
                -ms-overflow-style: none; /* IE and Edge */
              "> <style>
                .demo-tabs-container::-webkit-scrollbar {
                  display: none; /* Chrome, Safari and Opera */
                }
                .demo-tab {
                  padding: 6px 8px;
                  border-radius: 8px;
                  background: white;
                  border: none;
                  font-size: 0.8rem;
                  font-weight: 500;
                  color: var(--mondrian-black);
                  cursor: pointer;
                  transition: all 0.2s ease;
                  display: inline-flex;
                  align-items: center;
                  gap: 4px;
                  min-width: 100px;
                  justify-content: center;
                  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                }
                .demo-tab:hover {
                  background-color: #e2e8f0;
                  transform: translateY(-2px);
                }
                .demo-tab.active {
                  background: var(--mondrian-blue);
                  color: white;
                  box-shadow: 0 2px 6px rgba(37, 99, 235, 0.4);
                }
                .demo-emoji {
                  font-size: 1rem;
                }
              </style> <button class="demo-tab active" data-demo="hello-world"> <span class="demo-emoji">\u{1F44B}</span> <span class="demo-name" data-en="Hello World" data-zh="Hello World">Hello World</span> </button> <button class="demo-tab" data-demo="browser-use"> <span class="demo-emoji">\u{1F310}</span> <span class="demo-name" data-en="Browser Use" data-zh="\u6D4F\u89C8\u5668\u8C03\u7528">Browser Use</span> </button> <button class="demo-tab" data-demo="deep-research"> <span class="demo-emoji">\u{1F52C}</span> <span class="demo-name" data-en="Deep Research" data-zh="\u6DF1\u5EA6\u7814\u7A76">Deep Research</span> </button> <button class="demo-tab" data-demo="firecrawl"> <span class="demo-emoji">\u{1F577}\uFE0F</span> <span class="demo-name" data-en="Web Scraping" data-zh="\u7F51\u9875\u6293\u53D6">Web Scraping</span> </button> <button class="demo-tab" data-demo="weather"> <span class="demo-emoji">\u{1F324}\uFE0F</span> <span class="demo-name" data-en="Weather" data-zh="\u5929\u6C14\u83B7\u53D6">Weather</span> </button> <button class="demo-tab" data-demo="arxiv"> <span class="demo-emoji">\u{1F4DA}</span> <span class="demo-name" data-en="arXiv Research" data-zh="arXiv\u7814\u7A76">arXiv Research</span> </button> <button class="demo-tab" data-demo="moly-client"> <span class="demo-emoji">\u{1F916}</span> <span class="demo-name" data-en="Moly Client" data-zh="Moly\u5BA2\u6237\u7AEF">Moly Client</span> </button> <button class="demo-tab" data-demo="mem0-dataflow"> <span class="demo-emoji">\u{1F9E0}</span> <span class="demo-name" data-en="Mem0 Flow" data-zh="Mem0\u6D41\u7A0B">Mem0 Flow</span> </button> <button class="demo-tab" data-demo="camera-screenshot"> <span class="demo-emoji">\u{1F4F8}</span> <span class="demo-name" data-en="Camera Screenshot" data-zh="\u76F8\u673A\u622A\u56FE">Camera Screenshot</span> </button> </div> </div> <!-- Right Arrow --> <button class="carousel-arrow carousel-arrow-right" style="
              position: absolute;
              right: 0px;
              top: 50%;
              transform: translateY(-50%);
              width: 40px;
              height: 40px;
              border-radius: 50%;
              border: 2px solid var(--mondrian-gray);
              background: white;
              box-shadow: 0 2px 10px rgba(0,0,0,0.2);
              color: var(--mondrian-black);
              font-size: 18px;
              cursor: pointer;
              transition: all 0.2s ease;
              z-index: 10;
              display: flex;
              align-items: center;
              justify-content: center;
            " onmouseover="this.style.borderColor='var(--mondrian-red)'; this.style.background='var(--mondrian-red)'; this.style.color='white'" onmouseout="this.style.borderColor='var(--mondrian-gray)'; this.style.background='white'; this.style.color='var(--mondrian-black)'">
\u2192
</button> </div> <!-- Script to dynamically generate flow components --> <script>
            // Define all demos and their node configurations
            const demoConfigs = {
              'hello-world': {
                nodes: [
                  { emoji: '\u{1F4AC}', title: { en: 'Terminal Input', zh: '\u7EC8\u7AEF\u8F93\u5165' }, subtitle: { en: 'User query input', zh: '\u7528\u6237\u67E5\u8BE2\u8F93\u5165' } },
                  { emoji: '\u{1F916}', title: { en: 'Hello Agent', zh: '\u95EE\u5019\u4EE3\u7406' }, subtitle: { en: 'Process & respond', zh: '\u5904\u7406\u5E76\u54CD\u5E94' } }
                ],
                id: 'hello-world-demo',
                isActive: true
              },
              'browser-use': {
                nodes: [
                  { emoji: '\u2328\uFE0F', title: { en: 'Terminal Input', zh: '\u7EC8\u7AEF\u8F93\u5165' }, subtitle: { en: 'Browser task input', zh: '\u6D4F\u89C8\u5668\u4EFB\u52A1\u8F93\u5165' } },
                  { emoji: '\u{1F310}', title: { en: 'Browser Agent', zh: '\u6D4F\u89C8\u5668\u4EE3\u7406' }, subtitle: { en: 'Automate browser', zh: '\u81EA\u52A8\u5316\u6D4F\u89C8\u5668' } }
                ],
                id: 'browser-use-demo'
              },
              'deep-research': {
                nodes: [
                  { emoji: '\u{1F5A5}\uFE0F', title: { en: 'OpenAI Server', zh: 'OpenAI\u670D\u52A1\u5668' }, subtitle: { en: 'Chat interface', zh: '\u804A\u5929\u63A5\u53E3' } },
                  { emoji: '\u{1F52C}', title: { en: 'Research Planner', zh: '\u7814\u7A76\u89C4\u5212\u5668' }, subtitle: { en: 'Deep analysis', zh: '\u6DF1\u5EA6\u5206\u6790' } }
                ],
                id: 'deep-research-demo'
              },
              'firecrawl': {
                nodes: [
                  { emoji: '\u{1F517}', title: { en: 'URL Input', zh: 'URL\u8F93\u5165' }, subtitle: { en: 'Receive target URL', zh: '\u63A5\u6536\u76EE\u6807URL' } },
                  { emoji: '\u{1F577}\uFE0F', title: { en: 'Firecrawl Agent', zh: 'Firecrawl\u4EE3\u7406' }, subtitle: { en: 'Scrape & extract', zh: '\u6293\u53D6\u548C\u63D0\u53D6' } },
                  { emoji: '\u{1F4CB}', title: { en: 'Structured Data', zh: '\u7ED3\u6784\u5316\u6570\u636E' }, subtitle: { en: 'Clean content output', zh: '\u6E05\u6D01\u5185\u5BB9\u8F93\u51FA' } }
                ],
                id: 'firecrawl-demo'
              },
              'weather': {
                nodes: [
                  { emoji: '\u{1F4CD}', title: { en: 'Geolocation Agent', zh: '\u5730\u7406\u5B9A\u4F4D\u4EE3\u7406' }, subtitle: { en: 'Find coordinates', zh: '\u67E5\u627E\u5750\u6807' } },
                  { emoji: '\u{1F30A}', title: { en: 'Windy Crawler', zh: 'Windy\u722C\u866B' }, subtitle: { en: 'Scrape weather data', zh: '\u6293\u53D6\u5929\u6C14\u6570\u636E' } },
                  { emoji: '\u{1F9E0}', title: { en: 'Weather Predictor', zh: '\u5929\u6C14\u9884\u6D4B\u5668' }, subtitle: { en: 'Analyze & predict', zh: '\u5206\u6790\u548C\u9884\u6D4B' } },
                  { emoji: '\u{1F4CA}', title: { en: 'Weather Report', zh: '\u5929\u6C14\u62A5\u544A' }, subtitle: { en: 'Final forecast', zh: '\u6700\u7EC8\u9884\u62A5' } }
                ],
                id: 'weather-demo',
                nodeWidth: 140 // narrower for 4 nodes
              },
              'arxiv': {
                nodes: [
                  { emoji: '\u{1F50D}', title: { en: 'Keyword Extractor', zh: '\u5173\u952E\u8BCD\u63D0\u53D6\u5668' }, subtitle: { en: 'Extract keywords', zh: '\u63D0\u53D6\u5173\u952E\u8BCD' } },
                  { emoji: '\u{1F4E5}', title: { en: 'Paper Downloader', zh: '\u8BBA\u6587\u4E0B\u8F7D\u5668' }, subtitle: { en: 'Download papers', zh: '\u4E0B\u8F7D\u8BBA\u6587' } },
                  { emoji: '\u{1F52C}', title: { en: 'Paper Analyzer', zh: '\u8BBA\u6587\u5206\u6790\u5668' }, subtitle: { en: 'Analyze content', zh: '\u5206\u6790\u5185\u5BB9' } },
                  { emoji: '\u270D\uFE0F', title: { en: 'Report Writer', zh: '\u62A5\u544A\u64B0\u5199\u5668' }, subtitle: { en: 'Generate report', zh: '\u751F\u6210\u62A5\u544A' } },
                  { emoji: '\u{1F4AC}', title: { en: 'Feedback Agent', zh: '\u53CD\u9988\u4EE3\u7406' }, subtitle: { en: 'Suggest changes', zh: '\u63D0\u4F9B\u5EFA\u8BAE' } },
                  { emoji: '\u{1F527}', title: { en: 'Refinement Agent', zh: '\u4F18\u5316\u4EE3\u7406' }, subtitle: { en: 'Improve report', zh: '\u4F18\u5316\u62A5\u544A' } }
                ],
                id: 'arxiv-demo',
                nodeWidth: 120,
                nodePadding: 12,
                fontSize: {
                  emoji: '1.2rem',
                  title: '0.8rem',
                  subtitle: '0.65rem'
                },
                arrowWidth: 15,
                gap: 16
              },
              'moly-client': {
                nodes: [
                  { emoji: '\u{1F916}', title: { en: 'OpenAI Server', zh: 'OpenAI\u670D\u52A1\u5668' }, subtitle: { en: 'Chat completions', zh: '\u5BF9\u8BDD\u8865\u5168' } },
                  { emoji: '\u{1F9E0}', title: { en: 'Reasoner Agent', zh: '\u63A8\u7406\u4EE3\u7406' }, subtitle: { en: 'Process & reason', zh: '\u5904\u7406\u4E0E\u63A8\u7406' } }
                ],
                id: 'moly-client-demo',
                nodeWidth: 140
              },
              'mem0-dataflow': {
                nodes: [
                  { emoji: '\u2328\uFE0F', title: { en: 'Terminal Input', zh: '\u7EC8\u7AEF\u8F93\u5165' }, subtitle: { en: 'User input', zh: '\u7528\u6237\u8F93\u5165' } },
                  { emoji: '\u{1F9E0}', title: { en: 'Memory Agent', zh: '\u8BB0\u5FC6\u4EE3\u7406' }, subtitle: { en: 'Memory operations', zh: '\u8BB0\u5FC6\u64CD\u4F5C' } },
                  { emoji: '\u{1F914}', title: { en: 'Reasoner', zh: '\u63A8\u7406\u5668' }, subtitle: { en: 'Process & analyze', zh: '\u5904\u7406\u4E0E\u5206\u6790' } }
                ],
                id: 'mem0-dataflow-demo',
                nodeWidth: 140
              },
              'camera-screenshot': {
                nodes: [
                  { emoji: '\u2328\uFE0F', title: { en: 'Terminal Input', zh: '\u7EC8\u7AEF\u8F93\u5165' }, subtitle: { en: 'Command input', zh: '\u547D\u4EE4\u8F93\u5165' } },
                  { emoji: '\u{1F4F8}', title: { en: 'Camera Screenshot', zh: '\u76F8\u673A\u622A\u56FE' }, subtitle: { en: 'Capture screen', zh: '\u6355\u83B7\u5C4F\u5E55' } }
                ],
                id: 'camera-screenshot-demo',
                nodeWidth: 140
              }
            };

            // Function to generate a flow node HTML
            function generateNode(node, config) {
              const width = config.nodeWidth || 160;
              const padding = config.nodePadding || 16;
              const fontSize = config.fontSize || {
                emoji: '1.5rem',
                title: '0.9rem',
                subtitle: '0.7rem'
              };
              
              return \\\`
                <div class="flow-step">
                  <div class="agent-card interactive-agent" style="
                    padding: \\\${padding}px;
                    text-align: center;
                    transition: all 0.3s ease;
                    color: #333;
                    width: \\\${width}px;
                    background: rgba(245, 247, 250, 0.8);
                    border-radius: 4px;
                  ">
                    <div style="font-size: \\\${fontSize.emoji}; margin-bottom: 8px;">\\\${node.emoji}</div>
                    <h4 style="font-weight: bold; margin-bottom: 4px; font-size: \\\${fontSize.title};" 
                        data-en="\\\${node.title.en}"
                        data-zh="\\\${node.title.zh}">\\\${node.title.en}</h4>
                    <p style="font-size: \\\${fontSize.subtitle}; opacity: 0.9;" 
                       data-en="\\\${node.subtitle.en}"
                       data-zh="\\\${node.subtitle.zh}">\\\${node.subtitle.en}</p>
                  </div>
                </div>
              \\\`;
            }

            // Function to generate arrow between nodes
            function generateArrow(config) {
              const arrowWidth = config.arrowWidth || 40;
              
              return \\\`
                <div style="display: flex; align-items: center; color: var(--mondrian-black); position: relative;">
                  <div style="width: \\\${arrowWidth}px; height: 2px; background-color: var(--mondrian-black);"></div>
                  <div style="position: absolute; right: -5px; width: 0; height: 0; border-top: 5px solid transparent; border-bottom: 5px solid transparent; border-left: 5px solid var(--mondrian-black);"></div>
              </div>
              \\\`;
            }

            // Function to generate a complete flow container
            function generateFlowContainer(demoKey, config) {
              const { nodes, id, isActive } = config;
              const gap = config.gap || 40;
              
              let nodesHtml = '';
              
              nodes.forEach((node, index) => {
                nodesHtml += generateNode(node, config);
                
                // Add arrow if not the last node
                if (index < nodes.length - 1) {
                  nodesHtml += generateArrow(config);
                }
              });
              
              return \\\`
                <div class="demo-content \\\${isActive ? 'active' : ''}" id="\\\${id}" style="\\\${!isActive ? 'display: none;' : ''}">
              <div class="flow-container" style="
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    gap: \\\${gap}px;
                max-width: 1000px;
                margin: 0 auto;
                position: relative;
                    padding: 20px 0;
                    flex-wrap: nowrap;
                    overflow-x: auto;
                  ">
                    \\\${nodesHtml}
                <svg style="
                  position: absolute;
                  top: 0;
                  left: 0;
                  width: 100%;
                  height: 100%;
                  pointer-events: none;
                  z-index: -1;
                      display: none;
                " class="flow-connections">
                </svg>
              </div>
            </div>
              \\\`;
            }

            // Function to generate all demos
            function generateAllDemos() {
              let demosHtml = '';
              
              Object.keys(demoConfigs).forEach(demoKey => {
                demosHtml += generateFlowContainer(demoKey, demoConfigs[demoKey]);
              });
              
              return demosHtml;
            }
          <\/script> <!-- Interactive Flow Visualization --> <div class="flow-visualization"> <script>
              document.write(generateAllDemos());
            <\/script> </div> </div> </div> </section> <!-- \u5C0F\u578B\u5206\u9694\u7EBF --> <div class="mini-divider"> <div class="mini-line yellow-line"></div> <div class="mini-line red-line"></div> <div class="mini-line blue-line"></div> </div> <!-- Demo Video Section --> <section class="py-20" style="background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);"> <div class="container"> <div class="text-center mb-16"> <h2 class="text-4xl font-bold mb-4" data-en="See MoFA in <span class='gradient-text'>Action</span>" data-zh="\u89C2\u770B MoFA <span class='gradient-text'>\u5B9E\u6218\u6F14\u793A</span>">
See MoFA in <span class="gradient-text">Action</span> </h2> <p class="text-xl text-gray-600 max-w-2xl mx-auto" data-en="Watch how developers use MoFA to build sophisticated AI applications in minutes" data-zh="\u89C2\u770B\u5F00\u53D1\u8005\u5982\u4F55\u5728\u51E0\u5206\u949F\u5185\u4F7F\u7528 MoFA \u6784\u5EFA\u590D\u6742\u7684\u4EBA\u5DE5\u667A\u80FD\u5E94\u7528">Watch how developers use MoFA to build sophisticated AI applications in minutes</p> <!-- Video Embed --> <div class="video-container rounded-lg shadow-2xl overflow-hidden mx-auto" style="max-width: 800px; background-color: #2d3748;"> <iframe id="demo-video-iframe" width="100%" style="aspect-ratio: 16/9; display: block;" src="https://www.youtube.com/embed/YOUR_PLACEHOLDER_VIDEO_ID" title="MoFA in Action Demo Video" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen>
          </iframe> </div> </div> </div> <!-- \u5C0F\u578B\u5206\u9694\u7EBF --> <div class="mini-divider"> <div class="mini-line red-line"></div> <div class="mini-line blue-line"></div> <div class="mini-line yellow-line"></div> </div> </section></main> <footer style="background-color: var(--mondrian-black); color: white;"> <div class="container py-12"> <div class="text-center"> <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin-bottom: 16px;"> <img src="https://avatars.githubusercontent.com/u/167464495" alt="MoFA Logo" style="width: 32px; height: 32px; border-radius: 6px;"> <span style="font-size: 1.25rem; font-weight: 700;">MoFA</span> </div> <p style="color: #9ca3af; margin-bottom: 8px;" data-en="Make Ordinary Developers Full-stack AI Engineers" data-zh="\u8BA9\u666E\u901A\u5F00\u53D1\u8005\u6210\u4E3A\u5168\u6808 AI \u5DE5\u7A0B\u5E08">
Make Ordinary Developers Full-stack AI Engineers
</p> <p style="color: #9ca3af; margin-bottom: 24px;" data-en="Modular Framework for AI Agents" data-zh="\u6A21\u5757\u5316 AI \u4EE3\u7406\u6846\u67B6">
Modular Framework for AI Agents
</p> <div style="display: flex; justify-content: center; gap: 32px; margin-bottom: 16px;"> <a href="https://github.com/moxin-org/mofa" target="_blank" rel="noopener noreferrer" style="color: #9ca3af; text-decoration: none; transition: color 0.2s ease;" onmouseover="this.style.color='white'" onmouseout="this.style.color='#9ca3af'">GitHub</a> <a href="https://discord.gg/mofatesttesttesttse" target="_blank" rel="noopener noreferrer" style="color: #9ca3af; text-decoration: none; transition: color 0.2s ease;" onmouseover="this.style.color='white'" onmouseout="this.style.color='#9ca3af'">Discord</a> <a href="https://github.com/moxin-org/mofa/tree/main/Gosim_2024_Hackathon/documents" target="_blank" rel="noopener noreferrer" style="color: #9ca3af; text-decoration: none; transition: color 0.2s ease;" onmouseover="this.style.color='white'" onmouseout="this.style.color='#9ca3af'" data-en="Docs" data-zh="\u6587\u6863">Docs</a> </div> <p style="color: #6b7280; font-size: 0.875rem;" data-en="\xA9 2025 MoFA. All rights reserved. | Made with \u2764\uFE0F by MoFA Team" data-zh="\xA9 2025 MoFA. \u4FDD\u7559\u6240\u6709\u6743\u5229. | Made with \u2764\uFE0F by MoFA Team">
&copy; 2024 MoFA. All rights reserved. | Made with \u2764\uFE0F by MoFA Team
</p> </div> </div> </footer> <!-- \u8FD4\u56DE\u9876\u90E8\u6309\u94AE --> <button id="back-to-top" title="Go to top" style="
    display: none; /* Hidden by default */
    position: fixed;
    bottom: 30px;
    right: 30px;
    z-index: 99;
    border: none;
    outline: none;
    background-color: var(--mondrian-red);
    color: white;
    cursor: pointer;
    padding: 15px;
    border-radius: 50%;
    font-size: 18px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    transition: background-color 0.3s, opacity 0.3s, visibility 0.3s;
  ">
\u2191
</button> <!-- \u8BED\u8A00\u5207\u6362\u811A\u672C --> <script>
    // \u8FD4\u56DE\u9876\u90E8\u6309\u94AE\u903B\u8F91
    const backToTopButton = document.getElementById('back-to-top');

    window.onscroll = function() {
      if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
        backToTopButton.style.display = "block";
      } else {
        backToTopButton.style.display = "none";
      }
    };

    backToTopButton.addEventListener('click', function(){
      window.scrollTo({top: 0, behavior: 'smooth'});
    });

    // \u8BED\u8A00\u6570\u636E\u548C\u5207\u6362\u903B\u8F91
    const languages = {
      en: {
        flag: '\u{1F1FA}\u{1F1F8}',
        name: 'EN',
        title: 'MoFA - Make Ordinary Developers Full-stack AI Engineers'
      },
      zh: {
        flag: '\u{1F1E8}\u{1F1F3}',
        name: '\u4E2D\u6587',
        title: 'MoFA - \u8BA9\u666E\u901A\u5F00\u53D1\u8005\u6210\u4E3A\u5168\u6808 AI \u5DE5\u7A0B\u5E08'
      }
    };

    let currentLang = 'en'; // \u9ED8\u8BA4\u82F1\u6587

    function updateLanguage(lang) {
      currentLang = lang;
      
      // \u66F4\u65B0\u9875\u9762title
      document.getElementById('page-title').textContent = languages[lang].title;
      
      // \u66F4\u65B0html lang\u5C5E\u6027
      document.getElementById('html-root').setAttribute('lang', lang === 'zh' ? 'zh-CN' : 'en');
      
      // \u66F4\u65B0\u8BED\u8A00\u5207\u6362\u6309\u94AE\u663E\u793A
      const currentLangEl = document.getElementById('current-lang');
      const otherLang = lang === 'en' ? 'zh' : 'en';
      currentLangEl.textContent = \\\`\\\${languages[otherLang].flag} \\\${languages[otherLang].name}\\\`;
      
      // \u66F4\u65B0\u6240\u6709\u5E26\u6709data-en\u548Cdata-zh\u5C5E\u6027\u7684\u5143\u7D20
      const elements = document.querySelectorAll('[data-en][data-zh]');
      elements.forEach(element => {
        const text = element.getAttribute(\\\`data-\\\${lang}\\\`);
        if (text) {
          element.innerHTML = text;
        }
      });

      // \u66F4\u65B0\u89C6\u9891iframe\u7684src
      const videoIframe = document.getElementById('demo-video-iframe');
      if (videoIframe) {
        if (lang === 'zh') {
          videoIframe.src = "//player.bilibili.com/player.html?bvid=BV15fQPY6EnD&page=1&high_quality=1&danmaku=0";
        } else { // 'en' or default
          videoIframe.src = "https://www.youtube.com/embed/YOUR_PLACEHOLDER_VIDEO_ID"; // TODO: Replace with actual English video when ready
        }
      }
      
      // \u4FDD\u5B58\u8BED\u8A00\u8BBE\u7F6E\u5230localStorage
      localStorage.setItem('mofa-language', lang);
    }

    // \u521D\u59CB\u5316\u8BED\u8A00
    function initLanguage() {
      // \u4ECElocalStorage\u8BFB\u53D6\u4FDD\u5B58\u7684\u8BED\u8A00\u8BBE\u7F6E
      const savedLang = localStorage.getItem('mofa-language');
      
      if (savedLang && languages[savedLang]) {
        updateLanguage(savedLang);
      } else {
        // \u9ED8\u8BA4\u82F1\u6587
        updateLanguage('en');
      }
    }

    // \u8BED\u8A00\u5207\u6362\u4E8B\u4EF6
    document.getElementById('lang-toggle').addEventListener('click', () => {
      const newLang = currentLang === 'en' ? 'zh' : 'en';
      updateLanguage(newLang);
    });

    // \u9875\u9762\u52A0\u8F7D\u65F6\u521D\u59CB\u5316\u8BED\u8A00
    document.addEventListener('DOMContentLoaded', initLanguage);

    // \u4EA4\u4E92\u5F0F\u6D41\u7A0B\u53EF\u89C6\u5316
    let currentDemo = 'arxiv';
    let currentStep = 0;
    let isPlaying = false;
    let flowInterval;
    let demoSwitchInterval;

    // \u4E0D\u540Cdemo\u7684\u6D41\u7A0B\u914D\u7F6E
    const flowConfigs = {
      'hello-world': {
        steps: 2,
        connections: [
          { from: 1, to: 2 },
          { from: 2, to: 1 } // \u5FAA\u73AF
        ]
      },
      'browser-use': {
        steps: 2,
        connections: [
          { from: 1, to: 2 }
        ]
      },
      'deep-research': {
        steps: 2,
        connections: [
          { from: 1, to: 2 },
          { from: 2, to: 1 } // \u5FAA\u73AF
        ]
      },
      'firecrawl': {
        steps: 3,
        connections: [
          { from: 1, to: 2 },
          { from: 2, to: 3 }
        ]
      },
      'weather': {
        steps: 4,
        connections: [
          { from: 1, to: 2 },
          { from: 2, to: 3 },
          { from: 3, to: 4 }
        ]
      },
      'arxiv': {
        steps: 6,
        connections: [
          { from: 1, to: 2 },
          { from: 2, to: 3 },
          { from: 3, to: 4 },
          { from: 4, to: 5 },
          { from: 5, to: 6 },
          { from: 6, to: 1 } // cycle back for demonstration
        ]
      },
      'moly-client': {
        steps: 2,
        connections: [
          { from: 1, to: 2 },
          { from: 2, to: 1 } // bidirectional flow
        ]
      },
      'mem0-dataflow': {
        steps: 3,
        connections: [
          { from: 1, to: 2 },
          { from: 2, to: 3 },
          { from: 3, to: 2 }, // memory feedback loop
          { from: 2, to: 1 } // result feedback
        ]
      },
      'camera-screenshot': {
        steps: 2,
        connections: [
          { from: 1, to: 2 },
          { from: 2, to: 1 } // result feedback
        ]
      }
    };

    // \u6D41\u7A0B\u53EF\u89C6\u5316\u51FD\u6570
    function initFlowVisualization() {
      try {
        // \u7ED1\u5B9Ademo\u5207\u6362\u4E8B\u4EF6
        const demoTabs = document.querySelectorAll('.demo-tab');
        console.log('Found demo tabs:', demoTabs.length);
        
        demoTabs.forEach(tab => {
          tab.addEventListener('click', () => {
            console.log('Demo tab clicked:', tab.dataset.demo);
            switchDemo(tab.dataset.demo);
          });
        });
        
        // \u7ED1\u5B9A\u8F6E\u64AD\u7BAD\u5934\u4E8B\u4EF6
        const leftArrow = document.querySelector('.carousel-arrow-left');
        const rightArrow = document.querySelector('.carousel-arrow-right');
        
        if (leftArrow && rightArrow) {
          leftArrow.addEventListener('click', () => {
            const demos = ['hello-world', 'browser-use', 'deep-research', 'firecrawl', 'weather', 'arxiv', 'moly-client', 'mem0-dataflow', 'camera-screenshot'];
            const currentIndex = demos.indexOf(currentDemo);
            const prevIndex = (currentIndex - 1 + demos.length) % demos.length;
            switchDemo(demos[prevIndex]);
          });
          
          rightArrow.addEventListener('click', () => {
            const demos = ['hello-world', 'browser-use', 'deep-research', 'firecrawl', 'weather', 'arxiv', 'moly-client', 'mem0-dataflow', 'camera-screenshot'];
            const currentIndex = demos.indexOf(currentDemo);
            const nextIndex = (currentIndex + 1) % demos.length;
            switchDemo(demos[nextIndex]);
          });
        }
        
        // Set step attributes for all flow steps
        document.querySelectorAll('.demo-content').forEach(demo => {
          const steps = demo.querySelectorAll('.flow-step');
          steps.forEach((step, index) => {
            step.setAttribute('data-step', index + 1);
          });
        });
        
        // \u521D\u59CB\u5316\u5F53\u524Ddemo
        console.log('Initializing with hello-world demo');
        switchDemo('hello-world');
        
        // \u5F00\u59CB\u81EA\u52A8\u5FAA\u73AF\u64AD\u653E
        startAutoFlow();
        
        // \u6BCF60\u79D2\u81EA\u52A8\u5207\u6362demo
        demoSwitchInterval = setInterval(() => {
          const demos = ['hello-world', 'browser-use', 'deep-research', 'firecrawl', 'weather', 'arxiv', 'moly-client', 'mem0-dataflow', 'camera-screenshot'];
          const currentIndex = demos.indexOf(currentDemo);
          const nextIndex = (currentIndex + 1) % demos.length;
          switchDemo(demos[nextIndex]);
        }, 60000);
        
        console.log('Flow visualization initialized successfully');
      } catch (error) {
        console.error('Error initializing flow visualization:', error);
      }
    }

    function switchDemo(demoType) {
      try {
        console.log('Switching to demo:', demoType);
        if (demoType === currentDemo) return;
        
        // \u505C\u6B62\u5F53\u524D\u6D41\u7A0B
        stopFlow();
        
        // \u5207\u6362demo\u663E\u793A
        const allDemos = document.querySelectorAll('.demo-content');
        console.log('Found demo contents:', allDemos.length);
        
        allDemos.forEach(demo => {
          demo.style.display = 'none';
          demo.classList.remove('active');
        });
        
        const targetDemo = document.getElementById(\\\`\\\${demoType}-demo\\\`);
        console.log('Target demo element:', targetDemo);
        
        if (targetDemo) {
          targetDemo.style.display = 'block';
          targetDemo.classList.add('active');
        } else {
          console.error('Target demo not found:', \\\`\\\${demoType}-demo\\\`);
          return;
        }
        
        // \u66F4\u65B0tab\u72B6\u6001
        const allTabs = document.querySelectorAll('.demo-tab');
        allTabs.forEach(tab => {
          if (tab.dataset.demo === demoType) {
            tab.classList.add('active');
          } else {
            tab.classList.remove('active');
          }
        });
        
        currentDemo = demoType;
        currentStep = 0;
        
        // \u91CD\u65B0\u7ED8\u5236\u8FDE\u63A5\u7EBF\u5E76\u5F00\u59CB\u6D41\u7A0B
        setTimeout(() => {
          try {
            drawConnections();
            resetFlow();
            startAutoFlow();
            console.log('Demo switched successfully to:', demoType);
          } catch (error) {
            console.error('Error in demo switch timeout:', error);
          }
        }, 100);
      } catch (error) {
        console.error('Error switching demo:', error);
      }
    }

    function drawConnections() {
      const activeDemo = document.querySelector('.demo-content.active');
      if (!activeDemo) return;
      
      const svg = activeDemo.querySelector('.flow-connections');
      if (!svg) return;

      svg.innerHTML = '';
      
      const config = flowConfigs[currentDemo];
      if (!config) return;
      
      config.connections.forEach((connection, index) => {
        const fromElement = activeDemo.querySelector(\\\`[data-step="\\\${connection.from}"] .agent-card\\\`);
        const toElement = activeDemo.querySelector(\\\`[data-step="\\\${connection.to}"] .agent-card\\\`);
        
        if (fromElement && toElement) {
          const fromRect = fromElement.getBoundingClientRect();
          const toRect = toElement.getBoundingClientRect();
          const containerRect = activeDemo.querySelector('.flow-container').getBoundingClientRect();
          
          const fromX = fromRect.left - containerRect.left + fromRect.width / 2;
          const fromY = fromRect.top - containerRect.top + fromRect.height / 2;
          const toX = toRect.left - containerRect.left + toRect.width / 2;
          const toY = toRect.top - containerRect.top + toRect.height / 2;
          
          const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
          
          // \u521B\u5EFA\u8D1D\u585E\u5C14\u66F2\u7EBF\u8DEF\u5F84
          const controlX1 = fromX + (toX - fromX) * 0.5;
          const controlY1 = fromY;
          const controlX2 = toX - (toX - fromX) * 0.5;
          const controlY2 = toY;
          
          const pathData = \\\`M \\\${fromX} \\\${fromY} C \\\${controlX1} \\\${controlY1}, \\\${controlX2} \\\${controlY2}, \\\${toX} \\\${toY}\\\`;
          
          path.setAttribute('d', pathData);
          path.setAttribute('class', 'flow-path');
          path.setAttribute('data-connection', index);
          
          svg.appendChild(path);
        }
      });
    }

    function startAutoFlow() {
      if (isPlaying) return;
      
      isPlaying = true;
      currentStep = 0;
      
      const config = flowConfigs[currentDemo];
      if (!config) return;
      
      flowInterval = setInterval(() => {
        if (currentStep < config.steps) {
          activateStep(currentStep + 1);
          currentStep++;
        } else {
          // \u6D41\u7A0B\u5B8C\u6210\uFF0C\u91CD\u65B0\u5F00\u59CB
          setTimeout(() => {
            resetFlow();
            currentStep = 0;
          }, 2000);
        }
      }, 1500);
    }

    function stopFlow() {
      isPlaying = false;
      if (flowInterval) {
        clearInterval(flowInterval);
        flowInterval = null;
      }
    }

    function activateStep(step) {
      const activeDemo = document.querySelector('.demo-content.active');
      if (!activeDemo) return;
      
      // \u6FC0\u6D3B\u5F53\u524D\u6B65\u9AA4
      const stepElement = activeDemo.querySelector(\\\`[data-step="\\\${step}"] .agent-card\\\`);
      if (stepElement) {
        stepElement.classList.remove('pending', 'completed');
        stepElement.classList.add('active', 'processing');
        stepElement.style.transform = 'scale(1)';
        stepElement.style.opacity = '1';
        stepElement.style.boxShadow = '0 10px 30px rgba(99, 102, 241, 0.3)';
        
        // 1.2\u79D2\u540E\u6807\u8BB0\u4E3A\u5B8C\u6210
        setTimeout(() => {
          stepElement.classList.remove('active', 'processing');
          stepElement.classList.add('completed');
          stepElement.style.boxShadow = 'none';
        }, 1200);
      }
      
      // \u6FC0\u6D3B\u76F8\u5173\u8FDE\u63A5\u7EBF
      const config = flowConfigs[currentDemo];
      if (config) {
        config.connections.forEach((connection, index) => {
          if (connection.from === step) {
            setTimeout(() => {
              const path = activeDemo.querySelector(\\\`[data-connection="\\\${index}"]\\\`);
              if (path) {
                path.classList.add('active');
              }
            }, 600);
          }
        });
      }
    }

    function resetFlow() {
      stopFlow();
      currentStep = 0;
      
      const activeDemo = document.querySelector('.demo-content.active');
      if (!activeDemo) return;
      
      // \u91CD\u7F6E\u6240\u6709\u4EE3\u7406\u72B6\u6001
      const agents = activeDemo.querySelectorAll('.interactive-agent');
      agents.forEach(agent => {
        agent.classList.remove('active', 'completed', 'processing');
        agent.classList.add('pending');
        agent.style.transform = 'scale(0.95)';
        agent.style.opacity = '0.7';
        agent.style.boxShadow = 'none';
      });
      
      // \u91CD\u7F6E\u8FDE\u63A5\u7EBF
      const paths = activeDemo.querySelectorAll('.flow-path');
      paths.forEach(path => {
        path.classList.remove('active');
      });
    }

    // \u7A97\u53E3\u5927\u5C0F\u6539\u53D8\u65F6\u91CD\u65B0\u7ED8\u5236\u8FDE\u63A5\u7EBF
    window.addEventListener('resize', () => {
      setTimeout(drawConnections, 100);
    });

    // \u9875\u9762\u52A0\u8F7D\u65F6\u521D\u59CB\u5316\u6D41\u7A0B\u53EF\u89C6\u5316
    function initPage() {
      try {
        console.log('Page initialization started');
        initLanguage();
        setTimeout(() => {
          console.log('Starting flow visualization initialization');
          initFlowVisualization();
        }, 100);
      } catch (error) {
        console.error('Error during page initialization:', error);
      }
    }

    // \u786E\u4FDDDOM\u5B8C\u5168\u52A0\u8F7D\u540E\u518D\u521D\u59CB\u5316
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initPage);
    } else {
      // DOM\u5DF2\u7ECF\u52A0\u8F7D\u5B8C\u6210\uFF0C\u76F4\u63A5\u521D\u59CB\u5316
      initPage();
    }
  <\/script> </body> </html>`])), renderHead());
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/mofa-website/src/pages/index.astro", void 0);

const $$file$3 = "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/mofa-website/src/pages/index.astro";
const $$url$3 = "/mofa";

const index$3 = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Index$3,
  file: $$file$3,
  url: $$url$3
}, Symbol.toStringTag, { value: 'Module' }));

const $$Index$2 = createComponent(($$result, $$props, $$slots) => {
  const examples = [
    {
      id: "hello-world",
      title: "Hello World",
      description: "\u6700\u7B80\u5355\u7684\u5165\u95E8\u793A\u4F8B\uFF0C\u521B\u5EFA\u7B2C\u4E00\u4E2A AI \u4EE3\u7406",
      category: "\u5165\u95E8",
      difficulty: 1,
      time: "5\u5206\u949F",
      code: `from mofa import Agent, Pipeline
from mofa.messages import HumanMessage

# \u521B\u5EFA\u4EE3\u7406
agent = Agent(
    name="hello-agent",
    system_prompt="\u4F60\u662F\u4E00\u4E2A\u53CB\u597D\u7684\u52A9\u624B"
)

# \u521B\u5EFA\u7BA1\u9053\u5E76\u8FD0\u884C
pipeline = Pipeline().add(agent)
response = pipeline.run(
    HumanMessage("\u4F60\u597D\uFF01")
)

print(response.content)`,
      color: "bg-mondrian-red"
    },
    {
      id: "rag-qa",
      title: "RAG \u95EE\u7B54\u7CFB\u7EDF",
      description: "\u57FA\u4E8E\u68C0\u7D22\u589E\u5F3A\u751F\u6210\u7684\u667A\u80FD\u95EE\u7B54\u7CFB\u7EDF",
      category: "\u4E2D\u7EA7",
      difficulty: 3,
      time: "30\u5206\u949F",
      code: `from mofa import Agent, Pipeline
from mofa.agents import RAGAgent
from mofa.knowledge import VectorStore

# \u521B\u5EFA\u77E5\u8BC6\u5E93
knowledge = VectorStore()
knowledge.add_documents([
    "MoFA \u662F\u4E00\u4E2A\u6A21\u5757\u5316\u7684 AI \u4EE3\u7406\u6846\u67B6",
    "\u5B83\u652F\u6301\u7EC4\u5408\u5F0F\u5F00\u53D1\u6A21\u5F0F"
])

# \u521B\u5EFA RAG \u4EE3\u7406
rag_agent = RAGAgent(
    name="rag-qa",
    knowledge_base=knowledge
)

# \u8FD0\u884C\u67E5\u8BE2
pipeline = Pipeline().add(rag_agent)
response = pipeline.run("\u4EC0\u4E48\u662F MoFA\uFF1F")`,
      color: "bg-mondrian-blue"
    },
    {
      id: "arxiv-analyzer",
      title: "Arxiv \u8BBA\u6587\u5206\u6790",
      description: "\u81EA\u52A8\u5206\u6790\u548C\u603B\u7ED3\u5B66\u672F\u8BBA\u6587\u7684 AI \u4EE3\u7406",
      category: "\u9AD8\u7EA7",
      difficulty: 4,
      time: "60\u5206\u949F",
      code: `from mofa import Agent, Pipeline
from mofa.agents import PaperAnalyzer
from mofa.tools import ArxivTool

# \u521B\u5EFA\u8BBA\u6587\u5206\u6790\u4EE3\u7406
analyzer = PaperAnalyzer(
    name="arxiv-analyzer",
    tools=[ArxivTool()]
)

# \u5206\u6790\u8BBA\u6587
pipeline = Pipeline().add(analyzer)
result = pipeline.run(
    "\u5206\u6790\u8BBA\u6587 arxiv:2301.00001"
)

print(result.summary)`,
      color: "bg-mondrian-yellow"
    },
    {
      id: "reflection-agent",
      title: "\u53CD\u601D\u4EE3\u7406",
      description: "\u5177\u6709\u81EA\u6211\u53CD\u601D\u80FD\u529B\u7684\u667A\u80FD\u4EE3\u7406\u7CFB\u7EDF",
      category: "\u9AD8\u7EA7",
      difficulty: 4,
      time: "45\u5206\u949F",
      code: `from mofa import Agent, Pipeline
from mofa.patterns import ReflectionPattern

# \u521B\u5EFA\u53CD\u601D\u4EE3\u7406
agent = Agent(
    name="reflection-agent",
    pattern=ReflectionPattern(
        max_iterations=3
    )
)

pipeline = Pipeline().add(agent)
response = pipeline.run(
    "\u5199\u4E00\u4E2APython\u6392\u5E8F\u7B97\u6CD5\u5E76\u4F18\u5316\u5B83"
)`,
      color: "bg-mondrian-red"
    },
    {
      id: "multi-agent",
      title: "\u591A\u4EE3\u7406\u534F\u4F5C",
      description: "\u591A\u4E2A AI \u4EE3\u7406\u534F\u540C\u5DE5\u4F5C\u5B8C\u6210\u590D\u6742\u4EFB\u52A1",
      category: "\u4E13\u5BB6",
      difficulty: 5,
      time: "90\u5206\u949F",
      code: `from mofa import Agent, Pipeline
from mofa.patterns import CollaborationPattern

# \u521B\u5EFA\u591A\u4E2A\u4E13\u95E8\u4EE3\u7406
researcher = Agent(name="researcher")
writer = Agent(name="writer") 
reviewer = Agent(name="reviewer")

# \u8BBE\u7F6E\u534F\u4F5C\u6A21\u5F0F
pipeline = Pipeline(
    pattern=CollaborationPattern()
)
pipeline.add(researcher)
pipeline.add(writer)
pipeline.add(reviewer)

result = pipeline.run(
    "\u7814\u7A76\u5E76\u5199\u4E00\u7BC7\u5173\u4E8E AI \u53D1\u5C55\u7684\u6587\u7AE0"
)`,
      color: "bg-mondrian-blue"
    },
    {
      id: "community-examples",
      title: "\u793E\u533A\u6848\u4F8B",
      description: "\u6765\u81EA\u793E\u533A\u7684\u7CBE\u5F69\u5E94\u7528\u6848\u4F8B\u96C6\u5408",
      category: "\u793E\u533A",
      difficulty: 0,
      time: "\u53D8\u5316",
      code: `# \u793E\u533A\u8D21\u732E\u7684\u5404\u79CD\u521B\u610F\u6848\u4F8B
# \u5305\u62EC\u4F46\u4E0D\u9650\u4E8E\uFF1A
# - \u667A\u80FD\u5BA2\u670D\u7CFB\u7EDF
# - \u4EE3\u7801\u751F\u6210\u52A9\u624B
# - \u6570\u636E\u5206\u6790\u5DE5\u5177
# - \u521B\u610F\u5199\u4F5C\u52A9\u624B
# - \u6E38\u620F NPC \u7CFB\u7EDF

# \u67E5\u770B\u5B8C\u6574\u6848\u4F8B\u8BF7\u8BBF\u95EE\uFF1A
# https://github.com/moxin-org/mofa-examples`,
      color: "bg-mondrian-yellow"
    }
  ];
  const { base } = (Object.assign({"BASE_URL":"/mofa","MODE":"production","DEV":false,"PROD":true,"SSR":true,"SITE":"https://moxin-org.github.io","ASSETS_PREFIX":undefined},{_:process.env._,}));
  function getDifficultyStars(difficulty) {
    return "\u2605".repeat(difficulty) + "\u2606".repeat(5 - difficulty);
  }
  return renderTemplate`${renderComponent($$result, "BaseLayout", $$BaseLayout, { "title": "\u793A\u4F8B\u9879\u76EE", "description": "\u63A2\u7D22 MoFA \u7684\u5404\u79CD\u5E94\u7528\u573A\u666F\u548C\u5B9E\u73B0\u65B9\u5F0F" }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="container mx-auto px-4 py-16"> <!-- Header --> <div class="text-center mb-16"> <h1 class="text-5xl font-bold mb-4">
示例项目展示
</h1> <p class="text-xl text-gray-600 max-w-2xl mx-auto">
从简单到复杂，探索 <span class="gradient-text">MoFA</span> 的无限可能
</p> </div> <!-- Examples Grid --> <div class="max-w-7xl mx-auto"> ${examples.map((example) => renderTemplate`<div class="mb-12 group"${addAttribute(example.id, "id")}> <div class="card border-2 border-mondrian-black hover:border-4 transition-all duration-200"> <!-- Header --> <div class="flex flex-col lg:flex-row lg:items-start lg:justify-between mb-6"> <div class="flex-1"> <div class="flex items-center mb-3"> <span${addAttribute(`${example.color} text-white text-sm px-3 py-1 rounded-md font-medium mr-3`, "class")}> ${example.category} </span> ${example.difficulty > 0 && renderTemplate`<span class="text-sm text-gray-500 mr-3">
难度: ${getDifficultyStars(example.difficulty)} </span>`} <span class="text-sm text-gray-500">
预计时间: ${example.time} </span> </div> <h2 class="text-3xl font-bold mb-3 group-hover:text-mondrian-red transition-colors"> ${example.title} </h2> <p class="text-lg text-gray-600"> ${example.description} </p> </div> <div class="mt-4 lg:mt-0 lg:ml-6"> <a${addAttribute(`https://github.com/moxin-org/mofa-examples/tree/main/${example.id}`, "href")} target="_blank" rel="noopener noreferrer" class="btn-primary">
查看完整代码
<svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"> <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path> </svg> </a> </div> </div> <!-- Code Example --> <div class="relative group/code"> <div class="absolute -inset-1 bg-gradient-to-r from-mondrian-red via-mondrian-blue to-mondrian-yellow opacity-20 blur group-hover/code:opacity-30 transition duration-300"></div> <div class="relative bg-gray-900 rounded-lg p-6 border-2 border-mondrian-black"> <pre class="text-sm overflow-x-auto"><code class="text-gray-100">${example.code}</code></pre> </div> </div> </div> </div>`)} </div> <!-- Call to Action --> <div class="text-center mt-16"> <div class="bg-gray-50 rounded-lg p-8"> <h2 class="text-2xl font-bold mb-4">想要贡献你的示例？</h2> <p class="text-gray-600 mb-6">我们欢迎社区贡献更多有趣的应用案例</p> <div class="flex flex-col sm:flex-row gap-4 justify-center"> <a href="https://github.com/moxin-org/mofa-examples" target="_blank" rel="noopener noreferrer" class="btn-secondary">
查看示例仓库
</a> <a${addAttribute(`${base}/community/contributing`, "href")} class="btn-outline">
贡献指南
</a> </div> </div> </div> </div> ` })}`;
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/mofa-website/src/pages/examples/index.astro", void 0);

const $$file$2 = "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/mofa-website/src/pages/examples/index.astro";
const $$url$2 = "/mofa/examples";

const index$2 = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Index$2,
  file: $$file$2,
  url: $$url$2
}, Symbol.toStringTag, { value: 'Module' }));

const $$Index$1 = createComponent(async ($$result, $$props, $$slots) => {
  const posts = await getCollection("blog");
  const sortedPosts = posts.sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
  const { base } = (Object.assign({"BASE_URL":"/mofa","MODE":"production","DEV":false,"PROD":true,"SSR":true,"SITE":"https://moxin-org.github.io","ASSETS_PREFIX":undefined},{}));
  return renderTemplate`${renderComponent($$result, "BaseLayout", $$BaseLayout, { "title": "\u535A\u5BA2", "description": "MoFA \u7684\u6700\u65B0\u52A8\u6001\u548C\u6280\u672F\u5206\u4EAB" }, { "default": async ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="container mx-auto px-4 py-16"> <!-- Header --> <div class="text-center mb-16"> <h1 class="text-5xl font-bold mb-4"> <span class="gradient-text">MoFA</span> 博客
</h1> <p class="text-xl text-gray-600 max-w-2xl mx-auto">
分享 AI 开发的最新动态、技术洞察和实践经验
</p> </div> <!-- Blog Posts Grid --> <div class="max-w-4xl mx-auto"> ${sortedPosts.map((post) => renderTemplate`<article class="card mb-8 group hover:border-mondrian-red transition-all duration-200"> <div class="flex flex-col md:flex-row md:items-center md:justify-between"> <div class="flex-1"> <div class="flex items-center mb-2"> <time class="text-sm text-gray-500 mr-4"> ${post.data.date.toLocaleDateString("zh-CN")} </time> ${post.data.tags && renderTemplate`<div class="flex gap-2"> ${post.data.tags.map((tag) => renderTemplate`<span class="text-xs bg-mondrian-yellow text-gray-900 px-2 py-1 rounded"> ${tag} </span>`)} </div>`} </div> <h2 class="text-2xl font-semibold mb-2 group-hover:text-mondrian-red transition-colors"> <a${addAttribute(`${base}/blog/${post.slug}`, "href")}> ${post.data.title} </a> </h2> <p class="text-gray-600 mb-4"> ${post.data.description} </p> <div class="flex items-center text-sm text-gray-500"> <span>作者：${post.data.author}</span> </div> </div> <div class="md:ml-6 mt-4 md:mt-0"> <a${addAttribute(`${base}/blog/${post.slug}`, "href")} class="inline-flex items-center text-mondrian-blue hover:text-mondrian-red transition-colors">
阅读全文
<svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"> <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path> </svg> </a> </div> </div> </article>`)} </div> <!-- Empty state --> ${sortedPosts.length === 0 && renderTemplate`<div class="text-center py-16"> <div class="mondrian-grid grid-cols-3 grid-rows-3 w-24 h-24 mx-auto mb-6 opacity-50"> <div class="mondrian-block bg-mondrian-red"></div> <div class="mondrian-block bg-mondrian-white"></div> <div class="mondrian-block bg-mondrian-blue"></div> <div class="mondrian-block bg-mondrian-yellow"></div> <div class="mondrian-block bg-mondrian-white"></div> <div class="mondrian-block bg-mondrian-red"></div> <div class="mondrian-block bg-mondrian-white"></div> <div class="mondrian-block bg-mondrian-blue"></div> <div class="mondrian-block bg-mondrian-yellow"></div> </div> <h2 class="text-2xl font-semibold text-gray-700 mb-2">敬请期待</h2> <p class="text-gray-600">我们正在准备更多精彩内容</p> </div>`} </div> ` })}`;
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/mofa-website/src/pages/blog/index.astro", void 0);

const $$file$1 = "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/mofa-website/src/pages/blog/index.astro";
const $$url$1 = "/mofa/blog";

const index$1 = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Index$1,
  file: $$file$1,
  url: $$url$1
}, Symbol.toStringTag, { value: 'Module' }));

const $$Index = createComponent(($$result, $$props, $$slots) => {
  const { base } = (Object.assign({"BASE_URL":"/mofa","MODE":"production","DEV":false,"PROD":true,"SSR":true,"SITE":"https://moxin-org.github.io","ASSETS_PREFIX":undefined},{_:process.env._,}));
  return renderTemplate`${renderComponent($$result, "DocsLayout", $$DocsLayout, { "title": "\u6587\u6863", "description": "MoFA \u6846\u67B6\u7684\u5B8C\u6574\u6587\u6863" }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<h1>MoFA 文档</h1> <p style="font-size: 1.125rem; color: #6b7280; margin-bottom: 2rem;">
欢迎查阅 MoFA (Modular Framework for AI Agents) 的官方文档。在这里你可以找到关于如何使用 MoFA 构建 AI 应用的所有信息。
</p> <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px; margin-top: 3rem;"> <div class="card"> <h2 style="color: var(--mondrian-red); margin-bottom: 1rem;">🚀 快速开始</h2> <p style="color: #6b7280; margin-bottom: 1rem;">5分钟内创建你的第一个 AI 代理</p> <a${addAttribute(`${base}/docs/quick-start`, "href")} class="btn-primary" style="display: inline-flex;">
开始学习
</a> </div> <div class="card"> <h2 style="color: var(--mondrian-blue); margin-bottom: 1rem;">📚 核心概念</h2> <p style="color: #6b7280; margin-bottom: 1rem;">了解 MoFA 的核心设计理念和架构</p> <a${addAttribute(`${base}/docs/concepts/agent`, "href")} class="btn-secondary" style="display: inline-flex;">
深入了解
</a> </div> <div class="card"> <h2 style="color: var(--mondrian-yellow); margin-bottom: 1rem;">🔧 API 参考</h2> <p style="color: #6b7280; margin-bottom: 1rem;">完整的 API 文档和使用示例</p> <a${addAttribute(`${base}/docs/api`, "href")} class="btn-outline" style="display: inline-flex;">
查看 API
</a> </div> </div> <div style="margin-top: 3rem; padding: 2rem; background-color: #f3f4f6; border-radius: 8px;"> <h2 style="margin-bottom: 1rem;">📖 推荐阅读顺序</h2> <ol style="list-style: decimal; margin-left: 2rem; line-height: 2;"> <li><a${addAttribute(`${base}/docs/quick-start`, "href")} style="color: var(--mondrian-blue);">快速开始</a> - 安装和创建第一个代理</li> <li><a${addAttribute(`${base}/docs/concepts/agent`, "href")} style="color: var(--mondrian-blue);">代理概念</a> - 理解 Agent 的工作原理</li> <li><a${addAttribute(`${base}/docs/concepts/pipeline`, "href")} style="color: var(--mondrian-blue);">管道系统</a> - 学习如何组合多个代理</li> <li><a${addAttribute(`${base}/docs/patterns`, "href")} style="color: var(--mondrian-blue);">设计模式</a> - 探索不同的代理设计模式</li> <li><a${addAttribute(`${base}/docs/advanced`, "href")} style="color: var(--mondrian-blue);">高级主题</a> - 深入了解高级功能</li> </ol> </div> <div style="margin-top: 3rem; text-align: center; padding: 2rem; border: 2px solid var(--mondrian-black); border-radius: 8px;"> <h3 style="margin-bottom: 1rem;">需要帮助？</h3> <p style="color: #6b7280; margin-bottom: 1.5rem;">
如果你在使用过程中遇到任何问题，欢迎通过以下方式寻求帮助：
</p> <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;"> <a href="https://github.com/moxin-org/mofa/issues" target="_blank" rel="noopener noreferrer" class="btn-outline">
GitHub Issues
</a> <a href="https://discord.gg/mofatesttesttest" target="_blank" rel="noopener noreferrer" class="btn-primary">
Discord 社区
</a> </div> </div> ` })}`;
}, "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/mofa-website/src/pages/docs/index.astro", void 0);

const $$file = "/mnt/c/Users/ufop/Desktop/code/mofa/mofa/mofa-website/src/pages/docs/index.astro";
const $$url = "/mofa/docs";

const index = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Index,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

export { index$2 as a, index$1 as b, index as c, index$3 as i };
