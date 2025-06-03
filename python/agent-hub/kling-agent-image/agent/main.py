import json
import os
import time
from dotenv import load_dotenv
from loguru import logger
import sys
from mofa.agent_build.base.base_agent import MofaAgent, run_agent

# 确保同级目录可被导入
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from .klingimage.api import KlingAPIClient
    from .klingimage.utils import keyframe_parser
except ImportError as e:
    logger.error(f"无法导入 klingimage 模块: {str(e)}")
    raise

# 配置 loguru 日志
logger.add("kling-agent-image.log", rotation="10 MB", level="INFO")

# 动态确定 main.py 所在目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def generate_keyframes_images(
    keyframes_file: str,
    reference_image: str | None,
    output_dir: str,
    negative_prompt: str = None,
    aspect_ratio: str = None
) -> bool:
    logger.info("开始生成关键帧图像")
    # 使用相对路径，指向 kling 项目目录
    project_root = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "examples", "kling"))
    logger.info(f"切换工作目录到：{project_root}")
    if not os.path.exists(project_root):
        raise FileNotFoundError(f"工作目录不存在：{project_root}")
    os.chdir(project_root)
    
    # 从环境变量获取 Kling API 配置
    accesskey_api = os.getenv("ACCESSKEY_API", "")
    accesskey_secret = os.getenv("ACCESSKEY_SECRET", "")
    # 可灵官方更新 API 地址
    kling_api_base_url = os.getenv("KLING_API_BASE_URL", "https://api-beijing.klingai.com")
    kling_token_expiration = int(os.getenv("KLING_TOKEN_EXPIRATION", "1800"))
    kling_api_timeout = int(os.getenv("KLING_API_TIMEOUT", "60"))
    kling_api_max_retries = int(os.getenv("KLING_API_MAX_RETRIES", "3"))

    # 验证环境变量
    for key in ["ACCESSKEY_API", "ACCESSKEY_SECRET", "KLING_API_BASE_URL"]:
        logger.debug(f"环境变量 {key}: {os.getenv(key, '未设置')}")
        if not os.getenv(key):
            logger.error(f"环境变量 {key} 未设置")
            raise ValueError(f"环境变量 {key} 未设置")

    # 检查关键帧文件
    logger.info(f"关键帧文件：{keyframes_file}")
    if not keyframes_file:
        logger.error("关键帧文件路径未定义")
        raise ValueError("关键帧文件路径未定义")
    if not os.path.isfile(keyframes_file):
        logger.error(f"关键帧文件 {keyframes_file} 不存在")
        raise FileNotFoundError(f"关键帧文件 {keyframes_file} 不存在")

    with open(keyframes_file, "r", encoding="utf-8") as f:
        prompt = f.read().strip()
    if not prompt:
        logger.error("关键帧文件内容为空")
        raise ValueError(f"关键帧文件内容为空：{keyframes_file}")
    logger.info(f"关键帧提示词：{prompt}")
    if negative_prompt:
        logger.info(f"负面提示词：{negative_prompt}")
    if aspect_ratio:
        logger.info(f"宽高比：{aspect_ratio}")

    # 检查参考图像（支持纯文本生成）
    if reference_image:
        logger.info(f"参考图像路径：{reference_image}")
        if not os.path.exists(reference_image):
            logger.warning(f"参考图像 {reference_image} 不存在，将尝试纯文本生成")
            reference_image = None
    else:
        logger.info("未提供参考图像，将使用纯文本生成")

    # 确保输出目录存在
    logger.info(f"输出目录：{output_dir}")
    if not os.path.exists(output_dir):
        logger.info(f"创建输出目录：{output_dir}")
        try:
            os.makedirs(output_dir, exist_ok=True)
        except PermissionError as e:
            logger.error(f"创建输出目录失败：权限不足 - {str(e)}")
            raise

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
    logger.debug(f"解析的关键帧：{keyframes}")

    # 生成关键帧
    max_retries = kling_api_max_retries
    for attempt in range(max_retries):
        try:
            results = client.create_keyframes_from_text_and_image(
                keyframes=keyframes,
                reference_image_path=reference_image,
                model_name="kling-v1-5",
                image_reference=None if not reference_image else "face",  # 修改为小写 "face"
                image_fidelity=None if not reference_image else 0.7,
                human_fidelity=None if not reference_image else 0.8,
                output_dir=output_dir
            )
            
            if not results:
                logger.error("未生成任何关键帧图像")
                raise ValueError("未生成任何关键帧图像")
                
            # 打印生成结果
            for result in results:
                logger.info(f"关键帧 {result['frame_id']}:")
                logger.info(f"  任务 ID：{result['task_id']}")
                logger.info(f"  图像 URL：{result['image_url']}")
                logger.info(f"  本地路径：{result['local_path']}")
            
            # 检查输出目录，确保图像文件生成
            generated_files = [f for f in os.listdir(output_dir) if f.endswith(('.jpg', '.png'))]
            if not generated_files:
                logger.error(f"输出目录 {output_dir} 中未找到生成的图像文件")
                raise RuntimeError(f"未生成图像文件：{output_dir}")
            logger.info(f"生成的文件：{generated_files}")
            return True
            
        except FileNotFoundError as e:
            if reference_image:
                logger.error(f"参考图像文件错误：{str(e)}")
                raise
            logger.warning("无参考图像，将尝试纯文本生成")
        except Exception as e:
            if "Status: 429" in str(e) or "too many requests" in str(e).lower():
                if attempt < max_retries - 1:
                    logger.warning(f"遇到 429 错误，等待重试（第 {attempt + 1} 次）")
                    time.sleep(60)
                    continue
                raise RuntimeError("达到最大重试次数，API 配额限制")
            elif "auth failed" in str(e).lower():
                logger.error("Kling API 认证失败，请检查 ACCESSKEY_API 和 ACCESSKEY_SECRET")
                raise RuntimeError(f"Kling API 认证失败：{str(e)}")
            logger.error(f"生成关键帧图像失败：{str(e)}")
            logger.exception("详细错误堆栈：")
            raise RuntimeError(f"生成关键帧图像失败：{str(e)}")
    raise RuntimeError("生成关键帧图像失败：达到最大重试次数")
@run_agent
def run(agent: MofaAgent):
    try:
        # 初始化 event['metadata']
        if not hasattr(agent, 'event') or agent.event is None:
            agent.event = {'metadata': {}}
        elif 'metadata' not in agent.event:
            agent.event['metadata'] = {}

        # 接收输入
        user_input = agent.receive_parameter('query')
        logger.info(f"收到输入：{user_input}, 类型：{type(user_input)}, 长度：{len(user_input) if isinstance(user_input, str) else 0}")

        if not user_input:
            logger.error("未提供有效输入，终止处理")
            agent.send_output(
                agent_output_name='kling_result',
                agent_result=json.dumps({"value": "错误：未提供有效输入信号"})
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
            # 输入为 .env 文件，使用相对路径
            env_file_path = os.path.normpath(
                user_input if os.path.isabs(user_input) else os.path.join(BASE_DIR, "..", "..", "examples", "kling", user_input)
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
            logger.info("输入为关键帧描述文本，作为触发信号")
            keyframes_content = user_input
            # 写入临时关键帧文件到 ./tmp 目录
            tmp_dir = os.path.join(BASE_DIR, "tmp")
            os.makedirs(tmp_dir, exist_ok=True)
            keyframes_txt_path = os.path.join(tmp_dir, "temp_keyframes.txt")
            try:
                with open(keyframes_txt_path, 'w', encoding='utf-8') as f:
                    f.write(keyframes_content)
                logger.info(f"已创建临时关键帧文件：{keyframes_txt_path}")
            except Exception as e:
                logger.error(f"写入临时关键帧文件失败：{str(e)}")
                agent.send_output(
                    agent_output_name='kling_result',
                    agent_result=json.dumps({"value": f"错误：写入临时关键帧文件失败 - {str(e)}"})
                )
                return
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
            if not os.path.isfile(keyframes_txt_path):
                logger.error(f"关键帧文件不存在：{keyframes_txt_path}")
                agent.send_output(
                    agent_output_name='kling_result',
                    agent_result=json.dumps({"value": f"错误：关键帧文件不存在：{keyframes_txt_path}"})
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
            default_keyframes_path = os.path.join(BASE_DIR, "..", "..", "examples", "script2video", "output", "videoprompt_output.txt")
            logger.warning(f"关键帧文件路径未定义，使用默认路径：{default_keyframes_path}")
            keyframes_txt_path = default_keyframes_path
            if not os.path.isfile(keyframes_txt_path):
                logger.error(f"默认关键帧文件不存在：{keyframes_txt_path}")
                agent.send_output(
                    agent_output_name='kling_result',
                    agent_result=json.dumps({"value": f"错误：默认关键帧文件不存在：{keyframes_txt_path}"})
                )
                return

        # 从环境变量获取参考图像和输出目录
        reference_image = os.getenv("IMAGE_REFERENCE_IMAGE")
        output_keyframes_dir = os.getenv("IMAGE_OUTPUT_KEYFRAMES", os.path.join(BASE_DIR, "..", "..", "examples", "script2video", "output", "output_keyframes"))

        # 验证环境变量
        required_env_vars = ["ACCESSKEY_API", "ACCESSKEY_SECRET", "KLING_API_BASE_URL"]
        for var in required_env_vars:
            logger.debug(f"环境变量 {var}: {os.getenv(var, '未设置')}")
            if not os.getenv(var):
                logger.error(f"环境变量 {var} 未设置")
                agent.send_output(
                    agent_output_name='kling_result',
                    agent_result=json.dumps({"value": f"错误：环境变量 {var} 未设置"})
                )
                return

        # 读取关键帧文件
        try:
            with open(keyframes_txt_path, 'r', encoding='utf-8') as f:
                keyframes_content = f.read().strip()
        except Exception as e:
            logger.error(f"读取关键帧文件失败：{str(e)}")
            agent.send_output(
                agent_output_name='kling_result',
                agent_result=json.dumps({"value": f"错误：读取关键帧文件失败 - {str(e)}"})
            )
            return
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
        try:
            success = generate_keyframes_images(
                keyframes_file=keyframes_txt_path,
                reference_image=reference_image,
                output_dir=output_keyframes_dir,
                negative_prompt=negative_prompt,
                aspect_ratio=aspect_ratio
            )
        except Exception as e:
            logger.error(f"调用 generate_keyframes_images 失败：{str(e)}")
            agent.send_output(
                agent_output_name='kling_result',
                agent_result=json.dumps({"value": f"错误：生成关键帧图像失败 - {str(e)}"})
            )
            return

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
        logger.exception("详细错误堆栈：")
        agent.send_output(
            agent_output_name='kling_result',
            agent_result=json.dumps({"value": f"错误：运行异常 - {str(e)}"})
        )

def main():
    agent = MofaAgent(agent_name='kling-agent-image')
    run(agent)

if __name__ == "__main__":
    main()