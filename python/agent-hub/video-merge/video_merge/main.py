from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import subprocess
import os
import tempfile
import datetime

def merge_videos(video_list, output_path=None):
    """
    将多个视频文件转码后合并为一个视频文件

    参数：
    video_list (list): 要合并的视频文件路径列表
    output_path (str, optional): 输出文件路径，默认生成带时间戳的文件

    返回：
    str: 合并后的视频文件路径
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        # 生成中间TS文件
        ts_files = []
        for idx, video in enumerate(video_list):
            ts_path = os.path.join(tmp_dir, f"{idx}.ts")
            cmd = [
                'ffmpeg',
                '-y',  # 覆盖已存在文件
                '-i', video,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-profile:a', 'aac_low',
                '-b:a', '128k',
                ts_path
            ]
            subprocess.run(cmd, check=True)
            ts_files.append(ts_path)

        # 创建合并列表文件
        list_path = os.path.join(tmp_dir, 'list.txt')
        with open(list_path, 'w') as f:
            for ts in ts_files:
                f.write(f"file '{ts}'\n")

        # 设置默认输出路径
        if output_path is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            output_path = os.path.abspath(f"merged_video_{timestamp}.mp4")
        else:
            output_path = os.path.abspath(output_path)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # 执行合并操作
        merge_cmd = [
            'ffmpeg',
            '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', list_path,
            '-c:v', 'libx264',
            '-c:a', 'aac',
            output_path
        ]
        subprocess.run(merge_cmd, check=True)

    return output_path

@run_agent
def run(agent:MofaAgent):
    videos_path = agent.receive_parameter('videos_path')
    # 字符串转换成 list
    video_list = videos_path.split(',')
    output_path = merge_videos(video_list)
    agent_output_name = 'video_merge_path'
    agent.send_output(agent_output_name=agent_output_name,agent_result=output_path)
def main():
    agent = MofaAgent(agent_name='video-merge')
    run(agent=agent)
if __name__ == "__main__":
    main()
