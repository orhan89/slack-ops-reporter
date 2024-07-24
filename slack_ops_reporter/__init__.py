import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from flask import Flask

slack_app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


def create_app():
    app = Flask(__name__)

    from slack_ops_reporter import responders
    app.register_blueprint(responders.bp)

    from slack_ops_reporter import shortcuts

    handler = SocketModeHandler(slack_app, os.environ["SLACK_APP_TOKEN"])
    handler.connect()

    return app
