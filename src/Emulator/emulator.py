import socket as sock_module
import json


class emulator:
    def __init__(self, config={}):
        self.socket = sock_module.socket(
            sock_module.AF_INET, sock_module.SOCK_DGRAM)
        self.socket.bind(("localhost", 7005))
        self.ip = sock_module.gethostbyname(sock_module.gethostname())
        print(self.ip)
        if config["emulator_ip"] == self.ip:
            print("same ip", self.ip)

    def __del__(self):
        self.socket.close()
        del self.socket


config = json.load(open("../config.json"))
print(config)
print(config["emulator_port"])
c = emulator(config)
del c
