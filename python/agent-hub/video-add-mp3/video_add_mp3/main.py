from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import subprocess
import os
import datetime

def replace_video_audio(video_path, audio_path, output_path=None):
    """
    替换视频的音频轨道并生成新视频

    参数：
    video_path (str): 原始视频文件路径
    audio_path (str): 新音频文件路径（MP3格式）
    output_path (str, optional): 输出文件路径，默认生成带时间戳的文件

    返回：
    str: 处理后的视频文件路径

    异常：
    subprocess.CalledProcessError: FFmpeg执行失败时抛出
    RuntimeError: 输入文件不存在时抛出
    """
    # 验证输入文件是否存在
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"视频文件不存在: {video_path}")
    if not os.path.isfile(audio_path):
        raise FileNotFoundError(f"音频文件不存在: {audio_path}")

    # 处理输出路径
    if output_path is None:
        # 生成带时间戳的默认文件名
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        original_name = os.path.splitext(os.path.basename(video_path))[0]
        output_dir = os.path.dirname(os.path.abspath(video_path))
        output_filename = f"{original_name}_replaced_{timestamp}.mp4"
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
        '-i', audio_path,
        '-map', '0:v:0',  # 选择第一个输入的视频流
        '-map', '1:a:0',  # 选择第二个输入的音频流
        '-shortest',  # 按最短的流结束输出
        '-c:v', 'copy',  # 视频流直接复制
        '-c:a', 'aac',  # 音频编码为AAC
        '-b:a', '192k',  # 音频比特率
        output_path
    ]

    try:
        # 执行命令并捕获错误输出
        result = subprocess.run(
            cmd,
            check=True,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        return output_path
    except subprocess.CalledProcessError as e:
        # 解析错误信息
        error_lines = [line for line in e.stderr.split('\n') if 'Error' in line]
        error_msg = "\n".join(error_lines[-3:]) if error_lines else "未知错误"
        raise RuntimeError(f"音频替换失败: {error_msg}") from e

@run_agent
def run(agent:MofaAgent):
    parameters_data = agent.receive_parameters(parameter_names=['video_path', 'audio_path'])
    output_path = replace_video_audio(video_path=parameters_data['video_path'], audio_path=parameters_data['audio_path'])
    agent_output_name = 'replace_video_audio_path'
    agent.send_output(agent_output_name=agent_output_name,agent_result=output_path)
def main():
    agent = MofaAgent(agent_name='video-add-mp3')
    run(agent=agent)
if __name__ == "__main__":
    main()
