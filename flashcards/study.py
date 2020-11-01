"""Display cards' questions and answers to user."""
import click

from flashcards.editor import (
    prompt_via_editor,
    remove_instructions,
    parse_edited_card,
    Q_INSTRUCTION,
    A_INSTRUCTION,
)
from flashcards.decks import generate_deck_filepath, load_deck


def study(cards: list):
    """Iterate through cards, pausing for user input after each question/answer."""
    question_num = len(cards)

    for i, card in enumerate(cards, start=1):
        click.clear()
        click.echo(f"QUESTION {i} / {question_num} ({card['deck']} deck)")
        click.echo("\n" + card["question"] + "\n")
        click.pause("...")
        click.echo("\n" + card["answer"] + "\n")
        click.secho(
            "Press 'e' to edit this question, 'q' to quit, and any other key to show the next question.",
            fg="green",
        )
        key_press = click.getchar()
        if key_press == "q":
            return
        if key_press == "e":
            # create string of initial file to be edited
            filecontents = (
                card["question"]
                + "\n"
                + Q_INSTRUCTION
                + "\n"
                + card["answer"]
                + "\n"
                + A_INSTRUCTION
            )
            edited_card = prompt_via_editor(filecontents)
            parsed_card = parse_edited_card(edited_card)

            deck_path = generate_deck_filepath(card["deck"])
            deck = load_deck(deck_path)

            # make the change to the appropriate card in the deck
            for deck_card in deck.cards:
                if (
                    deck_card["question"] == card["question"]
                    and deck_card["answer"] == card["answer"]
                ):
                    deck_card["question"] = parsed_card["question"]
                    deck_card["answer"] = parsed_card["answer"]
            deck.save()
            click.echo("Card edited.")
            click.pause()

        if key_press == "d":
            click.echo("user pressed d")

    click.echo("All done!")
