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
        click.pause("Press any key to show the next question, and 'q' to quit.")
        key_press = click.getchar()
        if key_press == "q":
            return
        if key_press == "e":
            click.echo("user pressed e")
        if key_press == "d":
            click.echo("user pressed d")

    click.echo("All done!")
