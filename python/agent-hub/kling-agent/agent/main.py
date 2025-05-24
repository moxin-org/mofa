from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import os
import time
from dotenv import load_dotenv
from loguru import logger

# Import necessary functions and classes from klingdemo package
from klingdemo.api import KlingAPIClient
from klingdemo.utils import keyframe_parser

# 配置 loguru 日志
logger.add("kling-agent.log", rotation="10 MB", level="INFO")

# 动态确定 main.py 所在目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def generate_keyframes_images(keyframes_file: str, reference_image: str, output_dir: str) -> bool:
    """生成关键帧图像"""
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
                raise Exception(f"输出目录 {output_dir} 中未找到生成的图像文件")
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
        
        if not user_input.endswith(".env.secret"):
            logger.error("输入不是 .env.secret 文件路径，终止处理")
            agent.event = agent.event or {}
            agent.event['metadata'] = agent.event.get('metadata', {})
            agent.send_output(
                agent_output_name='cling_result',
                agent_result="错误：请输入 .env.secret 文件路径。"
            )
            return

        env_file_path = user_input
        KLING_BASE_DIR_DEFAULT = "/root/mofa-euterpe/python/examples/kling"
        if not os.path.isabs(user_input):
            env_file_path = os.path.join(KLING_BASE_DIR_DEFAULT, user_input)
        logger.info(f"输入被识别为 .env 文件路径，解析为：{env_file_path}")
        
        if not os.path.isfile(env_file_path):
            logger.error(f"用户提供的 .env 文件不存在：{env_file_path}")
            agent.event = agent.event or {}
            agent.event['metadata'] = agent.event.get('metadata', {})
            agent.send_output(
                agent_output_name='cling_result',
                agent_result=f"错误：用户提供的 .env 文件不存在：{env_file_path}"
            )
            return

        logger.info(f"加载用户输入的 .env 文件：{env_file_path}")
        load_dotenv(env_file_path, verbose=True, override=True)

        logger.info("加载 .env 文件后，打印环境变量：")
        for key, value in os.environ.items():
            if key in ["ACCESSKEY_API", "ACCESSKEY_SECRET", "KLING_API_BASE_URL", 
                       "KLING_TOKEN_EXPIRATION", "KLING_API_TIMEOUT", "KLING_API_MAX_RETRIES",
                       "image-REFERENCE_IMAGE", "image-KEYFRAMES_TXT", "image-OUTPUT_KEYFRAMES"]:
                logger.info(f"{key}: {value}")

        accesskey_api = os.getenv("ACCESSKEY_API")
        accesskey_secret = os.getenv("ACCESSKEY_SECRET")
        logger.info(f"ACCESSKEY_API: {accesskey_api}")
        logger.info(f"ACCESSKEY_SECRET: {accesskey_secret}")
        if not accesskey_api or not accesskey_secret:
            raise Exception("环境变量 ACCESSKEY_API 或 ACCESSKEY_SECRET 未设置")

        reference_image = os.getenv("image-REFERENCE_IMAGE", "/root/mofa-euterpe/python/examples/kling/input/reference_image.jpg")
        keyframes_txt_path = os.getenv("image-KEYFRAMES_TXT", "/root/mofa-euterpe/python/examples/kling/output/keyframes.txt")
        output_keyframes_dir = os.getenv("image-OUTPUT_KEYFRAMES", "/root/mofa-euterpe/python/examples/kling/output/output_keyframes")
        
        logger.info(f"image-REFERENCE_IMAGE: {reference_image}")
        logger.info(f"image-KEYFRAMES_TXT: {keyframes_txt_path}")
        logger.info(f"image-OUTPUT_KEYFRAMES: {output_keyframes_dir}")

        if not all([reference_image, keyframes_txt_path, output_keyframes_dir]):
            raise Exception("环境变量中缺少必要的路径配置：image-REFERENCE_IMAGE, image-KEYFRAMES_TXT, image-OUTPUT_KEYFRAMES")

        logger.info(f"读取 keyframes.txt 文件：{keyframes_txt_path}")
        if not os.path.isfile(keyframes_txt_path):
            logger.error(f"keyframes.txt 文件不存在：{keyframes_txt_path}")
            agent.event = agent.event or {}
            agent.event['metadata'] = agent.event.get('metadata', {})
            agent.send_output(
                agent_output_name='cling_result',
                agent_result=f"错误：keyframes.txt 文件不存在：{keyframes_txt_path}"
            )
            return

        try:
            with open(keyframes_txt_path, "r", encoding="utf-8") as f:
                keyframes_content = f.read().strip()
            logger.info(f"从文件 {keyframes_txt_path} 读取到 keyframes 内容：{keyframes_content!r}")
        except Exception as e:
            logger.error(f"读取 keyframes.txt 文件失败：{str(e)}")
            agent.event = agent.event or {}
            agent.event['metadata'] = agent.event.get('metadata', {})
            agent.send_output(
                agent_output_name='cling_result',
                agent_result=f"错误：读取 keyframes.txt 文件失败：{str(e)}"
            )
            return

        if not keyframes_content:
            logger.error("keyframes.txt 内容为空，终止处理")
            agent.event = agent.event or {}
            agent.event['metadata'] = agent.event.get('metadata', {})
            agent.send_output(
                agent_output_name='cling_result',
                agent_result="错误：keyframes.txt 内容为空，请提供有效的 keyframes 内容。"
            )
            return
        
        logger.info("收到有效 keyframes 内容，继续处理")
        
        # 生成关键帧图像
        success = generate_keyframes_images(keyframes_txt_path, reference_image, output_keyframes_dir)
        
        # 只有在所有图像生成成功后才输出成功提示
        agent.event = agent.event or {}
        agent.event['metadata'] = agent.event.get('metadata', {})
        
        if success:
            # 检查输出目录中的图像文件
            try:
                generated_files = os.listdir(output_keyframes_dir)
                if not generated_files:
                    logger.error(f"输出目录 {output_keyframes_dir} 中未找到生成的图像文件")
                    agent.send_output(
                        agent_output_name='cling_result',
                        agent_result=f"错误：未在 {output_keyframes_dir} 中生成任何图像文件"
                    )
                    return
                logger.info(f"所有图像生成完成，生成的文件：{generated_files}")
                agent.send_output(
                    agent_output_name='cling_result',
                    agent_result=f"关键帧图像已生成到 {output_keyframes_dir}，生成文件：{generated_files}"
                )
            except Exception as e:
                logger.error(f"检查输出目录失败：{str(e)}")
                agent.send_output(
                    agent_output_name='cling_result',
                    agent_result=f"错误：检查输出目录失败：{str(e)}"
                )
        else:
            logger.error("生成失败，未发送成功输出")
            agent.send_output(
                agent_output_name='cling_result',
                agent_result="错误：关键帧图像生成失败"
            )
        
    except Exception as e:
        logger.error(f"错误：{str(e)}")
        agent.event = agent.event or {}
        agent.event['metadata'] = agent.event.get('metadata', {})
        agent.send_output(
            agent_output_name='cling_result',
            agent_result=f"错误：{str(e)}"
        )

def main():
    logger.info("启动 kling-agent")
    agent = MofaAgent(agent_name='kling-agent')
    run(agent=agent)

if __name__ == "__main__":
    main()
