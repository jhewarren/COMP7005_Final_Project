import time
from threading import Thread
from socket import *
from connection import *


client_port = 7005
server_port = 7006


def run_client():
    time.sleep(0.2)
    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket.bind(("localhost", client_port))
    c = connection(client_socket, ("localhost", server_port))
    if c.connect_to_remote():
        print(c.get_state())
    client_socket.close()


def run_server():
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(("localhost", server_port))
    c = connection(server_socket, ("localhost", server_port))
    if c.accept_connection():
        print(c.get_state())
    server_socket.close()


if __name__ == "__main__":
    Thread(target=run_client).start()
    Thread(target=run_server).start()
