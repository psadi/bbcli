# -*- coding: utf-8 -*-

"""
bb: repo - repository management
"""

import typer

from bb.utils.cmnd import clone_repo
from bb.utils.ini import parse
from bb.utils.richprint import console, traceback_to_console
from bb.utils.validate import error_tip, state, validate_input

_repo = typer.Typer(add_completion=True)


@_repo.command()
def clone(
    name: str = typer.Argument(..., help="repository name, Format: project/repository")
) -> None:
    """Clone a BitBucket repository locally"""
    try:
        name = validate_input(
            name, "project/repository to clone", "repository can't be none"
        )
        console.print(f"Cloning '{name}' into '{name.split('/')[1]}'...")
        clone_repo(name, parse()[2])
    except Exception as err:
        console.print(f"ERROR: {err}", style="bold red")
        if state["verbose"]:
            traceback_to_console()
        else:
            error_tip()
