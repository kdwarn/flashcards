"""
Test editor functionality.
"""

from unittest.mock import patch

from flashcards.editor import prompt_via_editor, remove_instructions


def test_remove_instructions():
    filecontents_from_user = """
This is the question
# This is an instuction line
"""
    cleaned_contents = remove_instructions(filecontents_from_user)

    assert "# This is an instruction line" not in cleaned_contents


@patch("flashcards.editor.edit")
def test_prompt_via_editor(mock_edit):
    mock_edit.return_value = """
This is the question
# This is an instuction line
"""

    content = prompt_via_editor("# This is an instruction line")
    assert "# This is an instruction line" not in content
