import time
from threading import Thread
from socket import *
from connection import *
from packet import PACKET_TYPES
from packet import ALLOWED_MULTI_TYPES

client_port = 7005
server_port = 7006


def run_client():
    time.sleep(0.2)

    # allocate client network resources
    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket.bind(("localhost", client_port))
    main_connection = connection(client_socket, ("localhost", server_port))

    # attempt connection to server
    if not main_connection.connect_to_remote():
        print("failed main connection in client")
        return None
    print("Machine 1 state:", main_connection.get_state())

    # allocate data transfer network resources
    data_socket = socket(AF_INET, SOCK_DGRAM)
    data_socket.bind(("localhost", 0))
    data_connection = connection(socket=data_socket)

    # tell remote to connect to data_connection
    if not main_connection.send_command("GET", data_connection.local_port):
        print("Client main_connection Failed to send command")

    # await connection
    if not data_connection.accept_connection():
        print("failed data connection in client")
        return None
    print("Machine 1 data_connection state:", data_connection.get_state())

    data_connection.recv_file(file_name="./recv/file.dat")

    # clear resources
    data_socket.close()
    client_socket.close()
    del data_connection
    del main_connection


def run_server():
    # allocate server network resources
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(("localhost", server_port))
    main_connection = connection(server_socket)

    # accept client connection
    if not main_connection.accept_connection():
        print("failed main connection in server")
        return None
    print("Machine 2 state:", main_connection.get_state())

    # read command packet
    (command, rport) = main_connection.get_command()
    print("Server prased command:", command, "on port", rport)
    if command == "GET":
        main_connection.send_ack()
    elif command == "PUT":
        main_connection.send_ack()

    # allocate data transfer network resources
    data_socket = socket(AF_INET, SOCK_DGRAM)
    data_socket.bind(("localhost", 0))
    data_connection = connection(socket=data_socket, remote=(main_connection.remote[0], rport))

    # three way handshake back to client's data_connection
    if not data_connection.connect_to_remote():
        print("failed data connection")
        return None
    print("Machine 2 data_connection state:", data_connection.get_state())

    data_connection.send_file(filename="./testfiles/32b.dat", chunksize=40)

    # close socket
    server_socket.close()
    data_socket.close()
    del main_connection
    del data_connection


if __name__ == "__main__":
    Thread(target=run_client).start()
    Thread(target=run_server).start()
