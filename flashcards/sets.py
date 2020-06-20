"""
flashcards.sets
~~~~~~~~~~~~~~~~~~~

Contain the Deck object and logic related to it.
"""
from collections import OrderedDict

from flashcards import cards
from flashcards.cards import StudyCard

TITLE_KEY = "title"
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

    title = data[TITLE_KEY]
    description = data[DESC_KEY]
    study_cards = [cards.create_from_dict(card) for card in data[CARDS_KEY]]

    deck = Deck(title, description)

    for card in study_cards:
        deck.add(card)

    return deck


def _assert_data_is_valid(data):
    """ Check that data received in `create_from_dict` has a valid format """

    if TITLE_KEY not in data:
        raise KeyError("Invalid data string. %s key is missing" % TITLE_KEY)
    if DESC_KEY not in data:
        raise KeyError("Invalid data string. %s key is missing" % DESC_KEY)
    if CARDS_KEY not in data:
        raise KeyError("Invalid data string. %s key is missing" % CARDS_KEY)
    if not isinstance(data[CARDS_KEY], list):
        raise ValueError("Invalid data type. %s value's should be a list" % CARDS_KEY)


class Deck(object):
    """
    A Deck is a container of flash cards.
    """

    def __init__(self, title, description=None):
        """
        Creates a Deck.

        :param title: The title of the deck.
        :param description: The description for this deck.
        """
        self._title = title
        self._description = "" if description is None else description
        self._cards = []

    def __iter__(self):
        """Iter through the cards of this set."""
        return iter(self._cards)

    def __len__(self):
        """Return the number of cards in this Deck."""
        return len(self._cards)

    @property
    def title(self):
        """
        Get the title of this set.

        :returns: The title of this Deck.
        """
        return self._title

    @title.setter
    def title(self, value):
        """
        Set the title of this set.

        :param value: The new title for this set
        """
        if isinstance(value, basestring):
            self._title = value
        else:
            raise TypeError("Deck title should be of type str")

    @property
    def description(self):
        """
        Get the description of this set.
        """
        return self._description

    @description.setter
    def description(self, value):
        """
        Set the description of this set.

        :param value: The new description for this set
        """
        if isinstance(value, basestring):
            self._description = value
        else:
            raise TypeError("Deck description should be of type str")

    def add(self, card):
        """
        Add a card to the end of this set.

        :param card: A subclass of flashcards.cards.StudyCard object.
        """
        if isinstance(card, StudyCard):
            self._cards.append(card)
        else:
            raise TypeError("A Set can only contain instances of StudyCard objects.")

    def to_dict(self):
        """
        Get a dictionary object representing this Deck.

        :returns: a dictionary object representation of this Deck.
        """
        serialized_cards = [c.to_dict() for c in self]

        data = (
            (TITLE_KEY, self.title),
            (DESC_KEY, self.description),
            (CARDS_KEY, serialized_cards),
        )

        return OrderedDict(data)
