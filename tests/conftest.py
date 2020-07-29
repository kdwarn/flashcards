import os
from pathlib import Path

import pytest

from flashcards.cards import StudyCard
from flashcards.decks import Deck
from flashcards import storage


@pytest.fixture
def storage_path(tmp_path, monkeypatch):
    """Monkeypath storage.storage.path() so that we use a tmp directory."""

    def mockreturn():
        return Path(tmp_path, storage.STORAGE_DIR_NAME)

    monkeypatch.setattr(storage, "storage_path", mockreturn)

    return storage.storage_path()


@pytest.fixture
def create_storage_directory(storage_path, monkeypatch):
    """Monkey path create_storage_path, so we create the dir as named in fixture storage_path."""

    def mockreturn():
        if not os.path.exists(storage_path):
            storage_path.mkdir()

    monkeypatch.setattr(storage, "create_storage_directory", mockreturn)

    return storage.create_storage_directory()


@pytest.fixture
def math_deck():
    deck = Deck("Basic Math")
    deck.description = "For learning basic artithmetic."
    deck.cards = [
        StudyCard("2 + 2 = ?", "4"),
        StudyCard("2 + 3 = ?", "5"),
        StudyCard("2 + 4 = ?", "6"),
        StudyCard("2 + 5 = ?", "7"),
    ]
    print(storage.STORAGE_DIR_NAME)
    return deck


@pytest.fixture
def math_deck_file(math_deck):
    pass
