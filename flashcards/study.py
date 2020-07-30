"""Display cards' questions and answers to user."""
import random

import click

from flashcards.decks import Deck


def study(deck: Deck, ordered=False):
    """Iterate through Deck's cards, pausing for user input after each question/answer."""
    question_num = len(deck)

    if not ordered:
        random.shuffle(deck.cards)

    for i, card in enumerate(deck, start=1):
        click.clear()
        click.echo(f"QUESTION {i} / {question_num}")
        click.echo("\n" + card.question + "\n")
        click.pause("...")
        click.echo("\n" + card.answer + "\n")
        click.echo("Press any key to show the next question, and 'q' to quit.")
        key_press = click.getchar()
        if key_press == "q":
            return

    click.echo("All done!")
