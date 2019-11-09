
from flask import Flask
from flask_cors import CORS
from flask.views import MethodView


class WebView(MethodView):
    def get(self):
        return "Sup!"


app = Flask(__name__)
CORS(app)

app.add_url_rule('/', view_func=WebView.as_view("web"))
app.run(host='0.0.0.0')
