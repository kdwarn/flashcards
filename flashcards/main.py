"""Main entry point of the application, with commands and sub-commands."""
import os
from subprocess import call
import tempfile

import click

from flashcards import study
from flashcards import decks
from flashcards.cards import StudyCard


@click.group()
def cli():
    """Create and study flashcards on the command line."""
    decks.create_storage_directory()  # create it if it doesn't already exist


@click.command("status")
def status_cmd():
    """Show selected deck, if any, and details about it."""
    try:
        deck = decks.load_deck(decks.selected_deck_path())
    except IOError:
        return click.echo("No deck currently selected.")

    click.echo(f"\nCurrently selected deck: {deck.name}")
    click.echo(f"Number of cards: {len(deck)}")
    if deck.description:
        click.echo(f"Description: {deck.description}")
    click.echo("")


@click.command("study")
@click.argument("deck", default="")
@click.option(
    "--ordered", is_flag=True, help="Study the cards in the order they were added to the deck."
)
def study_cmd(deck, ordered):
    """
    Start a study session. By default, the cards are shuffled.

    If DECK is not provided, study the selected deck, if any.
    """
    if not deck:
        try:
            deck = decks.load_deck(decks.selected_deck_path()).name
        except IOError:
            return click.echo("No deck currently selected.")

    deck_path = decks.generate_deck_filepath(deck)

    try:
        deck = decks.load_deck(deck_path)
    except IOError:
        return click.echo("No deck by that name found.")

    if deck.cards:
        study.study(deck, ordered=ordered)
    else:
        click.echo(f"The {deck.name} deck currently has no cards.")


@click.command("create")
@click.option("--name", prompt="Name of the deck")
@click.option("--desc", prompt="Description of the deck")
def create(name, desc):
    """Create a new deck."""
    deck = decks.Deck(name, desc)
    try:
        deck.create_file()
    except IOError:
        return click.echo("A deck with that name already exists; aborting.")
    deck.save()
    decks.link_selected_deck(deck.filepath)  # make this the selected deck
    click.echo("Deck created!")


@click.command("select")
@click.argument("deck")
def select(deck):
    """Select a deck to add cards to and to study."""
    deck_path = decks.generate_deck_filepath(deck)
    try:
        deck_obj = decks.load_deck(deck_path)
    except FileNotFoundError:
        return click.echo("No deck by that name found.")

    decks.link_selected_deck(deck_path)  # make this the selected deck
    click.echo(f"Selected deck: {deck_obj.name}")
    click.echo("New cards will be added to this deck.")


@click.command("add")
@click.option(
    "-e",
    "editormode",
    is_flag=True,
    help="Use an editor rather than the command line to create the card.",
)
def add(editormode):
    """ Add a card to the currently selected deck. """
    try:
        deck = decks.load_deck(decks.selected_deck_path())
    except IOError:
        return click.echo("There is no deck currently selected. Select a deck to add a card.")

    question = ask_for_question(editormode)
    answer = ask_for_answer(editormode)
    deck.add(StudyCard(question, answer))
    deck.save()
    click.echo("Card added to the deck!")


def ask_for_question(editor_mode=False):
    """Prompt the user for a question."""
    if editor_mode:
        return prompt_via_editor("TMP_QUESTION_", "\n# Write your question above.")
    return click.prompt("Question")


def ask_for_answer(editor_mode=False):
    """Prompt the user for an answer."""
    if editor_mode:
        return prompt_via_editor("TMP_ANSWER_", "\n# Write your answer above.")
    return click.prompt("Answer")


def prompt_via_editor(filename, message):
    """
    Open a temp file in an editor and return the input from the user.

    :returns: the input str from the user.
    """
    editor = os.environ.get("EDITOR", "vim")
    filecontent = ""
    with tempfile.NamedTemporaryFile(prefix=filename, suffix=".tmp", mode="r+") as f:
        f.write(message)  # start the file with the instructions

        f.flush()
        call([editor, f.name])  # call the editor to open this file.

        f.seek(0)  # put us back to the top of the file
        filecontent = f.read()  # copy as string

    # remove the commented out lines telling user where to put question and answer
    data = ""
    for line in filecontent.split("\n"):
        if not line.startswith("#"):
            data += line + "\n"

    return data.rstrip("\n")


# Add the subcommands to this main entry point.
cli.add_command(status_cmd)
cli.add_command(study_cmd)
cli.add_command(create)
cli.add_command(select)
cli.add_command(add)
