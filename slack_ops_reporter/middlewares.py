from slack_ops_reporter.problems import CSVProblemProvider


def problem_provider(context, next):
    context['problem_provider'] = CSVProblemProvider()
    next()
