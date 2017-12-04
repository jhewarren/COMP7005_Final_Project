import socket as sock_module
import sys
from debug import dump_func_name
import json


class communications(object):
    @dump_func_name
    def __init__(self, config_data):
        self.config = self.load_config(config_data)
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

    @dump_func_name
    def __del__(self):
        try:
            self.out_socket.close()
            del self.out_socket
        except Exception:
            print("One of the objects did not exist on destructor call.")

    @dump_func_name
    def configure(self):
        if self.is_emulator:
            self.configure_emulator()
        elif self.is_server:
            self.configure_server()
        else:
            self.configure_client()

    @dump_func_name
    def configure_emulator(self):
        self.in_socket = sock_module.socket(sock_module.AF_INET, sock_module.SOCK_DGRAM)
        self.in_socket.bind((self.emulator_ip, self.emulator_port))

        self.out_socket = sock_module.socket(sock_module.AF_INET, sock_module.SOCK_DGRAM)
        self.out_socket.bind((self.emulator_ip, 0))

    @dump_func_name
    def configure_server(self):
        self.in_socket = sock_module.socket(sock_module.AF_INET, sock_module.SOCK_DGRAM)
        self.in_socket.bind((self.server_ip, self.server_port))

    @dump_func_name
    def configure_client(self):
        self.out_socket = sock_module.socket(sock_module.AF_INET, sock_module.SOCK_DGRAM)
        self.out_socket.bind(("localhost", 0))

    @dump_func_name
    def load_config(self, config_data):
        self.config = {}
        return json.loads(config_data)

    @dump_func_name
    def validate_config(self):
        self.emulator_ip = self.config["emulator_ip"]
        self.emulator_port = self.config["emulator_port"]
        self.server_ip = self.config["server_ip"]
        self.server_port = self.config["server_port"]
        if not all(isinstance(t, str) for t in [self.emulator_ip, self.server_ip]):
            sys.exit()
        if not all(isinstance(t, int) for t in [self.emulator_port, self.server_port]):
            sys.exit()
