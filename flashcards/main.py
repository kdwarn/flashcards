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
from flashcards import sets
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

    Displaying the currently selected studyset.
        - studyset title
        - studyset description
        - number of cards
    """
    try:
        studyset = storage.load_selected_studyset()

        click.echo("Currently selected studyset: %s \n" % studyset.title)
        click.echo("[NUMBER OF CARDS]: %s \n" % len(studyset))
        click.echo("[DESCRIPTION]:")
        click.echo(studyset.description + "\n")

    except IOError:
        click.echo("No studyset currently selected.")


@click.command("study")
@click.argument("studyset")
@click.option("--shuffle", is_flag=True)
def study_cmd(studyset, shuffle):
    """
    Start a study session.

    Study the studyset passed via the studyset argument.
    """
    studyset_path = os.path.join(storage.studyset_storage_path(), studyset + ".json")
    studyset = storage.load_studyset(studyset_path).load()
    if shuffle:
        studysession = study.get_study_session_template("shuffled")
    else:
        studysession = study.get_study_session_template("linear")
    studysession.start(studyset)


@click.command("create")
@click.option("--title", prompt="Title of the study set")
@click.option("--desc", prompt="Description for the study set (optional)")
def create(title, desc):
    """
    Create a new study set.

    User supplies a title and a description.
    If this study set does not exist, it is created.
    """
    study_set = sets.StudySet(title, desc)
    filepath = storage.create_studyset_file(study_set)

    # automatically select this studyset
    storage.link_selected_studyset(filepath)
    click.echo("Study set created!")


@click.command("select")
@click.argument("studyset")
def select(studyset):
    """
    Select a studyset.

    Focus on a studyset, every new added cards are going to be put directly in
    this studyset.
    """
    studyset_path = os.path.join(storage.studyset_storage_path(), studyset + ".json")
    storage.link_selected_studyset(studyset_path)
    studyset_obj = storage.load_studyset(studyset_path).load()
    click.echo("Selected studyset: %s" % studyset_obj.title)
    click.echo("Next created cards will be automatically added to this studyset.")


@click.command("add")
@click.option("-e", "editormode", flag_value=True, default=False)
def add(editormode):
    """ Add a studycard to the currently selected studyset. """
    try:
        studyset = storage.load_selected_studyset()

        question = _ask_for_question(editormode)
        answer = _ask_for_answer(editormode)

        # Create the card and add it to the studyset
        # Update the studyset by overwriting the old information.
        studyset.add(StudyCard(question, answer))
        storage.store_studyset(studyset)

        click.echo("Card added to the studyset !")

    except IOError:
        click.echo("There is no studyset currently selected. Select a studyset to add a card.")


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
