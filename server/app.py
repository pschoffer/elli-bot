
from flask import Flask, request
from flask_cors import CORS
from flask.views import MethodView
import socket
import logging
import threading
import signal
import sys
import json

ELLI_SOCKET_PORT = 5005

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)


class ElliCommunicator(threading.Thread):
    def __init__(self, port):
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("", port))
        self._stopFlag = False
        threading.Thread.__init__(self)

    def run(self):
        logging.info("Starting Elli communicator on port %s", self.port)
        while not self._stopFlag:
            self.socket.settimeout(2)
            self.socket.listen(1)
            try:
                self.elliConn, self.elliAddr = self.socket.accept()
                logging.info("Elli connected!")
                return
            except socket.timeout:
                pass
        self.cleanup()

    def cleanup(self):
        logging.info("Cleaning up sockets")
        if (hasattr(self, "elliConn")):
            self.elliConn.close()
        self.socket.close()

    def send(self, msg):
        if (hasattr(self, "elliConn")):
            encodedData = bytearray(json.dumps(msg), "utf-8")
            self.elliConn.sendall(encodedData)
        else:
            logging.error("No open connection")

    def stop(self):
        self._stopFlag = True


elliCommunicator = ElliCommunicator(ELLI_SOCKET_PORT)
elliCommunicator.start()


def sigint_handler(sig, frame):
    logging.info("Shutting down!!")
    if (elliCommunicator.isAlive()):
        elliCommunicator.stop()
        elliCommunicator.join()
    else:
        elliCommunicator.cleanup()
    logging.info("Communciator down.")
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)


class WebView(MethodView):
    def get(self):
        return app.send_static_file('index.html')


class StatusView(MethodView):
    def get(self):
        response = {}
        isConnected = hasattr(elliCommunicator, "elliAddr")
        logging.info("Checking if addr is set already: %s", isConnected)
        if (isConnected and elliCommunicator.elliAddr):
            response = {
                "status": "OK",
                "addr": elliCommunicator.elliAddr
            }
        else:
            response = {
                "status": "NOT_CONNECTED"
            }
        return response


class InstructionView(MethodView):
    def post(self):
        logging.info("Instruction request recieved '%s'", request.json)
        elliCommunicator.send(request.json)
        return "OK"


app.add_url_rule('/', view_func=WebView.as_view("web"))
app.add_url_rule('/status', view_func=StatusView.as_view("status"))
app.add_url_rule(
    '/instruction', view_func=InstructionView.as_view("instruction"))

app.run(host='0.0.0.0')
