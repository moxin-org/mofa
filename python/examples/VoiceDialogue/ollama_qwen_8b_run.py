import asyncio
import os
import json
import time

from dotenv import load_dotenv
from fastmcp import Client
from openai import OpenAI

# --- 配置 LLM 客户端 ---
t0_init_llm = time.time()
OLLAMA_MODEL_NAME = "qwen3:8b"
# 确保 NO_PROXY 配置正确，以便 FastMCP 客户端和 OLLAMA 客户端能正常通信
os.environ['NO_PROXY'] = "10.100.1.115,localhost,127.0.0.1"

# OpenAI 客户端实例 - 不使用 async with，直接实例化
planner_llm = OpenAI( # Renamed back to planner_llm as it's the direct instance
    base_url="http://127.0.0.1:11434/v1",
    api_key="ollama",
)
print(f'[计时] LLM 客户端初始化耗时：{round(time.time() - t0_init_llm, 3)} 秒')


async def chat_loop():
    total_start = time.time()

    # FastMCP 客户端连接
    t_client_connect = time.time()
    # 确保 FastMCP 客户端连接到正确的地址和端口
    mcp_client = Client("http://127.0.0.1:9001/mcp/") # Renamed for clarity

    print(f'[计时] FastMCP 客户端对象创建耗时：{round(time.time() - t_client_connect, 3)} 秒')

    # IMPORTANT: Only FastMCP client uses async with for proper resource management
    async with mcp_client:
        # 获取工具列表
        t_tool_list = time.time()
        tools = await mcp_client.list_tools() # Use mcp_client here
        print(f'[计时] 从 FastMCP 服务器获取工具列表耗时：{round(time.time() - t_tool_list, 3)} 秒')

        print("\n--- 从 FastMCP 服务器发现的原始工具信息 ---")
        if not tools:
            print("警告：没有发现任何工具。请确保 FastMCP 服务器已启动并注册工具。")
        else:
            for i, t in enumerate(tools):
                print(f"工具 {i + 1}:")
                print(f"  名称: {getattr(t, 'name', 'N/A')}")
                print(f"  描述: {getattr(t, 'description', 'N/A')}")
                # print(f"  输入 Schema: {getattr(t, 'inputSchema', 'N/A')}") # 避免输出过多信息
        print("--------------------------------------------------\n")

        # 构造 LLM 可用的 tool_def 列表
        t_tool_def = time.time()
        tool_defs = []
        for t in tools:
            tool_name = getattr(t, 'name', None)
            if not tool_name:
                print(f"警告：发现一个没有名称的工具，已跳过。原始数据: {t}")
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
                    print(f"警告：工具 '{tool_name}' 的 inputSchema 无法解析为 JSON，已跳过。")
                    continue
            elif not isinstance(tool_parameters, dict):
                print(f"警告：工具 '{tool_name}' 的 inputSchema 类型不正确，已跳过。")
                continue

            # 确保 tool_parameters 包含 'type' 和 'properties' 键
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
        print(f'[计时] 构建 LLM 工具定义耗时：{round(time.time() - t_tool_def, 3)} 秒')

        if not tool_defs:
            print("错误：没有生成任何 LLM 可用的工具定义。后续对话将无法使用工具。")
        else:
            print("\n--- 格式化后发送给 LLM 的工具定义 (仅展示部分) ---")
            # print(json.dumps(tool_defs[:3], indent=2, ensure_ascii=False))
            if len(tool_defs) > 3:
                print(f"... (总计 {len(tool_defs)} 个工具定义) ...")
            print("----------------------------------------------------\n")

        # 对话历史，包括系统消息
        messages = [{"role": "system",
                     "content": "你是一个智能 agent，可以决定是否调用相关工具来完成任务。你会与用户进行多轮对话，根据上下文进行回复或工具调用。当用户输入 'exit' 或 'quit' 时，结束对话。"}]

        print("\n--- 开始多轮对话 ---")
        print("输入 'exit' 或 'quit' 退出。")

        while True:
            user_query = input("\n用户: ")
            if user_query.lower() in ["exit", "quit"]:
                print("Agent: 好的，再见！")
                break

            messages.append({"role": "user", "content": user_query })

            t_llm_plan = time.time()
            try:
                if tool_defs:
                    plan_resp = planner_llm.chat.completions.create(
                        model=OLLAMA_MODEL_NAME,
                        messages=messages,
                        tools=tool_defs,
                        tool_choice="auto"  # 允许 LLM 自主选择是否调用工具
                    )
                else:
                    # 如果没有工具，直接进行普通对话
                    plan_resp = planner_llm.chat.completions.create(
                        model=OLLAMA_MODEL_NAME,
                        messages=messages
                    )
            except Exception as e:
                print(f"错误：LLM 调用失败: {e}")
                messages.pop()  # 移除最后一条用户消息，避免循环出错
                continue

            print(f'[计时] LLM 思考（工具选择或回复）耗时：{round(time.time() - t_llm_plan, 3)} 秒')

            llm_message = plan_resp.choices[0].message
            messages.append(llm_message)  # 将 LLM 的回复或工具调用加入历史

            if llm_message.tool_calls:
                # LLM 决定调用工具
                print("\n--- LLM 决定调用工具 ---")
                for func_call in llm_message.tool_calls:
                    tool_name = func_call.function.name
                    try:
                        args = json.loads(func_call.function.arguments)
                        print(f"  工具名称：{tool_name}")
                        print(f"  调用参数：{args}")

                        t_call_tool = time.time()
                        # 调用 FastMCP 工具
                        print('args  : ',args)
                        tool_result_obj = await mcp_client.call_tool(tool_name, args) # Use mcp_client here
                        tool_result = tool_result_obj.data if tool_result_obj else {}  # 获取结果数据
                        print(f'[计时] 工具 {tool_name} 调用耗时：{round(time.time() - t_call_tool, 3)} 秒')
                        print(f"\n--- 工具调用结果：{tool_result} ---")

                        # 将工具调用结果添加到对话历史，供 LLM 参考
                        messages.append({
                            "role": "tool",
                            "tool_call_id": func_call.id,  # 关联到之前的 tool_call
                            "name": tool_name,
                            "content": json.dumps(tool_result, ensure_ascii=False)
                        })

                        # 再次调用 LLM，让它根据工具结果给出最终回复
                        t_final_resp = time.time()
                        final_resp = planner_llm.chat.completions.create(
                            model=OLLAMA_MODEL_NAME,
                            messages=messages  # 包含工具调用和结果的完整历史
                        )
                        print(f'[计时] 最终回复生成耗时：{round(time.time() - t_final_resp, 3)} 秒')

                        final_content = final_resp.choices[0].message.content
                        print(f"\nAgent: {final_content}")
                        messages.append({"role": "assistant", "content": final_content})  # 将最终回复加入历史

                    except json.JSONDecodeError as e:
                        print(f"错误：解析工具参数失败: {e}")
                        messages.pop()  # 移除用户消息
                        messages.pop()  # 移除 LLM 的工具调用，避免错误持续
                        print("Agent: 我在解析工具参数时遇到问题，请重新提问。")
                    except Exception as e:
                        print(f"错误：工具 {tool_name} 调用失败: {e}")
                        messages.pop()  # 移除用户消息
                        messages.pop()  # 移除 LLM 的工具调用，避免错误持续
                        print("Agent: 工具调用过程中出现问题，请稍后再试或换个问题。")
            else:
                # LLM 决定不调用工具，直接回复
                print(f"\nAgent: {llm_message.content}")
                # llm_message 已经在前面加入 messages 了，这里无需重复添加

    print(f'\n[总计时] 整个会话流程耗时：{round(time.time() - total_start, 3)} 秒')


if __name__ == "__main__":
    asyncio.run(chat_loop())