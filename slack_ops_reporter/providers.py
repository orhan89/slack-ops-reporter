from slack_ops_reporter.problems import Problem

import csv


class CSVProblemTypeProvider(object):

    def __init__(self):
        self._parse_problem_types_csv('problem_types.csv')

    def _parse_problem_types_csv(self, filename):
        with open(filename) as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

        self.problem_types = list(map(lambda row: Problem.ProblemType(row[0], row[1]), rows))


defaultProblemTypeProvider = CSVProblemTypeProvider()
