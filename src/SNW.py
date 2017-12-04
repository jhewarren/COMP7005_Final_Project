import socket as sock_module
import packet
from chunker import read_in_chunks
import communications
import sys
from threading import Thread
import time


class SNW(communications.communications):
    def __init__(self, config_data, input_file=sys.stdin, SWS=5):
        super().__init__(config_data)
        self.last_ack_received = None
        self.LFS = None
        self.SWS = SWS
        self.parser = packet.packet_parser()

    def __del__(self):
        pass

    def establish_connections(self):
        if self.is_client:
            self.init_handshake()  # to emulator
        elif self.is_emulator:
            self.init_handshake()  # to server
            self.await_handshake()  # from client
        elif self.is_server:
            self.await_handshake()  # from emulator

    def init_handshake(self):
        pass

    def await_handshake(self):
        (data, address_info) = self.in_socket.recvfrom(512)
        if data is None:
            return None
        pkt = self.parser.parse_packet_string(data)
        print("got stome shizz")

    def send_file(self, file_name, chunk_size=34):
        packet_count = 0
        for file_chunk in read_in_chunks(file_name, chunk_size):
            self.send_packet(packet.packetize(packet.allowed_multi_types["PUT_PSH"], packet_count, 0, self.SWS, 0, file_chunk))
            packet_count += 1

    def send_packet(self, pkt):
        if self.is_client:
            count = self.out_socket.sendto(pkt, ("localhost", 7006))
        elif self.is_emulator:
            pass
        elif self.is_server:
            pass

    def test(self):
        print(self.config)
