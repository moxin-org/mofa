import requests


def download_video(video_url, save_path):
    """
    下载 MP4 视频文件。

    Args:
        video_url (str): 视频的 URL 地址。
        save_path (str): 下载后保存视频的本地路径。
    """
    try:
        # 发送 GET 请求下载视频
        response = requests.get(video_url, stream=True)
        response.raise_for_status()

        # 打开文件并写入数据
        with open(save_path, 'wb') as video_file:
            for chunk in response.iter_content(chunk_size=8192):
                video_file.write(chunk)

        print(f"视频已成功下载并保存在: {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"下载视频失败: {e}")


# 使用示例
if __name__ == "__main__":
    video_url = "https://cdn.klingai.com/bs2/upload-kling-api/0276045624/image2video/CjhLjGfqOR4AAAAAAIp3pA-0_raw_video_2.mp4"  # 替换为实际的 video_url
    save_path = "downloaded_video.mp4"  # 保存的视频文件路径

    download_video(video_url, save_path)
