import asyncio
import os
import json
import time

from dotenv import load_dotenv
from fastmcp import Client
from openai import OpenAI

# --- 配置 LLM 客户端 ---
t0 = time.time()
OLLAMA_MODEL_NAME = "qwen3-8b-local:latest"
os.environ['NO_PROXY'] = "10.100.1.115,localhost,127.0.0.1"

planner_llm = OpenAI(
    base_url="http://127.0.0.1:11434/v1",
    api_key="ollama",
)
print('[计时] 初始化 LLM 耗时：', round(time.time() - t0, 3), '秒')


async def main():
    total_start = time.time()
    client_connect_time = time.time()
    client = Client("http://127.0.0.1:9000/mcp/")
    print('[计时] 创建 MCP 客户端对象耗时：', round(time.time() - client_connect_time, 3), '秒')

    async with client:
        t_tool_list = time.time()
        tools = await client.list_tools()
        print('[计时] 获取工具列表耗时：', round(time.time() - t_tool_list, 3), '秒')

        print("\n--- 从 FastMCP 服务器发现的原始工具信息 ---")
        if not tools:
            print("警告：没有发现任何工具。请确保服务器已启动并注册工具。")
        else:
            for i, t in enumerate(tools):
                print(f"工具 {i + 1}:")
                print(f" 名称: {getattr(t, 'name', 'N/A')}")
                print(f" 描述: {getattr(t, 'description', 'N/A')}")
                print(f" 输入 Schema: {getattr(t, 'inputSchema', 'N/A')}")
        print("--------------------------------------------------\n")

        # 构造 tool_def 列表
        t_tool_def = time.time()
        tool_defs = []
        for t in tools:
            tool_name = getattr(t, 'name', None)
            if not tool_name:
                print(f"警告：发现一个没有名称的工具。跳过。原始数据: {t}")
                continue

            tool_description = getattr(t, 'description', "")
            if not isinstance(tool_description, str):
                tool_description = str(tool_description)

            tool_parameters = getattr(t, 'inputSchema', None)
            if not tool_parameters:
                tool_parameters = {"type": "object", "properties": {}}
            elif isinstance(tool_parameters, str):
                try:
                    tool_parameters = json.loads(tool_parameters)
                except json.JSONDecodeError:
                    print(f"警告：工具 '{tool_name}' 的 inputSchema 无法解析为 JSON。跳过。")
                    continue
            elif not isinstance(tool_parameters, dict):
                print(f"警告：工具 '{tool_name}' 的 inputSchema 类型不正确，跳过。")
                continue

            tool_parameters.setdefault("type", "object")
            tool_parameters.setdefault("properties", {})

            tool_defs.append({
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": tool_description,
                    "parameters": tool_parameters,
                }
            })
        print('[计时] 构建工具定义耗时：', round(time.time() - t_tool_def, 3), '秒')

        if not tool_defs:
            print("错误：没有生成任何工具定义。退出。")
            return

        print("\n--- 格式化后发送给 OpenAI API 的工具定义 ---")
        print(json.dumps(tool_defs, indent=2, ensure_ascii=False))
        print("----------------------------------------------------\n")

        user_query = """我想知道 除了vllm还有哪些开源的 LLM 推理框架效率很高？ 为什么？"""
        t_llm_plan = time.time()

        if tool_defs:
            plan_resp = planner_llm.chat.completions.create(
                model=OLLAMA_MODEL_NAME,
                messages=[
                    {"role": "system", "content": "你是一个智能 agent，能决定是否调用 deepsearch 工具来完成任务。"},
                    {"role": "assistant", "content": f"Available tools: {json.dumps(tool_defs, ensure_ascii=False)}"},
                    {"role": "user", "content": user_query}
                ],
                tools=tool_defs,
                tool_choice="auto"
            )
        else:
            plan_resp = planner_llm.chat.completions.create(
                model=OLLAMA_MODEL_NAME,
                messages=[
                    {"role": "system", "content": "你是一个智能 agent。"},
                    {"role": "user", "content": user_query}
                ]
            )
            print("LLM 最终回复 (无工具):", plan_resp.choices[0].message.content)
            return
        print('[计时] LLM 工具选择耗时：', round(time.time() - t_llm_plan, 3), '秒')

        if not plan_resp.choices[0].message.tool_calls:
            print("LLM 决定不调用任何工具，最终回复：")
            print(plan_resp.choices[0].message.content)
            return

        func_call = plan_resp.choices[0].message.tool_calls[0]
        t_parse = time.time()
        args = json.loads(func_call.function.arguments)
        print('[计时] 解析工具参数耗时：', round(time.time() - t_parse, 3), '秒')
        print(f"\n--- LLM 决定调用工具：{func_call.function.name}，参数：{args} ---")

        t_call_tool = time.time()
        tool_result = await client.call_tool(func_call.function.name, args)
        print('[计时] 工具调用耗时：', round(time.time() - t_call_tool, 3), '秒')
        print(f"\n--- 工具调用结果：{tool_result.data} ---")

        t_final = time.time()
        final_resp = planner_llm.chat.completions.create(
            model=OLLAMA_MODEL_NAME,
            messages=[
                {"role": "system", "content": "基于工具的搜索结果，给出分析比较。"},
                {"role": "user", "content": user_query},
                {"role": "assistant", "content": json.dumps(tool_result.data or {}, ensure_ascii=False)}
            ]
        )
        print('[计时] 最终回复生成耗时：', round(time.time() - t_final, 3), '秒')
        print("\n最终结果：", final_resp.choices[0].message.content)
        print('[总计时] 整个流程耗时：', round(time.time() - total_start, 3), '秒')


if __name__ == "__main__":
    asyncio.run(main())
