# # # import threading
# # # from mcp.server.fastmcp import FastMCP
# # #
# # # # 创建 FastMCP 实例
# # # mcp = FastMCP("Math")
# # #
# # # @mcp.tool()
# # # def add(a: int, b: int) -> int:
# # #     """Add two numbers"""
# # #     return a + b
# # #
# # # @mcp.tool()
# # # def multiply(a: int, b: int) -> int:
# # #     """Multiply two numbers"""
# # #     return a * b
# # #
# # #
# # #
# # # def run_server():
# # #     """在后台运行 MCP 服务器"""
# # #     mcp.run(transport="stdio")
# # #
# # # if __name__ == "__main__":
# # #     # 创建并启动一个新线程来运行服务器
# # #     server_thread = threading.Thread(target=run_server)
# # #     server_thread.daemon = True  # 设置为守护线程，确保主程序退出时线程也会退出
# # #     server_thread.start()
# # #
# # #     # 后续代码将在此处执行
# # #     print('服务器已在后台启动')
# # #     # 在此处添加其他需要执行的代码
# # #     while True:
# # #         pass
# #
# #
# #
# from mcp.server.fastmcp import FastMCP
#
# # Create an MCP server
# mcp = FastMCP()
#
# #### Tools ####
# # Add an addition tool
# @mcp.tool()
# def add(a: int, b: int) -> int:
#     """Add two numbers"""
#     print(f"Adding {a} and {b}")
#     return a + b
#
# # More tools can be added here
#
# #### Resources ####
# # Add a static resource
# @mcp.resource("resource://some_static_resource")
# def get_static_resource() -> str:
#     """Static resource data"""
#     return "Any static data can be returned"
#
#
# # Add a dynamic greeting resource
# @mcp.resource("greeting://{name}")
# def get_greeting(name: str) -> str:
#     """Get a personalized greeting"""
#     return f"Hello, {name}!"
#
#
# #### Prompts ####
# @mcp.prompt()
# def review_code(code: str) -> str:
#     return f"Please review this code:\n\n{code}"
#
#
# @mcp.prompt()
# def debug_error(error: str) -> list[tuple]:
#     return [
#         ("user", "I'm seeing this error:"),
#         ("user", error),
#         ("assistant", "I'll help debug that. What have you tried so far?"),
#     ]
#
#
# if __name__ == "__main__":
#     # Initialize and run the server
#     mcp.run(transport='sse')
