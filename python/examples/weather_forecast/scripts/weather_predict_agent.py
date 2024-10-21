import base64
import os
from openai import OpenAI
from dora import Node, DoraStatus
import pyarrow as pa
from mofa.kernel.utils.util import create_agent_output
from mofa.utils.files.dir import get_relative_path
from mofa.utils.files.read import read_yaml




def get_latest_files(directory:str, num_files=5):
    # 获取目录下的所有文件及其完整路径
    files = [os.path.join(directory, file) for file in os.listdir(directory) if
             os.path.isfile(os.path.join(directory, file))]

    # 按文件的修改时间排序
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    # 返回最新的 num_files 个文件
    return files[:num_files]


def encode_image(image_path:str):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')



class Operator:
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            agent_inputs = ['windy_crawler_response','task']
            if dora_event["id"] in agent_inputs:
                yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs',
                                                   target_file_name='weather_prodict_agent.yml')
                config = read_yaml(yaml_file_path)
                prompt, api_key, model_name = config['PROMPT'], config.get("MODEL")['MODEL_API_KEY'], \
                config.get("MODEL")['MODEL_NAME']
                file_dir_path = image_dir_path = './data/output/weather/'
                client = OpenAI(api_key=api_key)
                prompt_data = []
                for image_file in get_latest_files(file_dir_path):
                    prompt_data.append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encode_image(image_file)}"
                        }
                    })
                prompt_data.append({"type": "text", "text": prompt})
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt_data
                        }
                    ],
                )
                weather_response = response.choices[0].message.content
                send_output("weather_predict_response", pa.array([create_agent_output(step_name='weather_response',
                                                                                      output_data=weather_response,
                                                                                      dataflow_status=os.getenv(
                                                                                          'IS_DATAFLOW_END', True))]),
                            dora_event['metadata'])

        return DoraStatus.CONTINUE