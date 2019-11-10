
from flask import Flask
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
        elliConn, elliAddr = self.socket.accept()
        print(elliConn, elliAddr)


elliCommunicator = ElliCommunicator(ELLI_SOCKET_PORT)
elliCommunicator.start()


class WebView(MethodView):
    def get(self):
        return app.send_static_file('index.html')


class StatusView(MethodView):
    def get(self):
        return {
            "status": "NOT_CONNECTED"
        }


app.add_url_rule('/', view_func=WebView.as_view("web"))
app.add_url_rule('/status', view_func=StatusView.as_view("status"))

app.run(host='0.0.0.0')
