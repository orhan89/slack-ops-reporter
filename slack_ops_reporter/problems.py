import csv


class CSVProblemProvider(object):

    problems = []

    def __init__(self):
        self.problems = self.parse_problems_csv('problems.csv')

    @staticmethod
    def parse_problems_csv(filename):
        with open(filename) as csvfile:
            reader = csv.reader(csvfile)
            problems = list(reader)

        return problems

    def get_components(self, keyword):

        components = sorted(set(map(lambda problem: (problem[2], problem[3]), self.problems)), key=lambda component: component[0])

        if keyword is not None and len(keyword) > 0:
            components = filter(lambda component: keyword in component[0], components)

        return components

    def get_problems(self, component_value=None, keyword=None):

        returned_problems = sorted(self.problems, key=lambda problem: problem[0])
        if component_value is not None:
            returned_problems = filter(lambda problem: problem[3] == component_value, returned_problems)

        if keyword is not None and len(keyword) > 0:
            returned_problems = filter(lambda problem: keyword in problem[0], returned_problems)

        return returned_problems
