import pickle
from threading import Thread, Event
from time import sleep
import socket
import random

SEND_BUFFER_SIZE = 1024
RECV_BUFFER_SIZE = 1024 * 1024
DEBUG = True


class ServiceHost:
    def __init__(self):
        self.__buffer = {}

    def buffer(self, flow_id: str, recv_buffer: bytes, ack_address: str) -> bool:
        """
        将收到的数据按flow id分开存储起来，flow id作为不同应用的数据的标识

        @param ack_address: 往哪一个IP发送ACK消息
        @param flow_id: 应该包含 src ip, dst ip, src port, dst port，以标识流量
        @param recv_buffer:  和sendto方法中发出的消息格式一致的一个string
        @return: 返回bool量指示是否已经收到了一条完整的会话的结束
        """
        print(flow_id, recv_buffer, ack_address)

        if recv_buffer.startswith(b'over_'):
            serial = int(recv_buffer.split(b'_')[1])
            sock_ack = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ack_address = (ack_address, serial)
            sock_ack.sendto(f'{serial}_over'.encode(), ack_address)

            if str(flow_id) not in self.__buffer or str(serial) not in self.__buffer[str(flow_id)]:
                return False

            return True

        serial = int(recv_buffer.split(b'_')[0])
        pos = int(recv_buffer.split(b'_')[1])
        data = recv_buffer.split(b'_', maxsplit=3)[2]

        sock_ack = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ack_address = (ack_address, serial)
        sock_ack.sendto(f'{serial}_{pos}_ack'.encode(), ack_address)

        if str(flow_id) not in self.__buffer:
            self.__buffer[str(flow_id)] = {}

        try:
            buffered_pos = [x[0] for x in self.__buffer[str(flow_id)][str(serial)]]
            if pos not in buffered_pos:
                self.__buffer[str(flow_id)][str(serial)].append((pos, data))
        except KeyError:
            self.__buffer[str(flow_id)][str(serial)] = [(pos, data), ]

        return False

    def clean(self):
        self.__buffer = {}

    def fetch(self, flow_id, serial):
        """
        按先后次序取出流对应的数据，并且拼接成完整的数据。
        取出之后数据会从缓存中清除。
        @param serial:
        @param flow_id:
        @return:
        """

        def take_sort_elem(pkt):
            return int(pkt[0])

        data_list = self.__buffer[str(flow_id)][str(serial)]
        # data_list: list
        data_list.sort(key=take_sort_elem)

        data = b""
        for pos, pkt_data in data_list:
            print(pos, pkt_data)
            data = data + pkt_data

        self.__buffer[str(flow_id)].pop(str(serial))
        return data

    @staticmethod
    def sendto(msg, send_func):
        """
        将长的消息拆分后发送出去

        @param msg: str类型的长消息
        @param send_func: 发送用的函数，会直接调用send_func()来发送。
        """
        e = Event()
        e.clear()

        def sendto(_msg):
            msg_size = len(_msg)

            for start in range(msg_size // SEND_BUFFER_SIZE):
                position.append(start * SEND_BUFFER_SIZE)

            e.set()

            while position:  # send: [serial]_[pos]_data
                for pos in position:
                    send_func(f"{serial[0]}_{pos}_".encode() + msg[pos:pos + SEND_BUFFER_SIZE])
                sleep(0.1)

            while serial:  # send: over_[serial]
                send_func(f'over_{serial[0]}'.encode())

        def recv_ack():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(("", serial[0]))
            if DEBUG:
                print("Waiting ACK...")

            while position:  # ack: [serial]_[pos]_ack
                data, _ = sock.recvfrom(1024)
                ack_serial = int(data.split(b'_')[0])
                pos = int(data.split(b'_')[1])
                if DEBUG:
                    print("Receive ack:", ack_serial, pos)
                if ack_serial == serial[0] and pos in position:
                    position.remove(pos)

            while serial:  # ack: [serial]_over
                data, _ = sock.recvfrom(1024)
                ack_serial = int(data.split(b'_')[0])
                ack_over = data.split(b'_')[1]
                if ack_serial == serial[0] and ack_over == b'over':
                    serial.remove(ack_serial)

        position = []
        serial = [random.randint(1000, 65500)]
        e = Event()
        e.clear()

        t1 = Thread(target=sendto, args=(msg,))
        t1.start()
        print("started")

        print("Wait start")
        e.wait()
        print("start ack")
        t2 = Thread(target=recv_ack)
        t2.start()
        t2.join()
        t1.join()

    @staticmethod
    def get_serial(recv_buffer):
        if recv_buffer.startswith(b'over_'):
            serial = int(recv_buffer.split(b'_')[1])
        else:
            serial = int(recv_buffer.split(b'_')[0])

        return serial
