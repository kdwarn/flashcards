# flashcards

Application for creating and studying flashcards from the command line. Fork of [zergov/flashcards](https://github.com/zergov/flashcards).

## Installation

Use [pipx](https://github.com/pipxproject/pipx):

```
$ pipx install git+https://github.com/kdwarn/flashcards.git
```

## Creating a Deck and Adding Cards

The app stores flashcards in decks. To create a deck, run `flashcards create`. You will then be prompted to provide a name and a description of the deck.

To then add a card to the deck, run `flashcards add` and you will be prompted to provide a question and answer for the card.

You can also write the question and answer inside an editor by passing the `-e` parameter to the `flashcards add` command: `flashcards add -e`. This will open vim by default or the editor set to your `EDITOR` environment variable.

Add as many cards as you like.

## The Selected Deck and Deck Status

By default, after creating a deck, the application automaticaly selects it.  This means that the application is currently focused on this deck. Every new created card will be stored in this deck. Also, the `flashcards status` command will show information on the currently selected deck:

```
$ flashcards status

Currently using deck: Math

[NUMBER OF CARDS]: 1

[DESCRIPTION]:
Some math questions
```

To select a different deck:

```
$ flashcards select French

selected deck: French
any created card will be automatically added to this deck.
```

## Studying a Deck

You can study the currently selected deck with `flashcards study` or you can specify a different deck, e.g. `flashcards study German`.

The app will iterate through the cards, pausing between the question and answer. You can quit the session by pressing the "q" key.

By default, the cards will be displayed in the order they were added to the deck. To display them in a random order, pass the `--shuffled` flag: `flashcards study German --shuffled`.

## Bash Autocomplete

When installing with pip, auto completion should work out of the box for __linux__ distributions.

It hasn't been tested on __windows__.

For __OSX__, you might have to copy or reference the [flashcards-complete.sh](flashcards-complete.sh) script to your `.bash_profile` file.

## Storage directory

By default, decks are stored at `~/.flashcards/decks`, in json format.

