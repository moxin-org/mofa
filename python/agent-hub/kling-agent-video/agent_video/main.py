#!/usr/bin/env python
from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import os
import subprocess
import time
import glob
import json
import requests
import re
import uuid
from dotenv import load_dotenv
from loguru import logger
import yaml
from .klingvideo.models import TaskStatus, ImageToVideoRequest
from .klingvideo.api import KlingAPIClient, KlingAPIError, NetworkError
from .klingvideo.utils import encode_image_to_base64

# 配置 loguru 日志
logger.add("kling-agent-video.log", rotation="10 MB", level="INFO")

# 动态确定 main.py 所在目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENT_CONFIG_PATH = os.path.join(BASE_DIR, "agent_video", "configs", "agent.yml")

def check_agent_config():
    """检查 agent.yml 是否存在且名称正确"""
    if not os.path.isfile(AGENT_CONFIG_PATH):
        logger.error(f"缺少 agent.yml：{AGENT_CONFIG_PATH}")
        raise FileNotFoundError(f"缺少 agent.yml：{AGENT_CONFIG_PATH}")
    with open(AGENT_CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    if config.get('name') != 'kling-agent-video':
        logger.error(f"agent.yml 名称错误，期望 'kling-agent-video'，实际：{config.get('name')}")
        raise ValueError(f"agent.yml 名称错误，期望 'kling-agent-video'")
    logger.info("agent.yml 检查通过")
    return True

def save_video(url: str, output_dir: str, video_name: str) -> str:
    """下载并保存视频"""
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, video_name)
    logger.info(f"正在下载视频：{url}，保存为：{output_path}")
    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    logger.info(f"视频保存到：{output_path}")
    return output_path

def check_task_status(task_id: str, env: dict, output_dir: str, video_name: str) -> bool:
    """检查 Kling API 任务状态并下载视频"""
    api_base_url = env["KLING_API_BASE_URL"]
    access_key = env["ACCESSKEY_API"]
    secret_key = env["ACCESSKEY_SECRET"]
    url = f"{api_base_url}/task/{task_id}"
    headers = {
        "Authorization": f"Bearer {access_key}:{secret_key}"
    }
    max_attempts = 120  # 600 秒 / 5 秒检查间隔
    temp_name = f"temp_{task_id}_{uuid.uuid4().hex[:8]}.mp4"  # 唯一临时文件名
    for attempt in range(max_attempts):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            task_data = response.json()
            status = task_data.get("task_status")
            logger.info(f"任务 {task_id} 状态：{status}")
            if status == TaskStatus.SUCCEED:
                videos = task_data.get("task_result", {}).get("videos", [])
                if videos:
                    for i, video in enumerate(videos):
                        video_url = video.get("url")
                        if video_url:
                            # 下载到唯一临时文件名
                            temp_path = save_video(video_url, output_dir, temp_name)
                            # 重命名到目标文件名
                            target_path = os.path.join(output_dir, video_name)
                            if os.path.exists(temp_path):
                                if os.path.exists(target_path):
                                    logger.warning(f"目标文件 {target_path} 已存在，保留现有文件")
                                else:
                                    os.rename(temp_path, target_path)
                                    logger.info(f"重命名视频：{temp_name} -> {video_name}")
                            return True
                else:
                    logger.error("任务成功但未返回视频 URL")
                    return False
            elif status in [TaskStatus.FAILED, TaskStatus.CANCELED]:
                logger.error(f"任务失败，状态：{status}")
                return False
            logger.info(f"任务仍在处理，等待 5 秒后重试（第 {attempt + 1}/{max_attempts} 次）")
            time.sleep(5)
        except requests.RequestException as e:
            logger.error(f"检查任务状态失败：{str(e)}")
            if attempt < max_attempts - 1:
                time.sleep(5)
                continue
            return False
    logger.error(f"任务 {task_id} 在 600 秒内未完成")
    return False

def generate_keyframes_video(prompt: str, reference_image: str, output_dir: str, video_name: str, duration: str = "5") -> bool:
    """生成单个关键帧视频，返回成功状态"""
    logger.info(f"开始生成视频：{video_name}")
    project_root = os.path.join(BASE_DIR, "agent_video")
    logger.info(f"切换工作目录到：{project_root}")
    if not os.path.exists(project_root):
        raise FileNotFoundError(f"工作目录不存在：{project_root}")
    os.chdir(project_root)

    env = os.environ.copy()
    env["PYTHONPATH"] = project_root
    env["ACCESSKEY_API"] = os.getenv("ACCESSKEY_API", "At4EgQYM34AggbMPRhGhbNHmmEQratDQ")
    env["ACCESSKEY_SECRET"] = os.getenv("ACCESSKEY_SECRET", "989B4FJnAK4pEmmM8GhmAgdYQnrLrfJA")
    env["KLING_API_BASE_URL"] = os.getenv("KLING_API_BASE_URL", "https://api.klingai.com")
    env["KLING_TOKEN_EXPIRATION"] = os.getenv("KLING_TOKEN_EXPIRATION", "1800")
    env["KLING_API_TIMEOUT"] = os.getenv("KLING_API_TIMEOUT", "60")
    env["KLING_API_MAX_RETRIES"] = os.getenv("KLING_API_MAX_RETRIES", "3")

    logger.info(f"参考图像路径：{reference_image}")
    if not os.path.exists(reference_image):
        logger.error(f"参考图像 {reference_image} 不存在")
        raise FileNotFoundError(f"参考图像 {reference_image} 不存在")

    logger.info(f"视频提示词：{prompt!r}")

    # 使用唯一临时文件名
    temp_name = f"temp_{uuid.uuid4().hex[:8]}.mp4"
    temp_path = os.path.join(output_dir, temp_name)

    # 创建 Kling API 客户端
    client = KlingAPIClient(
        access_key=env["ACCESSKEY_API"],
        secret_key=env["ACCESSKEY_SECRET"],
        base_url=env["KLING_API_BASE_URL"],
        timeout=int(env["KLING_API_TIMEOUT"]),
        max_retries=int(env["KLING_API_MAX_RETRIES"]),
        token_expiration=int(env["KLING_TOKEN_EXPIRATION"])
    )

    # 编码图像为 base64
    encoded_image = encode_image_to_base64(reference_image)

    # 创建请求
    request = ImageToVideoRequest(
        model_name="kling-v1-5",
        image=encoded_image,
        prompt=prompt,
        negative_prompt="",
        cfg_scale=0.7,
        mode="pro",
        duration=int(duration),
        external_task_id=f"video_gen_{uuid.uuid4().hex[:8]}",
    )
    
    logger.info("初始化 Kling API 客户端并创建请求")
    max_retries = int(os.getenv("KLING_API_MAX_RETRIES", "3"))
    task_id = None
    for attempt in range(max_retries):
        try:
            # 提交任务
            logger.info(f"提交图像到视频生成任务 (尝试 {attempt+1}/{max_retries})")
            task = client.create_image_to_video_task(request)
            task_id = task.task_id
            logger.info(f"任务创建成功，ID: {task_id}")
            
            # 等待任务完成
            logger.info("等待任务完成...")
            task = client.wait_for_task_completion(
                task_id,
                check_interval=5,
                timeout=600  # 10分钟超时
            )
            
            # 处理结果
            if task.task_status == TaskStatus.SUCCEED and task.task_result:
                # 下载视频
                for i, video in enumerate(task.task_result.videos):
                    video_url = video.url
                    if video_url:
                        saved_path = save_video(video_url, output_dir, video_name)
                        logger.info(f"视频已保存到: {saved_path}")
                        target_path = os.path.join(output_dir, video_name)
                        if os.path.exists(target_path):
                            logger.info(f"生成的文件：{video_name}")
                            # 清理其他临时文件
                            for f in os.listdir(output_dir):
                                if f.startswith('temp_') and f.endswith('.mp4') and f != video_name:
                                    os.remove(os.path.join(output_dir, f))
                                    logger.info(f"清理临时文件：{f}")
                            return True
                logger.error("任务成功但未找到视频文件")
                return False
            else:
                logger.error(f"任务失败，状态：{task.task_status}")
                if hasattr(task, 'task_status_msg') and task.task_status_msg:
                    logger.error(f"错误信息：{task.task_status_msg}")
                return False
        except (KlingAPIError, NetworkError) as e:
            logger.error(f"API 错误 (尝试 {attempt+1}/{max_retries}): {str(e)}")
            if "Status: 429" in str(e) and attempt < max_retries - 1:
                logger.warning(f"遇到 429 错误，等待重试（第 {attempt + 1} 次）")
                time.sleep(60)
                continue
            
            # 如果有任务 ID，尝试查询任务状态
            if task_id:
                logger.warning(f"任务创建后出错，尝试轮询任务状态（第 {attempt + 1} 次）")
                if check_task_status(task_id, env, output_dir, video_name):
                    if os.path.exists(os.path.join(output_dir, video_name)):
                        # 清理临时文件
                        for f in os.listdir(output_dir):
                            if f.startswith('temp_') and f.endswith('.mp4'):
                                os.remove(os.path.join(output_dir, f))
                                logger.info(f"清理临时文件：{f}")
                        logger.info(f"生成的文件：{video_name}")
                        return True
        except TimeoutError as e:
            logger.error(f"超时错误 (尝试 {attempt+1}/{max_retries}): {str(e)}")
            # 如果任务 ID 存在，尝试继续查询任务状态
            if task_id:
                logger.warning(f"任务超时，尝试轮询任务状态（第 {attempt + 1} 次）")
                if check_task_status(task_id, env, output_dir, video_name):
                    if os.path.exists(os.path.join(output_dir, video_name)):
                        # 清理临时文件
                        for f in os.listdir(output_dir):
                            if f.startswith('temp_') and f.endswith('.mp4'):
                                os.remove(os.path.join(output_dir, f))
                                logger.info(f"清理临时文件：{f}")
                        logger.info(f"生成的文件：{video_name}")
                        return True
                    else:
                        logger.error(f"查询任务状态成功但未找到生成的视频文件")
        except Exception as e:
            logger.error(f"意外错误 (尝试 {attempt+1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                logger.warning(f"等待重试（第 {attempt + 1} 次）")
                time.sleep(5)
                continue
    
    # 如果所有尝试都失败
    raise Exception("生成视频失败：达到最大重试次数")
    raise Exception("生成视频失败：达到最大重试次数")

def process_image_folder(image_folder: str, keyframes_txt: str, output_dir: str, duration: str = "5") -> list:
    """处理图片文件夹，生成最多四个视频"""
    logger.info(f"处理图片文件夹：{image_folder}")
    if not os.path.isdir(image_folder):
        logger.error(f"图片文件夹不存在：{image_folder}")
        raise FileNotFoundError(f"图片文件夹不存在：{image_folder}")

    # 获取图片文件（只支持 jpg 和 png，最多 4 张）
    image_files = [f for f in glob.glob(os.path.join(image_folder, "*.jpg")) + glob.glob(os.path.join(image_folder, "*.png"))]
    
    # 按文件名中的数字排序
    def extract_number(filename):
        match = re.search(r'keyframe_(\d+)\.(jpg|png)', os.path.basename(filename))
        return int(match.group(1)) if match else float('inf')
    
    image_files = sorted(image_files, key=extract_number)[:4]  # 按数字排序并限制最多 4 张
    logger.info(f"排序后的图片文件：{image_files}")
    
    if not image_files:
        logger.error(f"图片文件夹 {image_folder} 中未找到 jpg 或 png 文件")
        raise FileNotFoundError(f"图片文件夹 {image_folder} 中未找到 jpg 或 png 文件")

    # 读取关键帧描述
    if not os.path.isfile(keyframes_txt):
        logger.error(f"关键帧描述文件不存在：{keyframes_txt}")
        raise FileNotFoundError(f"关键帧描述文件不存在：{keyframes_txt}")

    with open(keyframes_txt, "r", encoding="utf-8") as f:
        keyframes_content = f.read().strip()
    if not keyframes_content:
        logger.error("关键帧描述文件内容为空")
        raise ValueError("关键帧描述文件内容为空")

    # 按帧分割提示词
    frames = keyframes_content.split("\n\n")
    frames = [frame.strip() for frame in frames if frame.strip()][:4]  # 限制最多 4 帧
    logger.info(f"关键帧描述：{frames}")
    
    if not frames:
        logger.error("关键帧描述文件未包含有效帧")
        raise ValueError("关键帧描述文件未包含有效帧")

    # 确保帧数和图片数匹配
    if len(frames) > len(image_files):
        logger.warning(f"关键帧描述（{len(frames)} 帧）多于图片（{len(image_files)} 张），仅使用前 {len(image_files)} 帧")
        frames = frames[:len(image_files)]
    elif len(image_files) > len(frames):
        logger.warning(f"图片（{len(image_files)} 张）多于关键帧描述（{len(frames)} 帧），仅使用前 {len(frames)} 张图片")
        image_files = image_files[:len(frames)]

    generated_videos = []
    for i, (image, prompt) in enumerate(zip(image_files, frames), 1):
        video_name = f"video_frame_{i}.mp4"  # 规范化视频文件名
        logger.info(f"生成视频 {i}/{len(image_files)}，使用图片：{image}，提示词：{prompt}")
        try:
            success = generate_keyframes_video(prompt, image, output_dir, video_name, duration)
            if success:
                generated_videos.append(video_name)
            else:
                logger.error(f"生成视频 {video_name} 失败")
        except Exception as e:
            logger.error(f"生成视频 {video_name} 失败：{str(e)}")
    return generated_videos

@run_agent
def run(agent: MofaAgent):
    try:
        user_input = agent.receive_parameter('query')
        logger.info(f"接收到的输入：{user_input!r}")

        if not user_input or not user_input.strip():
            logger.error("未提供有效输入，终止处理")
            agent.send_output(
                agent_output_name='kling_result',
                agent_result=json.dumps({'value': "错误：未提供输入，请输入 .env.secret 文件路径或触发信号后重试。"})
            )
            return

        # 初始化变量，从环境变量获取配置
        image_folder = os.getenv("VIDEO_IMAGE_FOLDER")
        keyframes_txt_path = os.getenv("VIDEO_KEYFRAMES_TXT", "../../examples/script2video/output/keyframes_output.txt")
        output_keyframes_dir = os.getenv("VIDEO_OUTPUT_KEYFRAMES", "../../examples/script2video/output/output_video")
        duration = os.getenv("VIDEO_DURATION", "5")

        # 验证 image_folder 是否为目录
        if not image_folder or not os.path.isdir(image_folder):
            logger.error(f"VIDEO_IMAGE_FOLDER 不是有效目录：{image_folder}")
            agent.send_output(
                agent_output_name='kling_result',
                agent_result=json.dumps({'value': f"错误：VIDEO_IMAGE_FOLDER 不是有效目录：{image_folder}"})
            )
            return

        # 判断输入类型
        if user_input.endswith(".env.secret"):
            # 输入是 .env.secret 文件路径
            env_file_path = user_input
            BASE_DIR_DEFAULT = "../../examples/script2video"
            if not os.path.isabs(env_file_path):
                env_file_path = os.path.join(BASE_DIR_DEFAULT, env_file_path)
            logger.info(f"输入被识别为 .env 文件路径，解析为：{env_file_path}")

            if not os.path.isfile(env_file_path):
                logger.error(f"用户提供的 .env 文件不存在：{env_file_path}")
                agent.send_output(
                    agent_output_name='kling_result',
                    agent_result=json.dumps({'value': f"错误：用户提供的 .env 文件不存在：{env_file_path}"})
                )
                return

            logger.info(f"加载用户输入的 .env 文件：{env_file_path}")
            load_dotenv(env_file_path, verbose=True, override=True)

            # 重新加载环境变量
            image_folder = os.getenv("VIDEO_IMAGE_FOLDER")
            keyframes_txt_path = os.getenv("VIDEO_KEYFRAMES_TXT", keyframes_txt_path)
            output_keyframes_dir = os.getenv("VIDEO_OUTPUT_KEYFRAMES", output_keyframes_dir)
            duration = os.getenv("VIDEO_DURATION", duration)

            # 再次验证 image_folder
            if not image_folder or not os.path.isdir(image_folder):
                logger.error(f"加载 .env 后 VIDEO_IMAGE_FOLDER 无效：{image_folder}")
                agent.send_output(
                    agent_output_name='kling_result',
                    agent_result=json.dumps({'value': f"错误：加载 .env 后 VIDEO_IMAGE_FOLDER 无效：{image_folder}"})
                )
                return

            logger.info(f"VIDEO_IMAGE_FOLDER: {image_folder}")
            logger.info(f"VIDEO_KEYFRAMES_TXT: {keyframes_txt_path}")
            logger.info(f"VIDEO_OUTPUT_KEYFRAMES: {output_keyframes_dir}")
            logger.info(f"VIDEO_DURATION: {duration}")
        else:
            # 输入是触发信号（例如 keyframe-agent 的输出），直接使用环境变量
            logger.info("输入被识别为触发信号，使用缓存的环境变量")

        # 清理输出目录中的临时文件
        for f in glob.glob(os.path.join(output_keyframes_dir, "temp_*.mp4")):
            os.remove(f)
            logger.info(f"清理旧临时文件：{f}")

        # 处理图片文件夹并生成视频
        generated_videos = process_image_folder(image_folder, keyframes_txt_path, output_keyframes_dir, duration)
        if generated_videos:
            logger.info(f"所有视频生成成功，文件列表：{generated_videos}")
            agent.send_output(
                agent_output_name='kling_result',
                agent_result=json.dumps({'value': f"视频已生成到 {output_keyframes_dir}，生成文件：{generated_videos}"})
            )
        else:
            logger.error("未生成任何视频")
            agent.send_output(
                agent_output_name='kling_result',
                agent_result=json.dumps({'value': "错误：未生成任何视频，请检查日志"})
            )

    except Exception as e:
        logger.error(f"运行异常：{str(e)}")
        agent.send_output(
            agent_output_name='kling_result',
            agent_result=json.dumps({'value': f"错误：{str(e)}"})
        )

def main():
    logger.info("启动 kling-agent-video")
    check_agent_config()
    agent = MofaAgent(agent_name='kling-agent-video')
    run(agent=agent)

if __name__ == "__main__":
    main()
