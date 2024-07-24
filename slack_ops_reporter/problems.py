from slack_ops_reporter.responders import OpsgenieResponder
from datetime import datetime

import csv
import urllib.parse
import random
import string


class CSVProblemTypeProvider(object):

    def __init__(self):
        self._parse_problem_types_csv('problem_types.csv')

    def _parse_problem_types_csv(self, filename):
        with open(filename) as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

        self.problem_types = map(lambda row: Problem.ProblemType(row[0], row[1]), rows)


class Problem(object):

    class Component(object):

        def __init__(self, name=""):
            self._name = name
            self._key = urllib.parse.quote_plus(name)

        def __repr__(self):
            return self._name

        def __eq__(self, other):
            if isinstance(other, Problem.Component):
                return str(self) == str(other)
            return False

        @property
        def key(self):
            return self._key

        @staticmethod
        def list(keyword, provider=CSVProblemTypeProvider()):

            unique_component = []
            for problem_type in provider.problem_types:
                if problem_type.component not in unique_component:
                    unique_component.append(problem_type.component)

            components = sorted(unique_component, key=lambda component: str(component))
            if keyword is not None and len(keyword) > 0:
                components = filter(lambda component: keyword in str(component), components)

            return components

    class ProblemType(object):

        def __init__(
                self,
                name="",
                component="",
        ):
            self._name = name
            self._key = urllib.parse.quote_plus(name)
            self.component = Problem.Component(component)

        def __repr__(self):
            return self._name

        def __eq__(self, other):
            if isinstance(other, Problem.ProblemType):
                return str(self) == str(other)
            return False

        @property
        def key(self):
            return self._key

        @staticmethod
        def list(component_key=None, keyword=None, provider=CSVProblemTypeProvider()):

            problem_types = sorted(provider.problem_types, key=lambda problem_type: str(problem_type))
            if component_key is not None:
                problem_types = filter(lambda problem_type: problem_type.component.key == component_key, problem_types)

            if keyword is not None and len(keyword) > 0:
                problem_types = filter(lambda problem_type: keyword in str(problem_type), problem_types)

            return problem_types

        @staticmethod
        def get(key, provider=CSVProblemTypeProvider()):
            try:
                problem_type = next(filter(lambda problem_type: problem_type.key == key, provider.problem_types))
            except StopIteration:
                raise Exception("ProblemNotFound")

            return problem_type

    class Priority(object):

        priorities = [
            ("P1", "Urgent (under 30 min)"),
            ("P2", "High (between 30 min - 3 hours)"),
            ("P3", "Medium (between 3 hours - 24 hours"),
            ("P4", "Low (more than 24 hours)"),
        ]

        def __init__(self, name="P1"):
            self._priority = next(filter(lambda priority: priority[0] == name, self.priorities))

        def __repr__(self):
            return self._priority[1]

        def __eq__(self, other):
            if isinstance(other, Problem.Priority):
                return self._priority[0] == other._priority[0]
            return False

        @classmethod
        def list_priorities(cls):
            return map(lambda priority: Problem.Priority(priority[0]), cls.priorities)

        @property
        def key(self):
            return self._priority[0]

    def __init__(
            self,
            problem_type_key="",
            priority="",
            requester={},
            additional_info="",
            channel_id=None,
            message_ts=None
    ):
        self.problem_type = self.ProblemType.get(problem_type_key)
        self.priority = self.Priority(priority)
        self.requester = requester
        self.additional_info = additional_info
        self.created_at = datetime.now()
        self.acknowledge_at = None
        self.responders = None
        self.channel_id = channel_id
        self.message_ts = message_ts

    def create_private_channel(self, slack_client, members=[]):
        channel_name = "ops_" + ''.join(random.choice(string.ascii_lowercase+string.digits) for i in range(5))

        channel = slack_client.conversations_create(
            name=channel_name,
            is_private=True
        )

        self.channel_id = channel.data['channel']['id']

    def invite_to_private_channel(self, slack_client, member):
        slack_client.conversations_invite(
            channel=self.channel_id,
            users=member['id']
        )

    def prepare_summary_message_attachment(self):
        return [
            {
                "color": "#FF0000",
                "blocks": [
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": "*Problem Description*\n%s" % str(self.problem_type)
                            },
                            {
                                "type": "mrkdwn",
                                "text": "*Component/Service*\n%s" % str(self.problem_type.component)
                            },
                            {
                                "type": "mrkdwn",
                                "text": "*Requested By*\n@%s" % self.requester['name']
                            },
                            {
                                "type": "mrkdwn",
                                "text": "*Priority*\n%s" % str(self.priority)
                            },
                            {
                                "type": "mrkdwn",
                                "text": "*Requested at*\n%s" % self.created_at
                            },
                            {
                                "type": "mrkdwn",
                                "text": "*Acknowledge at*\n%s" % self.acknowledge_at
                            },
                            {
                                "type": "mrkdwn",
                                "text": "*Responders*\n%s" % self.responders
                            },
                            {
                                "type": "mrkdwn",
                                "text": "*Additional Info*\n%s" % self.additional_info
                            },
                        ]
                    }
                ]
            }
        ]

    def send_summary_message(self, slack_client, text):

        attachments = self.prepare_summary_message_attachment()
        message = slack_client.chat_postMessage(
            channel=self.channel_id,
            text=text,
            attachments=attachments
        )

        self.message_ts = message['ts']

    def update_summary_message(self, slack_client, text):
        attachments = self.prepare_summary_message_attachment()
        slack_client.chat_update(
            channel=self.channel_id,
            ts=self.message_ts,
            text=text,
            attachments=attachments
        )

    def notify_responder(self):
        opsgenie = OpsgenieResponder()
        opsgenie.notify(self)

    def acknowledge(self, acknowledge_at, responder):
        self.acknowledge_at = acknowledge_at
        self.responders = responder

    def send_acknowledged_message(self, slack_client):
        slack_client.chat_postMessage(
            channel=self.channel_id,
            text="Our Responder had received and acknowledge your report. They will contact you soon",
        )
