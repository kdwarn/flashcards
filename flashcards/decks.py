"""
flashcards.decks
~~~~~~~~~~~~~~~~~~~

Contain the Deck object and logic related to it.
"""
from collections import OrderedDict

from flashcards import cards
from flashcards.cards import StudyCard


def create_from_dict(data):
    """
    Construct a Deck Object from a dictionary object.

    :param data: the dictionary object

    :raises KeyError: when dictionary is missing a needed field to create obj
    :raises ValueError: if cards field in data is not of type list

    :returns: Deck object
    """

    if "name" not in data:
        raise KeyError("Invalid data string. 'name' key is missing")
    if "description" not in data:
        raise KeyError("Invalid data string. 'description' key is missing")
    if "cards" not in data:
        raise KeyError("Invalid data string. 'cards' key is missing")
    if not isinstance(data["cards"], list):
        raise ValueError("Invalid data type. 'cards' value should be a list")

    deck = Deck(data["name"], data["description"])

    for card in [cards.create_from_dict(card) for card in data["cards"]]:
        deck.add(card)

    return deck


class Deck:
    """A Deck is a container of flash cards."""

    def __init__(self, name, description=None):
        """
        Creates a Deck.

        :param name: The name of the deck.
        :param description: The description for this deck.
        """
        self.name = name
        self.description = "" if description is None else description
        self.cards = []

    def __iter__(self):
        """Iter through the cards of this deck."""
        return iter(self.cards)

    def __len__(self):
        """Return the number of cards in this Deck."""
        return len(self.cards)

    def add(self, card):
        """
        Add a card to the end of this deck.

        :param card: A subclass of flashcards.cards.StudyCard object.
        """
        if isinstance(card, StudyCard):
            self.cards.append(card)
        else:
            raise TypeError("A Deck can only contain instances of StudyCard objects.")

    def to_dict(self):
        """
        Get a dictionary object representing this Deck.

        :returns: a dictionary object representation of this Deck.
        """
        serialized_cards = [c.to_dict() for c in self]

        data = (
            ("name", self.name),
            ("description", self.description),
            ("cards", serialized_cards),
        )

        return OrderedDict(data)
