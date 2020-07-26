"""Contain the StudyCard object and logic related to it."""
from collections import OrderedDict


def create_from_dict(data):
    """Construct a StudyCard from a dictionary."""
    if "question" not in data:
        raise KeyError("Invalid data string. 'question' key is missing")
    if "answer" not in data:
        raise KeyError("Invalid data string. 'answer' key is missing")

    return StudyCard(data["question"], data["answer"])


class StudyCard:
    """Class with a Question and an Answer."""

    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def to_dict(self):
        return OrderedDict((("question", self.question), ("answer", self.answer)))
