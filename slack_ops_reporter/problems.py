from datetime import datetime

import csv
import urllib.parse


class Priority(object):

    priorities = [
        ("P1", "Urgent (under 30 min)"),
        ("P2", "Urgent (under 30 min)"),
        ("P3", "Urgent (under 30 min)"),
        ("P4", "Urgent (under 30 min)"),
        ("P5", "Urgent (under 30 min)"),
    ]

    def __init__(self, name="P1"):
        self._priority = next(filter(lambda priority: priority[0] == name, self.priorities))

    def __repr__(self):
        return self._priority[1]

    def __eq__(self, other):
        if isinstance(other, Priority):
            return self._priority[0] == other._priority[0]
        return False

    @classmethod
    def list_priorities(cls):
        return map(lambda priority: Priority(priority[0]), cls.priorities)

    @property
    def value(self):
        return self._priority[0]


class Component(object):

    def __init__(self, name=""):
        self._name = name
        self._value = urllib.parse.quote_plus(name)

    def __repr__(self):
        return self._name

    def __eq__(self, other):
        if isinstance(other, Component):
            return str(self) == str(other)
        return False

    @property
    def value(self):
        return self._value


class ProblemType(object):

    def __init__(
            self,
            name="",
            component="",
    ):
        self._name = name
        self._value = urllib.parse.quote_plus(name)
        self.component = Component(component)

    def __repr__(self):
        return self._name

    def __eq__(self, other):
        if isinstance(other, ProblemType):
            return str(self) == str(other)
        return False

    @property
    def value(self):
        return self._value


class Problem(object):

    def __init__(
            self,
            problem_type=None,
            requester={},
            priority=Priority("P1"),
            additional_info=""
    ):
        print(problem_type)
        print(type(problem_type))
              
        self.problem_type = problem_type
        self.requester = requester
        self.priority = priority
        self.additional_info = additional_info
        self.created_at = datetime.now()
        print(self.problem_type)
        print(type(self.problem_type))


class CSVProblemTypeProvider(object):

    def __init__(self):
        self._parse_problem_types_csv('problem_types.csv')

    def _parse_problem_types_csv(self, filename):
        with open(filename) as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

        self.problem_types = map(lambda row: ProblemType(row[0], row[1]), rows)

    def list_components(self, keyword):

        unique_component = []
        for problem_type in self.problem_types:
            if problem_type.component not in unique_component:
                unique_component.append(problem_type.component)

        components = sorted(unique_component, key=lambda component: str(component))
        if keyword is not None and len(keyword) > 0:
            components = filter(lambda component: keyword in str(component), components)

        return components

    def list_problem_types(self, component_value=None, keyword=None):

        problem_types = sorted(self.problem_types, key=lambda problem_type: str(problem_type))
        if component_value is not None:
            problem_types = filter(lambda problem_type: problem_type.component.value == component_value, problem_types)

        if keyword is not None and len(keyword) > 0:
            problem_types = filter(lambda problem_type: keyword in str(problem_type), problem_types)

        return problem_types

    def get_problem_type(self, problem_value):
        try:
            problem = next(filter(lambda problem_type: problem_type.value == problem_value, self.problem_types))
        except StopIteration:
            raise Exception("ProblemNotFound")

        return problem
