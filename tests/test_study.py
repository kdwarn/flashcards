"""
Test the study command and helper function.

TODO:
    * either move the other tests for the command here, or move the tests for the command here
to test_main and only test the helper here.
    * consider removing helper altogether and placing directly in command

NOTE: in the study helper, click.pause is called twice. One keystroke will then continue the
program. After the second pause, the key stroke is checked. Unlike click.prompt, when entering
input for this, you only need to string together as many single key-strokes as desired, rather
than separating them with \n. Each input will only be checked on the second pause, since that's
where the code does it. So each input is evaluated then, and it's as if there's 1 input per question
rather than 2. If there are not enough inputs to for every question, the program will just
continue until the end.
"""

from click.testing import CliRunner

from flashcards import main


def test_pressing_q_quits_session(math_deck):
    runner = CliRunner()
    result = runner.invoke(main.study_cmd, ["Basic Math", "-o"], input="jq")
    assert "2 + 2 = ?" in result.output  # first question should be in output
    assert "2 + 3 = ?" in result.output  # second questions hould be in output
    assert "2 + 4 = ?" not in result.output  # should not reach second question
    assert "All done!" not in result.output  # should not reach the end


def test_pressing_e_enters_editor(create_storage_directory, math_deck):
    runner = CliRunner()
    result = runner.invoke(main.study_cmd, ["Basic Math", "-o"], input="eq")

    # 1st question should be output - appears before the first input is received/checked
    assert "2 + 2 = ?" in result.output

    # confirmation statement should be output, appears after user saves file
    assert "Card edited" in result.output

    # 2nd question should be output - user just hit e, so it continues (after printing debug)
    assert "2 + 3 = ?" in result.output

    # nothing after the 2nd question - user hit "q" after 2nd question
    assert "2 + 4 = ?" not in result.output
    assert "All done!" not in result.output
