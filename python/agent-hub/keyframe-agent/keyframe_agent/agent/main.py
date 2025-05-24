import os
import logging
import warnings
import requests
from dotenv import load_dotenv
from mofa.agent_build.base.base_agent import MofaAgent, run_agent

# 抑制 Pydantic 警告
warnings.filterwarnings("ignore", category=DeprecationWarning)

# 日志设置
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='/root/mofa-euterpe/python/logs/log_keyframe-agent.txt',
    filemode='a'
)
logger = logging.getLogger('keyframe-agent')

@run_agent
def run(agent: MofaAgent):
    try:
        logger.info("Starting run function for keyframe-agent")

        # 读取参数
        logger.info("Receiving query parameter")
        env_path = agent.receive_parameter('query')
        logger.debug(f"Received env_path: {env_path}")
        if env_path is None:
            logger.error("Query parameter 'query' is None")
            raise ValueError("Query parameter 'query' is None")
        if not os.path.exists(env_path):
            logger.error(f".env file not found at: {env_path}")
            raise FileNotFoundError(f".env file not found: {env_path}")

        # 加载 .env.secret
        logger.info(f"Loading .env file: {env_path}")
        load_dotenv(env_path)

        # 环境变量
        description_path = os.getenv("KEYFRAME_TXT")
        output_path = os.getenv("KEYFRAME_OUTPUT")
        llm_base = os.getenv("LLM_API_BASE")
        llm_model = os.getenv("LLM_MODEL", "deepseek-chat")
        llm_api_key = os.getenv("LLM_API_KEY")

        logger.info(f"Loaded env: description_path={description_path}, output_path={output_path}, llm_base={llm_base}, llm_model={llm_model}, llm_api_key={'set' if llm_api_key else 'unset'}")

        # 校验环境变量
        if not description_path:
            logger.error("KEYFRAME_TXT not set in .env")
            raise ValueError("KEYFRAME_TXT not set in .env")
        if not output_path:
            logger.error("KEYFRAME_OUTPUT not set in .env")
            raise ValueError("KEYFRAME_OUTPUT not set in .env")
        if not llm_api_key:
            logger.error("LLM_API_KEY not set in .env")
            raise ValueError("LLM_API_KEY not set in .env")
        if not llm_base:
            logger.error("LLM_API_BASE not set in .env")
            raise ValueError("LLM_API_BASE not set in .env")

        # 校验路径
        logger.info(f"Checking description_path: {description_path}")
        if not os.path.exists(description_path):
            logger.error(f"Keyframe description file not found: {description_path}")
            raise FileNotFoundError(f"Keyframe description file not found: {description_path}")

        logger.info(f"Checking output directory for: {output_path}")
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            logger.error(f"Output directory not found: {output_dir}")
            raise FileNotFoundError(f"Output directory not found: {output_dir}")

        # 读取关键帧描述
        logger.info(f"Reading keyframe description from: {description_path}")
        with open(description_path, "r", encoding="utf-8") as f:
            keyframe_text = f.read().strip()
        if not keyframe_text:
            logger.error("Keyframe description file is empty")
            raise ValueError("Keyframe description file is empty")
        logger.debug(f"Keyframe description: {keyframe_text[:50]}...")

        # 构造提示词
        creative_prompt = f"""
你是一个创意生成助手，擅长将输入的描述转化为丁丁风格的探险故事关键帧创意。丁丁风格要求：
- 融入丁丁式探险家形象：穿浅蓝色探险外套、红色飞扬围巾、背棕色背包，动作夸张，表情卡通化。
- 使用 ligne claire 技法：粗细均匀的黑色描边，色块明亮饱和（以红、黄、蓝为主），卡通夸张感，仿旧纸张质感。
- 场景需适合 9:16 比例，温暖自然光，中焦视角，超高细节，卡通化光影，4K 分辨率。
- 避免图像中出现文字，将文字元素（如字幕）转为卡通化元素（如卡通卷轴、指南针）。

输入描述：{keyframe_text}

要求输出如下结构，每一帧都包括：
只需要输出关键帧描述，不要输出其他任何提示信息
[Frame X]
Prompt: （画面应卡通化、富有创意与视觉细节，符合“丁丁历险记”风格）
NegativePrompt: 模糊，低分辨率，渐变色，超写实，3D渲染，水彩画风格，线条潦草，色彩暗淡，现代设计，复杂阴影，写实纹理，任何文字，模糊边缘，杂乱背景。
AspectRatio: 9:16
"""

        # 调用 DeepSeek API
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {llm_api_key}"
        }
        payload = {
            "model": llm_model,
            "messages": [
                {"role": "system", "content": "You are a creative assistant for Tintin-style keyframe stories."},
                {"role": "user", "content": creative_prompt}
            ],
            "temperature": 0.7,
        }

        logger.info("Sending request to DeepSeek API")
        response = requests.post(f"{llm_base}/chat/completions", headers=headers, json=payload, timeout=60)
        if response.status_code != 200:
            logger.error(f"DeepSeek API error: {response.status_code} - {response.text}")
            raise RuntimeError(f"DeepSeek API error: {response.status_code}: {response.text}")

        data = response.json()
        result = data["choices"][0]["message"]["content"]

        logger.info(f"Writing result to {output_path}")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)

        agent.send_output(
            agent_output_name="keyframe_result",
            agent_result=result
        )

        logger.info("Keyframe generation completed successfully.")
        success_message = f"🎉 Successfully generated Tintin-style keyframes! Output saved to {output_path}"
        logger.info(success_message)
        print(success_message)

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}", exc_info=True)
        agent.send_output(
            agent_output_name="keyframe_result",
            agent_result=f"❌ Error: {str(e)}"
        )
        raise

def main():
    logger.info("Creating MofaAgent instance")
    agent = MofaAgent(agent_name='keyframe-agent')
    logger.info("Running agent")
    run(agent=agent)

if __name__ == "__main__":
    main()