import asyncio
import os
import json
import time
import ast

import torch
from fastmcp import Client
from transformers import AutoTokenizer, AutoModelForCausalLM

# === 本地模型加载 ===
t0_init_llm = time.time()
model_path = "/Users/chenzi/project/zcbc/mofa/python/agent-hub/qwen-model/models/hammer2.1-7b"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
print(f"[计时] 本地 LLM 客户端初始化耗时：{time.time() - t0_init_llm:.3f} 秒")

# === FastMCP 客户端配置 ===
os.environ["NO_PROXY"] = "10.100.1.115,localhost,127.0.0.1"
MCP_URL = "http://127.0.0.1:9000/mcp/"
mcp_client = Client(MCP_URL)

def is_tool_call(text: str) -> bool:
    txt = text.strip().strip("```")
    try:
        arr = json.loads(txt)
    except json.JSONDecodeError:
        try:
            arr = ast.literal_eval(txt)
        except Exception:
            return False
    return isinstance(arr, list) and all(
        isinstance(item, dict) and "name" in item and "arguments" in item
        for item in arr
    )

def parse_tool_call(text: str):
    txt = text.strip().strip("```")
    try:
        calls = json.loads(txt)
    except json.JSONDecodeError:
        calls = ast.literal_eval(txt)
    return [(c["name"], c["arguments"]) for c in calls]

async def chat_loop():
    total_start = time.time()

    # 获取工具列表
    t0 = time.time()
    async with mcp_client:
        tools = await mcp_client.list_tools()
    print(f"[计时] FastMCP 客户端创建 + 列表工具耗时：{time.time() - t0:.3f} 秒")

    # 打印工具信息
    print("\n--- FastMCP 可用工具列表 ---")
    for i, t in enumerate(tools, 1):
        print(f"{i}. {t.name} — {t.description or '无描述'}")
    print("------------------------------\n")

    # 构造 tool_defs
    t1 = time.time()
    tool_defs = [{
        "name": t.name,
        "description": t.description or "",
        "parameters": t.inputSchema or {"type": "object", "properties": {}}
    } for t in tools]
    print(f"[计时] 构建 tool_defs 耗时：{time.time() - t1:.3f} 秒")

    # 对话初始化
    messages = [{
        "role": "system",
        "content": (
            "你是一个智能 agent，可以决定是否调用相关工具来完成任务。"
            "当用户输入 'exit' 或 'quit' 时，结束对话。"
        )
    }]

    print("\n--- 开始对话，输入 'exit' 或 'quit' 退出 ---")
    async with mcp_client:
        while True:
            user_input = input("\n用户: ")
            if user_input.lower() in ("exit", "quit"):
                print("Agent: 再见！")
                break

            messages.append({"role": "user", "content": user_input})

            # 第一次模型推理（工具决策）
            t2 = time.time()
            inputs = tokenizer.apply_chat_template(
                messages,
                tools=tool_defs,
                add_generation_prompt=True,
                return_dict=True,
                return_tensors="pt",
            )
            inputs = {k: v.to(model.device) for k, v in inputs.items()}
            out = model.generate(**inputs, max_new_tokens=256)
            reply_str = tokenizer.decode(
                out[0][len(inputs["input_ids"][0]):],
                skip_special_tokens=True
            ).strip()
            print(f"[计时] 第一次推理耗时：{time.time() - t2:.3f} 秒")
            print(f"模型输出 (tool call): ```{reply_str}```")
            messages.append({"role": "assistant", "content": reply_str})

            # 如果检测到工具调用
            if is_tool_call(reply_str):
                calls = parse_tool_call(reply_str)
                for name, args in calls:
                    print(f"\n--- 调用工具：{name}，参数：{args} ---")
                    t3 = time.time()
                    res = await mcp_client.call_tool(name, args)
                    print(f"[计时] 工具 {name} 调用耗时：{time.time() - t3:.3f} 秒")
                    result = res.data if res else {}
                    print(f"工具返回: {result}")

                    messages.append({
                        "role": "tool",
                        "name": name,
                        "content": json.dumps(result, ensure_ascii=False)
                    })

                # --- 关键：第二次推理用 add_response_prompt=True ---
                t4 = time.time()
                inputs2 = tokenizer.apply_chat_template(
                    messages,
                    tools=tool_defs,               # 保留工具，但不再生成调用
                    add_response_prompt=True,      # 明确自然语言回答
                    return_dict=True,
                    return_tensors="pt",
                )
                inputs2 = {k: v.to(model.device) for k, v in inputs2.items()}
                out2 = model.generate(**inputs2, max_new_tokens=256)
                final = tokenizer.decode(
                    out2[0][len(inputs2["input_ids"][0]):],
                    skip_special_tokens=True
                ).strip()
                print(f"[计时] 第二次推理耗时：{time.time() - t4:.3f} 秒")
                print(f"\nAgent: {final}")
                messages.append({"role": "assistant", "content": final})
            else:
                # 直接回复（无工具调用）
                print(f"\nAgent: {reply_str}")

    print(f"\n[总计时] 会话总耗时：{time.time() - total_start:.3f} 秒")

if __name__ == "__main__":
    asyncio.run(chat_loop())
