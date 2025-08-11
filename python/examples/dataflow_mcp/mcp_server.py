# deepsearch_agent.py
import json
import os
from fastmcp import FastMCP
from fastmcp.server.context import Context  # 导入 Context
from openai import OpenAI
from dotenv import load_dotenv
import asyncio

# 加载环境变量
load_dotenv('.env.secret')
os.environ['OPENAI_API_KEY'] = os.getenv('LLM_API_KEY', 'sk-skjaksa')
mcp = FastMCP(name="deepsearch-agent")

@mcp.tool(
    name='deepsearch',
    description='深度搜索工具，基于 serper + LLM 进行搜索和总结的深度思考工具'
)
async def deepsearch(ctx: Context, query: str, top_k: int = 5) -> dict:
    """
    deepsearch 工具：
    - query：搜索语句
    - top_k：返回的结果数量（默认 5）
    返回值：
    - 包含搜索结果摘要的 JSON
    """
    client = OpenAI(
        base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:8000/v3"),
        api_key='sk-skjaksa'
    )

    try:
        # 同步流式调用 OpenAI
        response_stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "你是一个深度文档搜索助手。"},
                {"role": "user", "content": f"请基于以下 query 帮我找 top {top_k} 个相关信息：{query}"}
            ],
            stream=True
        )

        results = []
        current_content = ""
        count = 0

        # 使用同步 for 读取 stream
        for chunk in response_stream:
            delta = chunk.choices[0].delta.content
            if delta:
                current_content += delta
                count += len(delta)
                # 上报进度
                await ctx.report_progress(progress=count)

        results.append(current_content)
        return {"query": query, "results": results}

    except Exception as e:
        error_message = f"Error in deepsearch tool: {e}"
        # 使用 ctx.error 上报异常
        await ctx.error(error_message)
        return {"error": error_message}


@mcp.tool(
    name="generate_mofa_node",
    description=(
            "生成 MoFA 框架中用于构造节点（MoFA Node）的配置或代码片段。"
            "向 LLM 传入用户输入脚本、需求或描述，由 OpenAI 模型生成符合 MoFA DataFlow 或 Node 定义规范的内容。"
    )
)
async def generate_mofa_node(
        ctx: Context,
        user_input: str
) -> dict:
    """
    user_input: 来自用户的自然语言说明，或示例脚本、
                要集成入 MoFA Node 的上下文代码。

    本工具将调用 OpenAI API，通过 GPT-4o-mini 理解意图并输出适配 MoFA 节点生成内容。
    返回结果包含：
    - 'node_definition': 生成后的 MoFA Node YAML 或 Python 模板片段（字符串）
    - 'explanation': 对生成内容的简要说明，便于理解如何集成到 MoFA DataFlow 中
    """
    client = OpenAI(
        base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:8025/v1"),
        api_key=os.getenv("OPENAI_API_KEY")
    )
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "你是熟悉 MoFA 框架的开发助手。"},
                {"role": "user", "content": user_input},
            ],
        )

        choice = resp.choices[0].message.content
        # 假设 LLM 输出包含两个部分：node_definition 和 explanation，格式为 JSON
        try:
            parsed = json.loads(choice)
            return {
                "node_definition": parsed.get("node_definition", choice),
                "explanation": parsed.get("explanation", "")
            }
        except json.JSONDecodeError:
            # 若不是 JSON 输出，返回原始内容
            return {
                "node_definition": choice,
                "explanation": "（未能解析 JSON 格式，直接显示模型回复）"
            }

    except Exception as e:
        await ctx.error(f"OpenAI 调用失败: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    # 启动 HTTP SSE Server，供客户端调用
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=9000,
    )
