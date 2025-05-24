# klingdemo/utils/keyframe_parser.py
import re
from typing import List, Dict
from pathlib import Path

def parse_keyframes(file_path: str) -> List[Dict[str, str]]:
    """
    解析 .txt 文件，提取关键帧描述。
    Args:
        file_path: .txt 文件路径
    Returns:
        关键帧描述列表，每个关键帧为字典，包含 Prompt、NegativePrompt、AspectRatio 等字段
    """
    keyframes = []
    current_frame = {}
    frame_pattern = re.compile(r'\[Frame \d+\]')

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # 检测新帧开始
            if frame_pattern.match(line):
                if current_frame:
                    keyframes.append(current_frame)
                current_frame = {}
            # 解析字段
            elif ':' in line:
                key, value = map(str.strip, line.split(':', 1))
                current_frame[key] = value

        # 添加最后一个帧
        if current_frame:
            keyframes.append(current_frame)

    return keyframes