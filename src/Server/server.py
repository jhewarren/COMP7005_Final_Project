import socket as sock_module
import json


class server:
    def __init__(self, emulator=("192.168.0.14", 7005)):
        self.socket = sock_module.socket(
            sock_module.AF_INET, sock_module.SOCK_DGRAM)
        self.socket.bind(("localhost", 7005))

    def __del__(self):
        self.socket.close()
        del self.socket

    def connect_to_emulator(self):
        self.socket.connect(self.remote)


c = server()
c.connect_to_emulator()
del c
