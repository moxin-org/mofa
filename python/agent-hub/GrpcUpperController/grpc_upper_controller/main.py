# Dependencies:
#   - grpcio
#   - protobuf
#   - upper_controller_pb2.py and upper_controller_pb2_grpc.py must be present/generated from your .proto files.
#   - google.protobuf (standard with protobuf install)
#   - grpc server running at localhost:50051
#
# agent_name: GrpcUpperController

from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import grpc
import upper_controller_pb2 as pb2
import upper_controller_pb2_grpc as pb2_grpc
from google.protobuf import empty_pb2
import os
import json

@run_agent
def run(agent: MofaAgent):
    """Stateless agent to test and relay gRPC navigation service connectivity and call results."""
    # To facilitate composability, always try to receive a triggering parameter.
    # For this test node, we just need to receive an optional dummy input
    # (so it can be called from upstream nodes if required)
    dummy_input = agent.receive_parameter('user_input')
    # You may ignore 'dummy_input', processing is always carried out for demo

    # Fetch config (in real deployments, might be taken from env/yaml)
    grpc_host = os.getenv('GRPC_SERVER_ADDRESS', 'localhost')
    grpc_port = os.getenv('GRPC_SERVER_PORT', '50051')
    server_addr = f"{grpc_host}:{grpc_port}"

    # Default config for setConfig
    config_dict = {
        'incharge': 1,
        'filter_level': 1,
        'arm_mode': 1,
        'digit_mode': 1,
        'neck_mode': 1,
        'waist_mode': 1
    }

    results = {}
    channel = None
    try:
        channel = grpc.insecure_channel(server_addr)
        stub = pb2_grpc.UpperControllerStub(channel)

        # sendEndAction
        try:
            end_payload = pb2.EndPayload(
                end=pb2.EndPose(left=[0.1], right=[0.2]),
                effector=pb2.EffectorPosition(left=[0.3], right=[0.4])
            )
            send_end_action_resp = stub.sendEndAction(end_payload)
            results['sendEndAction'] = pb2.MessageToDict(send_end_action_resp) if hasattr(pb2, 'MessageToDict') else str(send_end_action_resp)
        except Exception as e:
            results['sendEndAction'] = f"ERROR: {repr(e)}"

        # recvEndState
        try:
            recv_state_resp = stub.recvEndState(empty_pb2.Empty())
            results['recvEndState'] = pb2.MessageToDict(recv_state_resp) if hasattr(pb2, 'MessageToDict') else str(recv_state_resp)
        except Exception as e:
            results['recvEndState'] = f"ERROR: {repr(e)}"
        
        # setConfig
        try:
            config = pb2.Config(**config_dict)
            set_config_resp = stub.setConfig(config)
            results['setConfig'] = pb2.MessageToDict(set_config_resp) if hasattr(pb2, 'MessageToDict') else str(set_config_resp)
        except Exception as e:
            results['setConfig'] = f"ERROR: {repr(e)}"

        # getConfig
        try:
            get_config_resp = stub.getConfig(empty_pb2.Empty())
            results['getConfig'] = pb2.MessageToDict(get_config_resp) if hasattr(pb2, 'MessageToDict') else str(get_config_resp)
        except Exception as e:
            results['getConfig'] = f"ERROR: {repr(e)}"

    except Exception as e:
        results['grpc_connection'] = f"ERROR: {repr(e)}"
    finally:
        if channel:
            try:
                channel.close()
            except Exception:
                pass
    
    # Ensure results is serializable
    try:
        agent.send_output(
            agent_output_name='grpc_test_result',
            agent_result=json.loads(json.dumps(results))
        )
    except Exception as e:
        # Fallback, send string-serialized error report
        agent.send_output(
            agent_output_name='grpc_test_result',
            agent_result=str(results)
        )

def main():
    agent = MofaAgent(agent_name='GrpcUpperController')
    run(agent=agent)

if __name__ == '__main__':
    main()
