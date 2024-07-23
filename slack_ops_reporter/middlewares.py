from slack_ops_reporter.problems import CSVProblemTypeProvider


def problem_provider(context, next):
    context['problem_provider'] = CSVProblemTypeProvider()
    next()
