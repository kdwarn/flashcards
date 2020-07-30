import pytest

from flashcards import cards
from flashcards.cards import StudyCard


card1 = {"question": "2+2=?", "answer": "4"}
card2 = {"question": "3+3?", "not_the_answer": "3"}
card3 = {"not_the_question": "this isn't math", "answer": "10"}


def test_create_card_from_dict():
    card = cards.create_from_dict(card1)
    assert card.question == "2+2=?"
    assert card.answer == "4"


def test_card_to_dict():
    card = cards.create_from_dict(card1)
    card_dict = card.to_dict()
    assert card_dict == card1


def test_card_to_dict_raises_error1():
    with pytest.raises(KeyError):
        cards.create_from_dict(card2)


def test_card_to_dict_raises_error2():
    with pytest.raises(KeyError):
        cards.create_from_dict(card3)
