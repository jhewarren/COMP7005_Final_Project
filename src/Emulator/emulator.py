import socket as sock_module
import sys


class emulator:
    def __init__(self, config={}):
        self.socket = sock_module.socket(
            sock_module.AF_INET, sock_module.SOCK_DGRAM)
        self.ip = sock_module.gethostbyname(sock_module.gethostname())
        if config["emulator_ip"] == self.ip:
            print("same ip", self.ip)
            self.socket.bind((config["emulator_ip"], config["emulator_port"]))
        else:
            sys.exit()

    def __del__(self):
        self.socket.close()
        del self.socket

    def accept_connections(self):
        while(1):
            buffer = self.socket.recv(1024)
            print(buffer)
            if buffer == "":
                break


def run(config):
    print(config)
    e = emulator(config)
    e.accept_connections()
    del e


if __name__ == "__main__":
    run()
