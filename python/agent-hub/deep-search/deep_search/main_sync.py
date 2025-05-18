import json
import asyncio
import hashlib
import os
import time
import uuid
from typing import AsyncGenerator, List, Dict, Optional
from mofa.agent_build.base.base_agent import MofaAgent, run_agent

import openai
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

from mofa.kernel.tools.web_search import search_web_with_serper

# 模拟 serper 搜索接口（请替换为真实实现）
# def search_web_with_serper(query: str, subscription_key: str) -> List[Dict]:
#     return [{'name': 'DeepSeek',
#   'url': 'https://www.deepseek.com/',
#   'snippet': "DeepSeek-R1 is now live and open source, rivaling OpenAI's Model o1. Available on web, app, and API. Click for details. Into ..."},
#  {'name': 'DeepSeek AI',
#   'url': 'https://deepseek.ai/',
#   'snippet': 'DeepSeek AI is the leading provider of advanced AI language models and enterprise solutions. Experience state-of-the-art artificial intelligence technology ...'},
#  {'name': 'DeepSeek rushes to launch new AI model as China goes all in',
#   'url': 'https://www.reuters.com/technology/artificial-intelligence/deepseek-rushes-launch-new-ai-model-china-goes-all-2025-02-25/',
#   'snippet': "DeepSeek is looking to press home its advantage. The Hangzhou-based firm is accelerating the launch of the successor to January's R1 model."},
#  {'name': 'DeepSeek: The Chinese AI app that has the world talking - BBC',
#   'url': 'https://www.bbc.com/news/articles/c5yv5976z9po',
#   'snippet': "DeepSeek is the name of a free AI-powered chatbot, which looks, feels and works very much like ChatGPT. That means it's used for many of ..."},
#  {'name': 'DeepSeek - AI Assistant - Apps on Google Play',
#   'url': 'https://play.google.com/store/apps/details?id=com.deepseek.chat&hl=en_US',
#   'snippet': "Experience seamless interaction with DeepSeek's official AI assistant for free! Powered by the groundbreaking DeepSeek-V3 model with over ..."},
#  {'name': 'deepseek-ai/DeepSeek-V3 - GitHub',
#   'url': 'https://github.com/deepseek-ai/DeepSeek-V3',
#   'snippet': 'We present DeepSeek-V3, a strong Mixture-of-Experts (MoE) language model with 671B total parameters with 37B activated for each token.'},
#  {'name': 'Wiz Research Uncovers Exposed DeepSeek Database Leaking ...',
#   'url': 'https://www.wiz.io/blog/wiz-research-uncovers-exposed-deepseek-database-leak',
#   'snippet': 'Wiz Research has identified a publicly accessible ClickHouse database belonging to DeepSeek, which allows full control over database operations, ...'},
#  {'name': 'Deepseek R2 Is About To Change That AI Industry ... - YouTube',
#   'url': 'https://www.youtube.com/watch?v=T9_t7ZwFddw',
#   'snippet': 'Comments233. Something Nothing. I hope deepseek v2 will slap some sense into modern ai companys.'},
#  {'name': 'DeepSeek - X',
#   'url': 'https://x.com/deepseek_ai/status/1895688300574462431',
#   'snippet': 'Day 6 of #OpenSourceWeek: One More Thing – DeepSeek-V3/R1 Inference System Overview Optimized throughput and latency via: Cross-node ...'},
#  {'name': 'What is DeepSeek and why is it disrupting the AI sector? | Reuters',
#   'url': 'https://www.reuters.com/technology/artificial-intelligence/what-is-deepseek-why-is-it-disrupting-ai-sector-2025-01-27/',
#   'snippet': 'Chinese startup DeepSeek is threatening to upset the technology world order.'},
#  {'name': 'DeepSeek-V3 Technical Report - arXiv',
#   'url': 'https://arxiv.org/html/2412.19437v1?ref=platformer.news',
#   'snippet': 'Comprehensive evaluations reveal that DeepSeek-V3 outperforms other open-source models and achieves performance comparable to leading closed-source models.'},
#  {'name': 'DeepSeek | Deep Seek Ai Free Chat Online',
#   'url': 'https://deep-seek.chat/',
#   'snippet': 'DeepSeek is an advanced artificial intelligence (AI) platform developed by a leading Chinese AI company. It serves as both a robust AI chatbot and a highly ...'},
#  {'name': 'deepseek-ai (DeepSeek) - Hugging Face',
#   'url': 'https://huggingface.co/deepseek-ai',
#   'snippet': 'DeepSeek (深度求索), founded in 2023, is a Chinese company dedicated to making AGI a reality. Unravel the mystery of AGI with curiosity.'},
#  {'name': 'DeepSeek on X',
#   'url': 'https://x.com/deepseek_ai/status/1895279409185390655',
#   'snippet': 'Day 5 of #OpenSourceWeek: 3FS, Thruster for All DeepSeek Data Access Fire-Flyer File System (3FS) - a parallel file system that utilizes the ...'},
#  {'name': 'DeepSeek R1 is now available on Azure AI Foundry and GitHub',
#   'url': 'https://azure.microsoft.com/en-us/blog/deepseek-r1-is-now-available-on-azure-ai-foundry-and-github/',
#   'snippet': 'DeepSeek R1 is now available in the model catalog on Azure AI Foundry and GitHub, joining a diverse portfolio of over 1,800 models, ...'},
#  {'name': 'DeepSeek shows power of V3, R1 models with theoretical 545 ...',
#   'url': 'https://www.scmp.com/tech/big-tech/article/3300734/deepseek-shows-power-v3-r1-models-theoretical-545-profit-margin',
#   'snippet': 'DeepSeek bills users based on the total input and output tokens processed by its models. DeepSeek, based in Hangzhou in eastern Zhejiang ...'},
#  {'name': 'Bipartisan congressional duo encourages governors to ban ...',
#   'url': 'https://www.nbcnews.com/politics/congress/bipartisan-congressional-duo-encourages-governors-ban-deepseek-rcna194295',
#   'snippet': 'First to NBC News: Reps. Josh Gottheimer and Darin LaHood introduced legislation to ban the app on federal government devices. DeepSeek App.'}]

load_dotenv('.env.secret')
# 配置项
MAX_ARTICLES = 50  # 最大处理文章数
DEFAULT_STREAM_DELAY = 0.1  # 流式延迟
openai.api_key = os.getenv("LLM_API_KEY")
openai.api_base = os.getenv("LLM_BASE_URL")
DEFAULT_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "gpt-4o")


class LLMClient:
    """封装 OpenAI LLM 的客户端，缓存模型名称及相关配置"""

    def __init__(self,file_path:str='.env.secret', model_name: str = 'gpt-4o'):
        self.model_name = model_name
        load_dotenv('.env.secret')
        if os.getenv('LLM_API_KEY') is not None:
            os.environ['OPENAI_API_KEY'] = os.getenv('LLM_API_KEY')
        if os.getenv('LLM_BASE_URL', None) is None:
            client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        else:
            client = OpenAI(api_key=os.environ['OPENAI_API_KEY'], base_url=os.getenv('LLM_BASE_URL'), )
        self.client = client

    async def generate_response(self, messages: List[Dict], max_tokens: int=3200) -> str:
        def sync_call():
            return self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=max_tokens
            )

        response = await asyncio.to_thread(sync_call)
        return response.choices[0].message.content


# --- 数据模型 ---
class ArticleRef:
    def __init__(self, title: str, url: str, snippet: str, source: str, relevance: float = 1.0):
        self.title = title
        self.url = url
        self.snippet = snippet
        self.source = source
        self.relevance = relevance

    def dict(self) -> dict:
        return {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
            "source": self.source,
            "relevance": self.relevance
        }


class ChatRequest:
    def __init__(self, messages: List[Dict], model: str = "deepseek-r1", search_query: Optional[str] = None,
                 max_articles: int = 20, stream: bool = True):
        self.messages = messages
        self.model = model
        self.search_query = search_query
        self.max_articles = max_articles
        self.stream = stream


# --- 简化版文章处理器 ---
class ArticleProcessor:
    """
    简化版文章处理器：
    1. 将 serper 返回的结果转换为 ArticleRef 对象
    2. 基于 URL 去重
    3. 根据 snippet 长度降序排序
    """

    def __init__(self, serper_results: List[Dict]):
        self.articles = [
            ArticleRef(
                title=article.get("name", ""),
                url=article.get("url", ""),
                snippet=article.get("snippet", ""),
                source=article.get("name", ""),
                relevance=len(article.get("snippet", ""))
            )
            for article in serper_results
        ]

    async def process(self) -> List[ArticleRef]:
        unique = self._remove_duplicates(self.articles)
        filtered = self._filter_quality(unique)
        return filtered

    def _remove_duplicates(self, articles: List[ArticleRef]) -> List[ArticleRef]:
        seen_urls = set()
        unique_articles = []
        for article in articles:
            if article.url not in seen_urls:
                seen_urls.add(article.url)
                unique_articles.append(article)
        return unique_articles

    def _filter_quality(self, articles: List[ArticleRef]) -> List[ArticleRef]:
        return sorted(articles, key=lambda a: a.relevance, reverse=True)


# --- 研究生成器（整合 OpenAI LLM 思考） ---
class ResearchGenerator:
    """研究生成器，使用 LLMClient 根据文章和思考阶段生成输出"""

    def __init__(self, articles: List[ArticleRef], llm_client: Optional[LLMClient] = None, max_output: int = 20):
        self.articles = articles
        self.max_output = max_output
        self.used_articles = set()
        self.llm_client = llm_client or LLMClient()
        self.thinking_stages = [
            {
                "name": "context_extraction",
                "description": "📝 Extract key context from the articles by isolating the most informative snippets. This establishes a strong foundation for subsequent analysis.",
                "article_selector": lambda articles: articles[:min(3, len(articles))]
            },
            {
                "name": "intent_analysis",
                "description": "🔍 Analyze the core user intent by examining the extracted context and inferring the underlying question and focus areas.",
                "article_selector": lambda articles: articles[:min(3, len(articles))]
            },
            {
                "name": "source_eval",
                "description": "📊 Evaluate source credibility by ranking articles based on trustworthiness and content quality. This step helps to filter out less reliable information.",
                "article_selector": lambda articles: self._select_by_metric(articles, 'source')
            },
            {
                "name": "contradiction_check",
                "description": "⚠️ Check for information consistency by cross-referencing details among the selected articles to identify discrepancies.",
                "article_selector": lambda articles: articles[::max(1, len(articles) // 3)]
            },
            {
                "name": "synthesis",
                "description": "🧠 Synthesize insights by integrating the validated information and constructing a coherent summary that answers the user's query.",
                "article_selector": lambda articles: articles
            }
        ]

    def _select_by_metric(self, articles: List[ArticleRef], metric: str) -> List[ArticleRef]:
        if metric == 'source':
            preferred_sources = ["journal", "report", "web"]
            filtered = [a for a in articles if a.source.lower() in preferred_sources]
            filtered.sort(key=lambda a: (preferred_sources.index(a.source.lower()), -a.relevance))
            return filtered
        return articles

    async def _llm_think(self, stage_description: str, selected_articles: List[ArticleRef]) -> str:
        """
        使用 LLMClient 生成思考输出。
        """
        context = " ".join([a.snippet for a in selected_articles])
        messages = [
            {"role": "system", "content": stage_description},
            {"role": "user", "content": f"Analyze the following context and provide your insights: {context}"}
        ]
        return await self.llm_client.generate_response(messages, max_tokens=100)

    async def _llm_generate_content(self, prompt: str, related_articles: List[ArticleRef]) -> str:
        """
        使用 LLMClient 生成内容输出。
        """
        context = " ".join([a.snippet for a in related_articles])
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Generate a comprehensive answer based on the following context: {context}"}
        ]
        return await self.llm_client.generate_response(messages, max_tokens=4800)

    async def generate_stream(self) -> AsyncGenerator[Dict, None]:
        # 生成各个思考阶段的输出
        for stage in self.thinking_stages:
            selected = stage["article_selector"](self.articles)
            context_articles = selected[:min(3, len(selected))]
            # 更新已使用的文章（用 URL 作为唯一标识）
            for article in context_articles:
                self.used_articles.add(article.url)
            llm_output = await self._llm_think(stage["description"], context_articles)
            await asyncio.sleep(DEFAULT_STREAM_DELAY)
            yield {
                "type": "thinking",
                "content": llm_output,
                "articles": [a.dict() for a in context_articles],
                "metadata": {"stage": stage["name"]}
            }

        # 动态生成内容阶段，根据文章数量分块处理
        phase_prompts = [
            "Current research indicates...", # 目前的研究表明……
            "Key findings include...", # 主要发现包括...
            "However, some studies suggest...", # 然而，一些研究表明……
            "In conclusion..." # 综上所述...
        ]
        num_articles = len(self.articles)
        num_phases = len(phase_prompts)
        chunk_size = max(1, num_articles // num_phases)
        content_outputs = []  # 用于收集各阶段生成的内容

        for i, prompt in enumerate(phase_prompts):
            start = i * chunk_size
            end = (i + 1) * chunk_size if i < num_phases - 1 else num_articles
            related = self.articles[start:end]
            for article in related:
                self.used_articles.add(article.url)
            llm_content = await self._llm_generate_content(prompt, related)
            content_outputs.append(llm_content)
            await asyncio.sleep(DEFAULT_STREAM_DELAY)
            yield {
                "type": "content",
                "content": llm_content,
                "articles": [a.dict() for a in related],
                "metadata": {"confidence": np.random.uniform(0.7, 0.95)}
            }

        # 最后进行最终综合：调用 LLM 对所有内容输出做总结
        final_context = "\n".join(content_outputs)
        final_prompt = (
            "Context: The aggregated content below contains insights gathered from multiple analysis stages—namely, context extraction, intent analysis, "
            "source evaluation, contradiction check, and preliminary synthesis—pertaining to the subject under investigation.\n\n"
            "Objective: Generate a comprehensive final synthesis that integrates all key insights from the provided content.\n\n"
            "Strategy:\n"
            "  - Carefully review the aggregated content below.\n"
            "  - Identify and recap the main points from each analysis stage.\n"
            "  - Produce a detailed, structured summary using bullet points or numbered sections for clarity.\n\n"
            "Tactics:\n"
            "  1. Recap the extracted context and highlight the core user intent regarding the topic.\n"
            "  2. Evaluate the credibility and reliability of the sources mentioned.\n"
            "  3. Summarize any contradictions or discrepancies identified and explain how they were addressed.\n"
            "  4. Synthesize all the information into a coherent overview that emphasizes the key findings, technological innovations, "
            "and overall value proposition of the subject matter.\n\n"
            "Audience: The final synthesis should be detailed, clear, and suitable for industry professionals and researchers seeking an in-depth analysis.\n\n"
            "Action: Based on the aggregated content provided below, generate a final, structured synthesis that covers all the critical insights and details.\n\n"
            "Aggregated Content:\n"
            f"{final_context}\n\n"
            "Please produce a final synthesis that is comprehensive and covers all the important points from the analysis."
        )
        final_synthesis = await self._llm_generate_content(final_prompt, self.articles)
        await asyncio.sleep(DEFAULT_STREAM_DELAY)
        yield {
            "type": "completion",
            "content": final_synthesis,
            "metadata": {
                "used_sources": len(self.used_articles),
                "article_ids": list(self.used_articles)
            }
        }

async def run(agent:MofaAgent):
    # 模拟用户查询
    user_query = agent.receive_parameter('task')
    raw_articles = search_web_with_serper(query=user_query, subscription_key=os.getenv("SERPER_API_KEY"))
    print("Serper search returned:")
    print(json.dumps(raw_articles, indent=2))

    # 使用 ArticleProcessor 处理搜索结果
    processor = ArticleProcessor(raw_articles)
    processed_articles = await processor.process()
    selected_articles = processed_articles[:20]

    # 初始化 LLMClient（使用 .env 中配置的模型名称）
    llm_client = LLMClient(model_name=os.getenv("LLM_MODEL_NAME", DEFAULT_MODEL_NAME))

    # 使用 ResearchGenerator 生成输出
    generator = ResearchGenerator(articles=selected_articles, llm_client=llm_client)

    print("\n--- Generating output ---\n")
    async for chunk in generator.generate_stream():
        print(json.dumps(chunk, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
