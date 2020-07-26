"""
flashcards.storage
~~~~~~~~~~~~~~~~~~~

Contain the logic to load and save items in the Flashcards
storage directory on this machine.
"""
import os
import errno

from flashcards.utils import storage as storageUtils
from flashcards import decks

# The directory name where all of the Flashcards data is stored on the machine.
STORAGE_DIR_NAME = ".flashcards"


# The directory name where all of the Flashcards's deck data is stored on the machine.
DECK_STORAGE_DIR = "decks"


# Default extension of a deck file on the machine
DECK_EXTENSION = ".json"


# Selected deck filename
SELECTED_DECK_NAME = ".SELECTEDDECK"


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
    Store the supplied deck the storage folder.

    An exception is raised if the file does not exists.

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
    storageUtils.assert_valid_file(filepath)
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


class DeckStorage(storageUtils.JSONFileStorage):
    """
    Utility object to load and save a Deck object from a
    file on the machine.
    """

    def load(self):
        """
        Load and return the Deck contain in this file.

        :returns: a Deck object
        """
        content = super(DeckStorage, self).load()
        return decks.create_from_dict(content)

    def save(self, deck):
        """ Save the provided Deck object in the current file. """
        data = deck.to_dict()
        super(DeckStorage, self).save(data)

        # rename the name of this file by the name of this deck.
        filename = generate_filename_from_str(deck.name)
        self._rename_filename(filename)


def storage_path():
    """ Get the absolute storage path on the machine """
    return os.path.join(os.path.expanduser("~"), STORAGE_DIR_NAME)


def deck_storage_path():
    """Get the absolute storage path for the decks on the machine."""
    return os.path.join(os.path.expanduser("~"), STORAGE_DIR_NAME, DECK_STORAGE_DIR)


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
    return os.path.join(deck_storage_path(), filename)


def verify_storage_dir_integrity():
    """ Check that the storage directory is intact. """

    path = storage_path()
    if not os.path.exists(path) or os.path.isfile(path):
        _create_storage_dir()

    path = deck_storage_path()
    if not os.path.exists(path) or os.path.isfile(path):
        _create_deck_storage_dir()


def _create_storage_dir():
    """ Create the storage directory in the home folder. """
    if os.path.exists(storage_path()) and os.path.isdir(storage_path()):
        raise IOError("Storage directory already exists.")

    os.mkdir(storage_path())


def _create_deck_storage_dir():
    """ Create the deck storage directory in the storage directory. """
    path = deck_storage_path()
    if os.path.exists(path) and os.path.isdir(path):
        raise IOError("Deck storage directory already exists.")

    os.mkdir(path)


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
