import os
from pathlib import Path

import pytest

from flashcards import decks


@pytest.fixture
def storage_path(tmp_path, monkeypatch):
    """Monkeypatch decks.storage.path() so that we use a tmp directory."""

    def mockreturn():
        return Path(tmp_path, decks.STORAGE_DIR_NAME)

    monkeypatch.setattr(decks, "storage_path", mockreturn)

    return decks.storage_path()


@pytest.fixture
def create_storage_directory(storage_path, monkeypatch):
    """Monkeypatch create_storage_path, so we create the dir as named in fixture storage_path."""

    def mockreturn():
        if not os.path.exists(storage_path):
            storage_path.mkdir()

    monkeypatch.setattr(decks, "create_storage_directory", mockreturn)

    return decks.create_storage_directory()


@pytest.fixture
def math_deck(create_storage_directory):
    deck = decks.Deck("Basic Math")
    deck.description = "For learning basic arithmetic."
    deck.cards = [
        {"question": "2 + 2 = ?", "answer": "4"},
        {"question": "2 + 3 = ?", "answer": "5"},
        {"question": "2 + 4 = ?", "answer": "6"},
        {"question": "2 + 5 = ?", "answer": "7"},
    ]

    deck.create_file()
    deck.save()
    return deck


@pytest.fixture
def math_deck_filepath(math_deck):
    return math_deck.filepath
