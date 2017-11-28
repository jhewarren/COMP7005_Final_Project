import socket as sock_module
import json


class client:
    def __init__(self, remote=("localhost", 7005)):
        self.remote = remote
        self.socket = sock_module.socket(
            sock_module.AF_INET, sock_module.SOCK_DGRAM)
        self.socket.bind(("localhost", 7005))

    def __del__(self):
        self.socket.close()
        del self.socket

    def connect_to_emulator(self):
        self.socket.connect(self.remote)


config_data = json.load(open("../config.json"))
print(config_data)
c = client(remote=(config_data["emulator_ip"], config_data["emulator_port"]))
del c
