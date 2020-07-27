"""Display cards' questions and answers to user."""
import random
import sys

import click


def study(cards, mode="linear"):
    """Iterate through cards, pausing for user input after each question/answer."""
    question_num = len(cards)
    question_count = 1

    cards_list = list(cards)

    if mode == "shuffled":
        random.shuffle(cards_list)

    for card in cards_list:
        click.clear()

        header = "[QUESTION %s / %s]" % (question_count, question_num)
        click.echo(header)
        click.echo("\n" + card.question + "\n")
        click.pause("...")

        question_count += 1
        click.echo("\n" + card.answer + "\n")

        click.echo("Press any key to show the next question, and 'q' to quit.")
        key_press = click.getchar()
        if key_press == "q":
            return
