from service_instance.function.image_processing import *
import random as rnd

import sys
import logging
import platform
import time
import socket
import getopt
import asyncio

from sfc.nsh.common import BASEHEADER, CONTEXTHEADER, ETHERNET_ADDR_SIZE, InnerHeader
from sfc.nsh.common import NSH_NEXT_PROTO_ETH, NSH_NEXT_PROTO_IPV4, VXLANGPE

from sfc.nsh.encode import build_nsh_header
from sfc.nsh.encode import build_udp_packet, process_context_headers

from service_instance.service_host import ServiceHost

try:
    import signal
except ImportError:
    signal = None

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


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

    def send_long(self, msg):
        reliable_host = ServiceHost()
        reliable_host.sendto(msg, self.send)


def __handler(signum=None, frame=None):
    loop = asyncio.new_event_loop()
    print("Signal handler called with signal {}".format(signum))
    loop.call_soon_threadsafe(loop.stop)
    time.sleep(1)
    loop.call_soon_threadsafe(loop.close)
    time.sleep(1)  # here check if process is done
    print("Wait done")
    sys.exit(0)


for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGABRT]:
    signal.signal(sig, __handler)

# Can not install SIGHUP in Windows
if platform.system() in ["Linux", "Darwin"]:
    signal.signal(signal.SIGHUP, __handler)
    signal.signal(signal.SIGQUIT, __handler)


def sff_client(argv, message='ping!'):
    # global base_values

    # Some Good defaults
    remote_sff_port = 4790
    local_port = 4790
    remote_sff_ip = "127.0.0.1"
    local_ip = "0.0.0.0"
    sfp_id = 0x000001
    sfp_index = 3
    trace_req = False
    num_trace_hops = 254
    inner_src_ip = "192.168.0.1"
    inner_dest_ip = "192.168.0.2"
    inner_src_port = 10000
    inner_dest_port = 20000
    encapsulate = 'gpe-nsh-ipv4'  # make vxlan-gpe encapsulation default
    ctx1 = ctx2 = ctx3 = ctx4 = 0
    inner_src_eth_list = [0x3c, 0x15, 0xc2, 0xc9, 0x4f, 0xbc]
    inner_dest_eth_list = [0x08, 0x00, 0x27, 0xb6, 0xb0, 0x58]

    try:
        logging.basicConfig(level=logging.INFO)
        opt, args = getopt.getopt(argv, "h",
                                  ["help", "local-port=", "local-ip=", "inner-src-ip=", "inner-dest-ip=",
                                   "inner-src-port=", "inner-dest-port=", "remote-sff-ip=",
                                   "remote-sff-port=", "sfp-id=", "sfp-index=", "trace-req", "num-trace-hops=",
                                   "encapsulate=", "ctx1=", "ctx2=", "ctx3=", "ctx4=", "inner-src-eth=",
                                   "inner-dest-eth="])
    except getopt.GetoptError:
        print(
            "sff_client --help | --local-port | --local-ip | --inner-src-ip | --inner-dest-ip | --inner-src-port | "
            "--inner-dest-port | --remote-sff-ip | --ctx1 | --ctx2 | --ctx3 | --ctx4"
            "--remote-sff-port | --sfp-id | --sfp-index | --trace-req | --num-trace-hops | --encapsulate"
            "--inner-src-eth | --inner-dest-eth")
        sys.exit(2)

    for opt, arg in opt:
        if opt == "--remote-sff-port":
            remote_sff_port = arg
            continue

        if opt in ('-h', '--help'):
            print("sff_client \n --remote-sff-ip=<IP address of remote SFF> \n "
                  "--remote-sff-port=<UDP port of remote SFF> \n "
                  "--sfp-id=<Service Function Path id> \n --sfp-index<SFP starting index> \n "
                  "--encapsulate=<gpe-nsh-ethernet|gre|gpe-nsh-ipv4|vxlan-nsh-ethernet-legacy> \n "
                  "--inner-src-ip=<source IP of inner packet> \n --inner-dest-ip=<destination IP of inner packet> \n "
                  "--ctx1=<context header 1> \n --ctx2=<context header 2> \n --ctx3=<context header 3> \n "
                  "--ctx4=<context header 4> \n --local-port=<source port> \n --local-ip=<source IP> \n"
                  "--inner-src-eth=<inner src ethernet address> \n --inner-dest-eth=<inner dest ethernet address>")
            sys.exit()

        if opt == "--inner-src-eth":
            inner_src_eth_list = arg.split(':')
            if len(inner_src_eth_list) == ETHERNET_ADDR_SIZE:
                for i, val in enumerate(inner_src_eth_list):
                    inner_src_eth_list[i] = int(val, 16)
            else:
                logger.error("Ethernet address must be in the form aa:bb:cc:dd:ee:ff")
                sys.exit(2)
            continue

        if opt == "--inner-dest-eth":
            inner_dest_eth_list = arg.split(':')
            if len(inner_dest_eth_list) == ETHERNET_ADDR_SIZE:
                for i, val in enumerate(inner_dest_eth_list):
                    inner_dest_eth_list[i] = int(val, 16)
            else:
                logger.error("Ethernet address must be in the form aa:bb:cc:dd:ee:ff")
                sys.exit(2)
            continue

        if opt == "--remote-sff-ip":
            remote_sff_ip = arg
            continue

        if opt == "--sfp-id":
            sfp_id = arg
            continue

        if opt == "--sfp-index":
            sfp_index = arg
            continue

        if opt == "--trace-req":
            trace_req = True
            continue

        if opt == "--num-trace-hops":
            num_trace_hops = arg
            continue

        if opt == "--encapsulate":
            encapsulate = arg
            continue

        if opt == "--local-port":
            local_port = int(arg)
            continue

        if opt == "--local-ip":
            local_ip = arg
            continue

        if opt == "--inner-dest-port":
            inner_dest_port = int(arg)
            continue

        if opt == "--inner-dest-ip":
            inner_dest_ip = arg
            continue

        if opt == "--inner-src-port":
            inner_src_port = int(arg)
            continue

        if opt == "--inner-src-ip":
            inner_src_ip = arg
            continue

        if opt == "--ctx1":
            ctx1 = arg
            continue

        if opt == "--ctx2":
            ctx2 = arg
            continue

        if opt == "--ctx3":
            ctx3 = arg
            continue

        if opt == "--ctx4":
            ctx4 = arg
            continue

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop = asyncio.get_event_loop()

    # Common initializations for all encapsulations types
    base_header_values = BASEHEADER(service_path=int(sfp_id), service_index=int(sfp_index),
                                    proto=NSH_NEXT_PROTO_ETH)

    context_headers = process_context_headers(ctx1, ctx2, ctx3, ctx4)

    ctx_values = CONTEXTHEADER(context_headers[0], context_headers[1], context_headers[2], context_headers[3])
    inner_header = InnerHeader(inner_src_ip, inner_dest_ip, inner_src_port, inner_dest_port)

    # NSH type 1
    vxlan_header_values = VXLANGPE()
    #  override encap type
    base_header_values.next_protocol = NSH_NEXT_PROTO_IPV4

    # udpclient = MyVxlanGpeNshIpClient(loop, vxlan_header_values, base_header_values,
    #                                   ctx_values, remote_sff_ip, int(remote_sff_port), inner_header,
    #                                   message=message)
    # start_client(loop, (local_ip, local_port), (remote_sff_ip, remote_sff_port), udpclient)

    packet = build_nsh_header(vxlan_header_values, base_header_values, ctx_values)
    udp_inner_packet = build_udp_packet(inner_header.inner_src_ip,
                                        inner_header.inner_dest_ip,
                                        inner_src_port,
                                        inner_dest_port,
                                        message)

    transport = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    logger.debug("Client sending packet to %s", (remote_sff_ip, int(remote_sff_port)))
    try:
        transport.sendto(packet + udp_inner_packet, (remote_sff_ip, int(remote_sff_port)))
        transport.close()
    except socket.error as msg:
        logger.error('Failed to send packet. Error Code : ' + str(msg))
        transport.close()
        sys.exit()
    except Exception as e:
        logger.error("Error processing client: %s" % str(e))
        transport.close()


if __name__ == "__main__":
    sfp_id = input("Specify a sfp ID: ")
    connection = ClientConnection(dest_ip="127.0.0.1",
                                  dest_port="4790",
                                  sff_ip="127.0.0.1",
                                  sff_port="4789",
                                  sfp_id=sfp_id)

    # # test 1: some words
    # connection.send("hello sfc!")

    # test 2: send base64 image
    b64_image = load_image_to_base64("image_sample.jpg")
    print("Image:", b64_image.decode('utf-8'))
    print("Base64 string length:", len(b64_image))

    connection.send_long(b64_image)
