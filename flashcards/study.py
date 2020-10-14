"""Display cards' questions and answers to user."""
import click


def study(cards: list):
    """Iterate through cards, pausing for user input after each question/answer."""
    question_num = len(cards)

    for i, card in enumerate(cards, start=1):
        click.clear()
        click.echo(f"QUESTION {i} / {question_num} ({card['deck']} deck)")
        click.echo("\n" + card["question"] + "\n")
        click.pause("...")
        click.echo("\n" + card["answer"] + "\n")
        click.echo("Press any key to show the next question, and 'q' to quit.")
        key_press = click.getchar()
        if key_press == "q":
            return

    click.echo("All done!")
