import argparse
import json
import os
from dora import Node
from mofa.kernel.utils.util import create_agent_output
import pyarrow as pa
import os
RUNNER_CI = True if os.getenv("CI") == "true" else False


def main():


    agent_config_dir_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/configs'

    # Handle dynamic nodes, ask for the name of the node in the dataflow, and the same values as the ENV variables.
    parser = argparse.ArgumentParser(description=" Agent")

    parser.add_argument(
        "--name",
        type=str,
        required=False,
        help="The name of the node in the dataflow.",
        default="arrow-assert",
    )
    parser.add_argument(
        "--task",
        type=str,
        required=False,
        help="Tasks required for the Reasoner agent.",
        default="Paris Olympics",
    )

    args = parser.parse_args()
    task = os.getenv("TASK", args.task)

    node = Node(
        args.name
    )  # provide the name to connect to the dataflow if dynamic node

    # assert_data = ast.literal_eval(data)

    for event in node:
        if event["type"] == "INPUT":
            if event['id'] in ['image_path']:
                image_path = event["value"][0].as_py()
                
                # TODO: 这里需要根据你的主函数进行配置
                import cv2
                import time

                try:
                    # Initialize the camera
                    cap = cv2.VideoCapture(0)
                    if not cap.isOpened():
                        print("Cannot open camera")
                        exit()
                    
                    # Allow the camera to warm up
                    time.sleep(1)
                    
                    # Capture the image
                    ret, frame = cap.read()
                    if not ret:
                        print("Failed to capture image")
                        cap.release()
                        exit()
                    
                    # Save the image
                    cv2.imwrite(image_path, frame)
                    print("Image saved as image.jpg")
                    
                except Exception as e:
                    print(f"An error occurred: {e}")
                finally:
                    # Release the camera
                    cap.release()
                
                
                node.send_output("camera_screenshot_result", pa.array([create_agent_output(
                    agent_name='camera_screenshot_result',
                    agent_result='image.jpg',
                    dataflow_status=os.getenv(
                                                                                    "IS_DATAFLOW_END",
                                                                                    True))]), event['metadata'])

if __name__ == "__main__":
    main()
