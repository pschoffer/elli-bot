import socket
import logging
import time
import json
from subprocess import call
from datetime import datetime
from gpiozero import LED, Button, Motor

SERVER_IP = "192.168.0.102"
SERVER_PORT = 5005
MOTION_STOP_MICROS = 2000

logging.basicConfig(level=logging.INFO)

statusLed = LED(24)
killButton = Button(21)
motorLeft = Motor(4, 3)
motorRight = Motor(16, 20)


class Communicator:
    def __init__(self, motionController):
        self.motionController = motionController

    def connect(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            logging.info("Trying to connect to a server %s:%s",
                         SERVER_IP, SERVER_PORT)
            try:
                self.serverSocket.connect((SERVER_IP, SERVER_PORT))
                break
            except (ConnectionRefusedError, TimeoutError):
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
                motionController.setInstruction(direction)
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


class MotionController:
    _opositeDirections = frozenset([
        frozenset(["straight", "back"]),
        frozenset(["left", "right"])
    ])

    def __init__(self, motorLeft, motorRight):
        self.motorLeft = motorLeft
        self.motorRight = motorRight
        self._setInstructionTime()
        self.currentInstruction = None
        self.nextInstruction = None
        
    def setInstruction(self, instruction):
        isOposite = self.isOpositeToCurrentInstruction(instruction)
        logging.info("Setting operation %s [oposite: %s]", instruction, isOposite)
        self.currentInstruction = instruction

    def isOpositeToCurrentInstruction(self, instruction):
        thisCombination = frozenset([self.currentInstruction, instruction])
        return thisCombination in MotionController._opositeDirections

    def _setInstructionTime(self):
        self.lastInstructionTime = datetime.now()

    def _forward(self):
        self.motorLeft.forward()
        self.motorRight.forward()
        self._setInstructionTime()

    def _backward(self):
        self.motorLeft.backward()
        self.motorRight.backward()
        self._setInstructionTime()


motionController = MotionController(motorLeft, motorRight)
communicator = Communicator(motionController)
while True:
    statusLed.blink(0.5, 0.5)
    communicator.connect()
    statusLed.on()
    communicator.listen()
    communicator.cleanup()
