import socket as sock_module
import sys


class server:
    def __init__(self, config={}):
        if bool(config) == False:
            sys.exit()
        self.socket = sock_module.socket(
            sock_module.AF_INET, sock_module.SOCK_DGRAM)
        self.socket.bind((config["localhost", config["server_port"]]))

    def __del__(self):
        self.socket.close()
        del self.socket

    def connect_to_emulator(self):
        self.socket.connect(self.remote)


def run(config):
    print(config)
    s = server(config)
    del s


if __name__ == "__main__":
    run()
