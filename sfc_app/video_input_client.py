__package__ = "sfc_app"

import cv2
import logging

logging.basicConfig(level=logging.CRITICAL)
from control_layer.connection.client_wrapper import ClientConnection
from .app_config import *
from service_instance.function.image_processing import encode_image_to_base64
from threading import Thread
from time import sleep

logger = logging.getLogger(__name__, )

if __name__ == '__main__':
    cap = cv2.VideoCapture("video_sample.mp4")
    logger.info("Thread")
    # get connection

    send_threads = []

    conn = ClientConnection(dest_ip=SERVER_IP,
                            dest_port=SERVER_PORT,
                            sff_ip=SFF_IP,
                            sff_port=SFF_PORT,
                            sfp_id=SFP_ID)


    def auto_join(my_tread):
        my_tread.join()
        send_threads.pop(send_threads.index(my_tread))


    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            logger.info("End of video, exiting...")
            break
        frame = cv2.resize(frame, None, fx=0.3, fy=0.3)
        cv2.imshow("UDP Client", frame)
        cv2.waitKey(1)

        # conn.send_long(encode_image_to_base64(frame))

        new_send_thread = Thread(target=conn.send_long, args=(encode_image_to_base64(frame),))
        new_send_thread.start()
        send_threads.append(new_send_thread)

        join_thread = Thread(target=auto_join, args=(new_send_thread,))
        join_thread.start()
        sleep(0.1)

        while True:
            if len(send_threads) < 10:
                break
        # sleep(0.1)
        # new_send_thread.join()
