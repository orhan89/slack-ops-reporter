from slack_ops_reporter import app
from slack_ops_reporter.middlewares import problem_provider

import logging
import os
import random
import string

logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO').upper())


@app.shortcut("new_report")
def message_hello(ack, shortcut, client):
    ack()
    client.views_open(
        trigger_id=shortcut["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "new_report",
            "title": {
                "type": "plain_text",
                "text": "New Report"
            },
            "blocks": [
                {
                    "type": "input",
                    "block_id": "component_input",
                    "label": {
                        "type": "plain_text",
                        "text": "Which service/component that you want to report or need help with?"
                    },
                    "dispatch_action": True,
                    "element": {
                        "action_id": "component_selection",
                        "type": "external_select",
                        "min_query_length": 0,
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select an item",
                            "emoji": True
                        },
                    }
                },
            ],
            "submit": {
                "type": "plain_text",
                "text": "Submit"
            }
        }
    )


@app.options("component_selection",
             middleware=[problem_provider])
def component_options(ack, context, payload):
    keyword = payload.get("value")

    components = context['problem_provider'].get_components(keyword)
    options = [prepare_option(item[0], item[1]) for item in components]
    options.append(prepare_option("Other", "other"))
    ack(options=options)


@app.action("component_selection")
def handle_component_selection(ack, action, client, body):
    ack()
    # selected_option = action['selected_option']
    client.views_update(
        view_id=body["view"]["id"],
        hash=body["view"]["hash"],
        view={
            "type": "modal",
            "callback_id": "new_report",
            "title": {
                "type": "plain_text",
                "text": "Need Help?"
            },
            "blocks": [
                {
                    "type": "input",
                    "block_id": "component_input",
                    "label": {
                        "type": "plain_text",
                        "text": "Which service/component that you want to report or need help with?"
                    },
                    "dispatch_action": True,
                    "element": {
                        "action_id": "component_selection",
                        "type": "external_select",
                        "min_query_length": 0,
                        "placeholder": {
                            "type": "plain_text",
                            "text": action["selected_option"]["text"]["text"],
                            "emoji": True
                        },
                    }
                },
                {
                    "type": "input",
                    "block_id": f"problem_input:{action['selected_option']['value']}",
                    "label": {
                        "type": "plain_text",
                        "text": "How can we help you?"
                    },
                    "element": {
                        "action_id": "problem_selection",
                        "type": "external_select",
                        "min_query_length": 0,
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select an item",
                            "emoji": True
                        },
                    }
                },
                {
                    "type": "input",
                    "block_id": "priority_input",
                    "label": {
                        "type": "plain_text",
                        "text": "How soon the problem need to be resolved? (Priority)"
                    },
                    "element": {
                        "type": "static_select",
                        "action_id": "priority_selection",
                        "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Urgent (under 30 min)"
                                },
                                "value": "P1"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "High (between 30 min - 3 hours)"
                                },
                                "value": "P2"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Medium (between 3 hours - 24 hours"
                                },
                                "value": "P3"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Low (more than 24 hours)"
                                },
                                "value": "P4"
                            }
                        ]
                    }
                },
                {
                    "type": "input",
                    "block_id": "additional_info_input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "additional_info_input",
                        "multiline": True,
                        "min_length": 0
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Additional Info",
                        "emoji": True
                    }
                }
            ],
            "submit": {
                "type": "plain_text",
                "text": "Submit"
            }
        },
    )


@app.options("problem_selection",
             middleware=[problem_provider])
def problem_options(ack, context, payload, options, body):
    keyword = payload.get("value")

    component_value = options["block_id"].lstrip("problem_input:")

    component_problems = context['problem_provider'].get_problems(component_value, keyword)
    options = [prepare_option(item[0], item[1]) for item in component_problems]
    options.append(prepare_option("Other", "other"))
    ack(options=options)


@app.view("new_report")
def handle_new_report_submission(ack, body, client, view, logger):

    component = view['state']['values']['component_input']['component_selection']['selected_option']['value']
    problem = view['state']['values'][f"problem_input:{component}"]['problem_selection']['selected_option']['value']
    priority = view['state']['values']['priority_input']['priority_selection']['selected_option']['value']
    additional_info = view['state']['values']['additional_info_input']['additional_info_input']['value']

    logger.info(f"component = {component}")
    logger.info(f"problem = {problem}")
    logger.info(f"priority = {priority}")
    logger.info(f"additional_info = {additional_info}")

    channel_name = "ops_" + ''.join(random.choice(string.ascii_lowercase+string.digits) for i in range(5))
    channel = client.conversations_create(
        name=channel_name,
        is_private=True
    )

    logger.info(f"channel = {channel}")

    client.conversations_invite(
        channel=channel.data['channel']['id'],
        users=body['user']['id']
    )
    ack()


def prepare_option(text, value):
    return {
        "text": {"type": "plain_text", "text": text},
        "value": value
    }
