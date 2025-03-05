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

    def generate_response(self, messages: List[Dict], max_tokens: int = 3200) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content

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

##############################################
# 简化版 ArticleProcessor（同步版）
##############################################
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

##############################################
# 同步版 ResearchGenerator
##############################################
class ResearchGenerator:
    """研究生成器，使用 LLMClient 根据文章和思考阶段生成输出（同步版本）"""

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

    def _llm_think(self, stage_description: str, selected_articles: List[ArticleRef]) -> str:
        context = " ".join([a.snippet for a in selected_articles])
        messages = [
            {"role": "system", "content": stage_description},
            {"role": "user", "content": f"Analyze the following context and provide detailed insights: {context}"}
        ]
        return self.llm_client.generate_response(messages, max_tokens=100)

    def _llm_generate_content(self, prompt: str, related_articles: List[ArticleRef]) -> str:
        context = " ".join([a.snippet for a in related_articles])
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Generate a comprehensive answer based on the following context: {context}"}
        ]
        return self.llm_client.generate_response(messages, max_tokens=4800)

    def generate_stream(self):
        content_outputs = []
        # 生成各个思考阶段的输出（同步方式）
        for stage in self.thinking_stages:
            selected = stage["article_selector"](self.articles)
            context_articles = selected[:min(3, len(selected))]
            for article in context_articles:
                self.used_articles.add(article.url)
            llm_output = self._llm_think(stage["description"], context_articles)
            time.sleep(DEFAULT_STREAM_DELAY)
            yield {
                "type": "thinking",
                "content": llm_output,
                "articles": [a.dict() for a in context_articles],
                "metadata": {"stage": stage["name"]}
            }
        # 动态生成内容阶段，根据文章数量分块处理
        phase_prompts = [
            "Current research indicates...",
            "Key findings include...",
            "However, some studies suggest...",
            "In conclusion..."
        ]
        num_articles = len(self.articles)
        num_phases = len(phase_prompts)
        chunk_size = max(1, num_articles // num_phases)
        for i, prompt in enumerate(phase_prompts):
            start = i * chunk_size
            end = (i + 1) * chunk_size if i < num_phases - 1 else num_articles
            related = self.articles[start:end]
            for article in related:
                self.used_articles.add(article.url)
            llm_content = self._llm_generate_content(prompt, related)
            content_outputs.append(llm_content)
            time.sleep(DEFAULT_STREAM_DELAY)
            yield {
                "type": "content",
                "content": llm_content,
                "articles": [a.dict() for a in related],
                "metadata": {"confidence": float(np.random.uniform(0.7, 0.95))}
            }
        # 最终综合阶段：结合之前所有内容生成最终总结
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
        time.sleep(DEFAULT_STREAM_DELAY)
        yield {
            "type": "completion",
            "content": final_synthesis,
            "metadata": {
                "used_sources": len(self.used_articles),
                "article_ids": list(self.used_articles)
            }
        }

@run_agent
def run(agent: MofaAgent):
    user_query = agent.receive_parameter('user_query')
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
    # results = ['{\n  "type": "thinking",\n  "content": "Here\\u2019s a detailed analysis of the provided context, focusing on key insights and implications:\\n\\n### 1. **Company Overview**\\n   - **DeepSeek AI** is a prominent Chinese artificial intelligence company specializing in the development of **large language models (LLMs)**. \\n   - It is headquartered in **Hangzhou, Zhejiang**, a region known for its tech innovation and proximity to major Chinese tech hubs like Shanghai.\\n   - The company is **owned and funded by a Chinese hedge",\n  "articles": [\n    {\n      "title": "DeepSeek - Wikipedia",\n      "url": "https://en.wikipedia.org/wiki/DeepSeek",\n      "snippet": "a Chinese artificial intelligence company that develops large language models (LLMs). Based in Hangzhou, Zhejiang, it is owned and funded by the Chinese hedge ...",\n      "source": "DeepSeek - Wikipedia",\n      "relevance": 162\n    },\n    {\n      "title": "DeepSeek AI",\n      "url": "https://deepseek.ai/",\n      "snippet": "DeepSeek AI is the leading provider of advanced AI language models and enterprise solutions. Experience state-of-the-art artificial intelligence technology ...",\n      "source": "DeepSeek AI",\n      "relevance": 159\n    },\n    {\n      "title": "DeepSeek - GitHub",\n      "url": "https://github.com/deepseek-ai",\n      "snippet": "A high-performance distributed file system designed to address the challenges of AI training and inference workloads. deepseek-ai/3FS\'s past year of commit ...",\n      "source": "DeepSeek - GitHub",\n      "relevance": 159\n    }\n  ],\n  "metadata": {\n    "stage": "context_extraction"\n  }\n}', '{\n  "type": "thinking",\n  "content": "### Core User Intent:\\nThe user is seeking detailed insights into a Chinese AI company, **DeepSeek AI**, which specializes in developing large language models (LLMs) and enterprise AI solutions. The focus areas include the company\'s background, technological advancements, and its contributions to AI training and inference workloads.\\n\\n### Underlying Questions:\\n1. **What is DeepSeek AI, and what is its core focus?**\\n2. **Where is DeepSeek AI based, and who owns/funds",\n  "articles": [\n    {\n      "title": "DeepSeek - Wikipedia",\n      "url": "https://en.wikipedia.org/wiki/DeepSeek",\n      "snippet": "a Chinese artificial intelligence company that develops large language models (LLMs). Based in Hangzhou, Zhejiang, it is owned and funded by the Chinese hedge ...",\n      "source": "DeepSeek - Wikipedia",\n      "relevance": 162\n    },\n    {\n      "title": "DeepSeek AI",\n      "url": "https://deepseek.ai/",\n      "snippet": "DeepSeek AI is the leading provider of advanced AI language models and enterprise solutions. Experience state-of-the-art artificial intelligence technology ...",\n      "source": "DeepSeek AI",\n      "relevance": 159\n    },\n    {\n      "title": "DeepSeek - GitHub",\n      "url": "https://github.com/deepseek-ai",\n      "snippet": "A high-performance distributed file system designed to address the challenges of AI training and inference workloads. deepseek-ai/3FS\'s past year of commit ...",\n      "source": "DeepSeek - GitHub",\n      "relevance": 159\n    }\n  ],\n  "metadata": {\n    "stage": "intent_analysis"\n  }\n}', '{\n  "type": "thinking",\n  "content": "Sure! Please provide the context or the articles you\'d like me to analyze, and I\\u2019ll evaluate their credibility, trustworthiness, and content quality. This will include assessing the source, author expertise, evidence provided, objectivity, and overall reliability. Let\\u2019s get started!",\n  "articles": [],\n  "metadata": {\n    "stage": "source_eval"\n  }\n}', '{\n  "type": "thinking",\n  "content": "Here\\u2019s a detailed analysis of the provided context:\\n\\n### Key Insights:\\n\\n1. **Company Overview**:\\n   - The company is a Chinese AI firm specializing in the development of large language models (LLMs).\\n   - It is based in Hangzhou, Zhejiang Province, a major hub for technology and innovation in China.\\n   - The company is owned and funded by a Chinese hedge fund, which suggests strong financial backing and potential alignment with strategic interests in AI development.\\n\\n2. **Technological",\n  "articles": [\n    {\n      "title": "DeepSeek - Wikipedia",\n      "url": "https://en.wikipedia.org/wiki/DeepSeek",\n      "snippet": "a Chinese artificial intelligence company that develops large language models (LLMs). Based in Hangzhou, Zhejiang, it is owned and funded by the Chinese hedge ...",\n      "source": "DeepSeek - Wikipedia",\n      "relevance": 162\n    },\n    {\n      "title": "DeepSeek - GitHub",\n      "url": "https://github.com/deepseek-ai",\n      "snippet": "A high-performance distributed file system designed to address the challenges of AI training and inference workloads. deepseek-ai/3FS\'s past year of commit ...",\n      "source": "DeepSeek - GitHub",\n      "relevance": 159\n    },\n    {\n      "title": "DeepSeek: The Chinese AI app that has the world talking - BBC",\n      "url": "https://www.bbc.com/news/articles/c5yv5976z9po",\n      "snippet": "DeepSeek is the name of a free AI-powered chatbot, which looks, feels and works very much like ChatGPT. That means it\'s used for many of ...",\n      "source": "DeepSeek: The Chinese AI app that has the world talking - BBC",\n      "relevance": 140\n    }\n  ],\n  "metadata": {\n    "stage": "contradiction_check"\n  }\n}', '{\n  "type": "thinking",\n  "content": "The context provided revolves around **DeepSeek AI**, a Chinese artificial intelligence company specializing in the development of **large language models (LLMs)** and enterprise AI solutions. Here\\u2019s a detailed analysis of the insights derived from the information:\\n\\n### 1. **Company Overview**\\n   - **Location and Ownership**: DeepSeek AI is based in **Hangzhou, Zhejiang**, a major hub for technology and innovation in China. The company is owned and funded by a **Chinese hedge fund",\n  "articles": [\n    {\n      "title": "DeepSeek - Wikipedia",\n      "url": "https://en.wikipedia.org/wiki/DeepSeek",\n      "snippet": "a Chinese artificial intelligence company that develops large language models (LLMs). Based in Hangzhou, Zhejiang, it is owned and funded by the Chinese hedge ...",\n      "source": "DeepSeek - Wikipedia",\n      "relevance": 162\n    },\n    {\n      "title": "DeepSeek AI",\n      "url": "https://deepseek.ai/",\n      "snippet": "DeepSeek AI is the leading provider of advanced AI language models and enterprise solutions. Experience state-of-the-art artificial intelligence technology ...",\n      "source": "DeepSeek AI",\n      "relevance": 159\n    },\n    {\n      "title": "DeepSeek - GitHub",\n      "url": "https://github.com/deepseek-ai",\n      "snippet": "A high-performance distributed file system designed to address the challenges of AI training and inference workloads. deepseek-ai/3FS\'s past year of commit ...",\n      "source": "DeepSeek - GitHub",\n      "relevance": 159\n    }\n  ],\n  "metadata": {\n    "stage": "synthesis"\n  }\n}', '{\n  "type": "content",\n  "content": "The Chinese artificial intelligence company in question, based in Hangzhou, Zhejiang, specializes in the development of large language models (LLMs). As a prominent player in the AI industry, the company leverages cutting-edge technologies to create advanced natural language processing (NLP) systems that can understand, generate, and interact with human language in a sophisticated manner. These LLMs are designed for a wide range of applications, including but not limited to customer service automation, content creation, language translation, and data analysis.\\n\\nHangzhou, being a major hub for technology and innovation in China, provides the company with access to a robust ecosystem of talent, resources, and infrastructure. This strategic location enables the company to stay at the forefront of AI research and development, fostering collaboration with academic institutions, tech startups, and established enterprises.\\n\\nThe company is owned and funded by a Chinese hedge fund, which underscores its strong financial backing and commitment to long-term growth in the AI sector. This funding allows the company to invest heavily in research and development, attract top-tier talent, and scale its operations to meet the growing demand for AI-driven solutions both domestically and internationally.\\n\\nAs part of its mission, the company is likely focused on advancing the capabilities of LLMs to achieve higher levels of accuracy, efficiency, and adaptability. This includes exploring areas such as multimodal AI (integrating text, image, and voice data), improving model interpretability, and addressing ethical considerations in AI deployment. Additionally, the company may be actively involved in collaborations with government and industry stakeholders to ensure its technologies align with national and global AI development goals.\\n\\nOverall, this company represents a significant contributor to the rapidly evolving field of artificial intelligence, particularly in the realm of large language models, and is well-positioned to play a key role in shaping the future of AI-driven innovation.",\n  "articles": [\n    {\n      "title": "DeepSeek - Wikipedia",\n      "url": "https://en.wikipedia.org/wiki/DeepSeek",\n      "snippet": "a Chinese artificial intelligence company that develops large language models (LLMs). Based in Hangzhou, Zhejiang, it is owned and funded by the Chinese hedge ...",\n      "source": "DeepSeek - Wikipedia",\n      "relevance": 162\n    }\n  ],\n  "metadata": {\n    "confidence": 0.7265697862073863\n  }\n}', '{\n  "type": "content",\n  "content": "DeepSeek AI stands at the forefront of artificial intelligence innovation, offering cutting-edge AI language models and comprehensive enterprise solutions. As a leader in the field, DeepSeek AI leverages state-of-the-art technology to deliver unparalleled performance, accuracy, and efficiency in natural language processing (NLP) and related applications. \\n\\n### Key Features and Offerings:  \\n1. **Advanced AI Language Models**:  \\n   DeepSeek AI develops and deploys highly sophisticated language models capable of understanding, generating, and interpreting human language with remarkable precision. These models are designed to handle complex tasks such as text generation, sentiment analysis, summarization, translation, and conversational AI.  \\n\\n2. **Enterprise Solutions**:  \\n   DeepSeek AI tailors its AI technologies to meet the unique needs of businesses across industries. Its enterprise solutions empower organizations to automate processes, enhance customer interactions, and derive actionable insights from vast amounts of unstructured data.  \\n\\n3. **State-of-the-Art Technology**:  \\n   By incorporating the latest advancements in machine learning, deep learning, and neural networks, DeepSeek AI ensures its models remain at the cutting edge of AI research. This commitment to innovation enables the company to deliver solutions that are both scalable and adaptable to evolving business demands.  \\n\\n4. **Applications Across Industries**:  \\n   DeepSeek AI\'s solutions are versatile and applicable across various sectors, including healthcare, finance, e-commerce, customer service, and more. For instance, its AI models can assist in medical diagnosis, financial forecasting, personalized marketing, and intelligent virtual assistants.  \\n\\n5. **Focus on Ethical AI**:  \\n   DeepSeek AI prioritizes ethical considerations in AI development, ensuring its models are transparent, fair, and free from bias. The company adheres to stringent data privacy and security standards to protect user information and maintain trust.  \\n\\n6. **Continuous Improvement and Support**:  \\n   DeepSeek AI is committed to continuous improvement, regularly updating its models and solutions to incorporate the latest research and user feedback. Additionally, the company provides robust support and training to help enterprises seamlessly integrate AI into their operations.  \\n\\n### Why Choose DeepSeek AI?  \\nDeepSeek AI distinguishes itself through its combination of technical expertise, industry-specific solutions, and a forward-thinking approach to AI development. By partnering with DeepSeek AI, organizations can harness the power of advanced AI to drive innovation, improve efficiency, and gain a competitive edge in their respective markets.  \\n\\nIn summary, DeepSeek AI is not just a provider of AI technology; it is a trusted partner in transforming businesses and industries through the intelligent application of artificial intelligence.",\n  "articles": [\n    {\n      "title": "DeepSeek AI",\n      "url": "https://deepseek.ai/",\n      "snippet": "DeepSeek AI is the leading provider of advanced AI language models and enterprise solutions. Experience state-of-the-art artificial intelligence technology ...",\n      "source": "DeepSeek AI",\n      "relevance": 159\n    }\n  ],\n  "metadata": {\n    "confidence": 0.8237388530808979\n  }\n}', '{\n  "type": "content",\n  "content": "DeepSeek-AI\'s **3FS** (a high-performance distributed file system) has been specifically engineered to tackle the unique challenges posed by AI training and inference workloads. Over the past year, the project has seen significant development and refinement, as evidenced by its commit history. Below is a comprehensive breakdown of its features, advancements, and the challenges it addresses:\\n\\n### Key Features of 3FS:\\n1. **High Throughput and Low Latency**:\\n   - Optimized for the massive data access patterns typical of AI workloads, ensuring fast read/write operations.\\n   - Reduces bottlenecks during training and inference by minimizing latency.\\n\\n2. **Scalability**:\\n   - Designed to scale horizontally across thousands of nodes, accommodating the growing data and compute requirements of AI models.\\n   - Efficiently handles petabytes of data without compromising performance.\\n\\n3. **Fault Tolerance and Reliability**:\\n   - Implements robust data replication and fault-tolerant mechanisms to ensure data integrity and availability.\\n   - Automatically recovers from node failures, minimizing downtime.\\n\\n4. **Efficient Metadata Management**:\\n   - Utilizes a distributed metadata architecture to handle the high volume of small files and metadata operations common in AI workloads.\\n   - Reduces metadata lookup times, improving overall system performance.\\n\\n5. **Data Locality Optimization**:\\n   - Ensures data is stored close to compute nodes, reducing network overhead and improving training efficiency.\\n   - Dynamically adjusts data placement based on workload patterns.\\n\\n6. **Multi-Tenancy Support**:\\n   - Provides isolation and resource management for multiple users or teams sharing the same infrastructure.\\n   - Ensures fair resource allocation and prevents one workload from impacting others.\\n\\n### Past Year of Commit Highlights:\\n- **Performance Enhancements**:\\n  - Optimized data transfer protocols to reduce latency and improve throughput.\\n  - Improved caching mechanisms to accelerate frequently accessed data.\\n\\n- **Scalability Improvements**:\\n  - Enhanced the system\\u2019s ability to handle larger clusters and more concurrent workloads.\\n  - Introduced dynamic load balancing to distribute workloads evenly across nodes.\\n\\n- **Fault Tolerance Upgrades**:\\n  - Implemented more efficient data replication strategies to reduce storage overhead.\\n  - Added automated failure detection and recovery mechanisms.\\n\\n- **Metadata Management Refinements**:\\n  - Reduced metadata contention through sharding and partitioning techniques.\\n  - Improved metadata query performance with advanced indexing methods.\\n\\n- **Usability and Monitoring**:\\n  - Added comprehensive monitoring and logging tools to help users track system performance and diagnose issues.\\n  - Simplified deployment and configuration processes for easier adoption.\\n\\n### Challenges Addressed:\\n1. **Data Bottlenecks in AI Workloads**:\\n   - AI training and inference often involve accessing large datasets repeatedly. 3FS mitigates this by optimizing data access patterns and reducing latency.\\n\\n2. **Scalability Issues**:\\n   - Traditional file systems struggle to scale to the demands of modern AI workloads. 3FS\\u2019s distributed architecture ensures it can grow with the workload.\\n\\n3. **Fault Tolerance**:\\n   - AI workloads are resource-intensive and time-consuming. 3FS ensures reliability by minimizing the impact of hardware failures.\\n\\n4. **Metadata Overhead**:\\n   - AI workloads generate a high volume of metadata operations. 3FS\\u2019s efficient metadata management reduces this overhead, improving performance.\\n\\n### Future Directions:\\n- **Integration with AI Frameworks**:\\n  - Further integration with popular AI frameworks like TensorFlow, PyTorch, and Hugging Face to streamline workflows.\\n- **Advanced Caching Strategies**:\\n  - Implementing AI-driven caching to predict and preload data based on workload patterns.\\n- **Energy Efficiency**:\\n  - Optimizing the system to reduce energy consumption, making it more sustainable for large-scale deployments.\\n\\nIn summary, DeepSeek-AI\'s 3FS represents a cutting-edge solution tailored to the demanding requirements of AI workloads. Its continuous development over the past year has focused on enhancing performance, scalability, and reliability, making it a robust choice for organizations leveraging AI at scale.",\n  "articles": [\n    {\n      "title": "DeepSeek - GitHub",\n      "url": "https://github.com/deepseek-ai",\n      "snippet": "A high-performance distributed file system designed to address the challenges of AI training and inference workloads. deepseek-ai/3FS\'s past year of commit ...",\n      "source": "DeepSeek - GitHub",\n      "relevance": 159\n    }\n  ],\n  "metadata": {\n    "confidence": 0.9121319972755207\n  }\n}', '{\n  "type": "content",\n  "content": "DeepSeek is a cutting-edge AI-powered chatbot that offers a seamless and intuitive user experience, rivaling popular platforms like ChatGPT. Powered by the advanced DeepSeek-V3 model, this free tool is designed to provide users with a robust and versatile AI assistant for a wide range of applications. Whether you\'re looking for creative writing assistance, problem-solving, or general information, DeepSeek delivers high-quality interactions that feel natural and engaging.\\n\\nDeepSeek is developed by a Hangzhou-based firm that is rapidly advancing its AI technology. The company has already launched the DeepSeek-R1 model, which is now live and open source, positioning itself as a strong competitor to OpenAI\'s Model o1. This latest iteration builds on the success of the R1 model released earlier in January, showcasing DeepSeek\'s commitment to innovation and continuous improvement.\\n\\nThe platform is accessible via web, app, and API, making it easy for users to integrate DeepSeek into their workflows or daily routines. Its open-source nature also encourages collaboration and customization, appealing to developers and tech enthusiasts. DeepSeek is leveraging its technological edge to expand its user base and solidify its position in the competitive AI landscape.\\n\\nFor those seeking a free, powerful, and user-friendly AI assistant, DeepSeek is an excellent choice. Its similarity to ChatGPT in functionality and design ensures a familiar experience, while its advanced models and open-source availability set it apart as a forward-thinking alternative. Explore DeepSeek today to experience the future of AI-powered interactions.",\n  "articles": [\n    {\n      "title": "DeepSeek - AI Assistant - Apps on Google Play",\n      "url": "https://play.google.com/store/apps/details?id=com.deepseek.chat&hl=en_US",\n      "snippet": "Experience seamless interaction with DeepSeek\'s official AI assistant for free! Powered by the groundbreaking DeepSeek-V3 model with over ...",\n      "source": "DeepSeek - AI Assistant - Apps on Google Play",\n      "relevance": 141\n    },\n    {\n      "title": "DeepSeek: The Chinese AI app that has the world talking - BBC",\n      "url": "https://www.bbc.com/news/articles/c5yv5976z9po",\n      "snippet": "DeepSeek is the name of a free AI-powered chatbot, which looks, feels and works very much like ChatGPT. That means it\'s used for many of ...",\n      "source": "DeepSeek: The Chinese AI app that has the world talking - BBC",\n      "relevance": 140\n    },\n    {\n      "title": "DeepSeek rushes to launch new AI model as China goes all in",\n      "url": "https://www.reuters.com/technology/artificial-intelligence/deepseek-rushes-launch-new-ai-model-china-goes-all-2025-02-25/",\n      "snippet": "DeepSeek is looking to press home its advantage. The Hangzhou-based firm is accelerating the launch of the successor to January\'s R1 model.",\n      "source": "DeepSeek rushes to launch new AI model as China goes all in",\n      "relevance": 139\n    },\n    {\n      "title": "DeepSeek",\n      "url": "https://www.deepseek.com/",\n      "snippet": "DeepSeek-R1 is now live and open source, rivaling OpenAI\'s Model o1. Available on web, app, and API. Click for details. Into ...",\n      "source": "DeepSeek",\n      "relevance": 128\n    }\n  ],\n  "metadata": {\n    "confidence": 0.8208259890479443\n  }\n}', '{\n  "type": "completion",\n  "content": "### Comprehensive Overview of DeepSeek AI\\n\\n#### Introduction\\nDeepSeek AI is a leading Chinese artificial intelligence company based in Hangzhou, Zhejiang, specializing in the development of large language models (LLMs) and advanced AI solutions. Owned and funded by a Chinese hedge fund, the company benefits from strong financial backing, enabling significant investment in research and development. DeepSeek AI leverages cutting-edge technologies to create sophisticated natural language processing (NLP) systems, catering to a wide range of applications across various industries.\\n\\n#### Core Offerings and Technological Innovations\\n\\n1. **Advanced AI Language Models**:\\n   - **DeepSeek-V3 Model**: The latest iteration of DeepSeek\'s language models, offering state-of-the-art performance in understanding, generating, and interpreting human language. This model powers the company\'s AI assistant, providing high-quality, natural, and engaging interactions.\\n   - **DeepSeek-R1 Model**: An open-source model launched earlier in January, now live and available on web, app, and API. It rivals OpenAI\'s Model o1 and is designed for versatility in applications such as creative writing, problem-solving, and general information retrieval.\\n\\n2. **Enterprise Solutions**:\\n   - DeepSeek AI tailors its AI technologies to meet the unique needs of businesses across various sectors, including healthcare, finance, e-commerce, and customer service. Its solutions enable process automation, enhanced customer interactions, and actionable insights from unstructured data.\\n\\n3. **High-Performance Distributed File System (3FS)**:\\n   - **Key Features**: Designed to address the challenges of AI training and inference workloads, 3FS offers high throughput, low latency, scalability, fault tolerance, efficient metadata management, data locality optimization, and multi-tenancy support.\\n   - **Recent Developments**: Over the past year, 3FS has seen significant enhancements in performance, scalability, fault tolerance, metadata management, and usability. These improvements ensure it remains a robust solution for organizations leveraging AI at scale.\\n\\n#### Strategic Advantages and Market Position\\n\\n1. **Strategic Location**:\\n   - Based in Hangzhou, a major hub for technology and innovation in China, DeepSeek AI benefits from access to a robust ecosystem of talent, resources, and infrastructure. This strategic location fosters collaboration with academic institutions, tech startups, and established enterprises.\\n\\n2. **Financial Backing**:\\n   - The company\'s ownership by a Chinese hedge fund underscores its strong financial backing, enabling heavy investment in R&D, talent acquisition, and scaling operations to meet growing domestic and international demand for AI-driven solutions.\\n\\n3. **Commitment to Ethical AI**:\\n   - DeepSeek AI prioritizes ethical considerations in AI development, ensuring its models are transparent, fair, and free from bias. The company adheres to stringent data privacy and security standards to protect user information and maintain trust.\\n\\n#### Applications and Industry Impact\\n\\n1. **Versatile Applications**:\\n   - DeepSeek AI\'s solutions are applicable across various industries, including healthcare (medical diagnosis), finance (financial forecasting), e-commerce (personalized marketing), and customer service (intelligent virtual assistants).\\n\\n2. **Continuous Improvement and Support**:\\n   - The company is committed to continuous improvement, regularly updating its models and solutions to incorporate the latest research and user feedback. Additionally, DeepSeek AI provides robust support and training to help enterprises seamlessly integrate AI into their operations.\\n\\n#### Future Directions and Expansion\\n\\n1. **Technological Advancements**:\\n   - DeepSeek AI is accelerating the launch of successor models to the DeepSeek-R1, showcasing its commitment to innovation and continuous improvement. The company is also exploring areas such as multimodal AI (integrating text, image, and voice data), improving model interpretability, and addressing ethical considerations in AI deployment.\\n\\n2. **Integration and Collaboration**:\\n   - DeepSeek AI is actively involved in collaborations with government and industry stakeholders to ensure its technologies align with national and global AI development goals. The company is also integrating its solutions with popular AI frameworks like TensorFlow, PyTorch, and Hugging Face to streamline workflows.\\n\\n3. **Energy Efficiency and Sustainability**:\\n   - Future developments include optimizing the 3FS system to reduce energy consumption, making it more sustainable for large-scale deployments.\\n\\n#### Conclusion\\nDeepSeek AI represents a significant contributor to the rapidly evolving field of artificial intelligence, particularly in the realm of large language models. With its advanced language models, high-performance distributed file system, and comprehensive enterprise solutions, DeepSeek AI is well-positioned to play a key role in shaping the future of AI-driven innovation. The company\'s strategic location, strong financial backing, commitment to ethical AI, and continuous improvement efforts make it a trusted partner for businesses seeking to harness the power of advanced AI to drive innovation, improve efficiency, and gain a competitive edge in their respective markets.",\n  "metadata": {\n    "used_sources": 7,\n    "article_ids": [\n      "https://deepseek.ai/",\n      "https://play.google.com/store/apps/details?id=com.deepseek.chat&hl=en_US",\n      "https://www.reuters.com/technology/artificial-intelligence/deepseek-rushes-launch-new-ai-model-china-goes-all-2025-02-25/",\n      "https://www.bbc.com/news/articles/c5yv5976z9po",\n      "https://github.com/deepseek-ai",\n      "https://www.deepseek.com/",\n      "https://en.wikipedia.org/wiki/DeepSeek"\n    ]\n  }\n}']
    results = []
    # for chunk in results:
    #     time.sleep(random.randint(1,6))
    #     print(chunk)
    #     agent.send_output(agent_output_name='deep_inquire_result', agent_result=chunk)
    for chunk in generator.generate_stream():
        print('chunk : ',json.dumps(chunk, indent=2))
        results.append(json.dumps(chunk, indent=2))
        agent.send_output(agent_output_name='deep_inquire_result', agent_result=json.dumps(chunk, indent=2))
    print('results : ',results)

def main():
    agent = MofaAgent(agent_name='DeepInquire')
    run(agent=agent)

if __name__ == "__main__":
    main()
