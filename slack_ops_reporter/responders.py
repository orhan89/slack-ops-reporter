from datetime import datetime
from flask import request
from slack_ops_reporter import app, defaultProblemTypeProvider
from slack_ops_reporter.problems import Problem
from slack_ops_reporter.slack_helpers import \
    invite_to_private_channel, \
    send_acknowledged_message, \
    update_summary_message, \
    send_close_message, \
    archive_private_channel
from slack_sdk.errors import SlackApiError

import opsgenie_sdk
import os


class Responder(object):

    def notify(self, problem, message_ts, channel_id):
        NotImplemented

    def acknowledge(self):
        NotImplemented

    def closed(self):
        NotImplemented


class OpsgenieResponder(Responder):

    def __init__(self):
        opsgenie_conf = opsgenie_sdk.configuration.Configuration()
        opsgenie_conf.api_key['Authorization'] = os.environ.get('OPSGENIE_API_KEY')

        opsgenie_client = opsgenie_sdk.api_client.ApiClient(configuration=opsgenie_conf)
        self.alert_api = opsgenie_sdk.AlertApi(api_client=opsgenie_client)

    def notify(self, problem):
        message = str(problem.problem_type)
        tags = []
        if message == 'Other':
            message_lines = problem.additional_info.splitlines()
            message = message_lines[0] if message_lines else message
        body = opsgenie_sdk.CreateAlertPayload(
            message=message,
            tags=tags,
            responders=None,
            source="Ops Reporter",
            details={
                'problem_type': problem.problem_type.key,
                'requester_id': problem.requester["id"],
                'requester_name': problem.requester["name"],
                'additional_info': problem.additional_info,
                'created_at': problem.created_at,
                'message_ts': problem.message_ts,
                'channel_id': problem.channel_id
            },
            priority=problem.priority.key
        )
        try:
            create_response = self.alert_api.create_alert(create_alert_payload=body)
            return create_response
        except opsgenie_sdk.ApiException as err:
            print("Exception when calling AlertApi->create_alert: %s\n" % err)

    def acknowledge(self, problem, ack_at, ack_by):
        responder_slack_user = app.client.users_lookupByEmail(email=ack_by)
        responder = responder_slack_user.data['user']

        problem.acknowledge(ack_at, responder['name'])
        try:
            invite_to_private_channel(app.client, problem.channel_id, responder)
        except SlackApiError:
            pass
        send_acknowledged_message(app.client, problem)
        update_summary_message(app.client, problem, text="Hey, we have received your request and will forward it to our Engineer")

    def close(self, problem):
        send_close_message(app.client, problem)
        archive_private_channel(app.client, problem)

    def handle_webhook(self, data):
        alert = data['alert']
        problem_type = alert["details"]["problem_type"]
        requester_name = alert["details"]["requester_name"]
        requester_id = alert["details"]["requester_id"]
        additional_info = alert["details"]["additional_info"]
        channel_id = alert["details"]["channel_id"]
        message_ts = alert["details"]["message_ts"]
        created_at = alert["details"]["created_at"]
        priority = alert["priority"]

        requester = {
            'name': requester_name,
            'id': requester_id
        }

        problem = Problem(
            defaultProblemTypeProvider,
            problem_type,
            priority=priority,
            requester=requester,
            additional_info=additional_info,
            created_at=created_at,
            channel_id=channel_id,
            message_ts=message_ts
        )

        action = data['action']
        if action == "Acknowledge":
            ack_at = datetime.fromtimestamp(alert['updatedAt']/1000000000)
            ack_by = alert['username']
            self.acknowledge(problem, ack_at, ack_by)

        elif action == "Close":
            self.close(problem)


def opsgenie_webhook():
    data = request.json

    responder = OpsgenieResponder()
    responder.handle_webhook(data)

    return "OK"
