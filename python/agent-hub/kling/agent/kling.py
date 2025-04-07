import json

import requests
import base64
import time


import time
import jwt

def download_video(video_url, save_path):
    """
    下载 MP4 视频文件。

    Args:
        video_url (str): 视频的 URL 地址。
        save_path (str): 下载后保存视频的本地路径。
    """
    try:
        # 发送 GET 请求下载视频
        response = requests.get(video_url, stream=True)
        response.raise_for_status()

        # 打开文件并写入数据
        with open(save_path, 'wb') as video_file:
            for chunk in response.iter_content(chunk_size=8192):
                video_file.write(chunk)

        print(f"视频已成功下载并保存在: {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"下载视频失败: {e}")

ak = "" # 填写access key
sk = "" # 填写secret key

def encode_jwt_token(ak, sk):
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    payload = {
        "iss": ak,
        "exp": int(time.time()) + 1800, # 有效时间，此处示例代表当前时间+1800s(30min)
        "nbf": int(time.time()) - 5 # 开始生效的时间，此处示例代表当前时间-5秒
    }
    token = jwt.encode(payload, sk, headers=headers)
    return token

api_token = encode_jwt_token(ak, sk)
print(api_token) # 打印生成的API_TOKEN

api_key = api_token
# 创建任务的 API 端点
create_task_endpoint = "https://api.klingai.com/v1/videos/image2video"
# 查询任务状态的 API 端点 (需要替换 task_id)
query_task_endpoint = "https://api.klingai.com/v1/videos/image2video/{task_id}"

headers = {
    'Authorization': 'Bearer '+ api_key,
    'Content-Type': 'application/json'
}

def generate_speaker_title_animation(image_path, presentation_title, duration=3):
    """
    根据演讲者照片和演讲题目生成短动画。

    Args:
        image_path (str): 演讲者照片的文件路径。
        presentation_title (str): 演讲的题目。
        duration (int): 视频时长 (3, 4, 或 5 秒)。

    Returns:
        str: 生成的视频 URL，如果失败则返回 None。
    """
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return None

    prompt = f"使用这张演讲者的照片，并在视频中以清晰且专业的方式呈现演讲题目：'{presentation_title}'。制作一个 {duration} 秒的动画，题目可以采用淡入、滑动或打字机等效果出现。照片本身可以有轻微的缩放或平移，以增加动态感。整体风格应该简洁且引人注目。 整体变成动漫效果 并且变成吉卜力的版本"

    create_payload = {
        "model_name": "kling-v1-6",
        "image": encoded_image,
        "prompt": prompt,
        # 您可以尝试调整 cfg_scale 来控制模型对 prompt 的遵循程度
    }

    try:
        # 1. 创建任务
        create_response = requests.post(create_task_endpoint, headers=headers, data=json.dumps(create_payload))
        print(create_response.content)

        create_response.raise_for_status()
        task_data = create_response.json().get("data")
        if task_data and task_data.get("task_id"):
            task_id = task_data["task_id"]
            print(f"任务创建成功，任务 ID: {task_id}")

            # 2. 查询任务状态 (需要轮询直到任务完成)
            while True:
                time.sleep(5)  # 每隔 5 秒查询一次状态
                query_url = query_task_endpoint.format(task_id=task_id)
                query_response = requests.get(query_url, headers=headers)
                query_response.raise_for_status()
                task_info = query_response.json().get("data")
                if task_info and task_info.get("task_status"):
                    task_status = task_info["task_status"]
                    print(f"任务状态: {task_status}")
                    if task_status == "succeed":
                        video_url = task_info["task_result"]["videos"][0]["url"]
                        download_video(video_url,'video.mp4')
                        print(f"视频下载生成成功！视频 URL: {video_url}")
                        return video_url
                    elif task_status == "failed":
                        error_message = task_info.get("task_status_msg", "未知错误")
                        print(f"任务失败！错误信息: {error_message}")
                        return None
                    elif task_status == "processing" or task_status == "submitted":
                        print("任务仍在处理中，请稍候...")
                    else:
                        print(f"未知任务状态: {task_status}")
                        return None
                else:
                    print("查询任务状态失败，响应数据格式不正确。")
                    return None
        else:
            print("创建任务失败，无法获取 task_id。")
            return None

    except requests.exceptions.RequestException as e:
        print(f"API 请求失败: {e}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"API 请求失败，HTTP 错误: {e}")
        print("错误响应内容:", e.response.text)
        return None
    except Exception as e:
        print(f"发生未知错误: {e}")
        return None

if __name__ == "__main__":
    speaker_photo_path = "img.png"
    presentation_title = "GoSim : Global Open-Source Innovation Meetup "
    video_duration = 4

    video_url = generate_speaker_title_animation(speaker_photo_path, presentation_title, video_duration)

    if video_url:
        print(f"生成的动画视频 URL: {video_url}")