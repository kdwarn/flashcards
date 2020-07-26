import unittest
import mock

from flashcards.decks import Deck
from flashcards.cards import StudyCard
from flashcards import study
from flashcards.study import BaseStudySession
from flashcards.study import ShuffledStudySession


def create_study_set():
    """ Create a simple study set for test purposes. """

    cards = [
        StudyCard("2 + 2 = ?", "4"),
        StudyCard("2 + 3 = ?", "5"),
        StudyCard("2 + 4 = ?", "6"),
        StudyCard("2 + 5 = ?", "7"),
    ]

    study_set = Deck("Basic Maths")
    study_set._cards = cards

    return study_set


def create_cards_list():
    """ Create a simple list of cards for test purposes. """

    cards = [
        StudyCard("2 + 2 = ?", "4"),
        StudyCard("2 + 3 = ?", "5"),
        StudyCard("2 + 4 = ?", "6"),
        StudyCard("2 + 5 = ?", "7"),
    ]

    return cards


def test_get_study_session_template_default():

    mode = "awdiowad"  # Something that is not in the mode options
    session = study.get_study_session_template(mode)

    assert isinstance(session, BaseStudySession)


def test_get_study_session_template_None_input():

    mode = None  # user did not supply any option --mode'
    session = study.get_study_session_template(mode)

    assert isinstance(session, BaseStudySession)


def test_get_study_session_template_basic():
    mode = "linear"  # user entered `linear` as --mode option.'
    session = study.get_study_session_template(mode)

    assert isinstance(session, BaseStudySession)


def test_get_study_session_template_shuffled():
    mode = "shuffled"  # user entered `shuffled` as --mode option.
    session = study.get_study_session_template(mode)

    assert isinstance(session, ShuffledStudySession)


"""
class TestBasicStudyStrategy(unittest.TestCase):
    def test_studySession_start(self):

        mock_show_question = mock.Mock()
        mock_show_answer = mock.Mock()

        study_set = create_study_set()

        session = BaseStudySession()
        session.show_question = mock_show_question
        session.show_answer = mock_show_answer

        session.start(study_set)
        self.assertEqual(4, mock_show_question.call_count)
        self.assertEqual(4, mock_show_answer.call_count)


class TestShuffledStudyStrategy(unittest.TestCase):
    @mock.patch("flashcards.study.random.shuffle")
    def test_cards_are_shuffled(self, mock_shuffle):

        mock_show_question = mock.Mock()
        mock_show_answer = mock.Mock()

        study_set = create_study_set()

        session = ShuffledStudySession()
        session.show_question = mock_show_question
        session.show_answer = mock_show_answer

        session.start(study_set)
        self.assertEqual(1, mock_shuffle.call_count)
        self.assertEqual(4, mock_show_question.call_count)
        self.assertEqual(4, mock_show_answer.call_count)
"""
