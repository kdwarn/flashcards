import os
from unittest.mock import patch

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

"""
NOTE: in main.study_cmd(), the program is paused twice on each card - first between the question and
the answer by click.pause(), and then after the answer by click.getchar(). However, if click.pause
is not run from a terminal, it's as if nothing happens, so this does not happen during testing.
So it's as if there's only one pause for user input to be entered. Unlike click.prompt, when
entering input for this, you only need to string together as many single key-strokes as desired (and
two per card), rather than separating them with \n. If there are not enough inputs to for every
question, the program will just continue until the end.
"""


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


def test_error_message_if_multiple_decks_have_no_cards(
    create_storage_directory, german_deck, italian_deck
):
    runner = CliRunner()
    result = runner.invoke(main.study_cmd, ["all"])
    assert "no cards to study" in result.output


def test_pressing_q_quits_session(math_deck):
    runner = CliRunner()
    result = runner.invoke(main.study_cmd, ["Basic Math", "-o"], input="jq")
    assert "2 + 2 = ?" in result.output  # first question should be in output
    assert "2 + 3 = ?" in result.output  # second question should be in output
    assert "2 + 4 = ?" not in result.output  # should not reach second question
    assert "All done!" not in result.output  # should not reach the end


def test_pressing_e_enters_editor(create_storage_directory, math_deck):
    """User edits first question and then quits after second question."""
    runner = CliRunner()
    result = runner.invoke(main.study_cmd, ["Basic Math", "-o"], input="eq")

    # 1st question should be output - appears before the first input is received/checked
    assert "2 + 2 = ?" in result.output

    # No edits occurred, so that message should then be displayed after entering/exiting editor
    assert "No edits detected" in result.output

    # 2nd question should be output - user just hit e, so it continues (after printing debug)
    assert "2 + 3 = ?" in result.output

    # nothing after the 2nd question - user hit "q" after 2nd question
    assert "2 + 4 = ?" not in result.output
    assert "All done!" not in result.output


################
# create command


def test_create_success_message_received(create_storage_directory):
    runner = CliRunner()
    result = runner.invoke(main.create, input="Italian\nStudy Italian")
    assert 'Deck "italian" created' in result.output


def test_deck_created(create_storage_directory):
    runner = CliRunner()
    result = runner.invoke(main.create, input="Italian\nStudy Italian")
    assert 'Deck "italian" created' in result.output  # message returned to the user

    # load the deck that was just created, and check its filename (although an exception would have
    # been raised if it wasn't created corrently)
    deck = decks.load_deck(decks.generate_deck_filepath("Italian"))
    assert deck.name == "italian"


def test_reprompt_if_deck_name_doesnt_start_with_letter(create_storage_directory):
    runner = CliRunner()

    # "1test" is incorrect so user is reprompted; then we submit acceptable name and desc
    result = runner.invoke(main.create, input="1test\ntest_name\ntest_desc")

    assert "Sorry, the name must start with a letter" in result.output
    assert 'Deck "test_name" created' in result.output

    # now check the name is correct
    deck = decks.load_deck(decks.generate_deck_filepath("test_name"))
    assert deck.name == "test_name"


def test_reprompt_if_deck_name_already_exists(math_deck):
    runner = CliRunner()

    # "Basic Math" already exists so user is reprompted; then we submit acceptable name and desc
    result = runner.invoke(main.create, input="Basic Math\nBasic Math1\nLearning math.")

    assert "Sorry, a deck with that name already exists." in result.output
    assert 'Deck "basic-math1" created' in result.output

    # now check the name is correct
    deck = decks.load_deck(decks.generate_deck_filepath("Basic Math1"))
    assert deck.name == "basic-math1"


def test_link_created_after_deck_created(create_storage_directory):
    runner = CliRunner()
    runner.invoke(main.create, input="Italian\nStudy Italian")
    assert decks.selected_deck_path().resolve() == decks.storage_path() / "italian.json"


################
# select command


def test_successful_deck_selection(math_deck):
    runner = CliRunner()
    result = runner.invoke(main.select, ["Basic Math"])
    assert "Selected deck: Basic Math" in result.output


def test_selecting_deck_that_doesnt_exist_returns_error_message():
    runner = CliRunner()
    result = runner.invoke(main.select, ["spanish"])
    assert "No deck by that name found" in result.output


def test_link_created_after_deck_selected(math_deck):
    runner = CliRunner()
    runner.invoke(main.select, ["Basic Math"])
    assert decks.selected_deck_path().resolve() == decks.storage_path() / "basic-math.json"


#############
# add command


def test_add_card_successful(math_deck):
    runner = CliRunner()
    runner.invoke(main.select, ["Basic Math"])
    result = runner.invoke(main.add, input="Square root of 25?\n5")
    assert "Card added to the deck!" in result.output


def test_add_card_returns_error_message_if_no_deck_selected(math_deck):
    runner = CliRunner()
    result = runner.invoke(main.add, input="Square root of 25?\n5")
    assert "No deck is currently selected" in result.output


@patch.dict(os.environ, {"EDITOR": "not_an_editor"})
def test_check_if_no_editor_env_var_and_no_vim_returns_error_message(math_deck):
    runner = CliRunner()
    runner.invoke(main.select, ["Basic Math"])
    result = runner.invoke(main.add, ["-e"])
    assert "Could not open" in result.output


######################
# list decks command


def test_listing_decks_successful(math_deck):
    runner = CliRunner()
    result = runner.invoke(main.list_decks)
    assert "Your decks:" in result.output and "Basic Math" in result.output


def test_list_multiple_decks_successful(math_deck, german_deck):
    runner = CliRunner()
    result = runner.invoke(main.list_decks)
    assert (
        "Your decks:" in result.output
        and "Basic Math" in result.output
        and "German" in result.output
    )


def test_error_message_if_no_decks_after_list_command(create_storage_directory):
    runner = CliRunner()
    result = runner.invoke(main.list_decks)
    assert "You don't have any decks yet." in result.output


@pytest.mark.xfail
def test_decks_listed_in_alpha_order(german_deck, math_deck):
    assert False


@pytest.mark.xfail
def test_error_message_if_deck_missing_key():
    assert 0
