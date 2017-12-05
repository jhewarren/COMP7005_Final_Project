import time
import sys
from socket import *
from connection import *
from packet import PACKET_TYPES
from packet import ALLOWED_MULTI_TYPES
import json
from threading import Thread


def run_client():
    # allocate client network resources
    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket.bind((config["client_ip"], config["client_port"]))
    command_connection = connection(client_socket, (config["emulator_ip"], config["emulator_port"]))

    # attempt connection to server
    if not command_connection.connect_to_remote():
        print(" Client failed main connection in client")
        return None
    print("Client state:", command_connection.get_state())

    # # allocate data transfer network resources
    # data_socket = socket(AF_INET, SOCK_DGRAM)
    # data_socket.bind((config["client_ip"], 0))
    # data_connection = connection(socket=data_socket)

    # # tell remote to connect to data_connection
    # if not command_connection.send_command("GET", data_connection.local_port):
    #     print("Client command_connection Failed to send command")

    # # await connection
    # if not data_connection.accept_connection():
    #     print("failed data connection in client")
    #     return None
    # print("Client data_connection state:", data_connection.get_state())

    # data_connection.recv_file(file_name="./recv/file.dat")

    # clear resources
    data_socket.close()
    client_socket.close()
    # del data_connection
    del command_connection


def run_server():
    # allocate server network resources
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind((config["server_ip"], config["server_port"]))
    command_connection = connection(server_socket)

    # accept client connection
    if not command_connection.accept_connection():
        print("server main connection in server")
        return None
    print("Server state:", command_connection.get_state())

    # # read command packet
    # (command, rport) = command_connection.get_command()
    # print("Server prased command:", command, "on port", rport)
    # if command == "GET":
    #     command_connection.send_ack()
    # elif command == "PUT":
    #     command_connection.send_ack()

    # allocate data transfer network resources
    # data_socket = socket(AF_INET, SOCK_DGRAM)
    # data_socket.bind((config["server_ip"], 0))
    # data_connection = connection(socket=data_socket, remote=(command_connection.remote[0], rport))

    # # three way handshake back to client's data_connection
    # if not data_connection.connect_to_remote():
    #     print("failed data connection")
    #     return None
    # print("Server data_connection state:", data_connection.get_state())

    # data_connection.send_file(filename="./testfiles/32b.dat", chunksize=40)

    # close socket
    server_socket.close()
    data_socket.close()
    del command_connection
    #del data_connection


def run_emulator():
    # allocate server network resources
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind((config["emulator_ip"], config["emulator_port"]))
    command_server_connection = connection(server_socket)

    # allocate client network resources
    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket.bind((config["emulator_ip"], 0))
    command_client_connection = connection(client_socket, (config["server_ip"], config["server_port"]))

    # connect to the server
    if not command_client_connection.connect_to_remote():
        print("Emulator failed at command_client_connection connect()")
    print("Emulator state with server")

    # await connection to forward to server
    if not command_server_connection.accept_connection():
        print("Emulator failed during connection")
    print("Emulator state with client:", command_connection.get_state())

    server_socket.close()
    client_socket.close()


config = {}
with open("./config.json") as file:
    config = json.load(file)

print("Loaded Config file\n", config)

if len(sys.argv) is 2:
    print(sys.argv[1])
    if sys.argv[1] == "server":
        run_server()
    elif sys.argv[1] == "client":
        run_client()
    else:
        run_emulator()
