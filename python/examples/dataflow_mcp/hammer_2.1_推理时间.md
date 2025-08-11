[计时] 本地 LLM 客户端初始化耗时：14.885 秒
[计时] FastMCP 客户端创建 + 列表工具耗时：0.159 秒

--- FastMCP 可用工具列表 ---
1. get_current_time_and_date — 获取当前系统的日期和时间。
2. calculate_expression — 计算一个简单的数学表达式。
3. get_random_fact — 获取一个有趣的随机事实。
4. convert_unit — 进行单位转换。支持长度、温度、质量等常见单位。
------------------------------

[计时] 构建 tool_defs 耗时：0.000 秒

--- 开始对话，输入 'exit' 或 'quit' 退出 ---

用户: 当前的系统时间
[计时] 第一次推理耗时：3.685 秒
模型输出 (tool call): ``````
[{'name': 'get_current_time_and_date', 'arguments': {}}]
``````

--- 调用工具：get_current_time_and_date，参数：{} ---
[计时] 工具 get_current_time_and_date 调用耗时：0.029 秒
工具返回: {'current_time': '2025-08-07 08:09:11'}
[计时] 第二次推理耗时：1.379 秒

Agent: ```
[]
```

用户: 计算 3*20—21+1212
[计时] 第一次推理耗时：3.951 秒
模型输出 (tool call): ``````
[{'name': 'calculate_expression', 'arguments': {'expression': '3*20-21+1212'}}]
``````

--- 调用工具：calculate_expression，参数：{'expression': '3*20-21+1212'} ---
[计时] 工具 calculate_expression 调用耗时：0.006 秒
工具返回: {'expression': '3*20-21+1212', 'result': 1251}
[计时] 第二次推理耗时：1.520 秒

Agent: ```
[]
```

------
/Users/chenzi/env/miniconda3/envs/py310/bin/python /Users/chenzi/project/zcbc/mofa/python/examples/dataflow_mcp/hammer2.1_local.py 
Loading checkpoint shards: 100%|██████████| 4/4 [00:11<00:00,  2.93s/it]
[计时] 本地 LLM 客户端初始化耗时：12.593 秒
[计时] FastMCP 客户端创建 + 列表工具耗时：0.094 秒

--- FastMCP 可用工具列表 ---
1. get_current_time_and_date — 获取当前系统的日期和时间。
2. calculate_expression — 计算一个简单的数学表达式。
3. get_random_fact — 获取一个有趣的随机事实。
4. convert_unit — 进行单位转换。支持长度、温度、质量等常见单位。
5. generate_random_number — 生成指定范围内的随机整数。
6. send_notification — 发送一条通知消息。这是一个模拟工具，不会真的发送。
7. check_website_status — 检查一个网站是否可访问。
8. get_random_joke — 获取一个随机的笑话。
------------------------------

[计时] 构建 tool_defs 耗时：0.000 秒

--- 开始对话，输入 'exit' 或 'quit' 退出 ---

用户: 检查google.com是否可以访问
[计时] 第一次推理耗时：4.174 秒
模型输出 (tool call): ``````
[{"name": "check_website_status", "arguments": {"url": "https://www.google.com"}}]
``````

--- 调用工具：check_website_status，参数：{'url': 'https://www.google.com'} ---
[计时] 工具 check_website_status 调用耗时：1.193 秒
工具返回: {'url': 'https://www.google.com', 'status': 'online', 'http_status_code': 200, 'source': 'live_check'}
[计时] 第二次推理耗时：2.219 秒

Agent: ```
[]
```

用户: 获取当前时间
[计时] 第一次推理耗时：3.553 秒
模型输出 (tool call): ``````
[{"name": "get_current_time_and_date", "arguments": {}}]
``````

--- 调用工具：get_current_time_and_date，参数：{} ---
[计时] 工具 get_current_time_and_date 调用耗时：0.004 秒
工具返回: {'current_time': '2025-08-07 08:12:43'}
[计时] 第二次推理耗时：1.941 秒

Agent: ```
[]
```

用户: 发送一个消息 你今天过的还好吗 
[计时] 第一次推理耗时：5.548 秒
模型输出 (tool call): ``````
[{"name": "send_notification", "arguments": {"recipient": "default_recipient", "message": "你今天过的还好吗"}}]
``````

--- 调用工具：send_notification，参数：{'recipient': 'default_recipient', 'message': '你今天过的还好吗'} ---
[计时] 工具 send_notification 调用耗时：0.017 秒
工具返回: {'status': 'success', 'message': "通知已模拟发送至 default_recipient，内容：'你今天过的还好吗'", 'source': 'mock_data'}
[计时] 第二次推理耗时：2.570 秒

Agent: ```
[]
```

-------


/Users/chenzi/env/miniconda3/envs/py310/bin/python /Users/chenzi/project/zcbc/mofa/python/examples/dataflow_mcp/hammer2.1_local.py 
Loading checkpoint shards: 100%|██████████| 4/4 [00:10<00:00,  2.57s/it]
[计时] 本地 LLM 客户端初始化耗时：11.118 秒
[计时] FastMCP 客户端创建 + 列表工具耗时：0.090 秒

--- FastMCP 可用工具列表 ---
1. get_current_time_and_date — 获取当前系统的日期和时间。
2. calculate_expression — 计算一个简单的数学表达式。
3. get_random_fact — 获取一个有趣的随机事实。
4. convert_unit — 进行单位转换。支持长度、温度、质量等常见单位。
5. generate_random_number — 生成指定范围内的随机整数。
6. send_notification — 发送一条通知消息。这是一个模拟工具，不会真的发送。
7. check_website_status — 检查一个网站是否可访问。
8. get_random_joke — 获取一个随机的笑话。
9. get_public_ip_address — 获取当前 FastMCP 服务器的公网 IP 地址。使用 ipify.org，免费且无需注册。
10. get_system_info — 获取当前 FastMCP 服务器的操作系统和CPU信息。此工具无需外部API。
11. ping_host — 尝试ping一个主机或IP地址以检查其可达性。此工具模拟ping命令，无需外部API。
12. get_disk_usage — 获取指定路径的磁盘使用情况（总空间、已用空间、可用空间）。此工具无需外部API。
13. get_network_interfaces — 获取当前系统的网络接口信息。此工具无需外部API。
14. get_process_list — 获取当前系统上运行的进程列表（简化版，仅列出部分信息）。此工具无需外部API。
15. list_directory_contents — 列出指定本地文件目录下的所有文件和子目录的名称。
16. create_directory — 在指定路径创建新目录。
------------------------------

[计时] 构建 tool_defs 耗时：0.000 秒

--- 开始对话，输入 'exit' 或 'quit' 退出 ---

用户: 获取当前的ip是多少
[计时] 第一次推理耗时：2.885 秒
模型输出 (tool call): ``````
[]
``````
[计时] 第二次推理耗时：3.692 秒

Agent: ```
[{"name": "get_public_ip_address", "arguments": {}}]
```

用户: 获取当前的时间
[计时] 第一次推理耗时：4.313 秒
模型输出 (tool call): ``````
[{"name": "get_current_time_and_date", "arguments": {}}]
``````

--- 调用工具：get_current_time_and_date，参数：{} ---
[计时] 工具 get_current_time_and_date 调用耗时：0.010 秒
工具返回: {'current_time': '2025-08-07 08:15:56'}
[计时] 第二次推理耗时：2.609 秒

Agent: ```
[]
```

用户: 获取当前的磁盘占用
[计时] 第一次推理耗时：4.248 秒
模型输出 (tool call): ``````
[{"name": "get_disk_usage", "arguments": {}}]
``````

--- 调用工具：get_disk_usage，参数：{} ---
[计时] 工具 get_disk_usage 调用耗时：0.004 秒
工具返回: {'path': '/', 'total_gb': 926.35, 'used_gb': 778.34, 'free_gb': 148.01, 'percent_used': 84.0, 'source': 'local_system'}
[计时] 第二次推理耗时：2.761 秒

Agent: ```
[]
```

