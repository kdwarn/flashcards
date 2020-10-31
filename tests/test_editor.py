"""
Test editor functionality.

*fake_process* is a fixture from the pytest-subprocess plugin.
"""
import os
from unittest.mock import patch


from flashcards.editor import prompt_via_editor, remove_instructions, edit


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

    edit("# instruction line")

    editor = os.environ.get("EDITOR", "vim")  # default to vim

    assert editor in fake_process.calls[0]


@patch.dict(os.environ, {"EDITOR": "nano"})
def test_check_if_mocked_editor_envvar__called_by_edit(fake_process):
    # register any process
    fake_process.register_subprocess([fake_process.any()])

    edit("# instruction line")

    assert "nano" in fake_process.calls[0]


@patch("flashcards.editor.edit")
def test_prompt_via_editor_mocked_results(mock_edit):
    mock_edit.return_value = """
This is the question
# This is an instuction line
"""

    content = prompt_via_editor("# This is an instruction line")
    assert "# This is an instruction line" not in content
