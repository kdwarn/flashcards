"""Load and save decks; add cards to decks."""
import errno
import json
import os
from pathlib import Path

import click

STORAGE_DIR_NAME = ".flashcards"
DECK_EXTENSION = ".json"
SELECTED_DECK_NAME = ".SELECTEDDECK"


class Deck:
    """A Deck is a container of flashcards."""

    def __init__(self, name, description=None):
        """Creates a Deck."""
        self.name = name
        self.description = "" if description is None else description
        self.cards = []
        self.filepath = generate_deck_filepath(name)

    def __str__(self):
        return self.name

    def to_dict(self):
        """Get a dictionary object representing this Deck."""

        return {
            "name": self.name,
            "description": self.description,
            "cards": self.cards,
        }

    def create_file(self):
        """Create a file for the deck."""

        if self.filepath.exists():
            raise IOError()

        open(self.filepath, "w+").close()

    def save(self):
        """Serialize and save the deck to its file."""

        with open(self.filepath, "w") as file:
            json.dump(self.to_dict(), file, indent=4)


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
    deck.cards = content["cards"]
    return deck


def storage_path() -> Path:
    """Get the absolute storage path on the machine."""
    return Path.home() / STORAGE_DIR_NAME


def create_storage_directory():
    """Create storage directory if it doesn't exist."""
    path = storage_path()
    if not path.exists():
        path.mkdir()


def name_starts_with_non_letter(name):
    """Helper function for check_deck_name(), to enable easier testing."""
    return not name[0].isalpha()


def file_would_be_duplicate(name):
    """Helper function for check_deck_name(), to enable easier testing."""
    return generate_deck_filepath(name).exists()


def check_and_standardize_deck_name(context, param, value):
    """Enforce contraints on the deck name."""
    while name_starts_with_non_letter(value):
        click.echo("Sorry, the name must start with a letter.")
        value = click.prompt("Name of the deck")

    while file_would_be_duplicate(value):
        click.echo("Sorry, a deck with that name already exists.")
        value = click.prompt("Name of the deck")

    return generate_stem(value)


def generate_stem(string: str) -> str:
    """Generate a valid filename from a given string."""

    string = string.replace(" ", "-")

    _ = [c for c in string if c.isalnum() or c in ["_", "-"]]
    stem = "".join(_)
    return stem.lower()


def generate_deck_filepath(deck_name: str) -> Path:
    """Generate the absolute filepath in which the given deck should be stored."""
    stem = generate_stem(deck_name) + DECK_EXTENSION
    return storage_path() / stem


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
