"""
flashcards.cards
~~~~~~~~~~~~~~~~~~~

Contain the StudyCard object and logic related to it.
"""
from collections import OrderedDict

# Serialization key's
QUESTION_KEY = "question"
ANSWER_KEY = "answer"


def create_from_dict(data):
    """
    Construct a StudyCard Object from a dictionary object.

    :param data: the dictionary object

    :raises KeyError: when dictionary is missing a needed field to create obj.

    :returns: StudyCard object
    """
    if QUESTION_KEY not in data:
        raise KeyError("Invalid data string. %s key is missing" % QUESTION_KEY)
    if ANSWER_KEY not in data:
        raise KeyError("Invalid data string. %s key is missing" % ANSWER_KEY)

    question = data[QUESTION_KEY]
    answer = data[ANSWER_KEY]

    return StudyCard(question, answer)


class StudyCard(object):
    """
    Class representing a question card.

    A question card is simple card containing a Question and an Answer.
    """

    def __init__(self, question, answer):
        """
        Creates a Question card containing a question and an answer to the
        question.

        :param question: The question of the card.
        :param answer: The answer to the question.
        """
        self.question = question
        self.answer = answer

    def to_dict(self):
        """
        Convert this StudyCard to a dictionary.

        :returns: a dictionary object representation of this StudyCard
        """
        data = ((QUESTION_KEY, self.question), (ANSWER_KEY, self.answer))
        return OrderedDict(data)
