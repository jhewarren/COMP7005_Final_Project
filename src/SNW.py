import socket as sock_module
import packet
from chunker import read_in_chunks
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
pparser = packet.packet_parser()
packets = []
count = 10

for chunk in read_in_chunks("./testfiles/32b.dat", 8):
    count += 1
    packets.append(packet.packetize(packet.packet_types["RSD"], 16, count, 5, 0, len(chunk), chunk))

for pkt in packets:
    print(pparser.parse_packet_string(pkt))

print(packets)
