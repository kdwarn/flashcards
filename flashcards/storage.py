"""
flashcards.storage
~~~~~~~~~~~~~~~~~~~

Contain the logic to load and save items in the Flashcards
storage directory on this machine.
"""
import errno
import json
import os

from flashcards import decks

STORAGE_DIR_NAME = ".flashcards"
DECK_EXTENSION = ".json"
SELECTED_DECK_NAME = ".SELECTEDDECK"


class DeckStorage:
    """
    Utility object to save and load serialized JSON objects stored in a file.
    """

    def __init__(self, filepath):
        self._filepath = filepath

    def load(self):
        """
        Load and serialize the data in this file.

        :returns: a Deck object
        """
        assert_valid_file(self._filepath)

        content = None
        with open(self._filepath, "r") as file:
            content = file.read()

        content = json.loads(content)
        return decks.create_from_dict(content)

    def save(self, deck):
        """
        Serialize and save the content in this file.

        :param content: the content to save
        """

        content = deck.to_dict()

        content = json.dumps(content, sort_keys=False, indent=4, separators=(",", ": "))

        assert_valid_file(self._filepath)

        with open(self._filepath, "w") as file:
            file.write(content)

        # rename the name of this file by the name of this deck.
        filename = generate_filename_from_str(deck.name)
        self._rename_filename(filename)

    def _rename_filename(self, filename):
        """
        Without changing the path and the extension, rename the
        base name of the file.

        :param filename: the new name for this file.
        """
        directory = os.path.dirname(self._filepath)  # keep the same path
        extension = os.path.splitext(self._filepath)[1]  # keep the extension

        # Concatenate the new path for the file, rename the file and update the
        # _filepath variable.
        new_path = os.path.join(directory, filename + extension)
        os.rename(self._filepath, new_path)
        self._filepath = new_path


def create_deck_file(deck):
    """
    Create a file and store the supplied deck in it.

    :param deck: the dick to store.
    """
    filepath = _generate_deck_filepath(deck)

    if os.path.isfile(filepath) or os.path.exists(filepath):
        raise IOError("A file already exist, cannot create deck.")

    # Create the file
    open(filepath, "a").close()

    # Store the deck in the file
    store_deck(deck)
    return filepath


def store_deck(deck):
    """
    Store the supplied deck in the storage folder.

    An exception is raised if the file does not exist.

    :param deck: the deck to store.
    """
    filepath = _generate_deck_filepath(deck)

    storage_item = DeckStorage(filepath)
    storage_item.save(deck)


def load_deck(filepath):
    """
    Attempt to load the deck from a storage item.

    :param filepath: the filepath of the deck file

    :returns: DeckStorage object
    """
    assert_valid_file(filepath)
    return DeckStorage(filepath)


def link_selected_deck(filepath):
    """
    Create a symbolic link to the selected deck.

    :param filepath: the filepath of the deck
    """
    linkpath = selected_deck_path()

    # Force symlink
    try:
        os.symlink(filepath, linkpath)

    except OSError as e:
        if e.errno == errno.EEXIST:
            os.remove(linkpath)
            os.symlink(filepath, linkpath)


def load_selected_deck():
    """
    Load and return the currently selected deck.

    :returns: Deck object.
    """
    item = DeckStorage(selected_deck_path())
    return item.load()


def storage_path():
    """ Get the absolute storage path on the machine """
    return os.path.join(os.path.expanduser("~"), STORAGE_DIR_NAME)


def selected_deck_path():
    """Get the absolute path for the currently selected deck on the machine."""
    return os.path.join(storage_path(), SELECTED_DECK_NAME)


def _generate_deck_filepath(deck):
    """
    Generate the absolute filepath in which the given deck should be stored

    :param deck: the deck to store.

    :returns: absolute file path to the storage file.
    """
    filename = generate_filename_from_str(deck.name)
    filename = filename + DECK_EXTENSION
    return os.path.join(storage_path(), filename)


def verify_storage_dir_integrity():
    """ Check that the storage directory is intact. """

    path = storage_path()
    if not os.path.exists(path) or os.path.isfile(path):
        os.mkdir(storage_path())


def generate_filename_from_str(string):
    """
    Generate a valid filename from a given string.

    - replace all spaces and dashes with underscore.
    - only keeps alphanumerical chars

    :param string: the string to create the filename from

    :returns: the generated string, a valid filename
    """
    keepchars = [" ", "-", "_"]  # characters to keep in the filename
    swapchars = {" ": "_", "-": "_"}  # keys are swapped by their values

    for key, value in swapchars.items():
        string = string.replace(key, value)

    _ = [c for c in string if c.isalnum() or c == " " or c in keepchars]
    return "".join(_).rstrip()


def assert_valid_file(filepath):
    """
    Raise an exception if the file at the given path is not a file or
    does not exists.
    """
    if not os.path.isfile(filepath):
        raise IOError("path: %s is not a file" % filepath)
    if not os.path.exists(filepath):
        raise IOError("path: %s does not exists" % filepath)
