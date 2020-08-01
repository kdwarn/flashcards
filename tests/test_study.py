from click.testing import CliRunner
import pytest

from flashcards.decks import Deck
from flashcards import main
from flashcards.study import study


@pytest.mark.xfail
def test_end_study(math_deck):
    runner = CliRunner()
    result = runner.invoke(main.study_cmd, [math_deck])
    print(result)
    # print(result.output)
    # assert result.exit_code == 0
    assert "All done!" in result.output
