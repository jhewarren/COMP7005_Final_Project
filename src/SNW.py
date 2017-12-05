import packet
from chunker import read_in_chunks
import communications
import sys
from threading import Thread
import time
import time
import json
from threading import Thread
from socket import *
from connection import *


class SNW(communications.communications):
    def __init__(self, config_data, input_file=sys.stdin, SWS=5):
        super().__init__(config_data)
        self.last_ack_received = None
        self.LFS = None
        self.SWS = SWS
        self.parser = packet_parser()

    def __del__(self):
        pass

    def establish_connections(self):
        if self.is_client:
            cc = connection(self.out_socket, (self.emulator_ip, self.emulator_port))
            self.init_handshake(cc)  # to emulator
        elif self.is_emulator:
            cc = connection(self.out_socket, (self.server_ip, self.server_port))
            sc = connection(self.in_socket, (self.client_ip, self.client_port))
            self.init_handshake(cc)  # to server
            self.await_handshake(dc)  # from client
        elif self.is_server:
            sc = connection(self.in_socket, (self.client_ip, self.client_port))
            self.await_handshake(sc)  # from emulator

    def init_handshake(self, conn):
        if conn.connect_to_remote():
            print("succeeded connection")

    def await_handshake(self, conn):
        conn.await_handshake()

    def send_file(self, file_name, chunk_size=34):
        packet_count = 0
        for file_chunk in read_in_chunks(file_name, chunk_size):
            self.send_packet(packet.packetize(packet.allowed_multi_types["PUT_PSH"],
                                              packet_count,
                                              0,
                                              self.SWS,
                                              0,
                                              file_chunk))
            packet_count += 1

    def send_packet(self, pkt):
        if self.is_client:
            pass
        elif self.is_emulator:
            pass
        elif self.is_server:
            pass

    def test(self):
        print(self.config)


if __name__ == "__main__":
    snw = SNW(config_data="./config.json", input_file="./testfiles/32b.dat", SWS=3)
