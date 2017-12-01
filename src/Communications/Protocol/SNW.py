import socket as sock_module
from packet import packet
from packet import packet_parser


class SNW(object):
    def __init__(self, local_port, SWS=512, ):
        """SWS->Send-Window-Size"""
        self.last_ack_received = None
        self.LFS = None
        self.local_port = local_port

    def __del__(self):
        pass

    def init_local_socket(self):
        self.local_socket = sock_module.socket(sock_module.AF_INET, sock_module.NI_DGRAM)
        self.local_socket.bind(("localhost", self.local_port))
