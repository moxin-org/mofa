import json
import random
import time
import os
import uuid
from typing import List, Dict, Optional
import openai
import numpy as np
from dotenv import load_dotenv
from playwright.sync_api import expect

from mofa.agent_build.base.base_agent import MofaAgent, run_agent
from mofa.kernel.tools.web_search import search_web_with_serper
from openai import OpenAI

# 加载环境变量
load_dotenv('.env.secret')
openai.api_key = os.getenv("LLM_API_KEY")
openai.api_base = os.getenv("LLM_BASE_URL")
DEFAULT_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "gpt-4o")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# 配置项
MAX_ARTICLES = 50  # 最大处理文章数
DEFAULT_STREAM_DELAY = 0.1  # 流式延迟


class LLMClient:
    def __init__(self, file_path: str = '.env.secret', model_name: str = 'gpt-4o'):
        self.model_name = model_name
        load_dotenv('.env.secret')
        if os.getenv('LLM_API_KEY') is not None:
            os.environ['OPENAI_API_KEY'] = os.getenv('LLM_API_KEY')
        if os.getenv('LLM_BASE_URL', None) is None:
            client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        else:
            client = OpenAI(api_key=os.environ['OPENAI_API_KEY'], base_url=os.getenv('LLM_BASE_URL'))
        self.client = client

    def generate_response(self, messages: List[Dict], max_tokens: int = 3200, stream: bool = True):
        """
        使用流式方式生成响应
        """
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            max_tokens=max_tokens,
            stream=stream  # 开启流式响应
        )

        for chunk in response:
            # 每个 chunk 包含一部分内容
            yield chunk['choices'][0]['delta'].get('content', '')  # 返回每个部分的内容


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

    def process(self) -> List[ArticleRef]:
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


class ResearchGenerator:
    """研究生成器，使用 LLMClient 根据文章和思考阶段生成输出（流式版本）"""

    def __init__(self, articles: List[ArticleRef], llm_client: Optional[LLMClient] = None, max_output: int = 20):
        self.articles = articles
        self.max_output = max_output
        self.used_articles = set()
        self.llm_client = llm_client or LLMClient()
        self.thinking_stages = [
            {
                "name": "context_extraction",
                "description": "📝 Extract key context from the articles by isolating the most informative snippets.",
                "article_selector": lambda articles: articles[:min(3, len(articles))]
            },
            {
                "name": "intent_analysis",
                "description": "🔍 Analyze the core user intent by examining the extracted context.",
                "article_selector": lambda articles: articles[:min(3, len(articles))]
            },
            {
                "name": "source_eval",
                "description": "📊 Evaluate source credibility by ranking articles based on trustworthiness.",
                "article_selector": lambda articles: self._select_by_metric(articles, 'source')
            },
            {
                "name": "contradiction_check",
                "description": "⚠️ Check for information consistency by cross-referencing articles.",
                "article_selector": lambda articles: articles[::max(1, len(articles) // 3)]
            },
            {
                "name": "synthesis",
                "description": "🧠 Synthesize insights by integrating the validated information.",
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

    def _llm_think(self, stage_description: str, selected_articles: List[ArticleRef]):
        context = " ".join([a.snippet for a in selected_articles])
        messages = [
            {"role": "system", "content": stage_description},
            {"role": "user", "content": f"Analyze the following context: {context}"}
        ]

        stream_output = ''
        for chunk in self.llm_client.generate_response(messages, max_tokens=1000):
            stream_output += chunk
            yield {
                "type": "thinking",
                "content": stream_output,
                "articles": [a.dict() for a in selected_articles],
                "metadata": {"stage": "context_extraction"}
            }

    def _llm_generate_content(self, prompt: str, related_articles: List[ArticleRef]):
        context = " ".join([a.snippet for a in related_articles])
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Generate content based on the context: {context}"}
        ]

        stream_output = ''
        for chunk in self.llm_client.generate_response(messages, max_tokens=3860):
            stream_output += chunk
            yield {
                "type": "content",
                "content": stream_output,
                "articles": [a.dict() for a in related_articles],
                "metadata": {"confidence": float(np.random.uniform(0.7, 0.95))}
            }

    def generate_stream(self):
        content_outputs = []  # 用于收集各阶段生成的内容

        # 生成各个思考阶段的输出（同步方式）
        for stage in self.thinking_stages:
            selected = stage["article_selector"](self.articles)
            context_articles = selected[:min(3, len(selected))]
            for article in context_articles:
                self.used_articles.add(article.url)
            yield from self._llm_think(stage["description"], context_articles)

        # 动态生成内容阶段，根据文章数量分块处理
        phase_prompts = [
            "Current research indicates...",
            "Key findings include...",
            "Some studies suggest...",
            "In conclusion..."
        ]
        num_articles = len(self.articles)
        chunk_size = max(1, num_articles // len(phase_prompts))
        for i, prompt in enumerate(phase_prompts):
            start = i * chunk_size
            end = (i + 1) * chunk_size if i < len(phase_prompts) - 1 else num_articles
            related = self.articles[start:end]
            for article in related:
                self.used_articles.add(article.url)
            llm_content = ''
            for chunk in self._llm_generate_content(prompt, related):
                llm_content += chunk
            content_outputs.append(llm_content)
            time.sleep(DEFAULT_STREAM_DELAY)
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
                "Aggregated Content:\n" + final_context + "\n\nFinal Synthesis:"
        )
        final_synthesis = self._llm_generate_content(final_prompt, self.articles)
        yield from final_synthesis


user_query = "deepseek "
load_dotenv('.env.secret')
print('user_query:', user_query)

raw_articles = search_web_with_serper(query=user_query, subscription_key=os.getenv("SERPER_API_KEY"))
print("Serper search returned:")
print(json.dumps(raw_articles, indent=2))

processor = ArticleProcessor(raw_articles)
processed_articles = processor.process()  # 同步调用
selected_articles = processed_articles[:20]

llm_client = LLMClient(model_name=os.getenv("LLM_MODEL_NAME", DEFAULT_MODEL_NAME))

generator = ResearchGenerator(articles=selected_articles, llm_client=llm_client)

print("\n--- Generating output ---\n")
results = []
for chunk in generator.generate_stream():
    print('chunk : ', json.dumps(chunk, indent=2))
    results.append(json.dumps(chunk, indent=2))
