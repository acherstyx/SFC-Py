import socket
import sys
import logging
from service_instance.service_host import ServiceHost
from service_instance.function.image_processing import *
import cv2

RECEIVE_BUFFER = 1024 * 41

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建 socket 对象
serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 获取本地主机名
host = "0.0.0.0"

port = 1234

# 绑定端口号
serversocket.bind((host, port))

logger.info("UDP Server start to receive image at %s:%s", host, port)

reliable_host = ServiceHost()

while True:
    # 建立客户端连接
    # clientsocket, addr = serversocket.recvfrom()

    data, addr = serversocket.recvfrom(RECEIVE_BUFFER)
    data = data[28:]
    logger.debug("Receive data: %s", data)

    serial = reliable_host.get_serial(data)

    over = reliable_host.buffer(serial, data, None)

    if over:
        image_raw = reliable_host.fetch(serial, serial)
        cv2.imshow("UDP Server", decode_base64_image(image_raw))
        cv2.waitKey(1)
