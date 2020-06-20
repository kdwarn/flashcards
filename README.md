# flashcards

Fork of [zergov/flashcards](https://github.com/zergov/flashcards), not yet on PyPI.

Command line application that focus on creating decks of flashcards quickly and easily.

## Installation

This fork is not yet on PyPI. To install the original:

```
$ sudo pip install pyflashcards
```

## Creating a Studyset and Adding Cards

Ideally, flashcards are contained in studysets (decks).

For this use case, we will create a basic mathematic studyset.

```
$ flashcards sets new
```

A series of prompts will ask you to enter the title for this set and also a description for this set.

Once all the information has been entered, a confirmation message will be shown, letting you know that the studyset has been created.

```
$ flashcards sets new

[cli][prompt] Title of the study set: Mathematics
[cli][prompt] Description for the study set: Some math questions.

Study set created !
```

At this point, you're ready to create flashcards to add in your studyset.

To add a card, run this command:

```
$ flashcards cards add
```

which will prompt you to enter the question and answer, and then provide a confirmation message.

```
[cli][prompt] Question: 2 + 2 = ?
[cli][prompt] Answer: 4 (duhh)

Card added to the studyset !
```

You can also write the question and the answer inside an editor by passing the `-e` parameter to the `flashcards cards add` command. This will open vim by default or the editor set to your `EDITOR` environment variable.

```
$ flashcards cards add -e
```

To see the status of this studyset, simply run this command:

```
$ flashcards status

Currently using studyset: Mathematics

[NUMBER OF CARDS]: 1

[DESCRIPTION]:
Some math questions
```

If you're wondering how the application knows you're asking about the status of the "Mathematics" studyset, it's because this is the currently selected studyset.

By default, after creating a studyset, the application automaticaly selects it.  This means that the application is currently focused on this studyset. Every new created card will be stored in this studyset. Also, the `status` command will show information on the currently selected studyset.

To select a different studyset:

```
# Let's say we want to select our "French" studyset
$ flashcards sets select French

selected studyset: French
any created card will be automatically added to this studyset.
```

## Studying a Studyset

Once you're satisfied with your studyset, you can start studying it with the command `flashcards study` followed by the name of the studyset, e.g.:

```
$ flashcards study French
```

During a study session, the application will iterate through the cards in your studyset.  For every card, the question of the card will be displayed. The program will then wait for any input before showing the answer to this question. After each question, you can quit the session by pressing the "q" key.

### Study Modes

Flashcards has two study modes. By default, the cards will be displayed in the order they were created. If you pass the `--shuffled` flag to the `flashcards study` command, they will instead be displayed in random order.

```
$ flashcards study French --shuffled
```

## Bash Autocomplete

When installing with pip, auto completion should work out of the box for __linux__ distributions.

It hasn't been tested on __windows__.

For __OSX__, you might have to copy or reference the [flashcards-complete.sh](flashcards-complete.sh) script to your `.bash_profile` file.

## Storage directory

By default, studysets are stored in the following path:

```
~/.flashcards/studysets
```
