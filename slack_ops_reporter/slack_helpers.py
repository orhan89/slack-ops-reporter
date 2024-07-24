from slack_ops_reporter.problems import Problem

import random
import string


def create_private_channel(slack_client, members=[]):
    channel_name = "ops_" + ''.join(random.choice(string.ascii_lowercase+string.digits) for i in range(5))

    channel = slack_client.conversations_create(
        name=channel_name,
        is_private=True
    )

    return channel.data['channel']['id']


def invite_to_private_channel(slack_client, channel_id, member):
    slack_client.conversations_invite(
        channel=channel_id,
        users=member['id']
    )


def send_summary_message(slack_client, problem, text):

    attachments = prepare_summary_message_attachment(problem)
    message = slack_client.chat_postMessage(
        channel=problem.channel_id,
        text=text,
        attachments=attachments
    )

    return message['ts']


def update_summary_message(slack_client, problem, text):
    attachments = prepare_summary_message_attachment(problem)
    slack_client.chat_update(
        channel=problem.channel_id,
        ts=problem.message_ts,
        text=text,
        attachments=attachments
    )


def send_acknowledged_message(slack_client, problem):
    slack_client.chat_postMessage(
        channel=problem.channel_id,
        text=f"Our Responder @{problem.responders} had received and acknowledge your report. They will contact you soon",
    )


def send_close_message(slack_client, problem):
    slack_client.chat_postMessage(
        channel=problem.channel_id,
        text="Your issue has been resolved. Please made another request if you facing another problem",
    )


def archive_private_channel(slack_client, problem):
    slack_client.conversations_archive(
        channel=problem.channel_id,
    )


def prepare_summary_message_attachment(problem):
    return [
        {
            "color": "#FF0000",
            "blocks": [
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*Problem Description*\n%s" % str(problem.problem_type)
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Component/Service*\n%s" % str(problem.problem_type.component)
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Requested By*\n@%s" % problem.requester['name']
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Priority*\n%s" % str(problem.priority)
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Requested at*\n%s" % problem.created_at
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Acknowledge at*\n%s" % problem.acknowledge_at
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Responders*\n@%s" % problem.responders
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Additional Info*\n%s" % problem.additional_info
                        },
                    ]
                }
            ]
        }
    ]


def prepare_option(text, value):
    return {
        "text": {"type": "plain_text", "text": text},
        "value": value
    }


def prepare_priority_options():
    options = []
    for priority in Problem.Priority.list_priorities():
        options.append({
            "text": {
                "type": "plain_text",
                "text": str(priority)
            },
            "value": priority.key
        })
    return options
