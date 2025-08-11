import os
import random
import socket
import psutil  # 用于获取系统信息，需要 pip install psutil
import platform  # 用于获取操作系统信息
import requests  # 用于进行网络请求
from datetime import datetime, timedelta
import shutil  # 用于文件复制、移动、删除等操作

from fastmcp import FastMCP
from fastmcp.server.context import Context  # 导入 Context

# 初始化 FastMCP 服务
mcp = FastMCP(name="my-free-local-ops-agent-server")



# 1. 获取当前系统时间
@mcp.tool(
    name='get_current_time_and_date',
    description='获取当前系统的日期和时间。'
)
async def get_current_time_and_date(ctx: Context) -> dict:
    """
    获取当前系统的日期和时间。
    """
    print("[FastMCP工具] get_current_time_and_date()")
    now = datetime.now()
    return {"current_time": now.strftime("%Y-%m-%d %H:%M:%S")}


# 2. 计算数学表达式
@mcp.tool(
    name='calculate_expression',
    description='计算一个简单的数学表达式。'
)
async def calculate_expression(ctx: Context, expression: str) -> dict:
    """
    计算一个简单的数学表达式。
    """
    print(f"[FastMCP工具] calculate_expression(expression='{expression}')")
    try:
        # 警告：eval 存在安全风险，在实际生产环境中不应直接使用用户输入的字符串
        result = eval(expression)
        return {"expression": expression, "result": result}
    except Exception as e:
        await ctx.error(f"计算表达式失败: {str(e)}")
        return {"error": f"计算表达式失败: {str(e)}"}


# 3. 获取随机事实
@mcp.tool(
    name='get_random_fact',
    description='获取一个有趣的随机事实。'
)
async def get_random_fact(ctx: Context) -> dict:
    """
    获取一个有趣的随机事实。
    """
    print("[FastMCP工具] get_random_fact()")
    facts = [
        "蜜蜂会跳舞来指示食物来源。",
        "企鹅是唯一一种不会飞的鸟，但它们是优秀的游泳者。",
        "人类的DNA有50%与香蕉的DNA相同。",
        "大象是唯一不会跳跃的哺乳动物。",
        "打喷嚏时，你的所有身体机能都会停止，甚至包括你的心脏。",
        "北极熊的皮肤是黑色的，毛发是透明的。",
        "一个完整的打哈欠会使你的身体降温。",
        "海马是唯一一种由雄性怀孕和生育的动物。",
        "你的左肺比右肺小，为心脏留出空间。",
        "袋鼠不能向后走。"
    ]
    return {"fact": random.choice(facts)}


# 4. 单位转换
@mcp.tool(
    name='convert_unit',
    description='进行单位转换。支持长度、温度、质量等常见单位。'
)
async def convert_unit(ctx: Context, value: float, from_unit: str, to_unit: str) -> dict:
    """
    进行单位转换。
    :param value: 要转换的数值。
    :param from_unit: 原始单位。
    :param to_unit: 目标单位。
    """
    print(f"[FastMCP工具] convert_unit(value={value}, from_unit='{from_unit}', to_unit='{to_unit}')")
    conversions = {
        ("meter", "kilometer"): lambda x: x / 1000,
        ("kilometer", "meter"): lambda x: x * 1000,
        ("meter", "centimeter"): lambda x: x * 100,
        ("centimeter", "meter"): lambda x: x / 100,
        ("celsius", "fahrenheit"): lambda x: (x * 9 / 5) + 32,
        ("fahrenheit", "celsius"): lambda x: (x - 32) * 5 / 9,
        ("pound", "kilogram"): lambda x: x * 0.453592,
        ("kilogram", "pound"): lambda x: x / 0.453592,
        ("liter", "milliliter"): lambda x: x * 1000,
        ("milliliter", "liter"): lambda x: x / 1000,
    }
    converter = conversions.get((from_unit.lower(), to_unit.lower()))
    if converter:
        return {"original_value": value, "from_unit": from_unit, "converted_value": converter(value),
                "to_unit": to_unit}
    return {"error": "不支持的单位转换。"}

# #
# 5. 生成随机整数
@mcp.tool(
    name='generate_random_number',
    description='生成指定范围内的随机整数。'
)
async def generate_random_number(ctx: Context, min_val: int, max_val: int) -> dict:
    """
    生成指定范围内的随机整数。
    """
    print(f"[FastMCP工具] generate_random_number(min_val={min_val}, max_val={max_val})")
    if min_val > max_val:
        return {"error": "最小值不能大于最大值。"}
    return {"random_number": random.randint(min_val, max_val)}


# 6. 发送模拟通知
@mcp.tool(
    name='send_notification',
    description='发送一条通知消息。这是一个模拟工具，不会真的发送。'
)
async def send_notification(ctx: Context, recipient: str, message: str) -> dict:
    """
    发送一条通知消息。
    """
    print(f"[FastMCP工具] send_notification(recipient='{recipient}', message='{message[:50]}...')")
    return {"status": "success", "message": f"通知已模拟发送至 {recipient}，内容：'{message}'", "source": "mock_data"}


# 7. 检查网站状态
@mcp.tool(
    name='check_website_status',
    description='检查一个网站是否可访问。'
)
async def check_website_status(ctx: Context, url: str) -> dict:
    """
    检查一个网站是否可访问。
    """
    print(f"[FastMCP工具] check_website_status(url='{url}')")
    try:
        response = requests.head(url, timeout=5)
        status_code = response.status_code
        if 200 <= status_code < 400:
            return {"url": url, "status": "online", "http_status_code": status_code, "source": "live_check"}
        else:
            await ctx.error(f"网站返回错误状态码: {status_code}")
            return {"url": url, "status": "offline_or_error", "http_status_code": status_code, "source": "live_check"}
    except requests.exceptions.RequestException as e:
        await ctx.error(f"检查网站状态失败: {str(e)}")
        return {"url": url, "status": "offline_or_error", "http_status_code": "N/A", "error_message": str(e),
                "source": "live_check"}
    except Exception as e:
        await ctx.error(f"检查网站状态时发生未知错误: {str(e)}")
        return {"url": url, "status": "error", "error_message": str(e), "source": "internal_error"}


# 8. 获取随机笑话
@mcp.tool(
    name='get_random_joke',
    description='获取一个随机的笑话。'
)
async def get_random_joke(ctx: Context) -> dict:
    """
    获取一个随机的笑话。
    """
    print("[FastMCP工具] get_random_joke()")
    jokes = [
        "为什么程序员总是穿黑色的衣服？因为他们不希望别人看到他们有 bug。",
        "一个栈去酒吧，服务员说：‘先进先出！’ 栈回答：‘不对，是后进先出！’",
        "有两个鸡蛋，一个煎鸡蛋说：‘我煎了！’ 另一个鸡蛋说：‘我还没煎呢！’",
        "如果一台电脑在下棋时作弊，那它就是一台骗子机。",
        "医生对病人说：‘你的病很严重，需要戒烟戒酒，还要戒掉和美女聊天。’ 病人说：‘前两条我能做到，第三条办不到。’ 医生问：‘为什么？’ 病人说：‘因为我不是在和美女聊天，而是在和帅哥聊天。’",
        "为什么数学书看起来总是很悲伤？因为它们充满了问题。",
        "我告诉我的妻子，我有一个奇怪的梦想，我被一个巨大的棉花糖追赶。她问：‘那很甜吗？’我说：‘我不知道，我醒了！’"
    ]
    return {"joke": random.choice(jokes)}

# #
# 9. 获取公网 IP 地址
@mcp.tool(
    name='get_public_ip_address',
    description='获取当前 FastMCP 服务器的公网 IP 地址。使用 ipify.org，免费且无需注册。'
)
async def get_public_ip_address(ctx: Context) -> dict:
    """
    获取当前 FastMCP 服务器的公网 IP 地址。
    """
    print("[FastMCP工具] get_public_ip_address() - 使用 ipify.org")
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        response.raise_for_status()
        ip_data = response.json()
        public_ip = ip_data.get("ip")
        if public_ip:
            return {"public_ip": public_ip, "source": "ipify.org"}
        else:
            await ctx.error("无法从 ipify.org 获取公网IP。")
            return {"error": "无法从 ipify.org 获取公网IP。", "source": "ipify.org"}
    except requests.exceptions.RequestException as e:
        await ctx.error(f"获取公网IP失败: {str(e)}")
        return {"error": f"获取公网IP失败: {str(e)}", "source": "network_error"}
    except Exception as e:
        await ctx.error(f"处理公网IP响应失败: {str(e)}")
        return {"error": f"处理公网IP响应失败: {str(e)}", "source": "internal_error"}


# 10. 获取系统信息
@mcp.tool(
    name='get_system_info',
    description='获取当前 FastMCP 服务器的操作系统和CPU信息。此工具无需外部API。'
)
async def get_system_info(ctx: Context) -> dict:
    """
    获取当前 FastMCP 服务器的操作系统和CPU信息。
    """
    print("[FastMCP工具] get_system_info()")
    return {
        "os_type": platform.system(),
        "os_version": platform.version(),
        "os_release": platform.release(),
        "processor": platform.processor(),
        "cpu_count": os.cpu_count(),
        "memory_total_gb": round(psutil.virtual_memory().total / (1024 ** 3), 2),
        "source": "local_system"
    }


# 11. 模拟 Ping 主机
@mcp.tool(
    name='ping_host',
    description='尝试ping一个主机或IP地址以检查其可达性。此工具模拟ping命令，无需外部API。'
)
async def ping_host(ctx: Context, host: str) -> dict:
    """
    尝试ping一个主机或IP地址以检查其可达性。
    """
    print(f"[FastMCP工具] ping_host(host='{host}') - 模拟ping")
    # 模拟ping命令的结果
    if "google.com" in host or "baidu.com" in host or "127.0.0.1" in host or "localhost" in host:
        return {"host": host, "status": "可达", "latency_ms": random.randint(20, 100), "loss_percent": 0,
                "source": "mock_ping"}
    else:
        await ctx.error(f"模拟ping失败，无法到达主机 '{host}'。")
        return {"host": host, "status": "不可达", "error_message": "模拟的ping失败", "loss_percent": 100,
                "source": "mock_ping"}


# 12. 获取磁盘使用情况
@mcp.tool(
    name='get_disk_usage',
    description='获取指定路径的磁盘使用情况（总空间、已用空间、可用空间）。此工具无需外部API。'
)
async def get_disk_usage(ctx: Context, path: str = '/') -> dict:
    """
    获取指定路径的磁盘使用情况。
    """
    print(f"[FastMCP工具] get_disk_usage(path='{path}')")
    try:
        usage = psutil.disk_usage(path)
        return {
            "path": path,
            "total_gb": round(usage.total / (1024 ** 3), 2),
            "used_gb": round(usage.used / (1024 ** 3), 2),
            "free_gb": round(usage.free / (1024 ** 3), 2),
            "percent_used": usage.percent,
            "source": "local_system"
        }
    except FileNotFoundError:
        await ctx.error(f"路径 '{path}' 未找到。")
        return {"error": f"路径 '{path}' 未找到。", "source": "local_system"}
    except Exception as e:
        await ctx.error(f"获取磁盘使用情况失败: {str(e)}")
        return {"error": f"获取磁盘使用情况失败: {str(e)}", "source": "local_system"}


# 13. 获取网络接口信息
@mcp.tool(
    name='get_network_interfaces',
    description='获取当前系统的网络接口信息。此工具无需外部API。'
)
async def get_network_interfaces(ctx: Context) -> dict:
    """
    获取当前系统的网络接口信息。
    """
    print("[FastMCP工具] get_network_interfaces()")
    interfaces = {}
    addrs = psutil.net_if_addrs()
    for iface_name, iface_addrs in addrs.items():
        details = []
        for addr in iface_addrs:
            if addr.family == socket.AF_INET:  # IPv4
                details.append({"address": addr.address, "netmask": addr.netmask, "broadcast": addr.broadcast})
            elif addr.family == socket.AF_INET6:  # IPv6
                details.append({"address": addr.address, "netmask": addr.netmask, "scope_id": addr.scopeid})
        if details:
            interfaces[iface_name] = details
    return {"network_interfaces": interfaces, "source": "local_system"}


# 14. 获取进程列表
@mcp.tool(
    name='get_process_list',
    description='获取当前系统上运行的进程列表（简化版，仅列出部分信息）。此工具无需外部API。'
)
async def get_process_list(ctx: Context) -> dict:
    """
    获取当前系统上运行的进程列表。
    """
    print("[FastMCP工具] get_process_list()")
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_percent']):
        try:
            pinfo = proc.info
            processes.append({
                "pid": pinfo['pid'],
                "name": pinfo['name'],
                "status": pinfo['status'],
                "cpu_percent": pinfo['cpu_percent'],
                "memory_percent": round(pinfo['memory_percent'], 2)
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    await ctx.report_progress(progress=50, message=f"已扫描 {len(processes)} 个进程，正在准备返回前10个。")
    return {"process_count": len(processes), "processes": processes[:10], "source": "local_system"}


# 15. 列出目录内容 (包括文件和文件夹)
@mcp.tool(
    name='list_directory_contents',
    description='列出指定本地文件目录下的所有文件和子目录的名称。'
)
async def list_directory_contents(ctx: Context, directory_path: str) -> dict:
    """
    列出指定本地文件目录下的所有文件和子目录的名称。
    """
    print(f"[FastMCP工具] list_directory_contents(directory_path='{directory_path}')")
    try:
        if not os.path.isdir(directory_path):
            await ctx.error(f"路径 '{directory_path}' 不是一个有效的目录。")
            return {"error": f"路径 '{directory_path}' 不是一个有效的目录。", "source": "local_system"}

        contents = os.listdir(directory_path)
        return {"directory": directory_path, "contents": contents, "source": "local_system"}
    except FileNotFoundError:
        await ctx.error(f"目录 '{directory_path}' 未找到。")
        return {"error": f"目录 '{directory_path}' 未找到。", "source": "local_system"}
    except PermissionError:
        await ctx.error(f"没有权限访问目录 '{directory_path}'。")
        return {"error": f"没有权限访问目录 '{directory_path}'。", "source": "local_system"}
    except Exception as e:
        await ctx.error(f"列出目录内容失败: {str(e)}")
        return {"error": f"列出目录内容失败: {str(e)}", "source": "local_system"}


# 16. 创建新目录
@mcp.tool(
    name='create_directory',
    description='在指定路径创建新目录。'
)
async def create_directory(ctx: Context, directory_path: str) -> dict:
    """
    在指定路径创建新目录。
    """
    print(f"[FastMCP工具] create_directory(directory_path='{directory_path}')")
    try:
        os.makedirs(directory_path, exist_ok=True)  # exist_ok=True 避免目录已存在时报错
        return {"status": "success", "message": f"目录 '{directory_path}' 已创建或已存在。", "source": "local_system"}
    except PermissionError:
        await ctx.error(f"没有权限在 '{directory_path}' 创建目录。")
        return {"error": f"没有权限在 '{directory_path}' 创建目录。", "source": "local_system"}
    except Exception as e:
        await ctx.error(f"创建目录失败: {str(e)}")
        return {"error": f"创建目录失败: {str(e)}", "source": "local_system"}
#
# #
# # 17. 删除文件
# @mcp.tool(
#     name='delete_file',
#     description='删除指定路径的文件。'
# )
# async def delete_file(ctx: Context, file_path: str) -> dict:
#     """
#     删除指定路径的文件。
#     """
#     print(f"[FastMCP工具] delete_file(file_path='{file_path}')")
#     try:
#         if not os.path.isfile(file_path):
#             await ctx.error(f"文件 '{file_path}' 不存在或不是一个文件。")
#             return {"error": f"文件 '{file_path}' 不存在或不是一个文件。", "source": "local_system"}
#         os.remove(file_path)
#         return {"status": "success", "message": f"文件 '{file_path}' 已删除。", "source": "local_system"}
#     except PermissionError:
#         await ctx.error(f"没有权限删除文件 '{file_path}'。")
#         return {"error": f"没有权限删除文件 '{file_path}'。", "source": "local_system"}
#     except Exception as e:
#         await ctx.error(f"删除文件失败: {str(e)}")
#         return {"error": f"删除文件失败: {str(e)}", "source": "local_system"}
#
#
# # 18. 删除空目录
# @mcp.tool(
#     name='delete_empty_directory',
#     description='删除指定路径的空目录。'
# )
# async def delete_empty_directory(ctx: Context, directory_path: str) -> dict:
#     """
#     删除指定路径的空目录。
#     """
#     print(f"[FastMCP工具] delete_empty_directory(directory_path='{directory_path}')")
#     try:
#         if not os.path.isdir(directory_path):
#             await ctx.error(f"路径 '{directory_path}' 不存在或不是一个目录。")
#             return {"error": f"路径 '{directory_path}' 不存在或不是一个目录。", "source": "local_system"}
#         if len(os.listdir(directory_path)) > 0:
#             await ctx.error(f"目录 '{directory_path}' 不为空，无法删除。")
#             return {"error": f"目录 '{directory_path}' 不为空，无法删除。", "source": "local_system"}
#         os.rmdir(directory_path)
#         return {"status": "success", "message": f"空目录 '{directory_path}' 已删除。", "source": "local_system"}
#     except PermissionError:
#         await ctx.error(f"没有权限删除目录 '{directory_path}'。")
#         return {"error": f"没有权限删除目录 '{directory_path}'。", "source": "local_system"}
#     except Exception as e:
#         await ctx.error(f"删除空目录失败: {str(e)}")
#         return {"error": f"删除空目录失败: {str(e)}", "source": "local_system"}
#
#
# # 19. 递归删除目录 (危险操作!)
# @mcp.tool(
#     name='delete_directory_recursively',
#     description='递归删除指定路径的目录及其所有内容。此操作不可逆，请谨慎使用！'
# )
# async def delete_directory_recursively(ctx: Context, directory_path: str) -> dict:
#     """
#     递归删除指定路径的目录及其所有内容。此操作不可逆，请谨慎使用！
#     """
#     print(f"[FastMCP工具] delete_directory_recursively(directory_path='{directory_path}') - !!! 危险操作 !!!")
#     await ctx.warning("警告：此操作将删除目录及其所有内容，不可逆！")
#     try:
#         if not os.path.isdir(directory_path):
#             await ctx.error(f"路径 '{directory_path}' 不存在或不是一个目录。")
#             return {"error": f"路径 '{directory_path}' 不存在或不是一个目录。", "source": "local_system"}
#
#         # 为了安全起见，这里可以添加一个额外的确认步骤，但FastMCP工具目前不支持互动式确认。
#         # 在实际应用中，你可能需要外部的确认机制。
#         shutil.rmtree(directory_path)
#         return {"status": "success", "message": f"目录 '{directory_path}' 及其所有内容已递归删除。",
#                 "source": "local_system"}
#     except PermissionError:
#         await ctx.error(f"没有权限递归删除目录 '{directory_path}'。")
#         return {"error": f"没有权限递归删除目录 '{directory_path}'。", "source": "local_system"}
#     except Exception as e:
#         await ctx.error(f"递归删除目录失败: {str(e)}")
#         return {"error": f"递归删除目录失败: {str(e)}", "source": "local_system"}
#
#
# # 20. 复制文件
# @mcp.tool(
#     name='copy_file',
#     description='复制一个文件到指定目标路径。'
# )
# async def copy_file(ctx: Context, source_path: str, destination_path: str) -> dict:
#     """
#     复制一个文件到指定目标路径。如果目标路径已存在同名文件，则会覆盖。
#     """
#     print(f"[FastMCP工具] copy_file(source_path='{source_path}', destination_path='{destination_path}')")
#     try:
#         if not os.path.isfile(source_path):
#             await ctx.error(f"源文件 '{source_path}' 不存在或不是一个文件。")
#             return {"error": f"源文件 '{source_path}' 不存在或不是一个文件。", "source": "local_system"}
#
#         shutil.copy2(source_path, destination_path)  # copy2 复制文件和元数据
#         return {"status": "success", "message": f"文件从 '{source_path}' 复制到 '{destination_path}' 成功。",
#                 "source": "local_system"}
#     except FileNotFoundError:
#         await ctx.error(f"目标目录不存在: '{os.path.dirname(destination_path)}'")
#         return {"error": f"目标目录不存在: '{os.path.dirname(destination_path)}'", "source": "local_system"}
#     except PermissionError:
#         await ctx.error(f"没有权限复制文件到 '{destination_path}'。")
#         return {"error": f"没有权限复制文件到 '{destination_path}'。", "source": "local_system"}
#     except Exception as e:
#         await ctx.error(f"复制文件失败: {str(e)}")
#         return {"error": f"复制文件失败: {str(e)}", "source": "local_system"}
#
#
# # 21. 移动/重命名文件或目录
# @mcp.tool(
#     name='move_or_rename_path',
#     description='移动或重命名文件或目录。'
# )
# async def move_or_rename_path(ctx: Context, source_path: str, destination_path: str) -> dict:
#     """
#     移动或重命名文件或目录。
#     :param source_path: 原始文件或目录的路径。
#     :param destination_path: 目标文件或目录的路径。
#     """
#     print(f"[FastMCP工具] move_or_rename_path(source_path='{source_path}', destination_path='{destination_path}')")
#     try:
#         if not os.path.exists(source_path):
#             await ctx.error(f"源路径 '{source_path}' 不存在。")
#             return {"error": f"源路径 '{source_path}' 不存在。", "source": "local_system"}
#
#         shutil.move(source_path, destination_path)
#         return {"status": "success", "message": f"'{source_path}' 已移动/重命名为 '{destination_path}'。",
#                 "source": "local_system"}
#     except PermissionError:
#         await ctx.error(f"没有权限移动/重命名 '{source_path}' 到 '{destination_path}'。")
#         return {"error": f"没有权限移动/重命名 '{source_path}' 到 '{destination_path}'。", "source": "local_system"}
#     except Exception as e:
#         await ctx.error(f"移动/重命名失败: {str(e)}")
#         return {"error": f"移动/重命名失败: {str(e)}", "source": "local_system"}
#
#
# # 22. 读取文本文件内容
# @mcp.tool(
#     name='read_text_file',
#     description='读取指定文本文件的内容。'
# )
# async def read_text_file(ctx: Context, file_path: str) -> dict:
#     """
#     读取指定文本文件的内容。
#     """
#     print(f"[FastMCP工具] read_text_file(file_path='{file_path}')")
#     try:
#         if not os.path.isfile(file_path):
#             await ctx.error(f"文件 '{file_path}' 不存在或不是一个文件。")
#             return {"error": f"文件 '{file_path}' 不存在或不是一个文件。", "source": "local_system"}
#
#         with open(file_path, 'r', encoding='utf-8') as f:
#             content = f.read()
#         return {"file_path": file_path, "content": content, "source": "local_system"}
#     except FileNotFoundError:
#         await ctx.error(f"文件 '{file_path}' 未找到。")
#         return {"error": f"文件 '{file_path}' 未找到。", "source": "local_system"}
#     except PermissionError:
#         await ctx.error(f"没有权限读取文件 '{file_path}'。")
#         return {"error": f"没有权限读取文件 '{file_path}'。", "source": "local_system"}
#     except UnicodeDecodeError:
#         await ctx.error(f"文件 '{file_path}' 不是有效的UTF-8编码文本文件，尝试其他编码。")
#         return {"error": f"文件 '{file_path}' 不是有效的UTF-8编码文本文件，尝试其他编码。", "source": "local_system"}
#     except Exception as e:
#         await ctx.error(f"读取文件失败: {str(e)}")
#         return {"error": f"读取文件失败: {str(e)}", "source": "local_system"}
#
#
# # 23. 写入文本文件内容 (会覆盖原有内容)
# @mcp.tool(
#     name='write_text_to_file',
#     description='将文本内容写入指定文件。如果文件不存在则创建，如果存在则覆盖。'
# )
# async def write_text_to_file(ctx: Context, file_path: str, content: str) -> dict:
#     """
#     将文本内容写入指定文件。
#     """
#     print(f"[FastMCP工具] write_text_to_file(file_path='{file_path}', content='{content[:50]}...')")
#     try:
#         # 确保目录存在
#         os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
#         with open(file_path, 'w', encoding='utf-8') as f:
#             f.write(content)
#         return {"status": "success", "message": f"内容已写入文件 '{file_path}'。", "source": "local_system"}
#     except PermissionError:
#         await ctx.error(f"没有权限写入文件 '{file_path}'。")
#         return {"error": f"没有权限写入文件 '{file_path}'。", "source": "local_system"}
#     except Exception as e:
#         await ctx.error(f"写入文件失败: {str(e)}")
#         return {"error": f"写入文件失败: {str(e)}", "source": "local_system"}
#
#
# # 24. 追加文本到文件
# @mcp.tool(
#     name='append_text_to_file',
#     description='将文本内容追加到指定文件末尾。如果文件不存在则创建。'
# )
# async def append_text_to_file(ctx: Context, file_path: str, content: str) -> dict:
#     """
#     将文本内容追加到指定文件末尾。
#     """
#     print(f"[FastMCP工具] append_text_to_file(file_path='{file_path}', content='{content[:50]}...')")
#     try:
#         os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
#         with open(file_path, 'a', encoding='utf-8') as f:
#             f.write(content)
#         return {"status": "success", "message": f"内容已追加到文件 '{file_path}'。", "source": "local_system"}
#     except PermissionError:
#         await ctx.error(f"没有权限追加内容到文件 '{file_path}'。")
#         return {"error": f"没有权限追加内容到文件 '{file_path}'。", "source": "local_system"}
#     except Exception as e:
#         await ctx.error(f"追加内容到文件失败: {str(e)}")
#         return {"error": f"追加内容到文件失败: {str(e)}", "source": "local_system"}
#
#
# # 25. 检查路径是否存在
# @mcp.tool(
#     name='check_path_exists',
#     description='检查指定路径（文件或目录）是否存在。'
# )
# async def check_path_exists(ctx: Context, path: str) -> dict:
#     """
#     检查指定路径（文件或目录）是否存在。
#     """
#     print(f"[FastMCP工具] check_path_exists(path='{path}')")
#     exists = os.path.exists(path)
#     is_file = os.path.isfile(path) if exists else False
#     is_dir = os.path.isdir(path) if exists else False
#     return {"path": path, "exists": exists, "is_file": is_file, "is_directory": is_dir, "source": "local_system"}
#
#
# # 26. 获取文件或目录的大小 (对于目录是其内容的总大小)
# @mcp.tool(
#     name='get_path_size',
#     description='获取指定文件或目录的大小（以字节为单位）。对于目录，返回其所有内容的汇总大小。'
# )
# async def get_path_size(ctx: Context, path: str) -> dict:
#     """
#     获取指定文件或目录的大小（以字节为单位）。对于目录，返回其所有内容的汇总大小。
#     """
#     print(f"[FastMCP工具] get_path_size(path='{path}')")
#     try:
#         if not os.path.exists(path):
#             await ctx.error(f"路径 '{path}' 不存在。")
#             return {"error": f"路径 '{path}' 不存在。", "source": "local_system"}
#
#         total_size = 0
#         if os.path.isfile(path):
#             total_size = os.path.getsize(path)
#         elif os.path.isdir(path):
#             for dirpath, dirnames, filenames in os.walk(path):
#                 for f in filenames:
#                     fp = os.path.join(dirpath, f)
#                     if not os.path.islink(fp):  # 避免计算符号链接文件的大小
#                         total_size += os.path.getsize(fp)
#         return {"path": path, "size_bytes": total_size, "source": "local_system"}
#     except PermissionError:
#         await ctx.error(f"没有权限访问路径 '{path}'。")
#         return {"error": f"没有权限访问路径 '{path}'。", "source": "local_system"}
#     except Exception as e:
#         await ctx.error(f"获取路径大小失败: {str(e)}")
#         return {"error": f"获取路径大小失败: {str(e)}", "source": "local_system"}
#
#
# # 27. 获取文件或目录的创建/修改时间
# @mcp.tool(
#     name='get_path_timestamps',
#     description='获取指定文件或目录的创建时间、最后修改时间、最后访问时间。'
# )
# async def get_path_timestamps(ctx: Context, path: str) -> dict:
#     """
#     获取指定文件或目录的创建时间、最后修改时间、最后访问时间。
#     时间格式为 ISO 8601 字符串。
#     """
#     print(f"[FastMCP工具] get_path_timestamps(path='{path}')")
#     try:
#         if not os.path.exists(path):
#             await ctx.error(f"路径 '{path}' 不存在。")
#             return {"error": f"路径 '{path}' 不存在。", "source": "local_system"}
#
#         # 获取时间戳（以秒为单位）
#         ctime_ts = os.path.getctime(path)  # 创建时间
#         mtime_ts = os.path.getmtime(path)  # 最后修改时间
#         atime_ts = os.path.getatime(path)  # 最后访问时间
#
#         # 转换为 datetime 对象并格式化
#         ctime_str = datetime.fromtimestamp(ctime_ts).isoformat()
#         mtime_str = datetime.fromtimestamp(mtime_ts).isoformat()
#         atime_str = datetime.fromtimestamp(atime_ts).isoformat()
#
#         return {
#             "path": path,
#             "creation_time": ctime_str,
#             "modification_time": mtime_str,
#             "access_time": atime_str,
#             "source": "local_system"
#         }
#     except FileNotFoundError:
#         await ctx.error(f"路径 '{path}' 未找到。")
#         return {"error": f"路径 '{path}' 未找到。", "source": "local_system"}
#     except PermissionError:
#         await ctx.error(f"没有权限访问路径 '{path}' 的时间戳信息。")
#         return {"error": f"没有权限访问路径 '{path}' 的时间戳信息。", "source": "local_system"}
#     except Exception as e:
#         await ctx.error(f"获取时间戳失败: {str(e)}")
#         return {"error": f"获取时间戳失败: {str(e)}", "source": "local_system"}
#
#
# # 28. 获取当前工作目录
# @mcp.tool(
#     name='get_current_working_directory',
#     description='获取当前Python脚本的运行目录。'
# )
# async def get_current_working_directory(ctx: Context) -> dict:
#     """
#     获取当前Python脚本的运行目录。
#     """
#     print("[FastMCP工具] get_current_working_directory()")
#     cwd = os.getcwd()
#     return {"current_working_directory": cwd, "source": "local_system"}
#
#
# # 29. 更改当前工作目录
# @mcp.tool(
#     name='change_current_working_directory',
#     description='更改当前Python脚本的工作目录。'
# )
# async def change_current_working_directory(ctx: Context, new_directory: str) -> dict:
#     """
#     更改当前Python脚本的工作目录。
#     """
#     print(f"[FastMCP工具] change_current_working_directory(new_directory='{new_directory}')")
#     try:
#         os.chdir(new_directory)
#         return {"status": "success", "message": f"工作目录已更改为 '{new_directory}'。", "source": "local_system"}
#     except FileNotFoundError:
#         await ctx.error(f"目录 '{new_directory}' 不存在。")
#         return {"error": f"目录 '{new_directory}' 不存在。", "source": "local_system"}
#     except PermissionError:
#         await ctx.error(f"没有权限更改到目录 '{new_directory}'。")
#         return {"error": f"没有权限更改到目录 '{new_directory}'。", "source": "local_system"}
#     except Exception as e:
#         await ctx.error(f"更改工作目录失败: {str(e)}")
#         return {"error": f"更改工作目录失败: {str(e)}", "source": "local_system"}
#
#
# # 30. 获取环境变量
# @mcp.tool(
#     name='get_environment_variable',
#     description='获取指定环境变量的值。'
# )
# async def get_environment_variable(ctx: Context, variable_name: str) -> dict:
#     """
#     获取指定环境变量的值。
#     """
#     print(f"[FastMCP工具] get_environment_variable(variable_name='{variable_name}')")
#     value = os.getenv(variable_name)
#     if value is not None:
#         return {"variable_name": variable_name, "value": value, "source": "local_system"}
#     else:
#         return {"variable_name": variable_name, "value": None, "message": f"环境变量 '{variable_name}' 未设置。",
#                 "source": "local_system"}
#
#
# # 31. 运行简单的系统命令 (警告: 安全风险)
# @mcp.tool(
#     name='run_simple_system_command',
#     description='运行一个简单的系统命令并返回其输出。存在安全风险，请谨慎使用！'
# )
# async def run_simple_system_command(ctx: Context, command: str) -> dict:
#     """
#     运行一个简单的系统命令并返回其输出。
#     """
#     print(f"[FastMCP工具] run_simple_system_command(command='{command}') - !!! 潜在安全风险 !!!")
#     await ctx.warning("警告：运行系统命令存在安全风险，请确保命令安全。")
#     try:
#         # 使用 subprocess.run 更安全，但为了简单演示，这里使用 os.popen
#         # 实际生产环境应使用 subprocess 模块，并仔细处理用户输入。
#         with os.popen(command) as p:
#             output = p.read()
#         return {"command": command, "output": output, "status": "success", "source": "local_system"}
#     except Exception as e:
#         await ctx.error(f"执行命令失败: {str(e)}")
#         return {"command": command, "error": f"执行命令失败: {str(e)}", "source": "local_system"}
#
# # 1. 获取当前经纬度 (通过IP地址反查)
# @mcp.tool(
#     name='get_current_location_by_ip',
#     description='通过公共IP地址反查当前的近似经纬度和城市信息。基于 ip-api.com，免费且无需注册。'
# )
# async def get_current_location_by_ip(ctx: Context) -> dict:
#     """
#     通过公共IP地址反查当前的近似经纬度和城市信息。
#     """
#     print("[FastMCP工具] get_current_location_by_ip()")
#     await ctx.report_progress(progress=20, message="正在通过IP地址获取当前位置信息...")
#     url = "http://ip-api.com/json/?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query"
#     try:
#         response = requests.get(url, timeout=5)
#         response.raise_for_status()
#         data = response.json()
#
#         if data.get('status') == 'success':
#             location_info = {
#                 "latitude": data.get('lat'),
#                 "longitude": data.get('lon'),
#                 "city": data.get('city'),
#                 "region_name": data.get('regionName'),
#                 "country": data.get('country'),
#                 "timezone": data.get('timezone'),
#                 "public_ip": data.get('query') # API返回的IP
#             }
#             await ctx.report_progress(progress=100, message="位置信息获取成功。")
#             return {"location_info": location_info, "source": "ip-api.com"}
#         else:
#             error_message = data.get('message', '未知错误')
#             await ctx.error(f"从 ip-api.com 获取位置信息失败: {error_message}")
#             return {"error": f"获取位置信息失败: {error_message}", "source": "ip-api.com"}
#     except requests.exceptions.RequestException as e:
#         await ctx.error(f"调用 ip-api.com API 失败: {str(e)}")
#         return {"error": f"获取位置信息失败: {str(e)}", "source": "ip-api.com"}
#     except Exception as e:
#         await ctx.error(f"处理 ip-api.com 响应失败: {str(e)}")
#         return {"error": f"处理位置信息响应失败: {str(e)}", "source": "ip-api.com"}
#
# # 2. 获取当前的公共 IP 地址 (使用 ipify.org)
# @mcp.tool(
#     name='get_public_ip_address',
#     description='获取当前 FastMCP 服务器的公网 IP 地址。使用 ipify.org，免费且无需注册。'
# )
# async def get_public_ip_address(ctx: Context) -> dict:
#     """
#     获取当前 FastMCP 服务器的公网 IP 地址。
#     """
#     print("[FastMCP工具] get_public_ip_address() - 使用 ipify.org")
#     await ctx.report_progress(progress=30, message="正在获取公共IP地址...")
#     try:
#         response = requests.get("https://api.ipify.org?format=json", timeout=5)
#         response.raise_for_status()
#         ip_data = response.json()
#         public_ip = ip_data.get("ip")
#         if public_ip:
#             await ctx.report_progress(progress=100, message="公共IP地址获取成功。")
#             return {"public_ip": public_ip, "source": "ipify.org"}
#         else:
#             await ctx.error("无法从 ipify.org 获取公网IP。")
#             return {"error": "无法从 ipify.org 获取公网IP。", "source": "ipify.org"}
#     except requests.exceptions.RequestException as e:
#         await ctx.error(f"获取公网IP失败: {str(e)}")
#         return {"error": f"获取公网IP失败: {str(e)}", "source": "network_error"}
#     except Exception as e:
#         await ctx.error(f"处理公网IP响应失败: {str(e)}")
#         return {"error": f"处理公网IP响应失败: {str(e)}", "source": "internal_error"}


# --- FastMCP 服务器启动部分 ---
if __name__ == "__main__":
    print("FastMCP 服务器正在启动，所有工具均基于免费公共API或本地系统操作。")
    print("总计工具数量：33 个。")
    print("请确保已安装必要的库: pip install fastmcp requests psutil")

    # 启动 HTTP SSE Server，供客户端调用
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=9000,
    )


