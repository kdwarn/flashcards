"""
TODO:
    Test renaming a file
    assess what else needs to be done
"""
import getpass

import pytest

from flashcards import storage
from flashcards.utils import storage as storageUtils
from flashcards.storage import DeckStorage
from flashcards.decks import Deck
from flashcards.cards import StudyCard


deck = Deck("French", "Studying French")


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


def test_get_storage_path():
    assert storage.storage_path() == f"/home/{getpass.getuser()}/.flashcards"
