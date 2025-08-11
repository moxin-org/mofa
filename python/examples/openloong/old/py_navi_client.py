#!/usr/bin/env python3
'''============ ***doc description @ yyp*** ============
//client发送，server接收
struct naviCtrlStruct{
    int mode; //0=绝对，1=相对
    float pos[3]; //目标位置，仅xy生效
    float rpy[3]; //目标朝向，仅yaw生效
};

//server发送，client接收
struct naviSensStruct{
    float pos[3]; //实际位置
    float rpy[3]; //实际朝向
};
======================================================'''
import socket
import struct
import time

ip='0.0.0.0'
port=8050

sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cmd = struct.pack('i6f',1, 0.2, 0.3, 0,  0, 0, 0.5)
sk.sendto(cmd, (ip, port))

time.sleep(0.1)

buf, addr = sk.recvfrom(1024)
msg=struct.unpack('6f', buf)
print(f"接收到数据:x={msg[0]}, y={msg[1]}, z={msg[2]}, rol={msg[3]}, pit={msg[4]}, yaw={msg[5]} 来自 {addr}")
