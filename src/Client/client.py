import socket as sock_module


class client:
    def __init__(self, remote=("localhost", 7005)):
        self.remote = remote
        self.socket = sock_module.socket(
            sock_module.AF_INET, sock_module.SOCK_DGRAM)
        self.socket.bind(remote)

    def __del__(self):
        self.socket.close()
        del self.socket

    def connect_to_emulator(self):
        self.socket.connect(["localhost", 7005])


c = client()
del c
