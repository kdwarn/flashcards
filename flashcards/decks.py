"""
flashcards.decks
~~~~~~~~~~~~~~~~~~~

Contain the Deck object and logic related to it.
"""
from collections import OrderedDict
import errno
import json
import os
from pathlib import Path
from typing import Dict

import click

from flashcards import cards
from flashcards import decks


STORAGE_DIR_NAME = ".flashcards"
DECK_EXTENSION = ".json"
SELECTED_DECK_NAME = ".SELECTEDDECK"


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
        self.filepath = generate_deck_filepath(name)

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
        if isinstance(card, cards.StudyCard):
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

    def create_file(self):
        """Create a file and store the supplied deck in it."""

        if os.path.isfile(self.filepath) or os.path.exists(self.filepath):
            raise IOError("A file already exists, cannot create deck.")

        # Create the file
        open(self.filepath, "a").close()

    def save(self):
        """Serialize and save the content in this file."""

        content = self.to_dict()
        content = json.dumps(content, sort_keys=False, indent=4, separators=(",", ": "))

        with open(self.filepath, "w") as file:
            file.write(content)


def load_deck(filepath: Path) -> Deck:
    """
    Construct a Deck Object from a dictionary object.
    Load and serialize the data in this file."""
    with open(filepath, "r") as file:
        content = file.read()

    content = json.loads(content)

    if "name" not in content:
        raise KeyError("Invalid data string. 'name' key is missing")
    if "description" not in content:
        raise KeyError("Invalid data string. 'description' key is missing")
    if "cards" not in content:
        raise KeyError("Invalid data string. 'cards' key is missing")
    if not isinstance(content["cards"], list):
        raise ValueError("Invalid data type. 'cards' value should be a list")

    deck = Deck(content["name"], content["description"])

    for card in [cards.create_from_dict(card) for card in content["cards"]]:
        deck.add(card)

    return deck


def storage_path() -> Path:
    """Get the absolute storage path on the machine."""
    return Path.home() / STORAGE_DIR_NAME


def create_storage_directory():
    """Create storage directory if it doesn't exist."""
    path = storage_path()
    if not os.path.exists(path):
        os.mkdir(path)


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
