import json

from openai import OpenAI
from typing import List
client = OpenAI(base_url="http://127.0.0.1:8000/v1", api_key="sk-jsha-1234567890")

# 极速前进 国家gpd等信息
# input_data = """
# import json
# import urllib.request
# import urllib.parse
# data = {}
# data["appkey"] = "your_appkey_here"
# data["name"]="中国"
# data["continent"]="亚洲"
# data["language"]="汉语"
# data["iscountry"]="0"
# data=urllib.parse.urlencode(data).encode('utf-8')
# url="https://api.jisuapi.com/country/query"
# result=urllib.request.urlopen(url,data)
# jsonarr=json.loads(result.read())
# if jsonarr["status"] != 0:
#     print(jsonarr["msg"])
#     print(jsonarr)
#     exit()
# result= jsonarr["result"][0]
# print(result["id"],result["name"],result["cname"],result["ename"],
#       result["capital"],result["nationalanthem"],result["currency"],result["code"],result["language"],
#       result["area"],result["timezone"],result["gdp"],result["avggdp"],
#       result["mainreligion"],result["political"],result["nationalflag"])
# """


# 血糖风险评估
# input_data = """
# import urllib, urllib3, sys, uuid
# import ssl
# host = 'https://hdl.market.alicloudapi.com'
# path = '/diabetes/getReport'
# method = 'POST'
# appcode = '你自己的AppCode'
# querys = 'age=18&sex=%E7%94%B7&type=diabetesRisk&weight=70&height=1.85&systolicPressure=130&diastolicPressure=100&familyHistoryOfDiabetes=%E5%90%A6%2C%E6%97%81%E7%B3%BB%E4%BA%B2%E5%B1%9E%EF%BC%88%E7%88%B7%E7%88%B7%2F%E5%A7%A5%E7%88%B7%E3%80%81%E5%A5%B6%E5%A5%B6%2F%E5%A7%A5%E5%A7%A5%E3%80%81%E5%A7%91%E3%80%81%E5%A7%A8%E3%80%81%E5%8F%94%E3%80%81%E4%BC%AF%E3%80%81%E8%88%85%E3%80%81%E8%A1%A8%2F%E5%A0%82%E5%85%84%E5%A6%B9%EF%BC%89%2C%E7%9B%B4%E7%B3%BB%E4%BA%B2%E5%B1%9E%EF%BC%88%E7%88%B6%E6%AF%8D%E3%80%81%E5%85%84%E5%A6%B9%E3%80%81%E5%AD%90%E5%A5%B3%EF%BC%89&historyOfHyperglycemia=%E5%90%A6&intakeOfVegetablesAndFruits=%E6%AF%8F%E5%A4%A9&waist=40&dailyExerciseTime=10'
# bodys = {}
# url = host + path + '?' + querys
# http = urllib3.PoolManager()
# headers = {
#     'X-Ca-Nonce': str(uuid.uuid4()), # 需要给X-Ca-Nonce的值生成随机字符串，每次请求不能相同
#     'Content-Type': 'application/json; charset=UTF-8',
#     'Authorization': 'APPCODE ' + appcode
# }
# bodys[''] = "{\"age\":\"18\",\"sex\":\"男\",\"weight\":\"70\",\"height\":\"1.85\",\"BMI\":\"25\",\"type\":\"diabetesRisk\",\"historyOfHyperglycemia\":\"否\",\"intakeOfVegetablesAndFruits\":\"每天\",\"waist\":\"40\",\"dailyExerciseTime\":\"10\",\"systolicPressure\":\"130\",\"diastolicPressure\":\"100\",\"familyHistoryOfDiabetes\":\"否\"}"
# post_data = bodys['']
# response = http.request('POST', url, body=post_data, headers=headers)
# content = response.data.decode('utf-8')
# if (content):
#     print(content)
# """

#接口包含全国所有知名不知名的景区景点、度假山庄、博物馆等信息。按省市分类，可模糊搜索。word、province、city三个参数必填其中一个。num参数默认1，最大15。
# input_data = """
# 接口地址：https://apis.tianapi.com/scenic/index
# 请求示例：https://apis.tianapi.com/scenic/index?key=你的APIKEY&word=虎丘
# 支持协议：http/https
# 请求方式：get/post
# 返回格式：utf-8 json
# """

# 查询英文单词释义
# input_data = """
# I want to create an agent to query the meaning of a certain word def define_word(word): response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}") if response.ok: definition = response.json()[0]["meanings"][0]["definitions"][0]["definition"] return f"{word}: {definition}" return "未找到释义" print(define_word("serendipity"))
# """

# wiki百科
# input_data = """
# 维基百科摘要（Knowledge 分类） I want to create an agent to query the summary information corresponding to a certain wiki . def wiki_summary(topic): response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}") if response.ok: return response.json() return "未找到相关信息" print(wiki_summary("Python"))
# """
file_path = '/Users/chenzi/project/zcbc/mofa/python/agent-hub/api-list/api_list/crawl_results_20250327_155352.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
# 自然语言创建agent
for i  in data:
    if i.get('llm_result',None) is not None:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": i.get('llm_result')},
            ],
        )
        print(f"完成 -> ",i.get('url'))