from pathlib import Path

from click.testing import CliRunner
import pytest

from flashcards.decks import link_selected_deck
from flashcards import main
from flashcards import decks

################
# Status command


def test_success_status(math_deck):
    runner = CliRunner()
    link_selected_deck(math_deck.filepath)
    result = runner.invoke(main.status_cmd)
    assert "Basic Math" in result.output
    assert "For learning basic arithmetic" in result.output
    assert "Number of cards: 4" in result.output


def test_success_no_deck(create_storage_directory):
    runner = CliRunner()
    result = runner.invoke(main.status_cmd)
    assert "No deck currently selected" in result.output


###############
# Study command


def test_success_study(math_deck):
    runner = CliRunner()
    result = runner.invoke(main.study_cmd, ["Basic Math"])
    assert "All done!" in result.output


def test_error_message_if_requested_deck_doesnt_exist():
    runner = CliRunner()
    result = runner.invoke(main.study_cmd, ["American"])
    assert "No deck by that name" in result.output


def test_error_message_if_no_deck_specified_and_no_selected_deck(create_storage_directory):
    runner = CliRunner()
    result = runner.invoke(main.study_cmd)
    assert "No deck currently selected" in result.output


def test_use_selected_deck_if_no_deck_specified(create_storage_directory, math_deck):
    link_selected_deck(math_deck.filepath)
    runner = CliRunner()
    result = runner.invoke(main.study_cmd)
    assert "2 + 2" in result.output
    assert "All done!" in result.output


def test_error_message_if_deck_has_no_cards(create_storage_directory, german_deck):
    runner = CliRunner()
    result = runner.invoke(main.study_cmd, ["German"])
    assert "has no cards" in result.output


################
# create command


def test_create_success_message_received(create_storage_directory):
    runner = CliRunner()
    result = runner.invoke(main.create, input="Italian\nStudy Italian")
    assert "Deck created" in result.output


def test_deck_created(create_storage_directory):
    runner = CliRunner()
    result = runner.invoke(main.create, input="Italian\nStudy Italian")
    assert "Deck created" in result.output  # message returned to the user

    # load the deck that was just created, and check its filename (although an exception would have
    # been raised if it wasn't created corrently)
    deck = decks.load_deck(decks.generate_deck_filepath("Italian"))
    assert deck.name == "Italian"


def test_trying_to_create_deck_that_already_exists_returns_error_message(math_deck):
    runner = CliRunner()
    result = runner.invoke(main.create, input="Basic Math\nStudy Math")
    assert "A deck with that name already exists; aborting." in result.output


@pytest.mark.xfail
def test_link_created(create_storage_directory):
    assert 0
