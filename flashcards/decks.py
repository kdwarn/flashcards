"""
flashcards.decks
~~~~~~~~~~~~~~~~~~~

Contain the Deck object and logic related to it.
"""
from collections import OrderedDict
import errno
from typing import Dict
import json
import os
from pathlib import Path

import click

from flashcards import cards
from flashcards import decks
from flashcards.cards import StudyCard


STORAGE_DIR_NAME = ".flashcards"
DECK_EXTENSION = ".json"
SELECTED_DECK_NAME = ".SELECTEDDECK"


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


class DeckStorage:
    """Utility object to save and load serialized JSON objects stored in a file."""

    def __init__(self, filepath):
        self.filepath = filepath

    def load(self) -> decks.Deck:
        """Load and serialize the data in this file."""
        check_valid_file(self.filepath)

        with open(self.filepath, "r") as file:
            content = file.read()

        content = json.loads(content)
        return decks.create_from_dict(content)

    def save(self, deck: decks.Deck):
        """Serialize and save the content in this file."""
        check_valid_file(self.filepath)

        content = deck.to_dict()
        content = json.dumps(content, sort_keys=False, indent=4, separators=(",", ": "))

        with open(self.filepath, "w") as file:
            file.write(content)


def storage_path() -> Path:
    """Get the absolute storage path on the machine."""
    return Path.home() / STORAGE_DIR_NAME


def create_storage_directory():
    """Create storage directory if it doesn't exist."""
    path = storage_path()
    if not os.path.exists(path):
        os.mkdir(path)


def check_valid_file(filepath: Path):
    """Raise an exception if the file at the given path is not a file or does not exist."""
    if not os.path.isfile(filepath):
        raise IOError(f"Path: {filepath} is not a file.")


def generate_filename_from_str(string: str) -> str:
    """Generate a valid filename from a given string."""
    keepchars = [" ", "-", "_"]  # characters to keep in the filename
    swapchars = {" ": "_", "-": "_"}  # keys are swapped by their values

    for key, value in swapchars.items():
        string = string.replace(key, value)

    _ = [c for c in string if c.isalnum() or c == " " or c in keepchars]
    return "".join(_).rstrip()


def generate_deck_filepath(deck_name: str) -> Path:
    """Generate the absolute filepath in which the given deck should be stored."""
    filename = generate_filename_from_str(deck_name)
    filename = filename + DECK_EXTENSION
    return storage_path() / filename


def selected_deck_path() -> Path:
    """Get the absolute path for the currently selected deck on the machine."""
    return storage_path() / SELECTED_DECK_NAME


def link_selected_deck(filepath: Path):
    """Create a symbolic link to the selected deck."""
    linkpath = selected_deck_path()

    try:
        os.symlink(filepath, linkpath)
    except OSError as e:
        if e.errno == errno.EEXIST:
            os.remove(linkpath)
            os.symlink(filepath, linkpath)


def create_deck_file(deck: decks.Deck) -> Path:
    """Create a file and store the supplied deck in it."""
    filepath = generate_deck_filepath(deck.name)

    if os.path.isfile(filepath) or os.path.exists(filepath):
        raise IOError("A file already exists, cannot create deck.")

    # Create the file
    open(filepath, "a").close()

    store_deck(deck)
    return filepath


def store_deck(deck: decks.Deck):
    """Store the supplied deck in the storage folder."""
    filepath = generate_deck_filepath(deck.name)
    storage_item = DeckStorage(filepath)
    storage_item.save(deck)
