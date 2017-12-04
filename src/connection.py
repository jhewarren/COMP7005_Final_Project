from bidict import bidict
from packet import *
from socket import *
from chunker import *
import traceback
from random import randint
import sys

STATES = bidict(
    closed=1,
    waiting=2,
    handshake=3,
    connected=4,
    inactive=5
)

'''
Make sure you check for retransmit requests
'''

MAX_VALUE_0xFFFF = 65535


class connection(object):
    def __init__(self, socket, remote=None):
        self.socket = socket
        self.remote = remote
        self.parser = packet_parser()
        self.is_listener = False
        self.sequence_number = MAX_VALUE_0xFFFF - 100  # randint(1, 65000)
        self.ack_number = 0
        if self.remote is None:
            self.is_listener = True
        self.set_state(STATES["inactive"])
        sock_name = socket.getsockname()
        self.local_port = sock_name[1]
        self.local_addr = sock_name[0]

    def connect_to_remote(self):
        self.set_state(STATES["handshake"])

        try:
            self.send_packet(packet_type=PACKET_TYPES["SYN"], rport=0, data=None)

            (pkt, address) = self.read_packet()

            if not pkt.check_packet(packet_type=ALLOWED_MULTI_TYPES["SYN_ACK"]):
                raise ValueError("This packet must be SYN_ACK")

            self.send_packet(packet_type=PACKET_TYPES["ACK"], address=address, rport=0, data=None)

            self.set_state(STATES["connected"])

            return True
        except Exception as e:
            print(e)
            return False
            traceback.print_exc()
        else:
            pass
        finally:
            pass

    def accept_connection(self):
        self.set_state(STATES["waiting"])
        try:
            (pkt, address) = self.read_packet()

            self.remote = address

            if pkt.packet_type is not PACKET_TYPES["SYN"]:
                raise ValueError("First Packet must be SYN")

            self.send_packet(packet_type=ALLOWED_MULTI_TYPES["SYN_ACK"], address=address, rport=0, data=None)

            (pkt, address) = self.read_packet()
            if pkt.packet_type is not PACKET_TYPES["ACK"]:
                raise ValueError("Final packet must be ACK")

            self.set_state(STATES["connected"])
            return True

        except Exception as e:
            print(e)
            return False
            traceback.print_exc()
        else:
            pass
        finally:
            pass

    def get_command(self):
        (pkt, address) = self.read_packet()
        return (self.parser.get_packet_type(pkt.packet_type), pkt.rport)

    def send_command(self, command, rport):
        self.send_packet(packet_type=PACKET_TYPES[command],
                         rport=rport)
        (pkt, address) = self.read_packet()
        return pkt.check_packet(packet_type=ALLOWED_MULTI_TYPES["ACK_PSH"], ack_number=self.sequence_number)

    def send_ack(self):
        self.send_packet(packet_type=PACKET_TYPES["ACK"], rport=0, data=None)

    def send_file(self, filename, chunksize):
        for file_chunk in read_in_chunks(filename, chunksize):
            count = self.send_packet(packet_type=ALLOWED_MULTI_TYPES["ACK_PSH"], data=file_chunk)
            (pkt, address) = self.read_packet()
            if pkt.check_packet(packet_type=PACKET_TYPES["ACK"], ack_number=self.sequence_number):
                print("sent", "SN", self.sequence_number, "BYTES:", count)
            elif pkt.check_packet(packet_type=PACKET_TYPES["RSD"]):
                print("requested RESEND\n\n\n")
                self.sequence_number -= 1
                count = self.send_packet(packet_type=ALLOWED_MULTI_TYPES["ACK_PSH"], data=file_chunk)

        self.send_packet(packet_type=ALLOWED_MULTI_TYPES["ACK_PSH"], data=None)

    def recv_file(self, file_name):
        r = reassembler(file_name)
        while True:
            (pkt, address) = self.read_packet()
            if not pkt.check_packet(packet_type=ALLOWED_MULTI_TYPES["ACK_PSH"]):
                print("Got:", pkt.ack_number, "Wanted:", self.sequence_number)
                self.send_packet(packet_type=PACKET_TYPES["RSD"])
            elif pkt.check_packet(packet_type=ALLOWED_MULTI_TYPES["ACK_PSH"]) and pkt.datasize == 0:
                print("transfer done")
                break
            else:
                r.put_chunk(pkt.data)
                self.send_ack()

    def send_packet(self, packet_type, address=None, rport=0, data=None):
        if address is None:
            address = self.remote

        pkt = packetize(packet_type=packet_type,
                        sequence_number=self.sequence_number,
                        ack_number=self.ack_number,
                        window_size=1,
                        rport=rport,
                        data=data)
        if data is not None:
            if self.sequence_number == MAX_VALUE_0xFFFF - 1:
                self.sequence_number = 0
            self.sequence_number += 1
        return self.socket.sendto(pkt, address)

    def read_packet(self):
        (data, address) = self.socket.recvfrom(256)
        pkt = self.parser.parse_packet_string(data)
        print("Server" if self.is_listener is True else "Client",
              "got", self.parser.get_packet_type(pkt.packet_type), "SN", pkt.sequence_number, "AN", pkt.ack_number)

        if pkt.datasize is not 0:
            self.ack_number = pkt.sequence_number + 1
        return (pkt, address)

    def set_state(self, state):
        self._state = state

    def get_state(self):
        return STATES.inv[self._state]

    def validate_packet(self, pkt, last_pkt):
        if pkt.ack_number == self.sequence_number:
            pass
