from slack_ops_reporter import app
from slack_ops_reporter.responders import opsgenie_webhook
from slack_bolt.adapter.socket_mode import SocketModeHandler
from flask import Flask, request

import os

handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
handler.connect()

flask_app = Flask(__name__)

flask_app.add_url_rule('/opsgenie', view_func=opsgenie_webhook, methods=['POST'])

@flask_app.route("/", methods=["GET"])
def index():
    return "Hello World"
