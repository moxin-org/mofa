# import json
#
# import requests
# url = "http://127.0.0.1:8010/agent_evaluation"  # Replace with your actual FastAPI server address and endpoint
# headers = {
#     "accept": "application/json",
#     "Content-Type": "application/json"
# }
# params = {
#                 "primary_data": '/Users/chenzi/project/zcbc/Moxin-App-Engine/mae/agent-applications/content_evaluation/first_data.md',
#                 "second_data": '/Users/chenzi/project/zcbc/Moxin-App-Engine/mae/agent-applications/content_evaluation/second_data.md',
#                 "comparison_data_task": '第二次世界大战'
#             }
# response = requests.post(url, data=json.dumps(params), headers=headers)
# print(response.json().get('data'))