class ServiceHost:
    def __init__(self):
        self.buffer = {}

    def buffer(self, flow_id, packet_str):
        """
        将收到的数据按flow id分开存储起来，flow id作为不同应用的数据的标识
        应该包含 src ip, dst ip, src port, dst port, serial number(随机出来的序列号)来唯一确定
        @param flow_id:
        @param packet_str:
        """
        try:
            self.buffer[str(flow_id)].append(packet_str)
        except KeyError:
            self.buffer[str(flow_id)] = [packet_str, ]

    def clean(self):
        self.buffer = {}

    def fetch(self, flow_id):
        """
        按先后次序取出流对应的数据，并且拼接成完整的数据。
        @param flow_id:
        @return:
        """
        data_list = self.buffer[str(flow_id)]
        data = ""
        for pkt_data in data_list:
            data = data + pkt_data

        self.buffer.pop(str(flow_id))
        return data

    def send(self, msg, send_func):
        """
        将长的消息拆分后发送出去

        @param msg: str类型的长消息
        @param send_func: 发送用的函数，会直接调用send_func()来发送。
        """

        for 
