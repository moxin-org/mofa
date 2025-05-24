from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
import json
import os
import subprocess
import time
from dotenv import load_dotenv

# 动态确定 .env.secret 的路径，相对于 main.py 的位置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取 agent-hub/kling-agent 目录
ENV_FILE_PATH = os.path.join(BASE_DIR, ".env.secret")  # 修正为直接在 BASE_DIR 下

# 定义基准目录，路径将基于此解析
KLING_BASE_DIR = "/root/mofa-euterpe/python/examples/kling"

def run_dify_workflow(api_key: str, script_input: str) -> str:
    """调用 Dify API 生成 keyframes.txt"""
    print("调用 Dify API 生成 keyframes.txt")
    url = "https://api.dify.ai/v1/workflows/run"
    
    if not api_key.isascii():
        raise ValueError("API Key 必须仅包含 ASCII 字符")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json; charset=utf-8"
    }
    
    payload = {
        "inputs": {
            "script": script_input
        },
        "response_mode": "blocking",
        "user": "difyuser"
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload, ensure_ascii=False).encode("utf-8"), timeout=30)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise Exception("Dify API 请求超时")
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP 错误：{str(e)} 响应内容：{e.response.text}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"请求失败：{str(e)} 响应内容：{e.response.text if e.response else '无响应内容'}")
    
    result = response.json()
    print(f"Dify API 响应：{result}")
    if "data" not in result or "outputs" not in result["data"]:
        raise Exception("Dify API 响应格式错误，未找到 outputs")
    
    keyframes_txt = result["data"]["outputs"].get("Creativity_Output", "")
    if not keyframes_txt:
        raise Exception("未从 Dify API 获取到 keyframes.txt 内容")
    
    return keyframes_txt

def save_keyframes_txt(keyframes_txt: str, output_path: str) -> str:
    """保存 keyframes.txt 到指定路径"""
    print("保存 keyframes.txt")
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
    except Exception as e:
        raise Exception(f"创建目录失败：{str(e)}")
    
    try:
        keyframes_txt.encode("utf-8")
    except UnicodeEncodeError:
        keyframes_txt = keyframes_txt.encode("utf-8", errors="ignore").decode("utf-8")
    
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(keyframes_txt)
        print(f"keyframes.txt 保存到 {output_path}")
        return output_path
    except Exception as e:
        raise Exception(f"保存 keyframes.txt 失败：{str(e)}")

def generate_keyframes_images(keyframes_file: str, reference_image: str, output_dir: str) -> bool:
    """生成关键帧图像"""
    print("生成关键帧图像")
    project_root = os.path.abspath(os.path.join(BASE_DIR, "../../examples/kling"))
    print(f"切换工作目录到：{project_root}")
    if not os.path.exists(project_root):
        raise FileNotFoundError(f"工作目录不存在：{project_root}")
    os.chdir(project_root)
    
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{project_root}"
    env["ACCESSKEY_API"] = os.getenv("ACCESSKEY_API")
    env["ACCESSKEY_SECRET"] = os.getenv("ACCESSKEY_SECRET")
    env["KLING_API_BASE_URL"] = os.getenv("KLING_API_BASE_URL", "https://api.klingai.com")
    env["KLING_TOKEN_EXPIRATION"] = os.getenv("KLING_TOKEN_EXPIRATION", "1800")
    env["KLING_API_TIMEOUT"] = os.getenv("KLING_API_TIMEOUT", "60")
    env["KLING_API_MAX_RETRIES"] = os.getenv("KLING_API_MAX_RETRIES", "3")
    
    print(f"参考图像路径：{reference_image}")
    if not os.path.exists(reference_image):
        print(f"警告：参考图像 {reference_image} 不存在，将尝试纯文本生成")
    
    cmd = [
        "python", "-m", "klingdemo.examples.keyframe_gen_demo",
        "--keyframes-file", keyframes_file,
        "--reference-image", reference_image,
        "--model", "kling-v1-5",
        "--image-fidelity", "0.7",
        "--output-dir", output_dir
    ]
    
    print(f"执行命令：{' '.join(cmd)}")
    max_retries = int(os.getenv("KLING_API_MAX_RETRIES", "3"))
    for attempt in range(max_retries):
        try:
            result = subprocess.run(cmd, check=True, env=env, capture_output=True, text=True)
            print(f"命令输出：{result.stdout}")
            if "ERROR" in result.stdout or not result.stdout.strip():
                raise Exception(f"命令执行失败，输出为空或包含错误：{result.stdout}")
            print(f"命令错误（如果有）：{result.stderr}")
            return True
        except subprocess.CalledProcessError as e:
            if "Status: 429" in str(e.stdout):
                if attempt < max_retries - 1:
                    print(f"遇到 429 错误，等待重试（第 {attempt + 1} 次）")
                    time.sleep(60)  # 等待 60 秒后重试
                    continue
            raise Exception(f"生成关键帧图像失败：{str(e)}\n命令输出：{e.stdout}\n命令错误：{e.stderr}")
    raise Exception("生成关键帧图像失败：达到最大重试次数")

@run_agent
def run(agent: MofaAgent):
    try:
        print(f"加载环境变量从 {ENV_FILE_PATH}")
        if not os.path.exists(ENV_FILE_PATH):
            raise FileNotFoundError(f"环境变量文件 {ENV_FILE_PATH} 不存在")
        load_dotenv(ENV_FILE_PATH, verbose=True)
        
        print("调试：打印所有环境变量：")
        for key, value in os.environ.items():
            if key in ["DIFY_API_KEY", "ACCESSKEY_API", "ACCESSKEY_SECRET", "KLING_API_BASE_URL", 
                      "KLING_TOKEN_EXPIRATION", "KLING_API_TIMEOUT", "KLING_API_MAX_RETRIES",
                      "image-INPUT_DIR", "image-REFERENCE_IMAGE", "image-INPUT_SCRIPT", 
                      "image-OUTPUT_DIR", "image-KEYFRAMES_TXT", "image-OUTPUT_KEYFRAMES"]:
                print(f"{key}: {value}")
        
        api_key = os.getenv("DIFY_API_KEY")
        print(f"DIFY_API_KEY: {api_key}")
        if not api_key:
            raise Exception("环境变量 DIFY_API_KEY 未设置")
        
        accesskey_api = os.getenv("ACCESSKEY_API")
        accesskey_secret = os.getenv("ACCESSKEY_SECRET")
        print(f"ACCESSKEY_API: {accesskey_api}")
        print(f"ACCESSKEY_SECRET: {accesskey_secret}")
        if not accesskey_api or not accesskey_secret:
            raise Exception("环境变量 ACCESSKEY_API 或 ACCESSKEY_SECRET 未设置")

        # 从环境变量中读取路径（相对路径）
        reference_image_rel = os.getenv("image-REFERENCE_IMAGE")
        keyframes_txt_rel = os.getenv("image-KEYFRAMES_TXT")
        output_keyframes_rel = os.getenv("image-OUTPUT_KEYFRAMES")
        input_script_rel = os.getenv("image-INPUT_SCRIPT")
        
        # 调试：打印读取的环境变量值
        print(f"image-REFERENCE_IMAGE: {reference_image_rel}")
        print(f"image-KEYFRAMES_TXT: {keyframes_txt_rel}")
        print(f"image-OUTPUT_KEYFRAMES: {output_keyframes_rel}")
        print(f"image-INPUT_SCRIPT: {input_script_rel}")

        if not all([reference_image_rel, keyframes_txt_rel, output_keyframes_rel, input_script_rel]):
            raise Exception("环境变量中缺少必要的路径配置：image-REFERENCE_IMAGE, image-KEYFRAMES_TXT, image-OUTPUT_KEYFRAMES, image-INPUT_SCRIPT")

        # 将相对路径解析为绝对路径，基于 KLING_BASE_DIR
        reference_image = os.path.join(KLING_BASE_DIR, reference_image_rel)
        keyframes_txt_path = os.path.join(KLING_BASE_DIR, keyframes_txt_rel)
        output_keyframes_dir = os.path.join(KLING_BASE_DIR, output_keyframes_rel)
        input_script_path = os.path.join(KLING_BASE_DIR, input_script_rel)

        user_input = agent.receive_parameter('query')
        print(f"接收到的输入：{user_input!r}")
        
        if user_input is None or not user_input.strip():
            print("未提供有效输入，终止处理")
            if not hasattr(agent, 'event') or agent.event is None:
                agent.event = {}
            if 'metadata' not in agent.event:
                agent.event['metadata'] = {}
            agent.send_output(
                agent_output_name='cling_result',
                agent_result="错误：未提供输入，请输入脚本内容或脚本文件路径后重试。"
            )
            print("已发送提示信息，流程终止")
            return
        
        script_input = user_input
        # 检查输入是否是 .env 文件路径（相对路径或绝对路径）
        if user_input.endswith(".env.secret"):
            env_file_path = user_input
            if not os.path.isabs(user_input):
                env_file_path = os.path.join(KLING_BASE_DIR, user_input)
            print(f"输入被识别为 .env 文件路径，解析为：{env_file_path}")
            if os.path.isfile(env_file_path):
                try:
                    # 加载 .env 文件（这里已经加载了 ENV_FILE_PATH，但允许用户输入覆盖）
                    print(f"加载用户输入的 .env 文件：{env_file_path}")
                    load_dotenv(env_file_path, verbose=True, override=True)
                    # 调试：重新打印环境变量
                    print("加载用户 .env 文件后，重新打印环境变量：")
                    for key, value in os.environ.items():
                        if key in ["DIFY_API_KEY", "ACCESSKEY_API", "ACCESSKEY_SECRET", "KLING_API_BASE_URL", 
                                  "KLING_TOKEN_EXPIRATION", "KLING_API_TIMEOUT", "KLING_API_MAX_RETRIES",
                                  "image-INPUT_DIR", "image-REFERENCE_IMAGE", "image-INPUT_SCRIPT", 
                                  "image-OUTPUT_DIR", "image-KEYFRAMES_TXT", "image-OUTPUT_KEYFRAMES"]:
                            print(f"{key}: {value}")
                    # 重新读取 image-INPUT_SCRIPT（如果用户输入了新的 .env 文件）
                    input_script_rel = os.getenv("image-INPUT_SCRIPT")
                    print(f"用户输入的 .env 文件中读取的 image-INPUT_SCRIPT: {input_script_rel}")
                    if not input_script_rel:
                        raise Exception("用户提供的 .env 文件中未定义 image-INPUT_SCRIPT 路径")
                    input_script_path = os.path.join(KLING_BASE_DIR, input_script_rel)
                except Exception as e:
                    print(f"读取用户提供的 .env 文件失败：{str(e)}")
                    if not hasattr(agent, 'event') or agent.event is None:
                        agent.event = {}
                    if 'metadata' not in agent.event:
                        agent.event['metadata'] = {}
                    agent.send_output(
                        agent_output_name='cling_result',
                        agent_result=f"错误：读取用户提供的 .env 文件失败：{str(e)}"
                    )
                    return
            else:
                print(f"错误：用户提供的 .env 文件不存在：{env_file_path}")
                if not hasattr(agent, 'event') or agent.event is None:
                    agent.event = {}
                if 'metadata' not in agent.event:
                    agent.event['metadata'] = {}
                agent.send_output(
                    agent_output_name='cling_result',
                    agent_result=f"错误：用户提供的 .env 文件不存在：{env_file_path}"
                )
                return

        # 检查输入是否是脚本文件路径
        if os.path.isfile(user_input):
            print(f"输入被识别为文件路径：{user_input}")
            try:
                with open(user_input, "r", encoding="utf-8") as f:
                    script_input = f.read().strip()
                print(f"从文件 {user_input} 读取到脚本内容：{script_input!r}")
            except Exception as e:
                print(f"读取脚本文件失败：{str(e)}")
                if not hasattr(agent, 'event') or agent.event is None:
                    agent.event = {}
                if 'metadata' not in agent.event:
                    agent.event['metadata'] = {}
                agent.send_output(
                    agent_output_name='cling_result',
                    agent_result=f"错误：读取脚本文件失败：{str(e)}"
                )
                return
        else:
            print("输入被识别为直接脚本内容")

        # 如果输入是脚本路径，验证是否与 image-INPUT_SCRIPT 匹配
        if user_input != script_input:  # 表示 user_input 是文件路径
            expected_input_script = input_script_path
            if os.path.abspath(user_input) != os.path.abspath(expected_input_script):
                print(f"警告：输入的脚本路径 {user_input} 与 .env 文件中定义的 image-INPUT_SCRIPT {expected_input_script} 不匹配")
        
        if not script_input:
            print("脚本内容为空，终止处理")
            if not hasattr(agent, 'event') or agent.event is None:
                agent.event = {}
            if 'metadata' not in agent.event:
                agent.event['metadata'] = {}
            agent.send_output(
                agent_output_name='cling_result',
                agent_result="错误：脚本内容为空，请提供有效的脚本内容。"
            )
            print("已发送提示信息，流程终止")
            return
        
        print("收到有效脚本内容，继续处理")
        
        keyframes_txt = run_dify_workflow(api_key, script_input)
        
        keyframes_file = save_keyframes_txt(keyframes_txt, keyframes_txt_path)
        
        success = generate_keyframes_images(keyframes_file, reference_image, output_keyframes_dir)
        
        if not hasattr(agent, 'event') or agent.event is None:
            agent.event = {}
        if 'metadata' not in agent.event:
            agent.event['metadata'] = {}

        if success:
            print("发送输出")
            agent.send_output(
                agent_output_name='cling_result',
                agent_result="关键帧图像已生成到 output_keyframes"
            )
        else:
            print("生成失败，未发送成功输出")
            agent.send_output(
                agent_output_name='cling_result',
                agent_result="错误：关键帧图像生成失败"
            )
        
    except Exception as e:
        print(f"Error: {str(e)}")
        if not hasattr(agent, 'event') or agent.event is None:
            agent.event = {}
        if 'metadata' not in agent.event:
            agent.event['metadata'] = {}
        agent.send_output(
            agent_output_name='cling_result',
            agent_result=f"Error: {str(e)}"
        )

def main():
    agent = MofaAgent(agent_name='kling-agent')
    run(agent=agent)

if __name__ == "__main__":
    main()