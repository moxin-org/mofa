import json
import os

from mofa.utils.ai.conn import create_openai_client
from mofa.utils.files.util import get_all_files
from pathlib import Path
def get_llm_response(client,messages:list, model_name:str='gpt-4o',stream:bool=False):
    response = client.chat.completions.create(
        model=os.environ['LLM_MODEL_NAME'] if os.getenv('LLM_MODEL_NAME') is not None else model_name,
        messages=messages,
        stream=False
    )
    return response.choices[0].message.content
# Function to read JSON data from a file and extract 'pedia' content
def extract_pedia_and_write_to_md_from_json(input_filename, output_filename="speaker_biographies.md"):
    # Load the JSON data from the provided file
    data = []
    with open(input_filename, 'r', encoding='utf-8') as f:
        for line in f:
            # 每行都是一个独立的 JSON 对象，使用 json.loads() 解析
            data.append(json.loads(line.strip()))  # strip() 去掉可能存在的换行符

    # Write the pedia content to a Markdown file with a separator '------'
    with open(output_filename, "w", encoding="utf-8") as file:
        for entry in data:
            pedia = entry.get("pedia", "")
            if pedia:
                file.write(pedia + "\n----------------\n")

def read_speakers_info(file_path:str):
    data = []
    with open(input_filename, 'r', encoding='utf-8') as f:
        for line in f:
            # 每行都是一个独立的 JSON 对象，使用 json.loads() 解析
            data.append(json.loads(line.strip()))  # strip() 去掉可能存在的换行符
    return data
def append_data_to_txt(file_path, new_data):
    """
    将一个 Python 字典（或列表）作为独立的 JSON 对象追加到文本文件（.txt）。

    Args:
        file_path (str): 要写入的文本文件路径。
        new_data (dict or list): 要追加的数据（一个 Python 字典或列表）。
    """
    try:
        # 将新数据转换为 JSON 格式字符串，注意 ensure_ascii=False 处理中文
        json_string = json.dumps(new_data, ensure_ascii=False)

        # 使用追加模式 'a' 打开文件，并添加换行符
        # 'a' 模式会在文件末尾追加内容
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(json_string + '\n')  # 写入 JSON 字符串，并加上换行符

        print(f"数据已追加到 {file_path}")

    except IOError as e:
        print(f"写入文件时发生 I/O 错误: {e}")
    except Exception as e:
        print(f"发生其他错误: {e}")
def find_full_filename_by_basename(base_name, filename_list):
  """
  根据文件名中 '.' 前面的部分在一个文件名列表中查找对应的完整文件名。

  Args:
    base_name: 文件名中 '.' 前面的部分作为查询条件 (str)。
    filename_list: 包含完整文件名的列表 (list of str)。

  Returns:
    如果找到 '.' 前面的部分匹配的文件名，则返回该完整文件名 (str)；
    如果未找到，则返回 None。
  """
  if not isinstance(base_name, str):
        print("错误：查询内容必须是一个字符串。")
        return None

  for full_filename in filename_list:
    # 使用 os.path.splitext 安全地获取文件名中 '.' 前面的部分
    # 例如 'yiran-zhong.png' -> ('yiran-zhong', '.png')
    # 我们取第一个元素 [0]，即 'yiran-zhong'
    file_base_name = os.path.splitext(full_filename)[0]

    # 检查提取出的文件名主体是否与您输入的查询内容匹配
    if file_base_name == base_name:
      return full_filename  # 找到匹配项，返回完整的这个文件名

  return None  # 遍历完列表，没有找到匹配项
# Example usage
input_filename = "new_new_speakers.json"  # Replace with the actual JSON file path
output_filename = "./images/speaker_biographies.md"
# extract_pedia_and_write_to_md_from_json(input_filename, output_filename)
speakers_info = read_speakers_info(file_path=input_filename)
llm_client = create_openai_client()

all_images = [image.replace('./images/','') for image in get_all_files('./images', )]
all_image_name = [Path(image).name.split('.')[0] for image in all_images]
result_data = []
optimization_speakers_file_path = 'optimization_speakers_new.json'
for speaker in speakers_info:
    select_image_status = find_full_filename_by_basename(speaker.get('id'), all_images)
    if select_image_status is not None:
        image_path= select_image_status
        result = get_llm_response(client=llm_client, messages=[
            {"role": "system", "content": """
            You are a quality reviewer for a speaker's report. Your task is to generate a detailed markdown report based on the provided image. The person in the image should be identified and included in the report. Below is the required structure for the report:

        1. **Image**: Include the person's image at the beginning, formatted appropriately.

Ensure the report follows the strictest quality control by focusing on:
- Clear and coherent language.
- Accurate data extraction and correct formatting.
- No repetitive content, ensuring each section serves a distinct purpose.
- Verification that all links and citations are correct and up-to-date.

The output should be in markdown format and can be used directly on a website or event program.
The returned result will be a direct Markdown format report without review notes.

            """},
            {"role": "user", "content": speaker['pedia']},
            {"role": "user", "content": "image path : " + image_path},
        ])
        speaker['pedia'] = result
        append_data_to_txt(optimization_speakers_file_path,speaker)
        # with open(output_filename, "a", encoding="utf-8") as file:
        #         file.write(result.replace('```markdown','').replace('```','') + "\n----------------\n")

    else:
        if speaker.get('id') + '.png' not in all_images:
            result = get_llm_response(client=llm_client, messages=[
                {"role": "system", "content": """
                    You are a quality reviewer for a speaker's report. 


        Ensure the report follows the strictest quality control by focusing on:
        - Clear and coherent language.
        - Accurate data extraction and correct formatting.
        - No repetitive content, ensuring each section serves a distinct purpose.
        - Verification that all links and citations are correct and up-to-date.

        The output should be in markdown format and can be used directly on a website or event program.
        The returned result will be a direct Markdown format report without review notes.

                    """},
                {"role": "user", "content": speaker['pedia']},
            ])
            speaker['pedia'] = result
            append_data_to_txt(optimization_speakers_file_path, speaker)

            # with open(output_filename, "a", encoding="utf-8") as file:
            #     file.write(result.replace('```markdown', '').replace('```', '') + "\n----------------\n")