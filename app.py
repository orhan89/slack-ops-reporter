import os
from slack_ops_reporter import app
from slack_bolt.adapter.socket_mode import SocketModeHandler

SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
