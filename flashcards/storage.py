"""Contain the logic to load and save items in the Flashcards storage directory."""
import errno
import json
import os

from flashcards import decks

STORAGE_DIR_NAME = ".flashcards"
DECK_EXTENSION = ".json"
SELECTED_DECK_NAME = ".SELECTEDDECK"


class DeckStorage:
    """Utility object to save and load serialized JSON objects stored in a file."""

    def __init__(self, filepath):
        self.filepath = filepath

    def load(self):
        """Load and serialize the data in this file."""
        assert_valid_file(self.filepath)

        with open(self.filepath, "r") as file:
            content = file.read()

        content = json.loads(content)
        return decks.create_from_dict(content)

    def save(self, deck):
        """Serialize and save the content in this file."""
        assert_valid_file(self.filepath)

        content = deck.to_dict()
        content = json.dumps(content, sort_keys=False, indent=4, separators=(",", ": "))

        with open(self.filepath, "w") as file:
            file.write(content)


def storage_path():
    """Get the absolute storage path on the machine."""
    return os.path.join(os.path.expanduser("~"), STORAGE_DIR_NAME)


def create_storage_directory():
    """Create storage directory if it doesn't exist."""
    path = storage_path()
    if not os.path.exists(path):
        os.mkdir(path)


def assert_valid_file(filepath):
    """Raise an exception if the file at the given path is not a file or does not exists."""
    if not os.path.isfile(filepath):
        raise IOError("path: %s is not a file" % filepath)
    if not os.path.exists(filepath):
        raise IOError("path: %s does not exists" % filepath)


def generate_filename_from_str(string):
    """Generate a valid filename from a given string."""
    keepchars = [" ", "-", "_"]  # characters to keep in the filename
    swapchars = {" ": "_", "-": "_"}  # keys are swapped by their values

    for key, value in swapchars.items():
        string = string.replace(key, value)

    _ = [c for c in string if c.isalnum() or c == " " or c in keepchars]
    return "".join(_).rstrip()


def generate_deck_filepath(deck_name):
    """Generate the absolute filepath in which the given deck should be stored."""
    filename = generate_filename_from_str(deck_name)
    filename = filename + DECK_EXTENSION
    return os.path.join(storage_path(), filename)


def selected_deck_path():
    """Get the absolute path for the currently selected deck on the machine."""
    return os.path.join(storage_path(), SELECTED_DECK_NAME)


def link_selected_deck(filepath):
    """Create a symbolic link to the selected deck."""
    linkpath = selected_deck_path()

    try:
        os.symlink(filepath, linkpath)
    except OSError as e:
        if e.errno == errno.EEXIST:
            os.remove(linkpath)
            os.symlink(filepath, linkpath)


def create_deck_file(deck):
    """Create a file and store the supplied deck in it."""
    filepath = generate_deck_filepath(deck)

    if os.path.isfile(filepath) or os.path.exists(filepath):
        raise IOError("A file already exists, cannot create deck.")

    # Create the file
    open(filepath, "a").close()

    store_deck(deck)
    return filepath


def store_deck(deck):
    """Store the supplied deck in the storage folder."""
    filepath = generate_deck_filepath(deck)
    storage_item = DeckStorage(filepath)
    storage_item.save(deck)


def load_deck(filepath):
    """Attempt to load the deck from a storage item."""
    assert_valid_file(filepath)
    return DeckStorage(filepath)


def load_selected_deck():
    """Load and return the currently selected deck."""
    item = DeckStorage(selected_deck_path())
    return item.load()
