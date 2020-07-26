"""
flashcards.decks
~~~~~~~~~~~~~~~~~~~

Contain the Deck object and logic related to it.
"""
from collections import OrderedDict

from flashcards import cards
from flashcards.cards import StudyCard

NAME_KEY = "name"
DESC_KEY = "description"
CARDS_KEY = "cards"


def create_from_dict(data):
    """
    Construct a Deck Object from a dictionary object.

    :param data: the dictionary object

    :raises KeyError: when dictionary is missing a needed field to create obj
    :raises ValueError: if cards field in data is not of type list

    :returns: Deck object
    """
    _assert_data_is_valid(data)

    name = data[NAME_KEY]
    description = data[DESC_KEY]
    study_cards = [cards.create_from_dict(card) for card in data[CARDS_KEY]]

    deck = Deck(name, description)

    for card in study_cards:
        deck.add(card)

    return deck


def _assert_data_is_valid(data):
    """ Check that data received in `create_from_dict` has a valid format """

    if NAME_KEY not in data:
        raise KeyError("Invalid data string. %s key is missing" % NAME_KEY)
    if DESC_KEY not in data:
        raise KeyError("Invalid data string. %s key is missing" % DESC_KEY)
    if CARDS_KEY not in data:
        raise KeyError("Invalid data string. %s key is missing" % CARDS_KEY)
    if not isinstance(data[CARDS_KEY], list):
        raise ValueError("Invalid data type. %s value's should be a list" % CARDS_KEY)


class Deck:
    """A Deck is a container of flash cards."""

    def __init__(self, name, description=None):
        """
        Creates a Deck.

        :param name: The name of the deck.
        :param description: The description for this deck.
        """
        self._name = name
        self._description = "" if description is None else description
        self._cards = []

    def __iter__(self):
        """Iter through the cards of this deck."""
        return iter(self._cards)

    def __len__(self):
        """Return the number of cards in this Deck."""
        return len(self._cards)

    @property
    def name(self):
        """
        Get the name of this deck.

        :returns: The name of this Deck.
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        Set the name of this deck.

        :param value: The new name for this deck
        """
        if isinstance(value, str):
            self._name = value
        else:
            raise TypeError("Deck name should be of type str")

    @property
    def description(self):
        """
        Get the description of this deck.
        """
        return self._description

    @description.setter
    def description(self, value):
        """
        Set the description of this deck.

        :param value: The new description for this deck
        """
        if isinstance(value, str):
            self._description = value
        else:
            raise TypeError("Deck description should be of type str")

    def add(self, card):
        """
        Add a card to the end of this deck.

        :param card: A subclass of flashcards.cards.StudyCard object.
        """
        if isinstance(card, StudyCard):
            self._cards.append(card)
        else:
            raise TypeError("A Deck can only contain instances of StudyCard objects.")

    def to_dict(self):
        """
        Get a dictionary object representing this Deck.

        :returns: a dictionary object representation of this Deck.
        """
        serialized_cards = [c.to_dict() for c in self]

        data = (
            (NAME_KEY, self.name),
            (DESC_KEY, self.description),
            (CARDS_KEY, serialized_cards),
        )

        return OrderedDict(data)
