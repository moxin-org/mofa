#!/usr/bin/env python3
import socket
import time

ip = "127.0.0.1"
port = 8010

def send_cmd(cmd):
    sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sk.sendto(cmd.encode('utf-8'), (ip, port))
    response, _ = sk.recvfrom(1024)
    print(f"[Client] 发送：{cmd} -> 响应：{response.decode('utf-8')}")
    sk.close()

if __name__ == "__main__":
    steps = [
        "cctv.set_ctrl nav_mode",
        "navi.set_destination 1.0 2.0 0.5",
        "navi.start_navi",
        "cctv.set_ctrl arm_mode",
        "cctv.set_ctrl inner_wave_mode",
        "skill.start_action wave",
        "skill.play_audio intro_001",
        "cctv.set_ctrl walk_arm_mode",
        "navi.set_destination 3.5 1.2 -0.2",
        "navi.start_navi",
        "cctv.set_ctrl arm_reset"
    ]

    for cmd in steps:
        send_cmd(cmd)
        time.sleep(0.3)
