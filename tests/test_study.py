import unittest
import mock

from flashcards.decks import Deck
from flashcards.cards import StudyCard
from flashcards import study


def create_deck():
    """ Create a simple deck for test purposes. """

    cards = [
        StudyCard("2 + 2 = ?", "4"),
        StudyCard("2 + 3 = ?", "5"),
        StudyCard("2 + 4 = ?", "6"),
        StudyCard("2 + 5 = ?", "7"),
    ]

    deck = Deck("Basic Math")
    deck.cards = cards

    return deck


def create_cards_list():
    """ Create a simple list of cards for test purposes. """

    cards = [
        StudyCard("2 + 2 = ?", "4"),
        StudyCard("2 + 3 = ?", "5"),
        StudyCard("2 + 4 = ?", "6"),
        StudyCard("2 + 5 = ?", "7"),
    ]

    return cards
