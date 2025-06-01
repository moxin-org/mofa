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
    filename='/root/mofa-euterpe/python/logs/logs-videoprompt.txt',
    filemode='a'
)
logger = logging.getLogger('videoprompt')

@run_agent
def run(agent: MofaAgent):
    try:
        logger.info("Starting run function for videoprompt")

        # 读取参数
        logger.info("Receiving query parameter")
        user_input = agent.receive_parameter('query')
        logger.debug(f"Received user_input: {user_input!r}")

        if not user_input or not user_input.strip():
            logger.error("Query parameter 'query' is empty or None")
            raise ValueError("Query parameter 'query' is empty or None")

        # 初始化变量
        videoprompt_text = None
        description_path = "/root/mofa-euterpe/python/examples/script2video/output/keyframes_output.txt"
        output_path = "/root/mofa-euterpe/python/examples/script2video/output/videoprompt_output.txt"
        llm_base = "https://api.deepseek.com/v1"
        llm_model = "deepseek-chat"
        llm_api_key = None

        # 判断输入类型
        if user_input.endswith(".env") or user_input.endswith(".env.secret"):
            # 输入是 .env 文件路径
            env_path = user_input
            BASE_DIR_DEFAULT = "/root/mofa-euterpe/python/examples/script2video"
            if not os.path.isabs(env_path):
                env_path = os.path.join(BASE_DIR_DEFAULT, env_path)
            logger.info(f"Input identified as .env file path, resolved to: {env_path}")

            if not os.path.exists(env_path):
                logger.error(f".env file not found at: {env_path}")
                raise FileNotFoundError(f".env file not found: {env_path}")

            # 加载 .env 文件
            logger.info(f"Loading .env file: {env_path}")
            load_dotenv(env_path)

            # 环境变量
            description_path = os.getenv("VIDEO_PROMPT_TXT", description_path)
            output_path = os.getenv("VIDEO_PROMPT_OUTPUT", output_path)
            llm_base = os.getenv("LLM_API_BASE", llm_base)
            llm_model = os.getenv("LLM_MODEL", llm_model)
            llm_api_key = os.getenv("LLM_API_KEY")

            logger.info(f"Loaded env: description_path={description_path}, output_path={output_path}, llm_base={llm_base}, llm_model={llm_model}, llm_api_key={'set' if llm_api_key else 'unset'}")

            # 校验环境变量
            if not description_path:
                logger.error("VIDEO_PROMPT_TXT not set in .env")
                raise ValueError("VIDEO_PROMPT_TXT not set in .env")
            if not output_path:
                logger.error("VIDEO_PROMPT_OUTPUT not set in .env")
                raise ValueError("VIDEO_PROMPT_OUTPUT not set in .env")
            if not llm_api_key:
                logger.error("LLM_API_KEY not set in .env")
                raise ValueError("LLM_API_KEY not set in .env")
            if not llm_base:
                logger.error("LLM_API_BASE not set in .env")
                raise ValueError("LLM_API_BASE not set in .env")

            # 校验路径
            logger.info(f"Checking description_path: {description_path}")
            if not os.path.exists(description_path):
                logger.error(f"videoprompt description file not found: {description_path}")
                raise FileNotFoundError(f"videoprompt description file not found: {description_path}")

            # 读取视频提示描述
            logger.info(f"Reading videoprompt description from: {description_path}")
            with open(description_path, "r", encoding="utf-8") as f:
                videoprompt_text = f.read().strip()
            if not videoprompt_text:
                logger.error("videoprompt description file is empty")
                raise ValueError("videoprompt description file is empty")
            logger.debug(f"videoprompt description: {videoprompt_text[:50]}...")
        else:
            # 输入是关键帧描述内容
            logger.info("Input identified as keyframe description content")
            videoprompt_text = user_input
            # 硬编码必要的环境变量（如果未通过 .env 提供）
            llm_api_key = os.getenv("LLM_API_KEY", "***REMOVED***")
            if not llm_api_key:
                logger.error("LLM_API_KEY not set in environment")
                raise ValueError("LLM_API_KEY not set in environment")

        # 校验输出路径
        logger.info(f"Checking output directory for: {output_path}")
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            logger.info(f"Creating output directory: {output_dir}")
            os.makedirs(output_dir, exist_ok=True)

        # 构造更新后的提示词
        creative_prompt = f"""
你是一个视频提示词生成器，任务是从输入多组的Frame Prompt中提取可以分配动作的元素（人物或非人物），为每个元素分配简单、适合其类型的动作，生成固定5秒的Kling视频提示词。动作仅限人物（挥手、微笑、走动、搓手）或非人物（淡入、滑入、视角转换），提示词仅描述元素和动作。

输入描述：{videoprompt_text}

### 指令
1. **元素提取**：
   - 从Prompt中识别可分配动作的元素，最多选取3个：
     - **人物**：探险家、科学家、观众等（包含“探险家”“科学家”“人物”等关键词）。
     - **非人物**：图标、卷轴、机械鸟、徽章、屏幕、转盘等动态或前景元素。
   - 忽略静态背景（如城市天际线、埃菲尔铁塔、布幔），仅提取可动元素。
   - 确定元素类型：
     - 人物：包含“探险家”“科学家”“观众”“肖像”。
     - 非人物：图标、卷轴、机械鸟、徽章、屏幕等。

2. **动作分配**：
   - 为每个元素分配一个简单动作：
     - **人物**：
       - 挥手：手部轻微挥动（适合科学家、观众）。
       - 微笑：面部表情变化（适合探险家、肖像）。
       - 走动：缓慢向前迈步（适合探险家）。
       - 搓手：双手摩擦表示期待（适合期待情境）。
     - **非人物**：
       - 淡入：从中心出现（适合图标、徽章）。
       - 滑入：从左侧、右侧、底部进入（适合卷轴、文本、屏幕）。
       - 视角转换：轻微放大或平移（适合转盘、机械鸟）。
   - 动作分配规则：
     - 人物：根据情境选择（例如，探险家坚定神情用微笑，期待用搓手）。
     - 非人物：图标/徽章用淡入，卷轴/屏幕用滑入，动态物体（如机械鸟、转盘）用视角转换。
   - 动作时长：
     - 每个动作1秒，剩余时间稳定显示。
     - 最多3个动作，渐变切换。
     - 人物照片/肖像（2个）：每张2秒（0.5秒滑入+微笑，1.5秒显示）。

3. **时间分配**：
   - 固定时长0-5秒。
   - 单个元素：1秒动作，4秒稳定显示。
   - 两个元素：每个1秒动作，3秒并排显示。
   - 三个元素：每个1秒动作，2秒并排显示。
   - 人物肖像（2个）：每张2秒（0.5秒滑入+微笑，1.5秒显示）。

4. **输出格式**：
   - 使用以下结构化格式：
     ```
     [元素1]执行[动作]，持续[时间]。[元素2]执行[动作]，持续[时间]。
     ```
   - 如果只有一个元素，省略多余句。
   - 仅描述元素和动作，不添加风格、音乐或其他描述。

### 示例
**输入**：
- f[Frame 1]  
[Frame 1]  
Prompt: A Tintin-style explorer in a blue coat and red scarf stands atop a vintage Parisian rooftop, pointing excitedly at a glowing "GOSIM AI Paris 2025" logo floating above the Eiffel Tower. The logo is designed as a retro-futuristic brass plaque with intricate gears and AI circuit motifs. The sky is a cheerful blue with puffy white clouds, and the scene is bathed in warm golden sunlight. Tiny cartoon AI robots hover around the logo, emitting sparkles.  
NegativePrompt: 模糊，低分辨率，渐变色，超写实，3D渲染，水彩画风格，线条潦草，色彩暗淡，现代设计，复杂阴影，写实纹理，任何文字，模糊边缘，杂乱背景。  
AspectRatio: 9:16  

[Frame 2]  
Prompt: The explorer now kneels on a giant open book with pages made of scrolling code. A whimsical neural network grows like a vine from the book, with glowing nodes as flowers. Two cartoon speaker portraits pop up like vintage stamps - one with a professor owl in goggles, another with a robot chef holding a baguette-shaped GPU. The background is a cozy library with brass telescopes and bubbling test tubes.  
NegativePrompt: 模糊，低分辨率，渐变色，超写实，3D渲染，水彩画风格，线条潦草，色彩暗淡，现代设计，复杂阴影，写实纹理，任何文字，模糊边缘，杂乱背景。  
AspectRatio: 9:16    

**输出**：
[Frame 1]
卡通AI图标执行视角转换，持续1秒。探险家执行微笑，持续1秒。地图执行滑入，持续1秒。

**输入**：
- frame_prompt: 丁丁风格的探险家步入巨大透明圆顶建筑，建筑内部漂浮着多层次发光的神经网络模型，如3D网状星球缓慢旋转，闪耀科技光芒。四周设有卡通化操作台，多位穿着鲜亮黄蓝测试服的卡通科学家围绕模型忙碌，动作夸张，表情兴奋，佩戴护目镜。建筑墙面上浮动着魔法图腾投影，象征“AI Model Track”，无任何文字。半空中漂浮幻彩屏幕，展示两位风格统一的卡通探险家肖像，一人戴未来感护目镜，一人举发光卷轴，其上方悬浮代表身份的图形化卡通徽章。整个空间中光影柔和，色调以蓝黄红为主，结构清晰，Ligne claire技法描边，整体保持9:16比例，细节丰富，呈现卡通未来感与探险情境融合风格。

**输出**：
探险家执行走动，持续1秒。第一位卡通探险家肖像执行微笑，持续2秒。第二位卡通探险家肖像执行微笑，持续2秒。

### 注意事项
- 人物动作仅限挥手、微笑、走动、搓手；非人物动作仅限淡入、滑入、视角转换。
- 最多3个元素，忽略静态背景（如天际线、建筑）。
- 人物肖像（2个）：每张2秒（0.5秒滑入+微笑，1.5秒显示）。
- 如果Prompt不完整，假设单个元素（例如探险家），使用微笑。
- 不添加风格、音乐或其他描述。
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
            agent_output_name="videoprompt_result",
            agent_result=result
        )

        logger.info("videoprompt generation completed successfully.")
        success_message = f"🎉 Successfully generated Tintin-style videoprompts! Output saved to {output_path}"
        logger.info(success_message)
        print(success_message)

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}", exc_info=True)
        agent.send_output(
            agent_output_name="videoprompt_result",
            agent_result=f"❌ Error: {str(e)}"
        )
        raise

def main():
    logger.info("Creating MofaAgent instance")
    agent = MofaAgent(agent_name='videoprompt')
    logger.info("Running agent")
    run(agent=agent)

if __name__ == "__main__":
    main()