#!/usr/bin/env python3
'''============ ***doc description @ yyp*** ============
//client发送，server接收
struct naviCtrlStruct{
    int checker;
    float pos[3]; //目标位置
    float rpy[3]; //目标朝向
};

//server发送，client接收
struct naviSensStruct{
    float pos[3]; //实际位置
    float rpy[3]; //实际朝向
};
======================================================'''
import socket
import struct

ip='0.0.0.0'
port=8050

sk=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sk.bind((ip, port))

def skRecvLoop():
    print(f"等待接收数据，监听端口 {port}...")
    while True:
        buf, addr = sk.recvfrom(1024)
        try:
            cmd=struct.unpack('i6f', buf)
            print(f"接收到数据: mode={cmd[0]}, x={cmd[0]}, y={cmd[1]}, z={cmd[2]}, rol={cmd[3]}, pit={cmd[4]}, yaw={cmd[5]} 来自 {addr}")
            
            feedback = struct.pack('6f', 0.1, 0.2, 0,   0, 0, 0.6)
            print('完成导航,到达位姿')
            sk.sendto(feedback, (addr[0], addr[1]))
        except struct.error as e:
            print(f"解包错误: {e}，数据包: {buf}")
if __name__ == "__main__":
    skRecvLoop()
