"""
flashcards.main
~~~~~~~~~~~~~~~~~~~

Main entry point of the application.
Contain commands and sub-commands grouping logic.
"""
import os
from subprocess import call
import tempfile

import click

from flashcards import storage
from flashcards import study
from flashcards import decks
from flashcards.cards import StudyCard


@click.group()
def cli():
    """
    Command line application that focus on creating decks of flashcards
    quickly and easily.
    """
    # Verify that the storage directory is present.
    storage.verify_storage_dir_integrity()
    pass


@click.command("status")
def status_cmd():
    """
    Show status of the application.

    Displaying the currently selected deck.
        - deck name
        - deck description
        - number of cards
    """
    try:
        deck = storage.load_selected_deck()

        click.echo("Currently selected deck: %s \n" % deck.name)
        click.echo("[NUMBER OF CARDS]: %s \n" % len(deck))
        click.echo("[DESCRIPTION]:")
        click.echo(deck.description + "\n")

    except IOError:
        click.echo("No deck currently selected.")


@click.command("study")
@click.argument("deck", default="")
@click.option("--shuffle", is_flag=True)
def study_cmd(deck, shuffle):
    """
    Start a study session.

    If DECK not provided, study the selected deck, if any.
    """
    if not deck:
        try:
            deck = storage.load_selected_deck().name
        except IOError:
            return click.echo("No deck currently selected.")

    deck_path = os.path.join(storage.deck_storage_path(), deck + ".json")
    deck = storage.load_deck(deck_path).load()
    if shuffle:
        studysession = study.get_study_session_template("shuffled")
    else:
        studysession = study.get_study_session_template("linear")
    studysession.start(deck)


@click.command("create")
@click.option("--name", prompt="Name of the deck")
@click.option("--desc", prompt="Description of the deck")
def create(name, desc):
    """
    Create a new deck.

    User supplies a name and a description.
    If this deck does not exist, it is created.
    """
    deck = decks.Deck(name, desc)
    filepath = storage.create_deck_file(deck)

    # automatically select this deck
    storage.link_selected_deck(filepath)
    click.echo("Deck created!")


@click.command("select")
@click.argument("deck")
def select(deck):
    """
    Select a deck.

    New cards will be added to this deck, and a study session will open this deck.
    """
    deck_path = os.path.join(storage.deck_storage_path(), deck + ".json")
    storage.link_selected_deck(deck_path)
    deck_obj = storage.load_deck(deck_path).load()
    click.echo("Selected deck: %s" % deck_obj.name)
    click.echo("New cards will be added to this deck.")


@click.command("add")
@click.option("-e", "editormode", flag_value=True, default=False)
def add(editormode):
    """ Add a card to the currently selected deck. """
    try:
        deck = storage.load_selected_deck()

        question = _ask_for_question(editormode)
        answer = _ask_for_answer(editormode)

        # Create the card and add it to the deck
        # Update the deck by overwriting the old information.
        deck.add(StudyCard(question, answer))
        storage.store_deck(deck)

        click.echo("Card added to the deck!")

    except IOError:
        click.echo("There is no deck currently selected. Select a deck to add a card.")


def _ask_for_question(editor_mode=False):
    """Prompt the user for a question."""
    if editor_mode:
        message = "\n# Write your question."
        return prompt_via_editor("TMP_QUESTION_", message)
    return click.prompt("Question")


def _ask_for_answer(editor_mode=False):
    """Prompt the user for an answer."""
    if editor_mode:
        message = "\n# Write your answer."
        return prompt_via_editor("TMP_ANSWER_", message)
    return click.prompt("Answer")


def prompt_via_editor(filename, init_message=None):
    """
    Open a temp file in an editor and return the input from the user.

    :param init_message: an initial message to write in the editor.

    :returns: the input str from the user.
    """
    editor = os.environ.get("EDITOR", "vim")
    filecontent = ""

    with tempfile.NamedTemporaryFile(prefix=filename, suffix=".tmp") as f:
        # write initial message
        if init_message is not None:
            f.write(init_message)

        f.flush()
        call([editor, f.name])  # call the editor to open this file.

        f.seek(0)
        filecontent = f.read()

    return _remove_lines_starting_with(filecontent, "#")


def _remove_lines_starting_with(string, start_char):
    """
    Utility function that removes line starting with the given character in the
    provided str.

    :param data: the str to remove lines.
    :param start_char: the character to look for at the begining of a line.

    :returns: the string without the lines starting with start_char.
    """
    data = ""
    for line in string.split("\n"):
        if not line.startswith(start_char):
            data += line + "\n"

    return data


# Add the subcommands to this main entry point.
cli.add_command(status_cmd)
cli.add_command(study_cmd)
cli.add_command(create)
cli.add_command(select)
cli.add_command(add)
