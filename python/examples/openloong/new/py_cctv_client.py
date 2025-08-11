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
import tkinter as tk
import struct
from threading import Thread
import time
import sys
from functools import partial

ip='192.168.31.33'
port=8010
group=0
id=0

sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cmd = struct.pack('4h', 1109, group, id, 0)

def skSendLoop():
    while(1):
        sk.sendto(cmd, (ip, port))  # 只发送到指定的 IP 地址
        time.sleep(0.5)

# # 接收循环
# def skRecvLoop():
#     global stateLabel
#     msg = {}
#     while(1):
#         buf, _ = sk.recvfrom(1024)
#         id, state = struct.unpack('hh', buf)
#         msg[id] = state
#         stateLabel["text"] = msg
def skRecvLoop():
    msg = {}
    while True:
        try:
            buf, _ = sk.recvfrom(1024)
            recv_id, state = struct.unpack('hh', buf)
            msg[recv_id] = state
            # 使用 after 方法让主线程更新 GUI
            root.after(0, lambda m=msg.copy(): stateLabel.config(text=str(m)))
        except Exception as e:
            print("Recv error:", e)

def setCmd(key):
    global cmd
    cmd = struct.pack('4h', 1109, group, id, key)
    print(key)

# 键盘按键
def keyPress(ev):
    key = ev.keysym
    print(key)
    if(key == 'KP_7'):
        pass

# 界面
root = tk.Tk()
if sys.platform.startswith('win'):
    root.geometry('800x400')
    length = 100
else:
    if(root.winfo_screenwidth() > 5000):
        root.geometry('1200x600+4600+1000')
        length = 120
    else:
        root.geometry('1000x500+2600+200')
        length = 100

# 按键
tips = ['rc', 'damp', 'rl', 'start', 'stop', 'mani介出', 'mani介入', 'mani act', 'mani挥手']
keys = [2, 12, 4, 6, 7, 220, 221, 115, 158]
for i in range(len(tips)):
    tk.Button(root, text=f'[{keys[i]}]\n{tips[i]}', command=partial(setCmd, keys[i])
              ).place(anchor='nw', relx=0.1*i, rely=0, width=length, height=length)

# 状态栏
tk.Label(root, text="状态栏，server反馈：").place(anchor='nw', relx=0.05, rely=0.3)
global stateLabel
stateLabel = tk.Label(root, text="{}")
stateLabel.place(anchor='nw', relx=0.2, rely=0.3)

# 启动线程
th1 = Thread(target=skSendLoop)
th1.daemon = 1
th1.start()
th2 = Thread(target=skRecvLoop)
th2.daemon = 1
th2.start()

tk.mainloop()
