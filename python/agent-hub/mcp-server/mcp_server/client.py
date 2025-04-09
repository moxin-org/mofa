# import asyncio
# from mcp import ClientSession, StdioServerParameters
# from mcp.client.stdio import stdio_client
#
# # 定义服务器参数，假设您的服务器脚本名为 'server.py'
# server_params = StdioServerParameters(
#     command='python',
#     args=['server.py'],
#     env=None
# )
#
# async def main():
#     # 创建与服务器的连接
#     async with stdio_client(server_params) as (read, write):
#         async with ClientSession(read, write) as session:
#             # 初始化会话
#             await session.initialize()
#
#             # 列出可用工具
#             tools = await session.list_tools()
#             print("可用工具:")
#             for tool in tools.tools:
#                 print(f"- {tool.name}: {tool.description}")
#                 print('------------------------------------------')
#
#             # 调用 'add' 工具
#             # result_add = await session.call_tool('add', {'a': 5, 'b': 3})
#             # print(f"5 + 3 = {result_add.content[0].text}")
#
#             # # 调用 'multiply' 工具
#             # result_multiply = await session.call_tool('multiply', {'a': 5, 'b': 3})
#             # print(f"5 * 3 = {result_multiply.content[0].text}")
#
# # 运行客户端
# if __name__ == '__main__':
#     asyncio.run(main())
from mcp import ClientSession
from mcp.client.sse import sse_client


async def run():
    async with sse_client(url="http://127.0.0.1:8000/sse") as streams:
        async with ClientSession(*streams) as session:

            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print(tools)

            # Call a tool
            # result = await session.call_tool("add", arguments={"a": 4, "b": 5})
            # print(result.content[0].text)
            #
            # # List available resources
            # resources = await session.list_resources()
            # print("resources", resources)
            #
            # # Read a resource
            # content = await session.read_resource("resource://some_static_resource")
            # print("content", content.contents[0].text)
            #
            # # Read a resource
            # content = await session.read_resource("greeting://yash")
            # print("content", content.contents[0].text)
            #
            # # List available prompts
            # prompts = await session.list_prompts()
            # print("prompts", prompts)
            #
            # # Get a prompt
            # prompt = await session.get_prompt(
            #     "review_code", arguments={"code": "print(\"Hello world\")"}
            # )
            # print("prompt", prompt)
            #
            # prompt = await session.get_prompt(
            #     "debug_error", arguments={"error": "SyntaxError: invalid syntax"}
            # )
            # print("prompt", prompt)


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())

