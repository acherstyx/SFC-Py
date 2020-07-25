import socket
import sys
import logging
from service_instance.service_host import ServiceHost
from service_instance.function.image_processing import *
import cv2
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['toolbar'] = 'None'


RECEIVE_BUFFER = 1024 * 1024

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建 socket 对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 获取本地主机名
host = "0.0.0.0"

port = 1234

# 绑定端口号
server_socket.bind((host, port))

logger.info("UDP Server start to receive image at %s:%s", host, port)

reliable_host = ServiceHost()

while True:
    # 建立客户端连接
    # clientsocket, addr = serversocket.recvfrom()

    data, addr = server_socket.recvfrom(RECEIVE_BUFFER)
    data = data[28:]
    logger.debug("Receive data: %s", data)

    serial = reliable_host.get_serial(data)

    over = reliable_host.buffer(serial, data, "127.0.0.1")

    if over:
        image_raw = reliable_host.fetch(serial, serial)
        image = decode_base64_image(image_raw)
        if np.shape(image)[0] == 0:
            pass
        # cv2.imshow("UDP Server", image)
        # cv2.waitKey(1)
        fig = plt.figure("UDP Server/Object Detection", clear=True, figsize=(1.6 * 3, 0.9 * 3))
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0,
                            hspace=0, wspace=0)
        plt.axis('off')
        plt.margins(0, 0)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.ion()
        plt.show()
        plt.imshow(image, interpolation='none')
        plt.draw()
        plt.pause(0.001)
