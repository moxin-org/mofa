import argparse
import os
from loguru import logger
from klingdemo.api import KlingAPIClient
from klingdemo.utils import setup_logging, keyframe_parser

def main():
    # 参数解析
    parser = argparse.ArgumentParser(description="生成关键帧")
    parser.add_argument(
        "--keyframes-file",
        default=os.path.join("Input", "keyframes.txt"),
        help="包含关键帧描述的 .txt 文件路径，默认为 Input/keyframes.txt"
    )
    parser.add_argument(
        "--reference-image",
        default=None,
        help="人物参考图像路径，可选，默认为 None"
    )
    parser.add_argument(
        "--model",
        default="kling-v1-5",
        help="使用的模型名称，默认为 kling-v1-5"
    )
    parser.add_argument(
        "--image-fidelity",
        type=float,
        default=0.5,
        help="参考图像遵循度，默认为 0.5（仅当提供参考图像时生效）"
    )
    parser.add_argument(
        "--output-dir",
        default="output_keyframes",
        help="原始关键帧输出目录，默认为 output_keyframes"
    )
    
    args = parser.parse_args()

    # 设置日志
    setup_logging()

    # 从环境变量加载 Kling API 配置
    access_key = os.getenv("ACCESSKEY_API")
    secret_key = os.getenv("ACCESSKEY_SECRET")
    base_url = os.getenv("KLING_API_BASE_URL", "https://api.klingai.com")
    token_expiration = int(os.getenv("KLING_TOKEN_EXPIRATION", 1800))
    timeout = int(os.getenv("KLING_API_TIMEOUT", 60))
    max_retries = int(os.getenv("KLING_API_MAX_RETRIES", 3))

    # 验证必须的配置
    if not access_key or not secret_key:
        logger.error("ACCESSKEY_API 或 ACCESSKEY_SECRET 未设置")
        raise ValueError("ACCESSKEY_API 或 ACCESSKEY_SECRET 未设置")

    # 创建客户端
    client = KlingAPIClient(
        access_key=access_key,
        secret_key=secret_key,
        base_url=base_url,
        token_expiration=token_expiration,
        timeout=timeout,
        max_retries=max_retries
    )

    # 确保输出目录存在
    os.makedirs(args.output_dir, exist_ok=True)

    # 解析关键帧描述
    keyframes = keyframe_parser.parse_keyframes(args.keyframes_file)

    # 生成关键帧
    results = []
    try:
        if args.reference_image and os.path.exists(args.reference_image):
            logger.info(f"使用参考图像生成关键帧：{args.reference_image}")
            # 使用参考图像生成关键帧
            results = client.create_keyframes_from_text_and_image(
                keyframes=keyframes,
                reference_image_path=args.reference_image,
                model_name=args.model,
                image_fidelity=args.image_fidelity,
                output_dir=args.output_dir
            )
        else:
            logger.info("未提供参考图像，仅使用文本描述生成关键帧")
            # 仍然使用 create_keyframes_from_text_and_image，但不传递参考图像参数
            results = client.create_keyframes_from_text_and_image(
                keyframes=keyframes,
                reference_image_path=None,
                model_name=args.model,
                image_fidelity=None,
                output_dir=args.output_dir
            )
    except Exception as e:
        if "No face detected" in str(e) and args.reference_image:
            logger.warning(f"参考图像 {args.reference_image} 未检测到人脸，切换到纯文本生成")
            try:
                results = client.create_keyframes_from_text_and_image(
                    keyframes=keyframes,
                    reference_image_path=None,
                    model_name=args.model,
                    image_fidelity=None,
                    output_dir=args.output_dir
                )
            except Exception as e:
                logger.error(f"纯文本生成失败：{str(e)}")
                raise
        else:
            logger.error(f"生成关键帧失败：{str(e)}")
            raise

    # 打印生成结果
    print("\n生成的关键帧：")
    for result in results:
        print(f"关键帧 {result['frame_id']}：")
        print(f"  任务 ID：{result['task_id']}")
        print(f"  图像 URL：{result['image_url']}")
        print(f"  本地路径：{result['local_path']}")

if __name__ == "__main__":
    main()