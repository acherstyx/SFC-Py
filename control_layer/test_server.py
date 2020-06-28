#!/usr/bin/python3
# 文件名：server.py

# 导入 socket、sys 模块
import socket
import sys

# 创建 socket 对象
serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 获取本地主机名
host = "127.0.0.1"

port = 1234

# 绑定端口号
serversocket.bind((host, port))
print("start.")

while True:
    # 建立客户端连接
    # clientsocket, addr = serversocket.recvfrom()

    data, addr = serversocket.recvfrom(1024)
    print("连接地址: %s" % str(addr))
    print(data)
    # s.close()
