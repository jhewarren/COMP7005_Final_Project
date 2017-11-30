import socket as sock_module
import sys


class packet(object):
    def __init__(self):
        self.packet_type = 0b00000000
        self.sequence_number = 0b0000000000000000
        self.ack_number = 0b0000000000000000


class communications(object):
    def __init__(self, config):
        self.config = config
        self.validate_config()

        self.local_ip = sock_module.gethostbyname(sock_module.gethostname())

        if self.local_ip == self.emulator_ip:
            self.is_emulator = True
            self.is_server = False
            self.is_client = False
        elif self.local_ip == self.server_ip:
            self.is_emulator = False
            self.is_server = True
            self.is_client = False
        else:
            self.is_emulator = False
            self.is_server = False
            self.is_client = True

        self.configure()

    def __del__(self):
        try:
            self.out_socket.close()
            del self.out_socket
        except Exception:
            print("One of the objects did not exist on destructor call.")

    def configure(self):
        if self.is_emulator:
            self.configure_emulator()
        elif self.is_server:
            self.configure_server()
        else:
            self.configure_client()

    def configure_emulator(self):
        self.in_socket = sock_module.socket(sock_module.AF_INET, sock_module.SOCK_DGRAM)
        self.in_socket.bind((self.emulator_ip, self.emulator_port))

        self.out_socket = sock_module.socket(sock_module.AF_INET, sock_module.SOCK_DGRAM)
        self.out_socket.bind((self.emulator_ip, 0))

    def configure_server(self):
        self.in_socket = sock_module.socket(sock_module.AF_INET, sock_module.SOCK_DGRAM)
        self.in_socket.bind((self.server_ip, self.server_port))

    def configure_client(self):
        pass

    def validate_config(self):
        self.emulator_ip = self.config["emulator_ip"]
        self.emulator_port = self.config["emulator_port"]
        self.server_ip = self.config["server_ip"]
        self.server_port = self.config["server_port"]
        if not all(isinstance(t, str) for t in [self.emulator_ip, self.server_ip]):
            sys.exit()
        if not all(isinstance(t, int) for t in [self.emulator_port, self.server_port]):
            sys.exit()


def run(config):
    print(config)
    c = communications(config)
    del c


test_config = {
    "emulator_ip": "192.168.0.1",
    "emulator_port": 7005,
    "server_ip": "192.168.0.2",
    "server_port": 7005


}

if __name__ == "__main__":
    run(test_config)
