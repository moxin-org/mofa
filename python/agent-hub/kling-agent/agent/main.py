from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import os
import time
from dotenv import load_dotenv
from loguru import logger

# Import necessary functions and classes from klingdemo package
from klingimage.api import KlingAPIClient
from klingimage.utils import keyframe_parser

# 配置 loguru 日志
logger.add("kling-agent-image.log", rotation="10 MB", level="INFO")

# 动态确定 main.py 所在目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def generate_keyframes_images(keyframes_file: str, reference_image: str, output_dir: str, negative_prompt: str = None, aspect_ratio: str = None) -> bool:
    logger.info("开始生成关键帧图像")
    project_root = os.path.abspath(os.path.join(BASE_DIR, "../../examples/kling"))
    logger.info(f"切换工作目录到：{project_root}")
    if not os.path.exists(project_root):
        raise FileNotFoundError(f"工作目录不存在：{project_root}")
    os.chdir(project_root)
    
    # 从环境变量获取Kling API配置（移除硬编码默认值）
    accesskey_api = os.getenv("ACCESSKEY_API")
    accesskey_secret = os.getenv("ACCESSKEY_SECRET")
    if not accesskey_api or not accesskey_secret:
        raise Exception("环境变量 ACCESSKEY_API 或 ACCESSKEY_SECRET 未设置")
    kling_api_base_url = os.getenv("KLING_API_BASE_URL", "https://api.klingai.com")
    kling_token_expiration = int(os.getenv("KLING_TOKEN_EXPIRATION", "1800"))
    kling_api_timeout = int(os.getenv("KLING_API_TIMEOUT", "60"))
    kling_api_max_retries = int(os.getenv("KLING_API_MAX_RETRIES", "3"))
    
    logger.info(f"参考图像路径：{reference_image}")
    if not os.path.exists(reference_image):
        logger.warning(f"参考图像 {reference_image} 不存在，将尝试纯文本生成")
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建 KlingAPIClient 实例
    client = KlingAPIClient(
        access_key=accesskey_api,
        secret_key=accesskey_secret,
        base_url=kling_api_base_url,
        token_expiration=kling_token_expiration,
        timeout=kling_api_timeout,
        max_retries=kling_api_max_retries
    )
    
    # 解析关键帧描述
    keyframes = keyframe_parser.parse_keyframes(keyframes_file)
    
    # 生成关键帧
    max_retries = kling_api_max_retries
    for attempt in range(max_retries):
        try:
            if os.path.exists(reference_image):
                logger.info(f"使用参考图像生成关键帧：{reference_image}")
                # 使用参考图像生成关键帧
                results = client.create_keyframes_from_text_and_image(
                    keyframes=keyframes,
                    reference_image_path=reference_image,
                    model_name="kling-v1-5",
                    image_fidelity=0.7,
                    output_dir=output_dir
                )
            else:
                logger.info("未提供参考图像或图像不存在，仅使用文本描述生成关键帧")
                # 使用纯文本生成关键帧
                results = client.create_keyframes_from_text_and_image(
                    keyframes=keyframes,
                    reference_image_path=None,
                    model_name="kling-v1-5",
                    image_fidelity=None,
                    output_dir=output_dir
                )
            
            if not results:
                raise Exception("未生成任何关键帧图像")
                
            # 打印生成结果
            for result in results:
                logger.info(f"关键帧 {result['frame_id']}：")
                logger.info(f"  任务 ID：{result['task_id']}")
                logger.info(f"  图像 URL：{result['image_url']}")
                logger.info(f"  本地路径：{result['local_path']}")
            
            # 检查输出目录，确保图像文件生成
            generated_files = os.listdir(output_dir)
            if not generated_files:
                logger.error(f"输出目录 {output_dir} 中未找到生成的图像文件")
                raise RuntimeError(f"未生成图像文件：{output_dir}")
            logger.info(f"生成的文件：{generated_files}")
            return True
            
        except Exception as e:
            if "Status: 429" in str(e):
                if attempt < max_retries - 1:
                    logger.warning(f"遇到 429 错误，等待重试（第 {attempt + 1} 次）")
                    time.sleep(60)
                    continue
            raise Exception(f"生成关键帧图像失败：{str(e)}")
    raise Exception("生成关键帧图像失败：达到最大重试次数")

@run_agent
def run(agent: MofaAgent):
    try:
        user_input = agent.receive_parameter('query')
        logger.info(f"接收到的输入：{user_input!r}")
        
        if not user_input or not user_input.strip():
            logger.error("未提供有效输入，终止处理")
            agent.event = agent.event or {}
            agent.event['metadata'] = agent.event.get('metadata', {})
            agent.send_output(
                agent_output_name='cling_result',
                agent_result="错误：未提供输入，请输入 .env.secret 文件路径后重试。"
            )
            return

        # 初始化变量
        keyframes_content = ''
        keyframes_txt_path = None
        prompt = None
        negative_prompt = None
        aspect_ratio = None

        # 处理输入
        is_env_file = isinstance(user_input, str) and user_input.endswith('.env.secret')
        is_keyframe_text = isinstance(user_input, str) and '[Frame' in user_input and 'Prompt:' in user_input

        if is_env_file:
            # 输入为 .env 文件
            env_file_path = os.path.normpath(
                user_input if os.path.isabs(user_input) else os.path.join("/root/mofa-euterpe/python/examples/kling", user_input)
            )
            logger.info(f"加载 .env 文件：{env_file_path}")
            if not os.path.isfile(env_file_path):
                logger.error(f".env 文件不存在：{env_file_path}")
                agent.send_output(
                    agent_output_name='kling_result',
                    agent_result=json.dumps({"value": f"错误：.env 文件不存在：{env_file_path}"})
                )
                return
            load_dotenv(env_file_path, override=True, verbose=True)
        elif is_keyframe_text:
            # 输入为关键帧描述文本，作为触发信号
            logger.info("输入为关键帧描述文本，作为触发信号，从缓存读取环境变量")
            # 不解析 user_input，依赖 .env 缓存
        elif isinstance(user_input, dict) and 'env_file' in user_input and 'keyframes_file' in user_input:
            # 从 keyframe-agent 获取 .env 文件路径和关键帧文件路径
            env_file_path = user_input['env_file']
            keyframes_txt_path = user_input['keyframes_file']
            logger.info(f"从 keyframe-agent 获取 env_file: {env_file_path}, keyframes_file: {keyframes_txt_path}")
            if os.path.isfile(env_file_path):
                logger.info(f"加载 .env 文件：{env_file_path}")
                load_dotenv(env_file_path, override=True, verbose=True)
            else:
                logger.error(f".env 文件不存在：{env_file_path}")
                agent.send_output(
                    agent_output_name='kling_result',
                    agent_result=json.dumps({"value": f"错误：.env 文件不存在：{env_file_path}"})
                )
                return
        else:
            logger.error("无效输入类型，仅支持 .env 文件、关键帧描述文本或字典")
            agent.send_output(
                agent_output_name='kling_result',
                agent_result=json.dumps({"value": "错误：无效输入类型"})
            )
            return

        # 从环境变量获取关键帧文件路径
        keyframes_txt_path = os.getenv("IMAGE_KEYFRAMES_TXT")
        if not keyframes_txt_path:
            logger.error("环境变量 IMAGE_KEYFRAMES_TXT 未设置")
            agent.send_output(
                agent_output_name='kling_result',
                agent_result=json.dumps({"value": "错误：环境变量 IMAGE_KEYFRAMES_TXT 未设置"})
            )
            return

        # 读取关键帧文件
        if not os.path.isfile(keyframes_txt_path):
            logger.error(f"提示词文件不存在：{keyframes_txt_path}")
            agent.send_output(
                agent_output_name='kling_result',
                agent_result=json.dumps({"value": f"错误：提示词文件不存在：{keyframes_txt_path}"})
            )
            return

        with open(keyframes_txt_path, 'r', encoding='utf-8') as f:
            keyframes_content = f.read().strip()
        if not keyframes_content:
            logger.error(f"提示词文件为空：{keyframes_txt_path}")
            agent.send_output(
                agent_output_name='kling_result',
                agent_result=json.dumps({"value": f"错误：提示词文件为空：{keyframes_txt_path}"})
            )
            return

        # 解析提示词
        try:
            lines = keyframes_content.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith("Prompt:"):
                    prompt = line[len("Prompt:"):].strip()
                elif line.startswith("NegativePrompt:"):
                    negative_prompt = line[len("NegativePrompt:"):].strip()
                elif line.startswith("AspectRatio:"):
                    aspect_ratio = line[len("AspectRatio:"):].strip()
            keyframes_content = prompt or keyframes_content
            logger.info(f"解析提示词：Prompt={prompt}, NegativePrompt={negative_prompt}, AspectRatio={aspect_ratio}")
        except Exception as e:
            logger.error(f"解析提示词失败：{str(e)}")
            agent.send_output(
                agent_output_name='kling_result',
                agent_result=json.dumps({"value": f"错误：解析提示词失败 - {str(e)}"})
            )
            return

        # 验证参考图像
        if not os.path.exists(reference_image):
            logger.error(f"参考图像不存在：{reference_image}")
            agent.send_output(
                agent_output_name='kling_result',
                agent_result=json.dumps({"value": f"错误：参考图像不存在：{reference_image}"})
            )
            return

        # 确保输出目录存在
        if not os.path.exists(output_keyframes_dir):
            logger.info(f"创建输出目录：{output_keyframes_dir}")
            try:
                os.makedirs(output_keyframes_dir, exist_ok=True)
            except PermissionError as e:
                logger.error(f"创建输出目录失败：权限不足 - {str(e)}")
                agent.send_output(
                    agent_output_name='kling_result',
                    agent_result=json.dumps({"value": f"错误：创建输出目录失败：{str(e)}"})
                )
                return

        # 生成关键帧图像
        success = generate_keyframes_images(
            keyframes_file=keyframes_txt_path,
            reference_image=reference_image,
            output_dir=output_keyframes_dir,
            negative_prompt=negative_prompt,
            aspect_ratio=aspect_ratio
        )

        if success:
            generated_files = [f for f in os.listdir(output_keyframes_dir) if f.endswith(('.jpg', '.png'))]
            if not generated_files:
                logger.error(f"输出目录 {output_keyframes_dir} 未找到生成文件")
                agent.send_output(
                    agent_output_name='kling_result',
                    agent_result=json.dumps({"value": []})
                )
                return
            logger.info(f"关键帧图像生成成功，文件列表：{generated_files}")
            agent.send_output(
                agent_output_name='kling_result',
                agent_result=json.dumps({"value": generated_files})
            )
        else:
            logger.error("关键帧图像生成失败")
            agent.send_output(
                agent_output_name='kling_result',
                agent_result=json.dumps({"value": "错误：关键帧图像生成失败"})
            )

    except Exception as e:
        logger.error(f"运行异常：{str(e)}")
        agent.send_output(
            agent_output_name='kling_result',
            agent_result=json.dumps({"value": f"错误：运行异常 - {str(e)}"})
        )
        
def main():
    agent = MofaAgent(agent_name='kling-agent-image')
    run(agent)

if __name__ == "__main__":
    main()