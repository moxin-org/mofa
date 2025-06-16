

from openai import OpenAI
import json
if __name__ == "__main__":
    client = OpenAI(base_url="http://127.0.0.1:8000/v1", api_key="***REMOVED***jsha-1234567890")

    # user_input = """"endpoint": "https://api.ipify.org?format=json","description": "Get the public IP address in IPv4 format.","documentation_url": "https://www.ipify.org/?ref=freepublicapis.com","request_type": "GET","request_parameter": "None","error": false    """
    user_input = """"import grpc
import gps_navigation_pb2
import gps_navigation_pb2_grpc
from google.protobuf import empty_pb2

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = gps_navigation_pb2_grpc.GPSNaviControllerStub(channel)

        # 调用 setDestination
        pose = gps_navigation_pb2.Pose(
            position=gps_navigation_pb2.Descartes(x=1, y=2, z=3),
            attitude=gps_navigation_pb2.Euler(roll=0, pitch=0, yaw=1)
        )
        res = stub.setDestination(pose)
        print("setDestination:", res)

        # 调用 startNavi
        print("startNavi:")
        for r in stub.startNavi(empty_pb2.Empty()):
            print(r)

        # 调用 getState
        state = stub.getState(empty_pb2.Empty())
        print("getState:", state)

        # 调用 stopNavi stop_res = stub.stopNavi(empty_pb2.Empty()) print("stopNavi:", stop_res) if __name__ == '__main__':     run()
"""
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content":str(user_input)},
    ],
    )
    print(response)