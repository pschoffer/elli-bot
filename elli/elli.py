import socket
import logging

SERVER_IP = "192.168.0.102"
SERVER_PORT = 5005

logging.basicConfig(level=logging.INFO)

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.connect((SERVER_IP, SERVER_PORT))
logging.info("Connected to a server %s:%s", SERVER_IP, SERVER_PORT)
