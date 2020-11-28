"""Main entry point of the application, with commands and sub-commands."""
import json
import os
import random

import click

from flashcards import decks
from flashcards.editor import edit_card, prompt_via_editor, remove_instructions
from flashcards.exceptions import NoEditsMadeException, InstructionsRemovedException


@click.group()
def cli():
    """
    Create and study flashcards on the command line.

    For additional help, run a command below with the --help option or visit https://github.com/kdwarn/flashcards.
    """
    decks.create_storage_directory()  # create it if it doesn't already exist


@cli.command("status")
def status_cmd():
    """Show details about selected deck, if any."""
    try:
        deck = decks.load_deck(decks.selected_deck_path())
    except IOError:
        return click.echo("No deck currently selected.")

    click.echo(f"\nCurrently selected deck: {deck.name}")
    click.echo(f"Number of cards: {len(deck.cards)}")
    if deck.description:
        click.echo(f"Description: {deck.description}")
    click.echo("")


@cli.command("study")
@click.argument("deck", default="")
@click.option(
    "-o",
    "--ordered",
    is_flag=True,
    help="Study the cards in the order they were added to the deck.",
)
def study_cmd(deck, ordered):
    """
    Start a study session. By default, the cards are shuffled.

    If DECK is not provided, study the selected deck, if any.

    Use "flashcards study all" to study cards from all decks.
    """
    # load decks (one or all), add deck name to each card to enable editing
    if deck == "all":
        cards = []
        for deck_path in decks.storage_path().iterdir():
            if deck_path.suffix == ".json":
                deck = decks.load_deck(deck_path)

                for card in deck.cards:
                    card["deck"] = deck.name
                    cards.append(card)
        if not cards:
            return click.echo("There are no cards to study.")
    else:
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

        if not deck.cards:
            return click.echo(f"The {deck.name} deck currently has no cards.")

        cards = deck.cards

        for card in cards:
            card["deck"] = deck.name

    if not ordered:
        random.shuffle(cards)

    # study - iterate through cards, pausing for user input after each question/answer.
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
        key_press = click.getchar()  # note that this also acts as a pause

        if key_press == "q":
            return
        if key_press == "e":
            try:
                edited_card = edit_card(card)
            except NoEditsMadeException:
                click.echo("No edits detected; card not edited.")
            except InstructionsRemovedException:
                click.echo("Unable to edit card - an instruction line was edited or deleted.")
            else:
                deck_path = decks.generate_deck_filepath(card["deck"])
                deck = decks.load_deck(deck_path)

                for deck_card in deck.cards:
                    if (
                        deck_card["question"] == card["question"]
                        and deck_card["answer"] == card["answer"]
                    ):
                        deck_card["question"] = edited_card["question"]
                        deck_card["answer"] = edited_card["answer"]
                deck.save()
                click.echo("Card edited.")

            click.pause()

    click.echo("All done!")


@cli.command("create")
@click.option("--name", prompt="Name of the deck", callback=decks.check_and_standardize_deck_name)
@click.option("--desc", prompt="Description of the deck")
def create(name, desc):
    """Create a new deck."""
    deck = decks.Deck(name, desc)
    deck.create_file()
    deck.save()
    decks.link_selected_deck(deck.filepath)  # make this the selected deck
    click.echo(f'Deck "{name}" created!')


@cli.command("select")
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


@cli.command("list")
def list_decks():
    """List all decks."""
    storage_dir = decks.storage_path()
    deck_paths = list(storage_dir.glob("**/*.json"))
    if not deck_paths:
        click.echo("You don't have any decks yet.")
    else:
        click.echo("\nYour decks:")
        for deck_path in sorted(deck_paths):
            try:
                deck = decks.load_deck(deck_path)
            except json.decoder.JSONDecodeError:
                click.echo(f"  Problem loading deck in file {deck_path.name}; ignored.")
                continue
            except KeyError as e:
                click.echo(e)
                continue
            click.echo(f"  {deck.name} ", nl=False)
            click.echo(f"({str(len(deck.cards))} cards)", nl=False)
            if deck.description:
                click.echo(f": {deck.description}")
            else:
                click.echo("")
        click.echo("")


@cli.command("add")
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
        return click.echo("No deck is currently selected. Select a deck to add a card.")

    if editormode:
        try:
            question = prompt_via_editor("\n# Write your question above.")
            question = remove_instructions(question).strip()
            if not question:
                return click.echo("Card not added - no question entered.")
            answer = prompt_via_editor("\n# Write your answer above.")
            answer = remove_instructions(answer).strip()
            if not answer:
                return click.echo("Card not added - no answer entered.")
        except FileNotFoundError:
            return click.echo(
                "Could not open an editor. Set the EDITOR environment variable to the name "
                "of your editor or install Vim."
            )
    else:
        question = click.prompt("Question")
        answer = click.prompt("Answer")

    deck.cards.append({"question": question, "answer": answer})
    deck.save()
    click.echo("Card added to the deck!")
