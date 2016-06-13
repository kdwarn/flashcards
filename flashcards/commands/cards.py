import click

from flashcards import storage
from flashcards.cards import StudyCard


@click.group('cards')
def cards_group():
    """Command related to StudyCard objects """
    pass


@click.command('add')
@click.option('--question', prompt='Question')
@click.option('--answer', prompt='Answer')
def add(question, answer):
    """ Add a studycard to the currently selected studyset. """

    # Load the currently selected studyset
    studyset = storage.load_selected_studyset()

    # Create the card and add it to the studyset
    card = StudyCard(question, answer)
    studyset.add(card)

    # Update the studyset by overwriting the old information.
    storage.store_studyset(studyset)

    click.echo('Card added to the studyset !')


cards_group.add_command(add)