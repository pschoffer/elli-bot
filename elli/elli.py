import socket
import logging
import time
import json
from subprocess import call
from gpiozero import LED, Button

SERVER_IP = "192.168.0.102"
SERVER_PORT = 5005

logging.basicConfig(level=logging.INFO)

statusLed = LED(24)
killButton = Button(21)


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
                instruction = json.loads(data.decode("utf-8"))
                direction = instruction["direction"]
                logging.info("Decoded to: %s", direction)
            else:
                eofRecieved = True
                logging.info("Reached end of connection.")

    def cleanup(self):
        logging.info("Cleaning up socket")
        self.serverSocket.close()


def shutdown():
    logging.info("Shutting Down!!")
    statusLed.blink(0.1, 0.1)
    call("sudo shutdown -h now", shell=True)


killButton.when_pressed = shutdown

communicator = Communicator()
while True:
    statusLed.blink(0.5, 0.5)
    communicator.connect()
    statusLed.on()
    communicator.listen()
    communicator.cleanup()
