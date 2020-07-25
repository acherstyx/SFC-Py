__package__ = "sfc_app"

import cv2
import logging
import numpy as np

logging.basicConfig(level=logging.DEBUG)
from control_layer.connection.client_wrapper import ClientConnection
from .app_config import *
from service_instance.function.image_processing import encode_image_to_base64
from threading import Thread
from time import sleep
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['toolbar'] = 'None'
logger = logging.getLogger(__name__, )

if __name__ == '__main__':
    cap = cv2.VideoCapture("video_sample.mp4")
    logger.info("Thread")
    # get connection

    send_threads = []


    def auto_join(my_tread):
        my_tread.join()
        send_threads.pop(send_threads.index(my_tread))


    while cap.isOpened():
        try:
            conn = ClientConnection(dest_ip=SERVER_IP,
                                    dest_port=SERVER_PORT,
                                    sff_ip=SFF_IP,
                                    sff_port=SFF_PORT,
                                    sfp_id=SFP_ID())
        except KeyError:
            logger.warning("Receive KeyError while loading SFP ID")
            continue

        ret, frame = cap.read()
        if not ret:
            logger.info("End of video, exiting...")
            break
        if np.shape(frame[0]) == 0:
            continue
        frame = cv2.resize(frame, None, fx=0.3, fy=0.3)

        # cv2.imshow("UDP Client", frame)
        # cv2.waitKey(1)

        fig = plt.figure("UDP Client", clear=True, figsize=(1.6 * 3, 0.9 * 3))
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0,
                            hspace=0, wspace=0)
        plt.axis('off')
        plt.margins(0, 0)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.ion()
        plt.show()
        plt.imshow(frame, interpolation='none')
        plt.draw()
        plt.pause(0.001)

        # conn.send_long(encode_image_to_base64(frame))
        # sleep(0.1)

        size = np.shape(frame)

        x = size[0]
        y = size[1]

        frame = frame[int(0 * x):int(0.7 * x), int(0.3 * y):int(1.0 * y)]
        cv2.putText(frame, "Processed By [Image Crop] Service", (0, 15), cv2.FONT_HERSHEY_PLAIN,1, (255, 255, 255),1)

        plt.figure("Image Crop", clear=True, figsize=(1.6 * 3, 0.9 * 3))
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0,
                            hspace=0, wspace=0)
        plt.axis('off')
        plt.margins(0, 0)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.ion()
        plt.show()
        plt.imshow(frame, cmap="gray", interpolation='none')
        plt.draw()
        plt.pause(0.001)

        new_send_thread = Thread(target=conn.send_long, args=(encode_image_to_base64(frame),))
        new_send_thread.start()
        send_threads.append(new_send_thread)

        join_thread = Thread(target=auto_join, args=(new_send_thread,))
        join_thread.start()
        sleep(0.3)

        while True:
            if len(send_threads) < 100:
                break
