# Contributing to Ops Issue Reporter Slack App

First off, thanks for taking the time to contribute! 🎉

The following is a set of guidelines for contributing to the Ops Issue Reporter Slack App. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How to Contribute](#how-to-contribute)
   - [Reporting Bugs](#reporting-bugs)
   - [Suggesting Features](#suggesting-features)
   - [Submitting Pull Requests](#submitting-pull-requests)
3. [Development Setup](#development-setup)
4. [Style Guide](#style-guide)
5. [Commit Messages](#commit-messages)
6. [License](#license)

## Code of Conduct

By participating in this project, you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md). Please read it to understand the kind of behavior we expect from contributors.

## How to Contribute

### Reporting Bugs

If you find a bug, please report it by opening an issue in the [issue tracker](https://github.com/orhan89/slack-ops-reporter/issues). Please include:

- A clear and descriptive title.
- A description of the problem, including steps to reproduce the issue.
- Any relevant logs or screenshots.

### Suggesting Features

We welcome feature suggestions! To propose a new feature:

1. Check if the feature is already requested by searching through the [issue tracker](https://github.com/orhan89/slack-ops-reporter/issues).
2. If the feature has not been requested, open a new issue and provide a detailed description of the feature, including any benefits and potential drawbacks.

### Submitting Pull Requests

To submit a pull request:

1. Fork the repository.
2. Create a new branch from `main` for your changes:
   ```sh
   git checkout -b feature/your-feature-name
   ```
3. Make your changes and commit them with descriptive commit messages.
4. Push your branch to your forked repository:
   ```sh
   git push origin feature/your-feature-name
   ```
5. Open a pull request against the `main` branch of the original repository.

Your pull request will be reviewed, and you may be asked to make changes. Please be responsive to feedback.

## Development Setup

To set up a development environment using Nix:

1. **Clone the Repository**
   ```sh
   git clone https://github.com/orhan89/slack-ops-reporter.git
   cd slack-ops-reporter
   ```

2. **Install Nix** (if not already installed)
   Follow the instructions [here](https://nixos.org/download.html) to install Nix.

3. **Set Up the Development Environment**
   Run the following command to enter the development shell:
   ```sh
   nix-shell
   ```

4. **Configure Environment Variables**
   Create a `.env` file in the root directory and add the necessary configuration:
   ```env
   SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
   SLACK_APP_TOKEN=your-slack-signing-secret
   OPSGENIE_API_KEY=your-ops-channel-id
   ```

5. **Run the App**
   ```sh
   FLASK_APP=slack_ops_reporter FLASK_ENVIRONMENT=development flask run -p 3000
   ```

## Style Guide

Please adhere to the following coding standards:

- Follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) coding style.
- Use meaningful variable and function names.
- Write clear and concise comments where necessary.

## Commit Messages

Write clear, concise commit messages in the following format:

```
[type]: [description]

[optional body]
```

Types:

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing or correcting existing tests
- **chore**: Changes to the build process or auxiliary tools and libraries such as documentation generation

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).

