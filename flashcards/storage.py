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

        content = deck.to_dict()
        content = json.dumps(content, sort_keys=False, indent=4, separators=(",", ": "))
        assert_valid_file(self.filepath)

        with open(self.filepath, "w") as file:
            file.write(content)

        # rename the name of this file by the name of this deck.
        filename = generate_filename_from_str(deck.name)
        directory = os.path.dirname(self.filepath)  # keep the same path
        extension = os.path.splitext(self.filepath)[1]  # keep the extension

        # Concatenate the new path for the file, rename the file and update the
        # filepath variable.
        new_path = os.path.join(directory, filename + extension)
        os.rename(self.filepath, new_path)
        self.filepath = new_path


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


def link_selected_deck(filepath):
    """Create a symbolic link to the selected deck."""
    linkpath = selected_deck_path()

    try:
        os.symlink(filepath, linkpath)
    except OSError as e:
        if e.errno == errno.EEXIST:
            os.remove(linkpath)
            os.symlink(filepath, linkpath)


def load_selected_deck():
    """Load and return the currently selected deck."""
    item = DeckStorage(selected_deck_path())
    return item.load()


def storage_path():
    """Get the absolute storage path on the machine."""
    return os.path.join(os.path.expanduser("~"), STORAGE_DIR_NAME)


def selected_deck_path():
    """Get the absolute path for the currently selected deck on the machine."""
    return os.path.join(storage_path(), SELECTED_DECK_NAME)


def generate_deck_filepath(deck):
    """Generate the absolute filepath in which the given deck should be stored."""
    filename = generate_filename_from_str(deck.name)
    filename = filename + DECK_EXTENSION
    return os.path.join(storage_path(), filename)


def verify_storage_dir_integrity():
    """Check that the storage directory is intact."""

    path = storage_path()
    if not os.path.exists(path) or os.path.isfile(path):
        os.mkdir(storage_path())


def generate_filename_from_str(string):
    """Generate a valid filename from a given string."""
    keepchars = [" ", "-", "_"]  # characters to keep in the filename
    swapchars = {" ": "_", "-": "_"}  # keys are swapped by their values

    for key, value in swapchars.items():
        string = string.replace(key, value)

    _ = [c for c in string if c.isalnum() or c == " " or c in keepchars]
    return "".join(_).rstrip()


def assert_valid_file(filepath):
    """Raise an exception if the file at the given path is not a file or does not exists."""
    if not os.path.isfile(filepath):
        raise IOError("path: %s is not a file" % filepath)
    if not os.path.exists(filepath):
        raise IOError("path: %s does not exists" % filepath)
