from bidict import bidict
from packet import *
from socket import *
import traceback
from random import randint


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


class connection(object):
    def __init__(self, socket, remote=None):
        self.socket = socket
        self.remote = remote
        self.parser = packet_parser()
        self.is_listener = False
        self.sequence_number = randint(1, 65000)
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
            self.ack_number = pkt.sequence_number + 1

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
            self.ack_number = pkt.sequence_number + 1

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

    def send_packet(self, packet_type, address=None, rport=0, data=None):
        if address is None:
            address = self.remote
        pkt = packetize(packet_type=packet_type,
                        sequence_number=self.sequence_number,
                        ack_number=self.ack_number,
                        window_size=1,
                        rport=rport,
                        data=data)
        self.sequence_number += 1
        self.socket.sendto(pkt, address)

    def read_packet(self):
        (data, address) = self.socket.recvfrom(512)
        pkt = self.parser.parse_packet_string(data)
        print("Server" if self.is_listener is True else "Client",
              "got", self.parser.get_packet_type(pkt.packet_type), "SN", pkt.sequence_number, "AN", pkt.ack_number)
        return (pkt, address)

    def set_state(self, state):
        self._state = state

    def get_state(self):
        return STATES.inv[self._state]

    def validate_packet(self, pkt, last_pkt):
        if pkt.ack_number == self.sequence_number:
            pass
