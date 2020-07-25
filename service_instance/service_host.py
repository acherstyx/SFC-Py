import pickle
import time
from threading import Thread, Event
from time import sleep
import socket
import random
import logging

logger = logging.getLogger(__name__)

SEND_BUFFER_SIZE = 1024 * 40
RECV_BUFFER_SIZE = 1024 * 1024
DEBUG = True
TIME_OUT = 10
DUPLICATED_LIMIT = 10


class ServiceHost:
    def __init__(self):
        self.__buffer = {}

    def buffer(self, flow_id: str, recv_buffer: bytes, ack_address) -> bool:
        """
        将收到的数据按flow id分开存储起来，flow id作为不同应用的数据的标识

        @param ack_address: 往哪一个IP发送ACK消息
        @param flow_id: 应该包含 src ip, dst ip, src port, dst port，以标识流量
        @param recv_buffer:  和sendto方法中发出的消息格式一致的一个string
        @return: 返回bool量指示是否已经收到了一条完整的会话的结束
        """
        # print(flow_id, recv_buffer, ack_address)

        logger.debug("[Server host] Buffering data, flow id: %s, ack address: %s, recv_buffer: %s",
                     flow_id,
                     ack_address,
                     recv_buffer)

        if recv_buffer.startswith(b'over_'):
            serial = int(recv_buffer.split(b'_')[1])
            if ack_address is not None:
                sock_ack = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                ack_address = (ack_address, serial)
                sock_ack.sendto(f'{serial}_over'.encode(), ack_address)
                sock_ack.close()
            if str(flow_id) not in self.__buffer or str(serial) not in self.__buffer[str(flow_id)]:
                return False

            return True

        serial = int(recv_buffer.split(b'_')[0])
        pos = int(recv_buffer.split(b'_')[1])
        data = recv_buffer.split(b'_', maxsplit=3)[2]

        if ack_address is not None:
            sock_ack = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ack_address = (ack_address, serial)
            sock_ack.sendto(f'{serial}_{pos}_ack'.encode(), ack_address)
            logger.debug("ACK reply is send to %s:%s", ack_address, serial)

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
            if DEBUG:
                logger.debug(f"{pos}, {pkt_data}")
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

            for start in range(msg_size // SEND_BUFFER_SIZE + 1):
                position.append(start * SEND_BUFFER_SIZE)

            e.set()

            timeout_mark = False

            start = time.time()
            duplicated = 0
            while position:  # send: [serial]_[pos]_data
                for pos in position:
                    send_func(f"{serial[0]}_{pos}_".encode() + msg[pos:pos + SEND_BUFFER_SIZE])
                duplicated += 1
                logger.debug("Serial %s Retry: %s", serial[0], duplicated)
                sleep(0.3)
                # time out
                if time.time() - start > TIME_OUT:
                    timeout_mark = True
                    break
                if duplicated > DUPLICATED_LIMIT:
                    timeout_mark = True
                    break

            if timeout_mark:
                exit()

            start = time.time()
            duplicated = 0
            while serial:  # send: over_[serial]
                send_func(f'over_{serial[0]}'.encode())
                sleep(0.1)
                duplicated += 1
                if time.time() - start > TIME_OUT:
                    logger.warning("Time out for sending over msg.", msg[:min(30, len(msg))])
                    break
                if duplicated > DUPLICATED_LIMIT:
                    break

        def recv_ack():
            if DEBUG:
                logger.info("Start receiving ACK...")

            start = time.time()
            while position:  # ack: [serial]_[pos]_ack
                try:
                    data, _ = sock.recvfrom(1024)
                except socket.timeout:
                    position.clear()
                    # break

                ack_serial = int(data.split(b'_')[0])
                try:
                    pos = int(data.split(b'_')[1])
                except ValueError as e:
                    logger.warning("Catch ValueError: %s", e)

                logger.debug("Receive ack: %s %s", ack_serial, pos)
                if ack_serial == serial[0] and pos in position:
                    position.remove(pos)
                if time.time() - start > TIME_OUT:
                    break

            while serial:  # ack: [serial]_over
                try:
                    data, _ = sock.recvfrom(1024)
                except socket.timeout:
                    logger.warning("Time out for waiting ACK: %s", msg[:min(30, len(msg))])
                    serial.clear()
                    break
                ack_serial = int(data.split(b'_')[0])
                ack_over = data.split(b'_')[1]

                if ack_serial == serial[0] and ack_over == b'over':
                    serial.remove(ack_serial)
                    logger.debug("Receive over ack: %s", data)

            sock.close()
            logger.debug("send thread exit.")

        position = []

        sock = None
        for i in range(10):
            try:
                serial = [random.randint(1000, 65500)]
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.bind(("", serial[0]))
                sock.settimeout(5)
                break
            except OSError:
                pass

        e = Event()
        e.clear()

        t1 = Thread(target=sendto, args=(msg,))
        t1.start()
        logger.info("Host start to send...")

        e.wait()

        t2 = Thread(target=recv_ack)
        t2.start()
        t1.join()
        t2.join()

    @staticmethod
    def get_serial(recv_buffer):
        if recv_buffer.startswith(b'over_'):
            serial = int(recv_buffer.split(b'_')[1])
        else:
            serial = int(recv_buffer.split(b'_')[0])

        return serial
