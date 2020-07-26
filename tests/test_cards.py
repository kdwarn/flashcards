import pytest

from flashcards import cards
from flashcards.cards import StudyCard


card1 = {"question": "2+2=?", "answer": "4"}
card2 = StudyCard("What is PI ?", "3.14159265359")


def test_create_card_from_dict():
    card = cards.create_from_dict(card1)
    assert card.question == "2+2=?"
    assert card.answer == "4"


def test_card_to_dict():
    card = cards.create_from_dict(card1)
    card_dict = card.to_dict()
    assert card_dict == {"question": "2+2=?", "answer": "4"}


def test_card_get_question():
    assert card2.question == "What is PI ?"


def test_card_get_answer():
    assert card2.answer == "3.14159265359"
