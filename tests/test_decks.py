import getpass
from pathlib import Path

import pytest

from flashcards import decks
from flashcards.cards import StudyCard


deck = decks.Deck("French", "Studying French")
math_deck = decks.Deck("Math", "A study set about maths")


def test_create_from_dict():
    card = StudyCard("2+2=?", "4")

    data = {"name": "Math", "description": "Math-145"}
    data["cards"] = [card.to_dict()]

    study_set = decks.create_from_dict(data)

    assert study_set.name == "Math"
    assert study_set.description == "Math-145"
    assert study_set.cards[0].question == "2+2=?"
    assert study_set.cards[0].answer == "4"


def test_StudySet_exists():
    assert decks.Deck("Math 145") is not None


def test_get_name():
    assert math_deck.name == "Math"


def test_get_description():
    assert math_deck.description == "A study set about maths"


def test_set_name():
    math_deck.name = "Math1"
    assert math_deck.name == "Math1"


def test_set_description():
    math_deck.description = "A study set about math"
    assert math_deck.description == "A study set about math"


def test_add():
    card = StudyCard("What is my name?", "Jonathan")
    math_deck.add(card)
    assert len(math_deck.cards) == 1
    assert card in math_deck.cards


def test_set_add_wrong_type():
    card = "A string is not a card!"
    with pytest.raises(TypeError):
        math_deck.add(card)


def test_len_deck():

    card0 = StudyCard("What is my name?", "Jonathan")
    card1 = StudyCard("What is bird's name ?", "Gandalf")
    card2 = StudyCard("What is the meaning of life ?", "42")
    deck = decks.Deck("another deck")
    deck.add(card0)
    deck.add(card1)
    deck.add(card2)

    assert len(deck) == 3


def test_to_dict():
    deck = decks.Deck("misc", "A misc deck")
    card = StudyCard("What is my name?", "Jonathan")
    deck.add(card)

    data = deck.to_dict()
    expected = {"name": "misc", "description": "A misc deck"}

    # List of serialized cards in this set
    cards = [c.to_dict() for c in deck]
    expected["cards"] = cards
    assert expected == data


def test_storage_path():
    assert decks.storage_path() == Path(f"/home/{getpass.getuser()}/.flashcards")


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


def test_check_file_exists():
    # TODO: use this to see if check_valid_file() is even necessary - I think an exception should
    # even without it if filepath does not exist
    filepath = Path("testing/kris.json")
    deck = decks.DeckStorage(filepath)
    print(deck.filepath)
    assert isinstance(deck, decks.DeckStorage)
    assert 0


@pytest.mark.parametrize(
    "input, expected",
    [
        ("!f@i#l$e%-^n&a*m(e)0", "file_name0"),
        ("file-name", "file_name"),
        ("file name", "file_name"),
    ],
)
def test_generate_filename_from_str_alphanum(input, expected):
    result = decks.generate_filename_from_str(input)
    assert expected == result


def test_loading_non_existant_deck_raises_error():

    no_deck = decks.DeckStorage("/home/usr/.flashcards/set01.json")

    with pytest.raises(IOError):
        no_deck.load()
