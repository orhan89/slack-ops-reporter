from datetime import datetime

import urllib.parse


class Problem(object):

    class Component(object):

        def __init__(self, name=""):
            self._name = name
            self._key = urllib.parse.quote_plus(name)

        def __repr__(self):
            return self._name

        def __eq__(self, other):
            if isinstance(other, Problem.Component):
                return str(self) == str(other)
            return False

        @property
        def key(self):
            return self._key

        @staticmethod
        def list(provider, keyword):

            unique_component = []
            for problem_type in provider.problem_types:
                if problem_type.component not in unique_component:
                    unique_component.append(problem_type.component)

            components = sorted(unique_component, key=lambda component: str(component))
            if keyword is not None and len(keyword) > 0:
                components = filter(lambda component: keyword in str(component), components)

            return components

    class ProblemType(object):

        def __init__(
                self,
                name="",
                component="",
        ):
            self._name = name
            self._key = urllib.parse.quote_plus(name)
            self.component = Problem.Component(component)

        def __repr__(self):
            return self._name

        def __eq__(self, other):
            if isinstance(other, Problem.ProblemType):
                return str(self) == str(other)
            return False

        @property
        def key(self):
            return self._key

        @staticmethod
        def list(provider, component_key=None, keyword=None):

            problem_types = sorted(provider.problem_types, key=lambda problem_type: str(problem_type))
            if component_key is not None:
                problem_types = filter(lambda problem_type: problem_type.component.key == component_key, problem_types)

            if keyword is not None and len(keyword) > 0:
                problem_types = filter(lambda problem_type: keyword in str(problem_type), problem_types)

            return problem_types

        @staticmethod
        def get(provider, key):
            try:
                problem_type = next(filter(lambda problem_type: problem_type.key == key, provider.problem_types))
            except StopIteration:
                raise Exception("ProblemNotFound")

            return problem_type

    class Priority(object):

        priorities = [
            ("P1", "Urgent (under 30 min)"),
            ("P2", "High (between 30 min - 3 hours)"),
            ("P3", "Medium (between 3 hours - 24 hours"),
            ("P4", "Low (more than 24 hours)"),
        ]

        def __init__(self, name="P1"):
            self._priority = next(filter(lambda priority: priority[0] == name, self.priorities))

        def __repr__(self):
            return self._priority[1]

        def __eq__(self, other):
            if isinstance(other, Problem.Priority):
                return self._priority[0] == other._priority[0]
            return False

        @classmethod
        def list_priorities(cls):
            return map(lambda priority: Problem.Priority(priority[0]), cls.priorities)

        @property
        def key(self):
            return self._priority[0]

    def __init__(
            self,
            provider,
            problem_type_key="",
            priority="",
            requester={},
            additional_info="",
            created_at=None,
            channel_id=None,
            message_ts=None
    ):
        self.provider = provider
        self.problem_type = self.ProblemType.get(provider, problem_type_key)
        self.priority = self.Priority(priority)
        self.requester = requester
        self.additional_info = additional_info
        if created_at is None:
            created_at = datetime.now()
        self.created_at = created_at
        self.acknowledge_at = None
        self.responders = None
        self.channel_id = channel_id
        self.message_ts = message_ts

    def set_channel_id(self, channel_id):
        self.channel_id = channel_id

    def set_summary_message_ts(self, message_ts):
        self.message_ts = message_ts

    def acknowledge(self, acknowledge_at, responder):
        self.acknowledge_at = acknowledge_at
        self.responders = responder


