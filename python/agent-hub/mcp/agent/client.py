import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 定义服务器参数，假设您的服务器脚本名为 'server.py'
server_params = StdioServerParameters(
    command='python',
    args=['server.py'],
    env=None
)

async def main():
    # 创建与服务器的连接
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化会话
            await session.initialize()

            # 列出可用工具
            tools = await session.list_tools()
            print("可用工具:")
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

            # 调用 'add' 工具
            result_add = await session.call_tool('add', {'a': 5, 'b': 3})
            print(f"5 + 3 = {result_add.content[0].text}")

            # 调用 'multiply' 工具
            result_multiply = await session.call_tool('multiply', {'a': 5, 'b': 3})
            print(f"5 * 3 = {result_multiply.content[0].text}")

# 运行客户端
if __name__ == '__main__':
    asyncio.run(main())
