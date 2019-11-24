import socket
import logging
import time
import json
import threading
from subprocess import call
from datetime import datetime
from gpiozero import LED, Button, Motor

SERVER_IP = "192.168.0.102"
SERVER_PORT = 5005
MOTION_STOP_SECS = 1.5

logging.basicConfig(level=logging.INFO)

statusLed = LED(24)
killButton = Button(21)
motorLeft = Motor(4, 3)
motorRight = Motor(16, 20)


class Communicator:
    def __init__(self, motionController):
        self.motionController = motionController
        self.motionController.start()

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


class MotionController(threading.Thread):
    _opositeDirections = frozenset([
        frozenset(["straight", "back"]),
        frozenset(["left", "right"])
    ])

    def __init__(self, motorLeft, motorRight):
        self.motorLeft = motorLeft
        self.motorRight = motorRight
        self._setInstructionTime()
        self.lastInstruction = None
        self.nextInstruction = None

        self._stopFlag = False
        threading.Thread.__init__(self)

    def run(self):
        logging.info("Starting motion controller")
        while not self._stopFlag:
            self._updateInstructionTimeOut()
            self._updateMotors()
            time.sleep(0.1)
    
    def _updateMotors(self):
        if self.nextInstruction is None:
            self._stop()
        elif self.nextInstruction == "straight":
            self._forward()
        elif self.nextInstruction == "back":
            self._backward()
        elif self.nextInstruction == "left":
            self._left()
        elif self.nextInstruction == "right":
            self._right()

    def _updateInstructionTimeOut(self):
        if self.nextInstruction is not None:
            timeDiff = (datetime.now() - self.lastInstructionTime).total_seconds()
            if (timeDiff > MOTION_STOP_SECS):
                logging.info("Stopping controller due to timeout!")
                self.nextInstruction = None

    def setInstruction(self, instruction):
        isOposite = self.isOpositeToCurrentInstruction(instruction)
        finalInstruction = None if isOposite else instruction
        logging.info("Setting operation %s [oposite: %s] => %s", instruction, isOposite, finalInstruction)
        
        self._setInstructionTime()
        self.lastInstruction = self.nextInstruction
        self.nextInstruction = finalInstruction

    def isOpositeToCurrentInstruction(self, instruction):
        thisCombination = frozenset([self.lastInstruction, instruction])
        return thisCombination in MotionController._opositeDirections

    def _setInstructionTime(self):
        self.lastInstructionTime = datetime.now()

    def _forward(self):
        self.motorLeft.forward()
        self.motorRight.forward()

    def _backward(self):
        self.motorLeft.backward()
        self.motorRight.backward()


    def _left(self):
        self.motorLeft.backward()
        self.motorRight.forward()

    def _right(self):
        self.motorLeft.forward()
        self.motorRight.backward()


    def _stop(self):
        self.motorLeft.stop()
        self.motorRight.stop()


motionController = MotionController(motorLeft, motorRight)
communicator = Communicator(motionController)
while True:
    statusLed.blink(0.5, 0.5)
    communicator.connect()
    statusLed.on()
    communicator.listen()
    communicator.cleanup()
