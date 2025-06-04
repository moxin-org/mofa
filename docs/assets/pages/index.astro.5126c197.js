import { a as createComponent, r as renderTemplate, m as maybeRenderHead, b as addAttribute, e as renderComponent, d as renderHead } from '../astro.7f8fc68a.js';
import 'clsx';
/* empty css                           *//* empty css                          */import { $ as $$BaseLayout, g as getCollection, a as $$DocsLayout } from './_...slug_.astro.8f774045.js';

const $$WorkflowShowcase = createComponent(($$result, $$props, $$slots) => {
  const workflows = [
    {
      id: "hello-world",
      title: {
        en: "Hello World",
        zh: "Hello World"
      },
      description: {
        en: "Simplest AI agent workflow for beginners",
        zh: "\u6700\u7B80\u5355\u7684 AI \u4EE3\u7406\u5DE5\u4F5C\u6D41"
      },
      category: "Basic",
      color: "mofa-color-1",
      scale: 0.3,
      mermaidGraph: `
    flowchart TB
      terminal-input[\u{1F5A5}\uFE0F Terminal Input<br/>User Query]
      agent[\u{1F916} Agent<br/>Process & Respond]
      
      terminal-input --> agent
      agent --> terminal-input
      
      classDef inputNode fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
      classDef agentNode fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
      
      class terminal-input inputNode
      class agent agentNode`
    },
    {
      id: "arxiv-research",
      title: {
        en: "ArXiv Research",
        zh: "ArXiv \u7814\u7A76"
      },
      description: {
        en: "Automated research workflow with paper analysis and report generation",
        zh: "\u81EA\u52A8\u5316\u7814\u7A76\u5DE5\u4F5C\u6D41\uFF0C\u5305\u542B\u8BBA\u6587\u5206\u6790\u548C\u62A5\u544A\u751F\u6210"
      },
      category: "Research",
      color: "mofa-color-2",
      scale: 1,
      mermaidGraph: `
    flowchart TB
      terminal[\u{1F5A5}\uFE0F Terminal Input<br/>Research Task]
      extractor[\u{1F50D} Keyword Extractor<br/>Extract Keywords]
      downloader[\u{1F4E5} Paper Downloader<br/>Download Papers]
      analyzer[\u{1F52C} Paper Analyzer<br/>Analyze Content]
      writer[\u270D\uFE0F Report Writer<br/>Generate Report]
      feedback[\u{1F4AC} Feedback Agent<br/>Review & Suggest]
      refinement[\u{1F527} Refinement Agent<br/>Improve Report]
      
      terminal --> extractor
      extractor --> downloader
      downloader --> analyzer
      terminal --> analyzer
      analyzer --> writer
      terminal --> writer
      writer --> feedback
      terminal --> feedback
      feedback --> refinement
      terminal --> refinement
      
      classDef inputNode fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
      classDef processNode fill:#fff3e0,stroke:#f57c00,stroke-width:2px
      classDef analysisNode fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
      classDef outputNode fill:#fce4ec,stroke:#c2185b,stroke-width:2px
      
      class terminal inputNode
      class extractor,downloader processNode
      class analyzer,feedback analysisNode
      class writer,refinement outputNode`
    },
    {
      id: "rag-system",
      title: {
        en: "RAG System",
        zh: "RAG \u7CFB\u7EDF"
      },
      description: {
        en: "Retrieval-Augmented Generation for intelligent Q&A",
        zh: "\u68C0\u7D22\u589E\u5F3A\u751F\u6210\u7CFB\u7EDF\uFF0C\u7528\u4E8E\u667A\u80FD\u95EE\u7B54"
      },
      category: "AI",
      color: "mofa-color-3",
      scale: 0.5,
      mermaidGraph: `
    flowchart TB
      terminal[\u{1F5A5}\uFE0F Terminal Input<br/>User Question]
      retrieval[\u{1F50D} RAG Retrieval<br/>Search Knowledge]
      reasoner[\u{1F9E0} Reasoner Agent<br/>Generate Answer]
      
      terminal --> retrieval
      retrieval --> reasoner
      terminal --> reasoner
      retrieval --> terminal
      reasoner --> terminal
      
      classDef inputNode fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
      classDef retrievalNode fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
      classDef reasoningNode fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
      
      class terminal inputNode
      class retrieval retrievalNode
      class reasoner reasoningNode`
    },
    {
      id: "gosim-pedia",
      title: {
        en: "GoSim Pedia",
        zh: "GoSim \u767E\u79D1"
      },
      description: {
        en: "Multi-agent system with web scraping and search capabilities",
        zh: "\u5177\u6709\u7F51\u9875\u6293\u53D6\u548C\u641C\u7D22\u80FD\u529B\u7684\u591A\u4EE3\u7406\u7CFB\u7EDF"
      },
      category: "Web",
      color: "mofa-color-4",
      scale: 0.9,
      mermaidGraph: `
    flowchart TB
      openai[\u{1F916} OpenAI Server<br/>Chat Interface]
      gosim[\u{1F3AE} GoSim Pedia Agent<br/>Main Controller]
      firecrawl[\u{1F577}\uFE0F Firecrawl Agent<br/>Web Scraping]
      rag[\u{1F9E0} GoSim RAG Agent<br/>Knowledge Retrieval]
      serper[\u{1F50D} Serper Search Agent<br/>Web Search]
      
      openai <--> gosim
      gosim --> firecrawl
      firecrawl --> gosim
      gosim --> rag
      rag --> gosim
      gosim --> serper
      serper --> gosim
      
      classDef serverNode fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
      classDef mainNode fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
      classDef toolNode fill:#fff3e0,stroke:#f57c00,stroke-width:2px
      
      class openai serverNode
      class gosim mainNode
      class firecrawl,rag,serper toolNode`
    },
    {
      id: "mem0-dataflow",
      title: {
        en: "Mem0 Memory System",
        zh: "Mem0 \u8BB0\u5FC6\u7CFB\u7EDF"
      },
      description: {
        en: "Memory-enhanced AI workflow with retrieval and recording",
        zh: "\u5177\u6709\u8BB0\u5FC6\u68C0\u7D22\u548C\u8BB0\u5F55\u80FD\u529B\u7684\u589E\u5F3AAI\u5DE5\u4F5C\u6D41"
      },
      category: "Memory",
      color: "mofa-color-1",
      scale: 0.75,
      mermaidGraph: `
    flowchart TB
      terminal[\u{1F5A5}\uFE0F Terminal Input<br/>User Task]
      retrieval[\u{1F9E0} Memory Retrieval<br/>Fetch Context]
      reasoner[\u{1F914} Reasoner<br/>Process & Think]
      record[\u{1F4BE} Memory Record<br/>Store Results]
      
      terminal --> retrieval
      retrieval --> reasoner
      terminal --> reasoner
      reasoner --> record
      terminal --> record
      retrieval --> terminal
      reasoner --> terminal
      record --> terminal
      
      classDef inputNode fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
      classDef memoryNode fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
      classDef processNode fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
      classDef storageNode fill:#fff3e0,stroke:#f57c00,stroke-width:2px
      
      class terminal inputNode
      class retrieval memoryNode
      class reasoner processNode
      class record storageNode`
    },
    {
      id: "intelligent-agent-creation",
      title: {
        en: "Agent Creation System",
        zh: "\u4EE3\u7406\u521B\u5EFA\u7CFB\u7EDF"
      },
      description: {
        en: "Intelligent system for generating AI agents automatically",
        zh: "\u81EA\u52A8\u751F\u6210AI\u4EE3\u7406\u7684\u667A\u80FD\u7CFB\u7EDF"
      },
      category: "Meta-AI",
      color: "mofa-color-2",
      scale: 0.75,
      mermaidGraph: `
    flowchart TB
      openai[\u{1F916} OpenAI Server<br/>API Interface]
      config[\u2699\uFE0F Config Generator<br/>Generate Settings]
      code[\u{1F468}\u200D\u{1F4BB} Code Generator<br/>Write Agent Code]
      dependency[\u{1F4E6} Dependency Generator<br/>Manage Dependencies]
      
      openai --> config
      openai --> code
      config --> code
      openai --> dependency
      code --> dependency
      config --> dependency
      dependency --> openai
      
      classDef serverNode fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
      classDef generatorNode fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
      classDef codeNode fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
      classDef depNode fill:#fff3e0,stroke:#f57c00,stroke-width:2px
      
      class openai serverNode
      class config generatorNode
      class code codeNode
      class dependency depNode`
    },
    {
      id: "xiaowang-workflow",
      title: {
        en: "XiaoWang Multi-Agent",
        zh: "\u591A\u4EE3\u7406\u7CFB\u7EDF"
      },
      description: {
        en: "Complex multi-agent workflow with reflection and generation",
        zh: "\u5177\u6709\u53CD\u601D\u548C\u751F\u6210\u80FD\u529B\u7684\u590D\u6742\u591A\u4EE3\u7406\u5DE5\u4F5C\u6D41"
      },
      category: "Complex",
      color: "mofa-color-3",
      scale: 0.75,
      mermaidGraph: `
    flowchart TB
      terminal[\u{1F5A5}\uFE0F XiaoWang Terminal<br/>Task Input]
      dlc[\u{1F3AF} Agent DLC<br/>Task Processing]
      generate[\u{1F527} Agent Generate<br/>Content Creation]
      reflection[\u{1F914} Agent Reflection<br/>Self-Improvement]
      
      terminal --> dlc
      dlc --> generate
      generate --> reflection
      reflection --> generate
      generate --> dlc
      dlc --> terminal
      generate --> terminal
      reflection --> terminal
      
      classDef inputNode fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
      classDef taskNode fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
      classDef generateNode fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
      classDef reflectNode fill:#fff3e0,stroke:#f57c00,stroke-width:2px
      
      class terminal inputNode
      class dlc taskNode
      class generate generateNode
      class reflection reflectNode`
    }
  ];
  return renderTemplate`${maybeRenderHead()}<section class="py-20" style="background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);" data-astro-cid-22cdqia5> <div class="container mx-auto px-4" data-astro-cid-22cdqia5> <div class="text-center mb-16" data-astro-cid-22cdqia5> <h2 class="text-4xl font-bold mb-4" data-en="Real Examples: <span class='gradient-text'>AI Workflows</span> in Action" data-zh="实际案例：<span class='gradient-text'>AI 工作流</span>实战" data-astro-cid-22cdqia5>
Real Examples: <span class="gradient-text" data-astro-cid-22cdqia5>AI Workflows</span> in Action
</h2> <p class="text-xl text-gray-600 max-w-3xl mx-auto" data-en="Explore different types of AI workflows - from simple hello world to complex research automation" data-zh="探索不同类型的 AI 工作流 - 从简单的问候到复杂的研究自动化" data-astro-cid-22cdqia5>
Explore different types of AI workflows - from simple hello world to complex research automation
</p> </div> <!-- Workflow Horizontal Scroll Container --> <div class="workflow-container" data-astro-cid-22cdqia5> <div class="workflow-scroll" data-astro-cid-22cdqia5> ${workflows.map((workflow) => renderTemplate`<div class="workflow-card bg-white rounded-lg shadow-lg border-4 border-gray-300 hover:border-4 hover:border-indigo-500 transition-all duration-300 overflow-hidden" data-astro-cid-22cdqia5> <!-- Header --> <div${addAttribute(`${workflow.color} p-6 text-white`, "class")} data-astro-cid-22cdqia5> <h3 class="text-2xl font-bold mb-2"${addAttribute(workflow.title.en, "data-en")}${addAttribute(workflow.title.zh, "data-zh")} data-astro-cid-22cdqia5> ${workflow.title.en} </h3> <p class="text-white text-opacity-90"${addAttribute(workflow.description.en, "data-en")}${addAttribute(workflow.description.zh, "data-zh")} data-astro-cid-22cdqia5> ${workflow.description.en} </p> </div> <!-- Mermaid Graph --> <div class="chart-container" data-astro-cid-22cdqia5> <div${addAttribute(`mermaid-container-${workflow.id} bg-gray-50 rounded-lg p-4 border-2 border-gray-200`, "class")}${addAttribute(workflow.scale, "data-scale")} data-astro-cid-22cdqia5> <div${addAttribute(`mermaid mermaid-${workflow.id}`, "class")} data-astro-cid-22cdqia5> ${workflow.mermaidGraph} </div> </div> </div> </div>`)} </div> </div> <!-- Scroll hint --> <div class="text-center mt-8" data-astro-cid-22cdqia5> <p class="text-sm text-gray-500" data-en="← Scroll horizontally to explore more workflows →" data-zh="← 水平滚动以探索更多工作流 →" data-astro-cid-22cdqia5>
← Scroll horizontally to explore more workflows →
</p> </div> </div> </section> <!-- Mermaid Script -->  `;
}, "/Users/liyao/Code/mofa/mofa-website/src/components/WorkflowShowcase.astro", void 0);

var __freeze = Object.freeze;
var __defProp = Object.defineProperty;
var __template = (cooked, raw) => __freeze(__defProp(cooked, "raw", { value: __freeze(raw || cooked.slice()) }));
var _a;
const $$Index$3 = createComponent(($$result, $$props, $$slots) => {
  return renderTemplate(_a || (_a = __template(['<html lang="en" id="html-root" style="scroll-behavior: smooth;"> <head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title id="page-title">MoFA - Make Ordinary Developers Full-stack AI Engineers</title><!-- Favicon --><link rel="icon" type="image/png" href="/mofa/favicon-32x32.png"><link rel="shortcut icon" href="/mofa/favicon-32x32.png"><link rel="apple-touch-icon" href="/mofa/apple-touch-icon.png"><link rel="icon" type="image/png" sizes="16x16" href="/mofa/favicon-16x16.png"><link rel="icon" type="image/png" sizes="32x32" href="/mofa/favicon-32x32.png"><link rel="icon" type="image/png" sizes="48x48" href="/mofa/favicon-48x48.png"><meta name="theme-color" content="#6366F1">', `</head> <body> <header style="position: sticky; top: 0; background: white; border-bottom: 4px solid var(--mondrian-black); box-shadow: 0 2px 4px rgba(0,0,0,0.1); z-index: 50;"> <nav class="container" style="padding: 16px; display: flex; align-items: center; justify-content: space-between;"> <a href="https://mofa.ai" style="display: flex; align-items: center; gap: 8px; text-decoration: none;" target="_blank" rel="noopener noreferrer"> <img src="/mofa/mofa-logo.png" alt="MoFA Logo" style="width: 40px; height: 40px; border-radius: 8px; object-fit: cover;"> <span class="gradient-text" style="font-size: 1.5rem; font-weight: 700;">MoFA</span> </a> <div style="display: flex; align-items: center; gap: 32px;"> <a href="https://github.com/moxin-org/mofa/tree/main/Gosim_2024_Hackathon/documents" class="nav-link" target="_blank" rel="noopener noreferrer" data-en="Docs" data-zh="\u6587\u6863">Docs</a> <a href="https://demo.mofa.ai" class="nav-link" target="_blank" rel="noopener noreferrer" data-en="Examples" data-zh="\u793A\u4F8B">Examples</a> <a href="http://blog.mofa.ai/" class="nav-link" target="_blank" rel="noopener noreferrer" data-en="Blog" data-zh="\u535A\u5BA2">Blog</a> <!-- \u8BED\u8A00\u5207\u6362\u6309\u94AE --> <div style="display: flex; align-items: center; gap: 8px;"> <button id="lang-toggle" style="
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
</a> </div> </nav> </header> <!-- \u4E3B\u8981\u5185\u5BB9 --> <main style="flex: 1;"> <!-- Hero \u533A\u57DF --> <section class="py-20" style="position: relative; overflow: hidden;"> <!-- \u8499\u5FB7\u91CC\u5B89\u80CC\u666F --> <div style="position: absolute; inset: 0; opacity: 0.1;"> <div class="mondrian-grid" style="grid-template-columns: repeat(12, 1fr); grid-template-rows: repeat(8, 1fr); height: 100%;"> <div class="mondrian-block animate-grid-float" style="background-color: var(--mondrian-red); grid-column: span 3; grid-row: span 2;"></div> <div class="mondrian-block animate-grid-float" style="background-color: var(--mondrian-blue); grid-column: span 2; grid-row: span 3; animation-delay: 0.5s;"></div> <div class="mondrian-block animate-grid-float" style="background-color: var(--mondrian-yellow); grid-column: span 4; grid-row: span 2; animation-delay: 1s;"></div> <div class="mondrian-block" style="background-color: var(--mondrian-white); grid-column: span 3; grid-row: span 3;"></div> </div> </div> <div class="container" style="position: relative; z-index: 10;"> <div class="max-w-4xl mx-auto text-center"> <!-- Logo --> <div style="display: flex; justify-content: center; margin-bottom: 32px;"> <div style="width: 200px; height: 200px; transition: all 0.3s ease; position: relative; overflow: hidden; border-radius: 20px;" onmouseover="this.style.transform='scale(1.1)'; this.style.boxShadow='0 15px 40px rgba(0, 0, 0, 0.25)'" onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='none'"> <img src="/mofa/mofa-logo.png" alt="MoFA Logo" style="width: 100%; height: 100%; object-fit: cover; border-radius: 20px;"> <div style="position: absolute; inset: 0; background: linear-gradient(135deg, transparent 30%, rgba(255, 255, 255, 0.2) 50%, transparent 70%); opacity: 0; transition: opacity 0.3s ease;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0'"></div> </div> </div> <!-- \u526F\u6807\u9898 --> <p class="text-2xl font-medium mb-4" style="color: var(--mondrian-black);" data-en="Make Ordinary Developers Full-stack AI Engineers" data-zh="\u8BA9\u666E\u901A\u5F00\u53D1\u8005\u6210\u4E3A\u5168\u6808 AI \u5DE5\u7A0B\u5E08">
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
</a> </div> </div> </div> </section> <!-- \u5C0F\u578B\u5206\u9694\u7EBF --> <div class="mini-divider"> <div class="mini-line blue-line"></div> <div class="mini-line yellow-line"></div> <div class="mini-line red-line"></div> </div> <!-- \u65B0\u7684\u5DE5\u4F5C\u6D41\u5C55\u793A\u7EC4\u4EF6 --> `, ` <!-- \u5C0F\u578B\u5206\u9694\u7EBF --> <div class="mini-divider"> <div class="mini-line yellow-line"></div> <div class="mini-line red-line"></div> <div class="mini-line blue-line"></div> </div> <!-- Demo Video Section --> <section class="py-20" style="background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);"> <div class="container"> <div class="text-center mb-16"> <h2 class="text-4xl font-bold mb-4" data-en="See MoFA in <span class='gradient-text'>Action</span>" data-zh="\u89C2\u770B MoFA <span class='gradient-text'>\u5B9E\u6218\u6F14\u793A</span>">
See MoFA in <span class="gradient-text">Action</span> </h2> <p class="text-xl text-gray-600 max-w-2xl mx-auto" data-en="Watch how developers use MoFA to build sophisticated AI applications in minutes" data-zh="\u89C2\u770B\u5F00\u53D1\u8005\u5982\u4F55\u5728\u51E0\u5206\u949F\u5185\u4F7F\u7528 MoFA \u6784\u5EFA\u590D\u6742\u7684\u4EBA\u5DE5\u667A\u80FD\u5E94\u7528">Watch how developers use MoFA to build sophisticated AI applications in minutes</p> <!-- Video Embed --> <div class="video-container rounded-lg shadow-2xl overflow-hidden mx-auto" style="max-width: 800px; background-color: #2d3748;"> <iframe id="demo-video-iframe" width="100%" style="aspect-ratio: 16/9; display: block;" src="https://www.youtube.com/embed/YOUR_PLACEHOLDER_VIDEO_ID" title="MoFA in Action Demo Video" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen>
          </iframe> </div> </div> </div> <!-- \u5C0F\u578B\u5206\u9694\u7EBF --> <div class="mini-divider"> <div class="mini-line red-line"></div> <div class="mini-line blue-line"></div> <div class="mini-line yellow-line"></div> </div> </section></main> <footer style="background-color: var(--mondrian-black); color: white;"> <div class="container py-12"> <div class="text-center"> <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin-bottom: 16px;"> <img src="/mofa/mofa-logo.png" alt="MoFA Logo" style="width: 32px; height: 32px; border-radius: 6px; object-fit: cover;"> <span style="font-size: 1.25rem; font-weight: 700;">MoFA</span> </div> <p style="color: #9ca3af; margin-bottom: 8px;" data-en="Make Ordinary Developers Full-stack AI Engineers" data-zh="\u8BA9\u666E\u901A\u5F00\u53D1\u8005\u6210\u4E3A\u5168\u6808 AI \u5DE5\u7A0B\u5E08">
Make Ordinary Developers Full-stack AI Engineers
</p> <p style="color: #9ca3af; margin-bottom: 24px;" data-en="Modular Framework for AI Agents" data-zh="\u6A21\u5757\u5316 AI \u4EE3\u7406\u6846\u67B6">
Modular Framework for AI Agents
</p> <div style="display: flex; justify-content: center; gap: 32px; margin-bottom: 16px;"> <a href="https://github.com/moxin-org/mofa" target="_blank" rel="noopener noreferrer" style="color: #9ca3af; text-decoration: none; transition: color 0.2s ease;" onmouseover="this.style.color='white'" onmouseout="this.style.color='#9ca3af'">GitHub</a> <a href="https://discord.gg/mofa-ai" target="_blank" rel="noopener noreferrer" style="color: #9ca3af; text-decoration: none; transition: color 0.2s ease;" onmouseover="this.style.color='white'" onmouseout="this.style.color='#9ca3af'">Discord</a> <a href="https://github.com/moxin-org/mofa/tree/main/Gosim_2024_Hackathon/documents" target="_blank" rel="noopener noreferrer" style="color: #9ca3af; text-decoration: none; transition: color 0.2s ease;" onmouseover="this.style.color='white'" onmouseout="this.style.color='#9ca3af'" data-en="Docs" data-zh="\u6587\u6863">Docs</a> </div> <p style="color: #6b7280; font-size: 0.875rem;" data-en="\xA9 2025 MoFA. All rights reserved. | Made with \u2764\uFE0F by MoFA Team" data-zh="\xA9 2025 MoFA. \u4FDD\u7559\u6240\u6709\u6743\u5229. | Made with \u2764\uFE0F by MoFA Team">
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
  <\/script> </body> </html>`], ['<html lang="en" id="html-root" style="scroll-behavior: smooth;"> <head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title id="page-title">MoFA - Make Ordinary Developers Full-stack AI Engineers</title><!-- Favicon --><link rel="icon" type="image/png" href="/mofa/favicon-32x32.png"><link rel="shortcut icon" href="/mofa/favicon-32x32.png"><link rel="apple-touch-icon" href="/mofa/apple-touch-icon.png"><link rel="icon" type="image/png" sizes="16x16" href="/mofa/favicon-16x16.png"><link rel="icon" type="image/png" sizes="32x32" href="/mofa/favicon-32x32.png"><link rel="icon" type="image/png" sizes="48x48" href="/mofa/favicon-48x48.png"><meta name="theme-color" content="#6366F1">', `</head> <body> <header style="position: sticky; top: 0; background: white; border-bottom: 4px solid var(--mondrian-black); box-shadow: 0 2px 4px rgba(0,0,0,0.1); z-index: 50;"> <nav class="container" style="padding: 16px; display: flex; align-items: center; justify-content: space-between;"> <a href="https://mofa.ai" style="display: flex; align-items: center; gap: 8px; text-decoration: none;" target="_blank" rel="noopener noreferrer"> <img src="/mofa/mofa-logo.png" alt="MoFA Logo" style="width: 40px; height: 40px; border-radius: 8px; object-fit: cover;"> <span class="gradient-text" style="font-size: 1.5rem; font-weight: 700;">MoFA</span> </a> <div style="display: flex; align-items: center; gap: 32px;"> <a href="https://github.com/moxin-org/mofa/tree/main/Gosim_2024_Hackathon/documents" class="nav-link" target="_blank" rel="noopener noreferrer" data-en="Docs" data-zh="\u6587\u6863">Docs</a> <a href="https://demo.mofa.ai" class="nav-link" target="_blank" rel="noopener noreferrer" data-en="Examples" data-zh="\u793A\u4F8B">Examples</a> <a href="http://blog.mofa.ai/" class="nav-link" target="_blank" rel="noopener noreferrer" data-en="Blog" data-zh="\u535A\u5BA2">Blog</a> <!-- \u8BED\u8A00\u5207\u6362\u6309\u94AE --> <div style="display: flex; align-items: center; gap: 8px;"> <button id="lang-toggle" style="
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
</a> </div> </nav> </header> <!-- \u4E3B\u8981\u5185\u5BB9 --> <main style="flex: 1;"> <!-- Hero \u533A\u57DF --> <section class="py-20" style="position: relative; overflow: hidden;"> <!-- \u8499\u5FB7\u91CC\u5B89\u80CC\u666F --> <div style="position: absolute; inset: 0; opacity: 0.1;"> <div class="mondrian-grid" style="grid-template-columns: repeat(12, 1fr); grid-template-rows: repeat(8, 1fr); height: 100%;"> <div class="mondrian-block animate-grid-float" style="background-color: var(--mondrian-red); grid-column: span 3; grid-row: span 2;"></div> <div class="mondrian-block animate-grid-float" style="background-color: var(--mondrian-blue); grid-column: span 2; grid-row: span 3; animation-delay: 0.5s;"></div> <div class="mondrian-block animate-grid-float" style="background-color: var(--mondrian-yellow); grid-column: span 4; grid-row: span 2; animation-delay: 1s;"></div> <div class="mondrian-block" style="background-color: var(--mondrian-white); grid-column: span 3; grid-row: span 3;"></div> </div> </div> <div class="container" style="position: relative; z-index: 10;"> <div class="max-w-4xl mx-auto text-center"> <!-- Logo --> <div style="display: flex; justify-content: center; margin-bottom: 32px;"> <div style="width: 200px; height: 200px; transition: all 0.3s ease; position: relative; overflow: hidden; border-radius: 20px;" onmouseover="this.style.transform='scale(1.1)'; this.style.boxShadow='0 15px 40px rgba(0, 0, 0, 0.25)'" onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='none'"> <img src="/mofa/mofa-logo.png" alt="MoFA Logo" style="width: 100%; height: 100%; object-fit: cover; border-radius: 20px;"> <div style="position: absolute; inset: 0; background: linear-gradient(135deg, transparent 30%, rgba(255, 255, 255, 0.2) 50%, transparent 70%); opacity: 0; transition: opacity 0.3s ease;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0'"></div> </div> </div> <!-- \u526F\u6807\u9898 --> <p class="text-2xl font-medium mb-4" style="color: var(--mondrian-black);" data-en="Make Ordinary Developers Full-stack AI Engineers" data-zh="\u8BA9\u666E\u901A\u5F00\u53D1\u8005\u6210\u4E3A\u5168\u6808 AI \u5DE5\u7A0B\u5E08">
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
</a> </div> </div> </div> </section> <!-- \u5C0F\u578B\u5206\u9694\u7EBF --> <div class="mini-divider"> <div class="mini-line blue-line"></div> <div class="mini-line yellow-line"></div> <div class="mini-line red-line"></div> </div> <!-- \u65B0\u7684\u5DE5\u4F5C\u6D41\u5C55\u793A\u7EC4\u4EF6 --> `, ` <!-- \u5C0F\u578B\u5206\u9694\u7EBF --> <div class="mini-divider"> <div class="mini-line yellow-line"></div> <div class="mini-line red-line"></div> <div class="mini-line blue-line"></div> </div> <!-- Demo Video Section --> <section class="py-20" style="background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);"> <div class="container"> <div class="text-center mb-16"> <h2 class="text-4xl font-bold mb-4" data-en="See MoFA in <span class='gradient-text'>Action</span>" data-zh="\u89C2\u770B MoFA <span class='gradient-text'>\u5B9E\u6218\u6F14\u793A</span>">
See MoFA in <span class="gradient-text">Action</span> </h2> <p class="text-xl text-gray-600 max-w-2xl mx-auto" data-en="Watch how developers use MoFA to build sophisticated AI applications in minutes" data-zh="\u89C2\u770B\u5F00\u53D1\u8005\u5982\u4F55\u5728\u51E0\u5206\u949F\u5185\u4F7F\u7528 MoFA \u6784\u5EFA\u590D\u6742\u7684\u4EBA\u5DE5\u667A\u80FD\u5E94\u7528">Watch how developers use MoFA to build sophisticated AI applications in minutes</p> <!-- Video Embed --> <div class="video-container rounded-lg shadow-2xl overflow-hidden mx-auto" style="max-width: 800px; background-color: #2d3748;"> <iframe id="demo-video-iframe" width="100%" style="aspect-ratio: 16/9; display: block;" src="https://www.youtube.com/embed/YOUR_PLACEHOLDER_VIDEO_ID" title="MoFA in Action Demo Video" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen>
          </iframe> </div> </div> </div> <!-- \u5C0F\u578B\u5206\u9694\u7EBF --> <div class="mini-divider"> <div class="mini-line red-line"></div> <div class="mini-line blue-line"></div> <div class="mini-line yellow-line"></div> </div> </section></main> <footer style="background-color: var(--mondrian-black); color: white;"> <div class="container py-12"> <div class="text-center"> <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin-bottom: 16px;"> <img src="/mofa/mofa-logo.png" alt="MoFA Logo" style="width: 32px; height: 32px; border-radius: 6px; object-fit: cover;"> <span style="font-size: 1.25rem; font-weight: 700;">MoFA</span> </div> <p style="color: #9ca3af; margin-bottom: 8px;" data-en="Make Ordinary Developers Full-stack AI Engineers" data-zh="\u8BA9\u666E\u901A\u5F00\u53D1\u8005\u6210\u4E3A\u5168\u6808 AI \u5DE5\u7A0B\u5E08">
Make Ordinary Developers Full-stack AI Engineers
</p> <p style="color: #9ca3af; margin-bottom: 24px;" data-en="Modular Framework for AI Agents" data-zh="\u6A21\u5757\u5316 AI \u4EE3\u7406\u6846\u67B6">
Modular Framework for AI Agents
</p> <div style="display: flex; justify-content: center; gap: 32px; margin-bottom: 16px;"> <a href="https://github.com/moxin-org/mofa" target="_blank" rel="noopener noreferrer" style="color: #9ca3af; text-decoration: none; transition: color 0.2s ease;" onmouseover="this.style.color='white'" onmouseout="this.style.color='#9ca3af'">GitHub</a> <a href="https://discord.gg/mofa-ai" target="_blank" rel="noopener noreferrer" style="color: #9ca3af; text-decoration: none; transition: color 0.2s ease;" onmouseover="this.style.color='white'" onmouseout="this.style.color='#9ca3af'">Discord</a> <a href="https://github.com/moxin-org/mofa/tree/main/Gosim_2024_Hackathon/documents" target="_blank" rel="noopener noreferrer" style="color: #9ca3af; text-decoration: none; transition: color 0.2s ease;" onmouseover="this.style.color='white'" onmouseout="this.style.color='#9ca3af'" data-en="Docs" data-zh="\u6587\u6863">Docs</a> </div> <p style="color: #6b7280; font-size: 0.875rem;" data-en="\xA9 2025 MoFA. All rights reserved. | Made with \u2764\uFE0F by MoFA Team" data-zh="\xA9 2025 MoFA. \u4FDD\u7559\u6240\u6709\u6743\u5229. | Made with \u2764\uFE0F by MoFA Team">
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
  <\/script> </body> </html>`])), renderHead(), renderComponent($$result, "WorkflowShowcase", $$WorkflowShowcase, {}));
}, "/Users/liyao/Code/mofa/mofa-website/src/pages/index.astro", void 0);

const $$file$3 = "/Users/liyao/Code/mofa/mofa-website/src/pages/index.astro";
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
}, "/Users/liyao/Code/mofa/mofa-website/src/pages/examples/index.astro", void 0);

const $$file$2 = "/Users/liyao/Code/mofa/mofa-website/src/pages/examples/index.astro";
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
<svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"> <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path> </svg> </a> </div> </div> </article>`)} </div> <!-- Empty state --> ${sortedPosts.length === 0 && renderTemplate`<div class="text-center py-16"> <div class="w-24 h-24 mx-auto mb-6 opacity-50 rounded-lg overflow-hidden"> <img${addAttribute(`${base}/mofa-logo.png`, "src")} alt="MoFA Logo" class="w-full h-full object-cover rounded-lg"> </div> <h2 class="text-2xl font-semibold text-gray-700 mb-2">敬请期待</h2> <p class="text-gray-600">我们正在准备更多精彩内容</p> </div>`} </div> ` })}`;
}, "/Users/liyao/Code/mofa/mofa-website/src/pages/blog/index.astro", void 0);

const $$file$1 = "/Users/liyao/Code/mofa/mofa-website/src/pages/blog/index.astro";
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
}, "/Users/liyao/Code/mofa/mofa-website/src/pages/docs/index.astro", void 0);

const $$file = "/Users/liyao/Code/mofa/mofa-website/src/pages/docs/index.astro";
const $$url = "/mofa/docs";

const index = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Index,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

export { index$2 as a, index$1 as b, index as c, index$3 as i };
