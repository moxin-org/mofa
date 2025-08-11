import grpc
import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'generated'))

# 导入生成的 stub
from generated import (
    cctv_pb2, cctv_pb2_grpc,
    navigation_pb2, navigation_pb2_grpc,
    navigation_pb2 as map_pb2,  # MapManager 在同一个 proto 文件里？
    navigation_pb2_grpc as map_grpc,
    skill_pb2, skill_pb2_grpc,
)
from google.protobuf.empty_pb2 import Empty
def main():
    # 1. 建立 gRPC Channel 和各服务 Stub
    chan = grpc.insecure_channel('localhost:50051')
    cctv_stub  = cctv_pb2_grpc.cctvServiceStub(chan)
    nav_stub   = navigation_pb2_grpc.NaviControllerStub(chan)
    map_stub   = navigation_pb2_grpc.MapManagerStub(chan)
    skill_stub = skill_pb2_grpc.SkillManagerStub(chan)

    # 0️⃣ 使能 CCTV 中控（key=999 仅作示例）
    print("0️⃣ Enable CCTV")
    cctv_stub.setCtrl(
        cctv_pb2.cctvCtrlRpc(checker=1109, tgtGroup=0, tgtId=0, key=999) # <-- 修改为 cctv_pb2.cctvCtrlRpc
    )

    # 1️⃣ 获取地图
    print("1️⃣ Get map …")
    # the_map = map_stub.getMap(Empty())
    # print(f"Map origin=({the_map.origin.x}, {the_map.origin.y}), resolution={the_map.resolution}")

    # 2️⃣ 设置第一个目标点
    pose1 = navigation_pb2.Pose(
        position = navigation_pb2.Descartes(x=1.0, y=2.0, z=0),
        attitude = navigation_pb2.Euler(roll=0, pitch=0, yaw=1.57)
    )
    print("2️⃣ Set destination:", pose1)
    nav_stub.setDestination(pose1)

    # 3️⃣ 启动导航并监听流
    print("3️⃣ startNavi…")
    for resp in nav_stub.startNavi(navigation_pb2.Config(relative=False)):
        print(f"   ↳ pos=({resp.state.position.x:.2f},{resp.state.position.y:.2f}), arrived={resp.arrived}")
        if resp.arrived:
            break

    # 4️⃣ 切换到上肢动作模式
    print("4️⃣ switch to arm mode")
    cctv_stub.setCtrl(
        cctv_pb2.cctvCtrlRpc(checker=1109, tgtGroup=0, tgtId=0, key=221)
    )

    # 5️⃣ 内部动作（挥手）
    print("5️⃣ internal wave")
    cctv_stub.setCtrl(
        cctv_pb2.cctvCtrlRpc(checker=1109, tgtGroup=0, tgtId=0, key=115)
    )
    time.sleep(2)

    # —— 如需用外部动作 + SkillManager，可解开注释 ——
    print("5.2️⃣ external mode + SkillManager")
    cctv_stub.setCtrl(cctv_pb2.cctvCtrlRpc(checker=1109, tgtGroup=0, tgtId=0, key=116))
    for a in skill_stub.startAction(skill_pb2.Action(file="wave.h5", fps=30, timeout_ms=5000)):
        print(f"     ↳ action progress = {a.precentage}%")

    # 6️⃣ 播放语音
    print("6️⃣ play audio")
    skill_stub.playAudio(
        skill_pb2.Audio(file="explain.wav", timeout_ms=3000)
    )

    # 7️⃣ 切换到行走摆臂模式
    print("7️⃣ walk with swing")
    cctv_stub.setCtrl(
        cctv_pb2.cctvCtrlRpc(checker=1109, tgtGroup=0, tgtId=0, key=220)
    )

    # 8️⃣ 设置第二个目标点
    pose2 = navigation_pb2.Pose(
        position = navigation_pb2.Descartes(x=3.0, y=1.0, z=0),
        attitude = navigation_pb2.Euler(roll=0, pitch=0, yaw=0)
    )
    print("8️⃣ setDestination2:", pose2)
    nav_stub.setDestination(pose2)

    # 9️⃣ 再次导航并监听
    print("9️⃣ startNavi2…")
    for resp in nav_stub.startNavi(navigation_pb2.Config(relative=False)):
        print(f"   ↳ arrived={resp.arrived}, pos=({resp.state.position.x:.2f},{resp.state.position.y:.2f})")

    # 🔟 手臂回正
    print("🔟 reset arm")
    cctv_stub.setCtrl(
        cctv_pb2.cctvCtrlRpc(checker=1109, tgtGroup=0, tgtId=0, key=114)
    )

    print("🏁 All steps completed.")

if __name__ == '__main__':
    main()