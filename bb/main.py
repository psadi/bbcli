# -*- coding: utf-8 -*-
# pylint: disable=W0613,C0103,W0703,W0613,W0621,W0622
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
from bb.utils.cmnd import is_git_repo
from bb.utils.richprint import console, traceback_to_console

# new app
_bb = typer.Typer()

# globals
state: dict = {"verbose": False}
id_cannot_be_none: str = "id cannot be none"
not_a_git_repo: str = "Not a git repository"
skip_prompt: str = "skip confirmation prompt"


def version_callback(value: bool) -> None:
    """
    - It takes a boolean value as input.
    - If the value is `True`,
      it prints the docstring of the current module (`__doc__`)
      and exits the program.
    """
    if value:
        console.print(__doc__)
        raise typer.Exit(code=0)


def error_tip() -> None:
    """
    reusable error message across mainstream commands
    """
    console.print(
        "\n💻 Try running 'bb --verbose [OPTIONS] COMMAND [ARGS]' to debug",
        style="dim white",
    )


def validate_input(_input: any, expected: str, error: str) -> str:
    """
    validates the input, raise the error if the value is not as expected
    """
    if not _input:
        _input: str = typer.prompt(f"? {expected}")

    if _input is None or _input.lower() == "none":
        console.print(f"{error}", style="red")
        raise typer.Exit(code=1)

    return _input


@_bb.callback()
def callback(
    verbose: bool = False,
    version: bool = typer.Option(None, "--version", callback=version_callback),
):
    """
    run: "bb --help" for more information
    """
    if verbose:
        state["verbose"] = True


@_bb.command()
def create(
    target: str = typer.Option("", help="target branch name"),
    yes: bool = typer.Option(False, help=skip_prompt),
    diff: bool = typer.Option(False, help="show diff after raising pull request"),
    rebase: bool = typer.Option(
        False, help="rebase source branch with target before creation"
    ),
):
    """- create new pull request"""
    try:
        if not is_git_repo():
            console.print(not_a_git_repo, style="red")
            raise typer.Exit(code=1)

        target = validate_input(target, "Target branch", "Target branch cannot be none")

        create_pull_request(target, yes, diff, rebase)

    except Exception:
        error_tip()
        if state["verbose"]:
            traceback_to_console()


@_bb.command()
def delete(
    id: str = typer.Option("", help="pull request number(s) to delete"),
    yes: bool = typer.Option(False, help=skip_prompt),
    diff: bool = typer.Option(False, help="show diff before deleting pull request"),
):
    """- delete pull request's by id's"""
    try:
        if not is_git_repo():
            console.print(not_a_git_repo, style="red")
            raise typer.Exit(code=1)

        _id = validate_input(
            id,
            "Pull request id(s) to delete\n? ex: id (or) id1, id2",
            "Id's cannot be empty",
        ).split(",")

        delete_pull_request(_id, yes, diff)

    except Exception:
        error_tip()
        if state["verbose"]:
            traceback_to_console()


class Role(str, Enum):
    """
    enum role choices for pr.show
    defaults to curent
    """

    AUTHOR = "author"
    REVIEWER = "reviewer"
    CURRENT = "current"


@_bb.command()
def show(
    role: Role = Role.CURRENT.value,
    all: bool = typer.Option(
        False, help="show all pull request(s) based on selected role"
    ),
):
    """- show pull request's authored & reviewing"""
    try:
        if not is_git_repo():
            console.print(not_a_git_repo, style="red")
            raise typer.Exit(code=1)

        show_pull_request(role.value, all)

    except Exception:
        error_tip()
        if state["verbose"]:
            traceback_to_console()


@_bb.command()
def test():
    """- test .alt config (or) prompt for manual config"""
    try:
        validate()
    except Exception:
        error_tip()
        if state["verbose"]:
            traceback_to_console()


# `Action` is a subclass of `str` that has a fixed set of values
class Action(str, Enum):
    """review enum choices"""

    APPROVE = "approve"
    UNAPPROVE = "unapprove"
    NEEDS_WORK = "needs_work"
    NONE = "none"


@_bb.command()
def review(
    id: str = typer.Option("", help="pull request number to review"),
    action: Action = Action.NONE.value,
):
    """- review Pull Request by ID"""
    try:

        _id = validate_input(id, "Pull request id to review", id_cannot_be_none)
        action = validate_input(
            False if action.value == "none" else action.value,
            "Action [approve|unapprove|needs_work]",
            "action cannot be none",
        )

        review_pull_request(_id, action)

    except Exception:
        error_tip()
        if state["verbose"]:
            traceback_to_console()


@_bb.command()
def merge(
    id: str = typer.Option("", help="pull request number to merge"),
    delete_source_branch: bool = typer.Option(
        False, help="deletes source branch after merge"
    ),
    rebase: bool = typer.Option(
        False, help="rebase source branch with target before merge"
    ),
    yes: bool = typer.Option(False, help=skip_prompt),
):
    """- merge pull request by id"""
    try:

        _id = validate_input(id, "Pull request id to merge", id_cannot_be_none)
        merge_pull_request(_id, delete_source_branch, rebase, yes)
    except Exception:
        error_tip()
        if state["verbose"]:
            traceback_to_console()


@_bb.command()
def diff(
    id: str = typer.Option("", help="pull request number to show diff"),
):
    """- view diff in pull request (file only)"""
    try:
        _id = validate_input(id, "Pull request number to show diff", id_cannot_be_none)
        show_diff(_id)
    except Exception:
        error_tip()
        if state["verbose"]:
            traceback_to_console()


@_bb.command()
def copy(id: str = typer.Option("", help="pull request number to copy")):
    """- copy pull request url to clipboard by id"""
    try:
        _id = validate_input(id, "Pull request number to show copy", id_cannot_be_none)
        copy_pull_request(_id)
    except Exception:
        error_tip()
        if state["verbose"]:
            traceback_to_console()
