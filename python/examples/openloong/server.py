import time
import grpc
from concurrent import futures
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'generated'))
from grpc_reflection.v1alpha import reflection
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


# 导入 gRPC 生成的模块
from generated import (
    cctv_pb2_grpc,
    cctv_pb2,
    navigation_pb2_grpc,
    navigation_pb2,
    skill_pb2_grpc,
    skill_pb2,
)

class CCTVService(cctv_pb2_grpc.cctvServiceServicer):
    def setCtrl(self, request, context):
        print(f"[CCTV] setCtrl: key={request.key}")
        # 这里我们简单地回一个 id=1, state=0 的确认
        return cctv_pb2.cctvSensRpc(id=1, state=0)

    def getSens(self, request, context):
        # 测试流式返回 5 条状态
        for i in range(5):
            yield cctv_pb2.cctvSensRpc(id=1, state=i)
            time.sleep(1)

# -------------------------------
# 导航服务实现
# -------------------------------
class NaviService(navigation_pb2_grpc.NaviControllerServicer):
    def setDestination(self, request, context):
        pos = request.position
        att = request.attitude
        print(f"[NAVI] Destination set to x={pos.x}, y={pos.y}, yaw={att.yaw}")
        return navigation_pb2.Response(succeeded=True, msg="Destination set")

    def startNavi(self, request, context):
        # 模拟导航过程中的流式返回
        for i in range(3):
            resp = navigation_pb2.NaviResponse(
                succeeded=True,
                msg="Navigating...",
                arrived=False,
                state=navigation_pb2.NaviState(
                    position = navigation_pb2.Descartes(x=0.1*i, y=0.2*i, z=0),
                    velocity = navigation_pb2.Descartes(x=0, y=0, z=0),
                    attitude = navigation_pb2.Euler(roll=0, pitch=0, yaw=0),
                    navigating=True
                )
            )
            yield resp
            time.sleep(1)
        # 最后一条标记到达
        yield navigation_pb2.NaviResponse(
            succeeded=True,
            msg="Arrived",
            arrived=True,
            state=navigation_pb2.NaviState(navigating=False)
        )

    def stopNavi(self, request, context):
        return navigation_pb2.Response(succeeded=True, msg="Navigation stopped")

    def getState(self, request, context):
        return navigation_pb2.NaviState(navigating=False)

# -------------------------------
# 技能服务实现
# -------------------------------
class SkillService(skill_pb2_grpc.SkillManagerServicer):
    def startAction(self, request, context):
        print(f"[SKILL] startAction: file={request.file}")
        # 模拟动作进度流
        for pct in range(0, 101, 25):
            yield skill_pb2.ActionResponse(
                succeeded=True,
                msg="Action in progress",
                precentage=pct
            )
            time.sleep(0.5)

    def stopAction(self, request, context):
        return skill_pb2.Response(succeeded=True, msg="Action stopped")

    def playAudio(self, request, context):
        print(f"[AUDIO] Playing file: {request.file}")
        return skill_pb2.Response(succeeded=True, msg="Audio played")

    def stopAudio(self, request, context):
        return skill_pb2.Response(succeeded=True, msg="Audio stopped")

# -------------------------------
# 启动 gRPC Server
# -------------------------------
def serve():
    free_port(50051)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))

    cctv_pb2_grpc.add_cctvServiceServicer_to_server(CCTVService(), server)
    navigation_pb2_grpc.add_NaviControllerServicer_to_server(NaviService(), server)
    skill_pb2_grpc.add_SkillManagerServicer_to_server(SkillService(), server)
    SERVICE_NAMES = [
        cctv_pb2.DESCRIPTOR.services_by_name['cctvService'].full_name,
        navigation_pb2.DESCRIPTOR.services_by_name['NaviController'].full_name,
        navigation_pb2.DESCRIPTOR.services_by_name['MapManager'].full_name,
        skill_pb2.DESCRIPTOR.services_by_name['SkillManager'].full_name,
        reflection.SERVICE_NAME,
    ]
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port('[::]:50051')
    server.start()
    print("✅ gRPC Server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
