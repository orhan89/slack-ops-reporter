from slack_ops_reporter import app
from slack_ops_reporter.problems import Problem

import logging
import os

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
            ]
        }
    )


@app.options("component_selection")
def component_options(ack, context, payload):
    keyword = payload.get("value")

    components = Problem.Component.list(keyword)
    options = [prepare_option(str(item), item.key) for item in components]
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
                        "options": prepare_priority_options()
                    }
                },
                {
                    "type": "input",
                    "optional": True,
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


@app.options("problem_selection")
def problem_options(ack, context, payload, options, body):
    keyword = payload.get("value")

    component_key = options["block_id"].lstrip("problem_input:")

    problem_types = Problem.ProblemType.list(component_key, keyword)
    options = [prepare_option(str(item), item.key) for item in problem_types]
    options.append(prepare_option("Other", "other"))
    ack(options=options)


@app.view("new_report")
def handle_new_report_submission(ack, context, body, client, view):
    ack()

    component_key = view['state']['values']['component_input']['component_selection']['selected_option']['value']
    problem_type_key = view['state']['values'][f"problem_input:{component_key}"]['problem_selection']['selected_option']['value']
    priority_key = view['state']['values']['priority_input']['priority_selection']['selected_option']['value']
    additional_info = view['state']['values']['additional_info_input']['additional_info_input']['value']

    requester = body['user']
    problem = Problem(problem_type_key, priority_key, requester, additional_info)

    problem.create_private_channel(client)
    problem.invite_to_private_channel(client, requester)
    problem.send_summary_message(client, text="Hey, we have received your request and will forward it to our Engineer")
    problem.notify_responder()


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
