"""
TODO:
    next: test creating files, accessing files, all the functions where storage.storage_path() is used
"""
import getpass
from pathlib import Path

import pytest

from flashcards import storage
from flashcards.storage import DeckStorage
from flashcards.decks import Deck
from flashcards.cards import StudyCard


deck = Deck("French", "Studying French")


def test_storage_path():
    assert storage.storage_path() == Path(f"/home/{getpass.getuser()}/.flashcards")


def test_generate_deck_filepath():
    path = storage.generate_deck_filepath("French")
    assert path == Path(f"/home/{getpass.getuser()}/.flashcards/French.json")


def test_selected_deck_path():
    path = storage.selected_deck_path()
    assert path == Path(f"/home/{getpass.getuser()}/.flashcards/.SELECTEDDECK")


def test_temp_storage_path(storage_path):
    """Fixture should overwrite location set in storage.storage_path()."""
    storage_path = storage.storage_path()
    assert isinstance(storage_path, Path)
    assert str(storage_path.resolve()).startswith("/tmp")  # TODO: more OS-agnostic way for this?
    assert storage_path.name == storage.STORAGE_DIR_NAME


def test_temp_create_storage_directory(create_storage_directory, storage_path):
    """Fixture should create tmp directory."""
    storage.create_storage_directory()
    storage_path = storage.storage_path()
    assert storage_path.exists()


@pytest.mark.parametrize(
    "input, expected",
    [
        ("!f@i#l$e%-^n&a*m(e)0", "file_name0"),
        ("file-name", "file_name"),
        ("file name", "file_name"),
    ],
)
def test_generate_filename_from_str_alphanum(input, expected):
    result = storage.generate_filename_from_str(input)
    assert expected == result


def test_loading_non_existant_deck_raises_error():

    no_deck = DeckStorage("/home/usr/.flashcards/set01.json")

    with pytest.raises(IOError):
        no_deck.load()
