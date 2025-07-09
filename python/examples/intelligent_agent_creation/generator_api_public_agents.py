# import json
# import time
# from openai import OpenAI
#
# # file_path = '/Users/chenzi/chenzi/project/zcbc/mofa/python/agent-hub/freepublic-apis/agent/freepublic-apis.json'
# file_path = '/Users/chenzi/project/zcbc/mofa/python/agent-hub/freepublic-apis/agent/freepublic-apis.json'
#
# def read_json_lines(file_path):
#     """
#     读取 JSON lines 文件，返回所有条目列表
#     """
#     entries = []
#     with open(file_path, "r", encoding="utf-8") as f:
#         for line in f:
#             try:
#                 entry = json.loads(line)
#                 entries.append(entry)
#             except json.JSONDecodeError as e:
#                 print(f"JSON decode error: {e}")
#     return entries
#
# def save_json_lines(entries, file_path):
#     """
#     将 JSON 对象列表写入文件，每行一个 JSON
#     """
#     with open(file_path, "w", encoding="utf-8") as f:
#         for entry in entries:
#             f.write(json.dumps(entry, ensure_ascii=False) + "\n")
#
# if __name__ == "__main__":
#     all_data = read_json_lines(file_path)
#
#     new_agent_apis = []
#     error_url_apis = []
#
#     client = OpenAI(base_url="http://127.0.0.1:8025/v1", api_key="sk-jsha-1234567890")
#
#     for api_data in all_data:
#         # 只处理 success=True 且 node_gen 为 False 或缺失 的项
#         if api_data.get("success") and not api_data.get("node_gen", False):
#             t1 = time.time()
#             try:
#                 response = client.chat.completions.create(
#                     model="gpt-4o-mini",
#                     messages=[
#                         {"role": "system", "content": "You are a helpful assistant."},
#                         {"role": "user", "content":'i want create node : this is node code ' + str(json.dumps(api_data.get('data')))},
#                     ],
#                 )
#                 print(f"完成 -> {api_data.get('url')}")
#                 new_agent_apis.append(api_data.get('url'))
#                 api_data["node_gen"] = True  # 标记为已处理
#                 print('消耗时间 -> ', time.time() - t1)
#                 print('------------')
#             except Exception as e:
#                 print(e)
#                 print('Error data', api_data)
#                 error_url_apis.append(api_data.get('url'))
#                 api_data["node_gen"] = False  # 保留未处理状态
#
#     # 回写状态到文件（覆盖原文件）
#     save_json_lines(all_data, file_path)
#
#     print('✅ 处理完成')
#     print('正确的是 ->', new_agent_apis)
#     print('错误的是 ->', error_url_apis)
import json
import time
from openai import OpenAI

file_path = '/Users/chenzi/project/zcbc/mofa/python/agent-hub/freepublic-apis/agent/freepublic-apis.json'

def read_json_lines(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def append_json_line(entry, file_path):
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    all_data = read_json_lines(file_path)

    # 备份原始文件（可选）
    with open(file_path + ".bak", "w", encoding="utf-8") as backup:
        for entry in all_data:
            backup.write(json.dumps(entry, ensure_ascii=False) + "\n")

    client = OpenAI(base_url="http://127.0.0.1:8025/v1", api_key="sk-jsha-1234567890")

    # 清空原文件，逐行重新写入
    with open(file_path, "w", encoding="utf-8") as f:
        pass

    for api_data in all_data:
        # 只处理 success=True 且 node_gen 为 False 的项
        if api_data.get("success") and not api_data.get("node_gen", False):
            t1 = time.time()
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": 'i want create node : this is node code ' + str(json.dumps(api_data.get('data')))},
                    ],
                )
                print(f"✅ 完成 -> {api_data.get('url')}")
                api_data["node_gen"] = True
                print('⏱️ 消耗时间 ->', time.time() - t1)
                print('------------')
            except Exception as e:
                print(f"❌ 错误 -> {api_data.get('url')} | {e}")
                api_data["node_gen"] = False  # 保留原状态

        # 不管成功失败，都写入这一行
        append_json_line(api_data, file_path)

    print('✅ 所有数据处理完成')

