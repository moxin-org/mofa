
import json
import os # 导入 os 模块用于检查文件是否存在
from openai import OpenAI
def append_data_to_json_lines(file_path, new_data):
    """
    将一个 Python 字典（或列表）作为独立的 JSON 对象追加到 JSON Lines 文件。

    Args:
        file_path (str): 要写入的 JSON Lines 文件路径。
        new_data (dict or list): 要追加的数据（一个 Python 字典或列表）。
    """
    try:
        # 将新数据转换为 JSON 格式字符串，注意 ensure_ascii=False 处理中文
        json_string = json.dumps(new_data, ensure_ascii=False)

        # 使用追加模式 'a' 打开文件，并添加换行符
        # 'a' 模式会在文件末尾追加内容
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(json_string + '\n') # 写入 JSON 字符串，并加上换行符

        print(f"数据已追加到 {file_path}")

    except IOError as e:
        print(f"写入文件时发生 I/O 错误: {e}")
    except Exception as e:
        print(f"发生其他错误: {e}")
if __name__ == "__main__":
    file_path = 'Speakers.json'
    with open(file_path, 'r', encoding='utf-8') as f:
        # 使用 json.load() 从文件中读取数据
        data = json.load(f)
    speakers = data.get('speakers', [])
    new_json_file = 'new_speakers.json'
    client = OpenAI(base_url="http://127.0.0.1:8000/v1", api_key="***REMOVED***jsha-1234567890")

    if len(speakers) > 0:
        for speaker in speakers:

        #     user_input = """
        #     Sray Agarwal
        # Head of Responsible AI (EMEA & APAC) at Infosys
        # linkedin
        # Sray Agarwal has applied AI and analytics from Financial Services to Hospitality and has led the development of Responsible AI framework for multiple banks in the UK and the US.
        # Based out of London, his is conversant in Predictive Modelling, Forecasting and advanced Machine Learning with profound knowledge of algorithms and advanced statistic, Sray is Head of Responsible AI (EMEA & APAC) at Infosys.
        # He is an active blogger and has given his talks on Ethical AI at major AI conferences across the globe (more than 20) and has podcasts, video interviews and lectures on reputed websites and social media at United Nations, Microsoft, ODSC to name a few.
        # His contribution to the development of the technology was recognised by Microsoft when he won the Most Valued Professional in AI award in 2020 to 2025. He is also an expert for United Nations (UNCEFACT) and have recently authored a book on Responsible AI published by Springer.
        # He has been a trainer with leading consulting firms and have delivered training on business transformation using AI. He is guest lecturer at Jio institute. He holds patents on RAI system and methods.
        #     """
            user_input = json.dumps(speaker)
            response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content":user_input},
            ],
            )
            result = response.choices[0].message
            speaker['pedia'] = result
            append_data_to_json_lines(file_path=new_json_file,new_data=speaker)
            print(response)
