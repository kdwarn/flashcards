from click.testing import CliRunner

from flashcards.decks import link_selected_deck
from flashcards import main

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
