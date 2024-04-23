"""
copyright WMMKSLab Gbanyan

modified by wwolfyTC 2019/1/24
"""
import socket
from subprocess import call
from enum import Enum, unique
from traceback import print_exc
from utils import wait_confirmation, transfer_data, receive_data, bytes2string
import socket
import json
import os


CONNECT_HOST = "192.168.239.46"
CONNECT_PORT = 1277
FILE_TO_SEND = "recording.wav"
FILE_RECEIVE = "response.txt"
## << PARAMETERS
# send file ===================================================================================
def transfer_arguments(client_socket : socket.socket, arguments : dict) -> None:
    client_socket.sendall(bytes2string(json.dumps(arguments).encode("utf-8")).encode("utf-8") + b"@")

def send_data(FILE_TO_SEND):
    print("1. Transferring data...")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((CONNECT_HOST, CONNECT_PORT))
    transfer_arguments(client_socket, { "method" : "send", "path" : FILE_TO_SEND })
    wait_confirmation(client_socket)
    transfer_data(client_socket, FILE_TO_SEND)
    client_socket.close()
    print("1. Transferred data...\n")
    # =============================================================================================
    # receive file ================================================================================
    print("2. Receiving data...")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((CONNECT_HOST, CONNECT_PORT))
    transfer_arguments(client_socket, { "method" : "receive", "path" : FILE_RECEIVE })
    response = wait_confirmation(client_socket)
    if (response == 1):
        print("File path not found...")
    else:
        dst_path = os.path.join(os.path.dirname(__file__), os.path.basename(FILE_RECEIVE))
        receive_data(client_socket, dst_path)
        print("2. Received data...")
        with open('response.txt', 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)

