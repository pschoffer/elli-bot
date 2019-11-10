import socket
import logging
import time

SERVER_IP = "192.168.0.102"
SERVER_PORT = 5005

logging.basicConfig(level=logging.INFO)


class Communicator:
    def connect(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            logging.info("Trying to connect to a server %s:%s",
                         SERVER_IP, SERVER_PORT)
            try:
                self.serverSocket.connect((SERVER_IP, SERVER_PORT))
                break
            except ConnectionRefusedError:
                time.sleep(5)
            pass
        logging.info("Connected to a server!")

    def listen(self):
        eofRecieved = False
        while not eofRecieved:
            data = self.serverSocket.recv(1024)
            if data:
                logging.info("Got data: %s", data)
            else:
                eofRecieved = True
                logging.info("Reached end of connection.")

    def cleanup(self):
        logging.info("Cleaning up socket")
        self.serverSocket.close()


communicator = Communicator()
while True:
    communicator.connect()
    communicator.listen()
    communicator.cleanup()
