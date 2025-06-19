from concurrent import futures
import grpc
import gps_navigation_pb2
import gps_navigation_pb2_grpc
from google.protobuf import empty_pb2

class GPSNaviControllerServicer(gps_navigation_pb2_grpc.GPSNaviControllerServicer):
    def setDestination(self, request, context):
        print("Set destination to:", request)
        return gps_navigation_pb2.Response(succeeded=True, msg="Destination set.")

    def startNavi(self, request, context):
        for i in range(3):
            yield gps_navigation_pb2.NaviResponse(
                succeeded=True,
                msg=f"Step {i+1}",
                arrived=(i == 2),
                state=gps_navigation_pb2.State()
            )

    def stopNavi(self, request, context):
        return gps_navigation_pb2.Response(succeeded=True, msg="Navigation stopped.")

    def getState(self, request, context):
        return gps_navigation_pb2.State()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    gps_navigation_pb2_grpc.add_GPSNaviControllerServicer_to_server(GPSNaviControllerServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
