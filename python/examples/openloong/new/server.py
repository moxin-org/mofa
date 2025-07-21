#!/usr/bin/env python3
import socket
import subprocess


def free_port(port=50051):
    # 查出所有占用该端口的 PID
    cmd_find = ["lsof", "-t", f"-i", f"tcp:{port}"]
    try:
        pids = subprocess.check_output(cmd_find, text=True).split()
    except subprocess.CalledProcessError:
        # 没找到任何进程
        print(f"No process is listening on port {port}.")
        return

    if not pids:
        print(f"No process is listening on port {port}.")
        return

    print(f"Killing processes on port {port}: {pids}")
    # 强制杀掉
    cmd_kill = ["kill", "-9"] + pids
    subprocess.run(cmd_kill)
    print("Done.")

class CCTVService:
    def set_ctrl(self, mode):
        return f"[CCTVService] 模式切换为 {mode}"

class NaviController:
    def set_destination(self, x, y, yaw):
        return f"[NaviController] 目的地设置为 x={x}, y={y}, yaw={yaw}"

    def start_navi(self):
        return "[NaviController] 开始导航并已完成"

class SkillManager:
    def start_action(self, action_name):
        return f"[SkillManager] 执行动作: {action_name}"

    def play_audio(self, audio_id):
        return f"[SkillManager] 播放语音: {audio_id}"

def parse_and_execute(command: str):
    parts = command.strip().split()
    if len(parts) < 2:
        return "无效指令"

    target, method = parts[0].split('.')
    args = parts[1:]

    # 实例初始化
    service_map = {
        "cctv": CCTVService(),
        "navi": NaviController(),
        "skill": SkillManager()
    }

    if target not in service_map:
        return "未知模块"

    obj = service_map[target]

    try:
        func = getattr(obj, method)
        # 参数转换：支持 float / str 混合
        parsed_args = [float(x) if x.replace('.', '', 1).replace('-', '', 1).isdigit() else x for x in args]
        result = func(*parsed_args)
        return result
    except Exception as e:
        return f"执行失败: {e}"

def start_server(ip="0.0.0.0", port=8010):
    free_port(8010)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    print(f"[Server] 监听中：{ip}:{port}")

    while True:
        data, addr = sock.recvfrom(1024)
        cmd = data.decode('utf-8')
        print(f"[Server] 收到命令: {cmd}")
        result = parse_and_execute(cmd)
        sock.sendto(result.encode('utf-8'), addr)

if __name__ == "__main__":
    start_server()
