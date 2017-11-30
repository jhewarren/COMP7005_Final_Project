import socket as sock_module
import sys
import base


class emulator(base.base):
    def __init__(self, config={}):
        base.base(config)
        if config["emulator_ip"] == self.ip:
            print("same ip", self.ip)
            self.socket.bind((config["emulator_ip"], config["emulator_port"]))
        else:
            sys.exit()


def run(config):
    print(config)
    e = emulator(config)
    e.accept_connections()
    del e


if __name__ == "__main__":
    run(base.test_config)
