import os
from subprocess import run
import tempfile

Q_INSTRUCTION = "# Edit the question above. Do not edit or remove this line."
A_INSTRUCTION = "# Edit the answer above. Do not edit or remove this line."


def prompt_via_editor(instructions: str) -> str:
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
    user_input = ""
    for line in content.split("\n"):
        if not line.startswith("#"):
            user_input += line + "\n"

    return user_input.rstrip("\n")


def parse_edited_card(content: str) -> dict:
    edited_card = {}
    question = []
    answer = []

    lines = content.split("\n")
    lines = lines[:-1]  # remove the empty line created from the final \n

    # raise exception if the instruction lines have been removed or altered
    if Q_INSTRUCTION not in lines or A_INSTRUCTION not in lines:
        raise ValueError

    # get line numbers of instructions
    q_instruction_line = lines.index(Q_INSTRUCTION)
    a_instruction_line = lines.index(A_INSTRUCTION)

    for i, line in enumerate(lines):
        if line == Q_INSTRUCTION:
            q_instruction_line = i
        if line == A_INSTRUCTION:
            a_instruction_line = i

    # now get the user's edited answer and question
    for line in lines[0:q_instruction_line]:
        question.append(line)

    for line in lines[q_instruction_line + 1 : a_instruction_line]:
        answer.append(line)

    edited_card["question"] = "\n".join(question)
    edited_card["answer"] = "\n".join(answer)

    return edited_card
