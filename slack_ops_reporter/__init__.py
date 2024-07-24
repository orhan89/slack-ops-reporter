import os
from slack_bolt import App

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

from slack_ops_reporter.problems import CSVProblemTypeProvider

defaultProblemTypeProvider = CSVProblemTypeProvider()

from slack_ops_reporter import shortcuts
