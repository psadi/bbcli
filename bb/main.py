# -*- coding: utf-8 -*-
"""
bbcli: a comman line utility that can manage pull requests in bitbucket.
"""

# This is importing all the required modules for the script to run.
from enum import Enum
import typer
from bb import __doc__
from bb.pr.create import create_pull_request
from bb.pr.delete import delete_pull_request
from bb.pr.configtest import validate
from bb.pr.show import show_pull_request
from bb.pr.review import review_pull_request
from bb.pr.merge import merge_pull_request
from bb.pr.diff import show_diff
from bb.pr.copy import copy_pull_request
from bb.utils.cmnd import is_git_repo, checkout_and_pull
from bb.utils.richprint import console, traceback_to_console

# Creating a new Typer app.
app = typer.Typer()
# A global variable that is used to store the state of the application.
state = {"verbose": False}


def version_callback(value: bool):
    """
    - It takes a boolean value as input.
    - If the value is `True`, it prints the docstring of the current module (`__doc__`) and exits the
    program.
    """
    if value:
        console.print(__doc__)
        raise typer.Exit(code=0)


def error_tip():
    console.print(
        f"\n💻 Try running 'bb --verbose [OPTIONS] COMMAND [ARGS]' to debug",
        style="dim white",
    )


def validate_input(input: any, expected: str, error: str) -> str:
    if not input:
        input: str = typer.prompt(f"? {expected}")

    if input == None or input.lower() == "none":
        console.print(f"{error}", style="red")
        raise (typer.Exit(code=1))

    return input


@app.callback()
def callback(
    verbose: bool = False,
    version: bool = typer.Option(None, "--version", callback=version_callback),
):
    """
    run: "bb --help" for more information
    """
    if verbose:
        state["verbose"] = True


@app.command()
def create(
    target: str = typer.Option("", help="target branch name"),
    yes: bool = typer.Option(False, help="skip confirmation prompt"),
    diff: bool = typer.Option(False, help="show diff after raising pull request"),
    rebase: bool = typer.Option(
        False, help="rebase source branch with target before creation"
    ),
):
    """- create new pull request"""
    try:
        if not is_git_repo():
            console.print("Not a git repository", style="red")
            raise typer.Exit(code=1)

        target = validate_input(target, "Target branch", "Target branch cannot be none")

        create_pull_request(target, yes, diff, rebase)

    except Exception:
        error_tip()
        if state["verbose"]:
            traceback_to_console(Exception)


@app.command()
def delete(
    id: str = typer.Option("", help="pull request number(s) to delete"),
    yes: bool = typer.Option(False, help="skip confirmation prompt"),
    diff: bool = typer.Option(False, help="show diff before deleting pull request"),
):
    """- delete pull request's by id's"""
    try:
        if not is_git_repo():
            console.print("Not a git repository", style="red")
            raise typer.Exit(code=1)

        id = validate_input(
            False,
            "Pull request id(s) to delete\n? ex: id (or) id1, id2",
            "Id's cannot be empty",
        ).split(",")

        delete_pull_request(id, yes, diff)

    except Exception:
        error_tip()
        if state["verbose"]:
            traceback_to_console(Exception)


# `Role` is a subclass of `str` that has a fixed set of values
class Role(str, Enum):
    author = "author"
    reviewer = "reviewer"
    current = "current"


@app.command()
def show(
    role: Role = Role.current.value,
    all: bool = typer.Option(
        False, help="show all pull request(s) based on selected role"
    ),
):
    """- show pull request's authored & reviewing"""
    try:
        if not is_git_repo():
            console.print("Not a git repository", style="red")
            raise typer.Exit(code=1)

        show_pull_request(role.value, all)

    except Exception:
        error_tip()
        if state["verbose"]:
            traceback_to_console(Exception)


@app.command()
def test():
    """- test .alt config (or) prompt for manual config"""
    try:
        validate()
    except Exception:
        error_tip()
        if state["verbose"]:
            traceback_to_console(Exception)


# `Action` is a subclass of `str` that has a fixed set of values
class Action(str, Enum):
    """review enum choices"""

    approve = "approve"
    unapprove = "unapprove"
    needs_work = "needs_work"
    none = "none"


@app.command()
def review(
    id: str = typer.Option("", help="pull request number to review"),
    action: Action = Action.none.value,
):
    """- review Pull Request by ID"""
    try:

        id = validate_input(id, "Pull request id to review", "id cannot be none")
        action = validate_input(
            False if action.value is "none" else action.value,
            "Action [approve|unapprove|needs_work]",
            "action cannot be none",
        )

        review_pull_request(id, action)

    except Exception:
        error_tip()
        if state["verbose"]:
            traceback_to_console(Exception)


@app.command()
def merge(
    id: str = typer.Option("", help="pull request number to merge"),
    delete_source_branch: bool = typer.Option(
        False, help="deletes source branch after merge"
    ),
    rebase: bool = typer.Option(
        False, help="rebase source branch with target before merge"
    ),
    yes: bool = typer.Option(False, help="skip confirmation prompt"),
):
    """- merge pull request by id"""
    try:

        id = validate_input(id, "Pull request id to merge", "id cannot be none")
        merge_pull_request(id, delete_source_branch, rebase, yes)
    except Exception:
        error_tip()
        if state["verbose"]:
            traceback_to_console(Exception)


@app.command()
def diff(
    id: int = typer.Option("", help="pull request number to show diff"),
):
    """- view diff in pull request (file only)"""
    try:
        id = validate_input(id, "Pull request number to show diff", "id cannot be none")
        show_diff(id)
    except Exception:
        error_tip()
        if state["verbose"]:
            traceback_to_console(Exception)


@app.command()
def copy(id: int = typer.Option("", help="pull request number to copy")):
    """- copy pull request url to clipboard by id"""
    copy_pull_request(id)
