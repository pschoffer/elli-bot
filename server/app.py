
from flask import Flask
from flask_cors import CORS
from flask.views import MethodView


app = Flask(__name__)
CORS(app)


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
