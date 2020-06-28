from sfc.sff_client import main as sff_client


class ClientConnection:
    def __init__(self,
                 dest_ip,
                 dest_port,
                 sff_ip,
                 sff_port,
                 sfp_id,
                 sfp_index=255
                 ):
        self.dest_ip = dest_ip
        self.dest_port = dest_port
        self.sff_ip = sff_ip
        self.sff_port = sff_port
        self.sfp_id = sfp_id
        self.sfp_index = sfp_index

    def send(self, msg):
        sff_client(["--remote-sff-ip", self.sff_ip,
                    "--remote-sff-port", self.sff_port,
                    "--sfp-id", self.sfp_id,
                    "--sfp-index", self.sfp_index,
                    "--inner-dest-ip", self.dest_ip,
                    "--inner-dest-port", self.dest_port],
                   msg)


if __name__ == "__main__":
    sfp_id = input("Specify a sfp ID: ")
    connection = ClientConnection(dest_ip="127.0.0.1",
                                  dest_port="4790",
                                  sff_ip="127.0.0.1",
                                  sff_port="4789",
                                  sfp_id=sfp_id)
    connection.send("hello sfc!")
