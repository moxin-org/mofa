from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import subprocess
import os
import datetime

def add_logo_to_video(video_path, logo_path, output_path=None):
    """
    给视频添加Logo并生成新视频

    参数：
    video_path (str): 原始视频文件路径
    logo_path (str): Logo图片路径
    output_path (str, optional): 输出文件路径，默认生成带时间戳的文件

    返回：
    str: 添加Logo后的视频文件路径

    异常：
    subprocess.CalledProcessError: FFmpeg执行失败时抛出
    """
    # 处理输出路径
    if output_path is None:
        # 生成带时间戳的默认文件名
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        original_name = os.path.splitext(os.path.basename(video_path))[0]
        output_dir = os.path.dirname(os.path.abspath(video_path))
        output_filename = f"{original_name}_with_logo_{timestamp}.mp4"
        output_path = os.path.join(output_dir, output_filename)
    else:
        output_path = os.path.abspath(output_path)

    # 创建输出目录（如果不存在）
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 构建FFmpeg命令
    cmd = [
        'ffmpeg',
        '-y',  # 覆盖输出文件
        '-i', video_path,
        '-i', logo_path,
        '-filter_complex',
        '[0:v][1:v]overlay=W-w-10:H-h-10',  # Logo定位在右下角，距边缘10像素
        '-codec:a', 'copy',  # 直接复制音频流
        output_path
    ]

    try:
        # 执行命令
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE)
        return output_path
    except subprocess.CalledProcessError as e:
        # 增强错误信息
        error_msg = f"FFmpeg命令执行失败: {e.stderr.decode()}" if e.stderr else "FFmpeg命令执行失败"
        raise RuntimeError(error_msg) from e


@run_agent
def run(agent:MofaAgent):
    parameters_data = agent.receive_parameters(parameter_names=['video_path', 'logo_path'])
    output_path = add_logo_to_video(video_path=parameters_data['video_path'], logo_path=parameters_data['logo_path'])
    agent_output_name = 'video_add_logo_path'
    agent.send_output(agent_output_name=agent_output_name,agent_result=output_path)
def main():
    agent = MofaAgent(agent_name='video-add-logo')
    run(agent=agent)
if __name__ == "__main__":
    main()
