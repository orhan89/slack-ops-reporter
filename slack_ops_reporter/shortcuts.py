from slack_ops_reporter import app


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
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Which service/component that you want to report or need help with?"
                    },
                    "accessory": {
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
