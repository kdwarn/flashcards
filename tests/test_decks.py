import getpass
from pathlib import Path

import pytest

from flashcards import decks


def test_get_name(math_deck):
    assert math_deck.name == "Basic Math"


def test_get_description(math_deck):
    assert math_deck.description == "For learning basic arithmetic."


def test_create_redundant_file_raises_error(math_deck):
    with pytest.raises(IOError):
        math_deck.create_file()


def test_len_deck(math_deck):
    assert len(math_deck.cards) == 4


def test_add_card_success(math_deck):
    math_deck.cards.append({"question": "5x5", "answer": "25"})
    assert len(math_deck.cards) == 5


def test_to_dict():
    deck = decks.Deck("misc", "A misc deck")
    card = {"question": "What is my name?", "answer": "Kris"}
    deck.cards.append(card)

    data = deck.to_dict()
    expected = {"name": "misc", "description": "A misc deck"}

    expected["cards"] = [card]
    assert expected == data


def test_storage_path():
    assert decks.storage_path() == Path(f"/home/{getpass.getuser()}/.flashcards")


def test_create_storage_path_raises_error_if_exists():
    pass


def test_generate_deck_filepath():
    path = decks.generate_deck_filepath("French")
    assert path == Path(f"/home/{getpass.getuser()}/.flashcards/French.json")


def test_selected_deck_path():
    path = decks.selected_deck_path()
    assert path == Path(f"/home/{getpass.getuser()}/.flashcards/.SELECTEDDECK")


def test_temp_storage_path(storage_path):
    """Fixture should overwrite location set in decks.storage_path()."""
    storage_path = decks.storage_path()
    assert isinstance(storage_path, Path)
    assert str(storage_path.resolve()).startswith("/tmp")  # TODO: more OS-agnostic way for this?
    assert storage_path.name == decks.STORAGE_DIR_NAME


def test_temp_create_storage_directory(create_storage_directory, storage_path):
    """Fixture should create tmp directory."""
    decks.create_storage_directory()
    storage_path = decks.storage_path()
    assert storage_path.exists()


@pytest.mark.parametrize(
    "input, expected",
    [
        ("!f@i#l$e%-^n&a*m(e)0", "file_name0.json"),
        ("file-name", "file_name.json"),
        ("file name", "file_name.json"),
    ],
)
def test_generate_filename_alphanum(input, expected):
    result = decks.generate_filename(input)
    assert expected == result


def test_loading_non_existant_deck_raises_error():
    with pytest.raises(FileNotFoundError):
        decks.load_deck(Path("/home/usr/.flashcards/set01.json"))


def test_load_deck_success(math_deck_filepath):
    math_deck = decks.load_deck(math_deck_filepath)
    assert isinstance(math_deck, decks.Deck)


@pytest.mark.parametrize(
    "path",
    [
        (Path("tests/corrupted_decks/1.json")),
        (Path("tests/corrupted_decks/2.json")),
        (Path("tests/corrupted_decks/3.json")),
    ],
)
def test_corrupted_deck_raises_error1(path):
    with pytest.raises(KeyError):
        decks.load_deck(path)


def test_corrupted_deck_raises_error2():
    with pytest.raises(ValueError):
        decks.load_deck(Path("tests/corrupted_decks/4.json"))
