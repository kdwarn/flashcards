"""
Test editor functionality.

*fake_process* is a fixture from the pytest-subprocess plugin.
"""
import os
from unittest.mock import patch

import pytest

from flashcards.editor import (
    Q_INSTRUCTION,
    A_INSTRUCTION,
    edit_card,
    prompt_via_editor,
    remove_instructions,
)
from flashcards.exceptions import InstructionsRemovedException


def test_remove_instructions():
    filecontents_from_user = """
This is the question
# This is an instuction line
"""
    cleaned_contents = remove_instructions(filecontents_from_user)

    assert "# This is an instruction line" not in cleaned_contents


def test_check_if_default_editor_called_by_edit(fake_process):
    # register any process and use EDITOR env var (as edit() does) to check proper one was called
    fake_process.register_subprocess([fake_process.any()])

    prompt_via_editor("# instruction line")

    editor = os.environ.get("EDITOR", "vim")  # default to vim

    assert editor in fake_process.calls[0]


@patch.dict(os.environ, {"EDITOR": "nano"})
def test_check_if_mocked_editor_envvar_called_by_edit(fake_process):
    # register any process
    fake_process.register_subprocess([fake_process.any()])

    prompt_via_editor("# instruction line")

    assert "nano" in fake_process.calls[0]


@patch("flashcards.editor.prompt_via_editor")
def test_prompt_via_editor_mocked_results(mock_edit):
    mock_edit.return_value = """
This is the question
# This is an instuction line
"""

    content = prompt_via_editor("# This is an instruction line")
    content = remove_instructions(content)
    assert "# This is an instruction line" not in content


@patch("flashcards.editor.prompt_via_editor")
def test_altered_instruction_lines_raise_exception(mock_editor_function):
    mock_editor_function.return_value = "instructions have been removed"
    card = {"question": "Why?", "answer": "Because"}
    with pytest.raises(InstructionsRemovedException):
        edit_card(card)


@patch("flashcards.editor.prompt_via_editor")
def test_edited_card_returns_correct_results(mock_editor_function):
    mock_editor_function.return_value = f"""Why?
{Q_INSTRUCTION}
Because
{A_INSTRUCTION}
"""
    original_card = {"question": "Why not?", "answer": "Because not"}

    card = edit_card(original_card)

    assert card["question"] == "Why?"
    assert card["answer"] == "Because"
