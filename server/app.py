
from flask import Flask, request
from flask_cors import CORS
from flask.views import MethodView
import socket
import logging
import threading

ELLI_SOCKET_PORT = 5005

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)


class ElliCommunicator(threading.Thread):
    def __init__(self, port):
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("", port))
        threading.Thread.__init__(self)

    def run(self):
        self.socket.listen()
        logging.info("Starting Elli communicator on port %s", self.port)
        self.elliConn, self.elliAddr = self.socket.accept()
        logging.info("Elli connected!")


elliCommunicator = ElliCommunicator(ELLI_SOCKET_PORT)
elliCommunicator.start()


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
        return "OK"


app.add_url_rule('/', view_func=WebView.as_view("web"))
app.add_url_rule('/status', view_func=StatusView.as_view("status"))
app.add_url_rule(
    '/instruction', view_func=InstructionView.as_view("instruction"))

app.run(host='0.0.0.0')
