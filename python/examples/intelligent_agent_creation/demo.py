from openai import OpenAI
from typing import List
client = OpenAI(base_url="http://127.0.0.1:8000/v1", api_key="sk-jsha-1234567890")
input_data = """
加班记录同步
接口说明: 同步员工的加班记录。
请求方式:POST（HTTPS）
请求地址:https://api.xinrenxinshi.com/v5/attendance/sync/overtime
请求Header:
key	value
access_token	获取的access_token的实际值
Query参数:
key	value
sign	签名值
Body参数:
参数	类型	必传(Y/N)	说明
employeeId	String	Y	员工id
overtimeDate	String	Y	所属考勤日,yyyy-MM-dd
startTime	String	Y	开始时间，HH:mm
endTime	String	Y	结束时间，HH:mm
overtimeHour	Double	Y	加班小时数
compensationWay	Integer	Y	补偿方式 1:调休 2:加班费 0:无补偿
expireDate	String	N	过期时间, yyyy-MM-dd,若不填,则表示该加班记录为永久有效
timestamp	Long	Y	请求时间戳（精确到毫秒）
返回结果:
参数	类型	必传(Y/N)	说明
errcode	Integer	Y	0成功，其他失败
errmsg	String	Y	结果描述
"""
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": input_data},
    ],
)
print(f"output -> ",response.choices[0].message.content)