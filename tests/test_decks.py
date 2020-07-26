import pytest

from flashcards import decks
from flashcards.decks import Deck
from flashcards.cards import StudyCard

math_deck = Deck("Math", "A study set about maths")


def test_create_from_dict():
    card = StudyCard("2+2=?", "4")

    data = {"name": "Math", "description": "Math-145"}
    data["cards"] = [card.to_dict()]

    study_set = decks.create_from_dict(data)

    assert study_set.name == "Math"
    assert study_set.description == "Math-145"
    assert study_set.cards[0].question == "2+2=?"
    assert study_set.cards[0].answer == "4"


def test_StudySet_exists():
    assert Deck("Math 145") is not None


def test_get_name():
    assert math_deck.name == "Math"


def test_get_description():
    assert math_deck.description == "A study set about maths"


def test_set_name():
    math_deck.name = "Math1"
    assert math_deck.name == "Math1"


def test_set_description():
    math_deck.description = "A study set about math"
    assert math_deck.description == "A study set about math"


def test_add():
    card = StudyCard("What is my name?", "Jonathan")
    math_deck.add(card)
    assert len(math_deck.cards) == 1
    assert card in math_deck.cards


def test_set_add_wrong_type():
    card = "A string is not a card!"
    with pytest.raises(TypeError):
        math_deck.add(card)


def test_len_deck():

    card0 = StudyCard("What is my name?", "Jonathan")
    card1 = StudyCard("What is bird's name ?", "Gandalf")
    card2 = StudyCard("What is the meaning of life ?", "42")
    deck = Deck("another deck")
    deck.add(card0)
    deck.add(card1)
    deck.add(card2)

    assert len(deck) == 3


def test_to_dict():
    deck = Deck("misc", "A misc deck")
    card = StudyCard("What is my name?", "Jonathan")
    deck.add(card)

    data = deck.to_dict()
    expected = {"name": "misc", "description": "A misc deck"}

    # List of serialized cards in this set
    cards = [c.to_dict() for c in deck]
    expected["cards"] = cards
    assert expected == data
