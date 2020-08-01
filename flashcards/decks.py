"""Load and save decks; add cards to decks."""
from collections import OrderedDict
import errno
import json
import os
from pathlib import Path

import click

from flashcards import cards
from flashcards import decks


STORAGE_DIR_NAME = ".flashcards"
DECK_EXTENSION = ".json"
SELECTED_DECK_NAME = ".SELECTEDDECK"


class Deck:
    """A Deck is a container of flash cards."""

    def __init__(self, name, description=None):
        """Creates a Deck."""
        self.name = name
        self.description = "" if description is None else description
        self.cards = []
        self.filepath = generate_deck_filepath(name)

    def __str__(self):
        return self.name

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
        """Get a dictionary object representing this Deck."""
        serialized_cards = [c.to_dict() for c in self.cards]

        data = (
            ("name", self.name),
            ("description", self.description),
            ("cards", serialized_cards),
        )

        return OrderedDict(data)

    def create_file(self):
        """Create a file for the deck."""

        if self.filepath.exists():
            raise IOError()

        open(self.filepath, "w+").close()

    def save(self):
        """Serialize and save the deck to its file."""

        with open(self.filepath, "w") as file:
            json.dump(self.to_dict(), file)


def load_deck(filepath: Path) -> Deck:
    """Load a json file and create a Deck from it."""
    with open(filepath, "r") as file:
        content = json.load(file)

    if "name" not in content:
        raise KeyError("The deck file is corrupted - deck 'name' key is missing.")
    if "description" not in content:
        raise KeyError("The deck file is corrupted - deck 'description' key is missing.")
    if "cards" not in content:
        raise KeyError("The deck file is corrupted - deck 'cards' key is missing.")
    if not isinstance(content["cards"], list):
        raise ValueError("The deck file is corrupted - 'cards' value should be a list.")

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
    if not path.exists():
        path.mkdir()


def generate_filename(string: str) -> str:
    """Generate a valid filename from a given string."""
    swapchars = {" ": "_", "-": "_"}  # keys are swapped by their values

    for key, value in swapchars.items():
        string = string.replace(key, value)

    _ = [c for c in string if c.isalnum() or c == "_"]
    filename = "".join(_)
    return filename + DECK_EXTENSION


def generate_deck_filepath(deck_name: str) -> Path:
    """Generate the absolute filepath in which the given deck should be stored."""
    filename = generate_filename(deck_name)
    return storage_path() / filename


def selected_deck_path() -> Path:
    """Get the absolute path for the currently selected deck on the machine."""
    return storage_path() / SELECTED_DECK_NAME


def link_selected_deck(filepath: Path):
    """Create a symbolic link to the selected Deck's filepath."""
    linkpath = selected_deck_path()

    try:
        os.symlink(filepath, linkpath)
    except OSError as e:
        if e.errno == errno.EEXIST:
            os.remove(linkpath)
            os.symlink(filepath, linkpath)
