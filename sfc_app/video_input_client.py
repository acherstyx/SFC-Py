__package__ = "sfc_app"

import cv2

from control_layer.connection.client_wrapper import ClientConnection
from .app_config import *
from service_instance.function.image_processing import encode_image_to_base64
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    cap = cv2.VideoCapture("video_sample.mp4")

    # get connection
    conn = ClientConnection(dest_ip=SERVER_IP,
                            dest_port=SERVER_PORT,
                            sff_ip=SFF_IP,
                            sff_port=SFF_PORT,
                            sfp_id=SFP_ID)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            logger.info("End of video, exiting...")
            break

        conn.send_long(encode_image_to_base64(frame))
