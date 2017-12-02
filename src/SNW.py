import socket as sock_module
from packet import packet
from packet import packet_parser
import communications
import asyncio
import sys


class SNW(communications.communications):
    def __init__(self, config_data, input_file=sys.stdin, SWS=5):
        super().__init__(config_data)
        self.last_ack_received = None
        self.LFS = None
        self.eventloop = asyncio.get_event_loop()
        self.queue = asyncio.Queue(loop=self.eventloop)

    def __del__(self):
        pass

    def send_packets(self, packets):
        if self.is_client:
            pass
        elif self.is_emulator:
            pass
        elif self.is_server:
            pass

    def test(self):
        print(self.config)


config_data = None
with open("config.json") as file:
    config_data = file.read()

s = SNW(config_data)


pkt = packet(packet_type=0b00000011, data="hello world this is a message".encode("utf-8"))
print(pkt.data)
print(pkt.packetize())
pkts = [pkt]
s.send_packets(pkts)
