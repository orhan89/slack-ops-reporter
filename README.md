# Ops Issue Reporter Slack App

## Overview

The Ops Issue Reporter Slack App allows your team to report operational issues directly from Slack. Once an issue is reported, it is logged and dispatched to the ops team for immediate attention. This app streamlines the process of issue reporting and ensures that all relevant details are captured efficiently.

![Screenshot of the new report form](assets/screenshot.png?raw=true)

## Features

- **Easy Issue Reporting**: Report issues with a simple Slack command or button.
- **Detailed Issue Form**: Collects essential details such as description, priority, affected system, and time of occurrence.
- **Notifications**: Alerts the ops team via responder (currently only support opsgenie).
- **Follow up channel**: New report will create a new private channel and invite both reporter and responder to follow up the report.

## Installation

### Prerequisites

- A Slack workspace
- Slack API token
- A server or cloud function to handle the backend logic

### Slack App Configuration

1. **Create a Slack App**
   - Go to [Slack API](https://api.slack.com/apps) and create a new app.
   - Add the necessary permissions (e.g., `chat:write`, `commands`, `incoming-webhook`).

2. **Set Up Interactive Components**
   - Enable interactivity and the webhook mode.

### Slack App Configuration

### Run the app

1. **Pull docker image**
   ```sh
   docker pull rickyhariady/slack-ops-reporter
   ```

2. **Run the app**
   ```sh
   docker run -it -e SLACK_BOT_TOKEN=<you-slack-bot-token> -e SLACK_APP_TOKEN=<your-slack-app-token> -e OPSGENIE_API_KEY=<your-opsgenie-api-key> rickyhariady/slack-ops-reporter
   ```

## Usage

### Reporting an Issue

- Click the "Report an Issue" button available from shortcut menu.
- Fill out the form with the issue details.
- Submit the form to report the issue.
- Responder will be invited to a new private channel for report follow up.

### Ops Team Notification

- The ops team will receive a notification through configured methods (currently only support opsgenie)
- Once the alert is acknowledged, the responder will be invited to the created private channel.
- When the alert is closed, the channel will be automatically archived.

## Contributing

We welcome contributions! Please read our [Contributing Guide](CONTRIBUTING.md) for details on how to contribute to this project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or feedback, please open an issue or reach out to us at [ricky.hariady@gmail.com].

