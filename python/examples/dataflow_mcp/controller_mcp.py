import asyncio
import os
import json

from dotenv import load_dotenv
from fastmcp import Client
from openai import OpenAI

# 配置 LLM 用于规划工具调用
load_dotenv('.env.secret')
os.environ['OPENAI_API_KEY'] = os.getenv('LLM_API_KEY')
planner_llm = OpenAI()


async def main():
    # 确保客户端连接的URL与服务器端实际监听的URL一致，注意末尾的斜杠
    # 根据您之前服务器的启动日志：🔗 Server URL: http://127.0.0.1:9000/mcp/
    client = Client("http://127.0.0.1:9000/mcp/")

    async with client:
        # 获取 available tools，供 LLM 选择
        tools = await client.list_tools()

        # --- 调试信息：打印从 FastMCP 服务器获取的原始工具列表 ---
        print("\n--- 从 FastMCP 服务器发现的原始工具信息 ---")
        if not tools:
            print("警告：没有发现任何工具。请确保 deepsearch_mcp.py 服务器已成功启动并注册了工具。")
        else:
            for i, t in enumerate(tools):
                print(f"工具 {i + 1}:")
                print(f"  名称: {getattr(t, 'name', 'N/A')}")
                print(f"  描述: {getattr(t, 'description', 'N/A')}")
                print(f"  输入 Schema: {getattr(t, 'inputSchema', 'N/A')}")
                # 使用 hasattr 和 getattr 来安全访问属性，防止属性不存在导致错误
        print("--------------------------------------------------\n")

        tool_defs = []
        for t in tools:
            # 验证工具名称
            tool_name = getattr(t, 'name', None)
            if not tool_name:
                print(f"警告：发现一个没有名称的工具。跳过此工具。原始数据: {t}")
                continue

            # 验证工具描述 (描述可以为空，但确保它是字符串)
            tool_description = getattr(t, 'description', "")
            if not isinstance(tool_description, str):
                tool_description = str(tool_description)  # 强制转换为字符串

            # 验证和格式化输入 Schema
            # OpenAI 的 parameters 字段要求是 JSON Schema 对象
            # 即使工具没有参数，也应该是 {"type": "object", "properties": {}}
            tool_parameters = getattr(t, 'inputSchema', None)

            if not tool_parameters:
                # 如果 inputSchema 为空或 None，则提供一个最小的有效 JSON Schema
                tool_parameters = {"type": "object", "properties": {}}
            elif isinstance(tool_parameters, str):
                # 如果 inputSchema 是字符串，尝试将其解析为 JSON
                try:
                    tool_parameters = json.loads(tool_parameters)
                except json.JSONDecodeError:
                    print(
                        f"警告：工具 '{tool_name}' 的 inputSchema 不是有效的 JSON 字符串，尝试跳过此工具。原始Schema: {t.inputSchema}")
                    continue
            elif not isinstance(tool_parameters, dict):
                # 如果 inputSchema 既不是 None 也不是字符串也不是字典，则有问题
                print(
                    f"警告：工具 '{tool_name}' 的 inputSchema 类型不正确，尝试跳过此工具。类型: {type(tool_parameters)}, 原始Schema: {t.inputSchema}")
                continue

            # 确保 tool_parameters 是一个符合 OpenAI 要求的最小 JSON Schema 结构
            if "type" not in tool_parameters:
                tool_parameters["type"] = "object"
            if "properties" not in tool_parameters:
                tool_parameters["properties"] = {}

            # 构建符合 OpenAI API 要求的工具定义
            tool_def = {
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": tool_description,
                    "parameters": tool_parameters,
                }
            }
            tool_defs.append(tool_def)

        # --- 调试信息：打印格式化后的工具定义，这将发送给 OpenAI ---
        print("\n--- 格式化后发送给 OpenAI API 的工具定义 ---")
        if not tool_defs:
            print("错误：没有生成任何有效的工具定义。无法继续 LLM 规划。")
            return  # 如果没有有效工具，直接退出
        else:
            print(json.dumps(tool_defs, indent=2, ensure_ascii=False))  # ensure_ascii=False 以便正确显示中文
        print("----------------------------------------------------\n")

        user_query = """我想创建一个 mofa的 node  任务是下面的内容： 查询英文单词释义 I want to create an agent to query the meaning of a certain word def define_word(word): response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}") if response.ok: definition = response.json()[0]["meanings"][0]["definitions"][0]["definition"] return f"{word}: {definition}" return "未找到释义" print(define_word("serendipity"))"""

        # LLM 规划工具调用
        # 只有在有可用工具时才传递 functions 参数
        if tool_defs:
            plan_resp = planner_llm.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "你是一个智能 agent，能决定是否调用 deepsearch 工具来完成任务。"},
                    # 最好将 tool_defs 作为 JSON 字符串嵌入到 assistant 消息中，以便 LLM 更好地理解
                    {"role": "assistant", "content": f"Available tools: {json.dumps(tool_defs, ensure_ascii=False)}"},
                    {"role": "user", "content": user_query}
                ],
                tools=tool_defs,  # 传递格式化后的工具定义列表
                tool_choice="auto"
            )
        else:
            # 如果没有工具，直接让 LLM 回答，不进行工具调用
            print("没有可用的工具，LLM 将直接回答。")
            plan_resp = planner_llm.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "你是一个智能 agent。"},
                    {"role": "user", "content": user_query}
                ]
            )
            print("LLM 最终回复 (无工具):", plan_resp.choices[0].message.content)
            return

        # 检查 LLM 是否确实进行了工具调用
        if not plan_resp.choices[0].message.tool_calls:
            print("LLM 决定不调用任何工具。最终回复:")
            print(plan_resp.choices[0].message.content)
            return

        func_call = plan_resp.choices[0].message.tool_calls[0]
        args = json.loads(func_call.function.arguments)

        print(f"\n--- LLM 决定调用工具：{func_call.function.name}，参数：{args} ---")

        # 调用 deepsearch（或其他工具）
        tool_result = await client.call_tool(
            func_call.function.name,
            args
        )
        print(f"\n--- 工具调用结果：{tool_result.data} ---")

        # LLM 使用工具结果生成最终回复
        final_resp = planner_llm.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "基于工具的搜索结果，给出分析比较。"},
                {"role": "user", "content": user_query},
                # 确保 tool_result.data 是 JSON 字符串
                {"role": "assistant", "content": json.dumps(tool_result.data or {}, ensure_ascii=False)}
            ]
        )
        print("\n最终结果：", final_resp.choices[0].message.content)


if __name__ == "__main__":
    asyncio.run(main())