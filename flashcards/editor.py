import os
from subprocess import run
import tempfile


def prompt_via_editor(instructions: str) -> str:
    """Open a temp file in an editor and return the input from the user, excluding instructions."""
    filecontent = edit(instructions)

    return remove_instructions(filecontent)


def edit(instructions: str) -> str:
    """Open a temporary file with user's editor, with *instructions* written into it, and return
    the contents when closed.
    """
    editor = os.environ.get("EDITOR", "vim")  # default to vim

    with tempfile.NamedTemporaryFile(mode="r+") as f:
        f.write(instructions)

        f.flush()
        run([editor, f.name])  # call the editor to open this file.

        f.seek(0)  # put us back to the top of the file
        filecontent = f.read()  # copy as string

    return filecontent


def remove_instructions(content: str) -> str:
    data = ""
    for line in content.split("\n"):
        if not line.startswith("#"):
            data += line + "\n"

    return data.rstrip("\n")
