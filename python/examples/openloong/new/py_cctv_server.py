#!/usr/bin/env python3
'''============ ***doc description @ yyp*** ============
//client发送，server接收
struct cctvCtrlStruct{
	short checker;
	short tgtGroup,tgtId; //多机器人可分组响应；另每个机器人唯一id响应；全=0为广播
	short key;
};

//server发送，client接收
struct cctvSensStruct{
	short id;
	short state;
};
======================================================'''
import socket
import struct

ip='0.0.0.0'
port=8010

sk=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sk.bind((ip, port))

# 定义反馈函数
def send_feedback(client_ip, client_port, id,status):
    # 将反馈消息打包
    feedback = struct.pack('2h', id,  status)
    sk.sendto(feedback, (client_ip, client_port))  # 发送到指定客户端
    print(f"反馈已发送到 {client_ip}:{client_port}")

# 接收循环
def skRecvLoop():
    print(f"等待接收数据，监听端口 {port}...")
    while True:
        buf, addr = sk.recvfrom(1024)
        try:
            checker, group, id, key=struct.unpack('4h', buf)
            print(f"接收到数据: checker={checker}, group={group}, id={id}, key={key} 来自 {addr}")
            if checker==1109:  # 假设收到 checker=1109 时，做反馈
                send_feedback(addr[0], addr[1], id, key)  # 发送反馈，状态为 1 (成功)
            else:
                send_feedback(addr[0], addr[1], 0, 0)  # 如果命令不是 1109，则发送失败反馈
        except struct.error as e:
            print(f"解包错误: {e}，数据包: {buf}")
if __name__ == "__main__":
    skRecvLoop()
