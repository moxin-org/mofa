import os
import time

import cv2
import numpy as np
import pyarrow as pa

from dora import DoraStatus

import logging

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_INDEX = int(os.getenv("CAMERA_INDEX", 0))
CI = os.environ.get("CI")

font = cv2.FONT_HERSHEY_SIMPLEX

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Operator:
    """
    Sending image from webcam to the dataflow
    """

    def __init__(self):
        # self.video_capture = cv2.VideoCapture(CAMERA_INDEX)
        self.start_time = time.time()
        # self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        # self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
        # self.failure_count = 0

    def on_event(
        self,
        dora_event: str,
        send_output,
    ) -> DoraStatus:
        event_type = dora_event["type"]        
        if event_type == "INPUT":
            id = dora_event["id"]
            value = dora_event["value"]
            logging.info("id: %s", id)
            logging.info("value: %s", value)
            if id == "image_path":
                # frame = cv2.imread(value[0])
                frame = cv2.imread(value[0].as_py())
                if frame is None:
                    logging.info("frame is None")
                    return DoraStatus.CONTINUE
                frame = cv2.resize(frame, (CAMERA_WIDTH, CAMERA_HEIGHT))

                send_output(
                    "image",
                    pa.array(frame.ravel()),
                    dora_event["metadata"],
                )        
                return DoraStatus.CONTINUE            
        elif event_type == "STOP":
            print("received stop")
        else:
            print("received unexpected event:", event_type)
