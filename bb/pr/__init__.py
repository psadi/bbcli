# -*- coding: utf-8 -*-
"""
bb pr: Manage pull requests
"""

# This is importing all the required modules for the script to run.
from enum import Enum
import typer
from bb.pr.create import create_pull_request
from bb.pr.delete import delete_pull_request
from bb.pr.list import list_pull_request
from bb.pr.review import review_pull_request
from bb.pr.merge import merge_pull_request
from bb.pr.diff import show_diff
from bb.pr.copy import copy_pull_request
from bb.pr.view import view_pull_request
from bb.utils.validate import validate_input, error_tip, state
from bb.utils.cmnd import is_git_repo
from bb.utils.richprint import traceback_to_console, console

_pr = typer.Typer(add_completion=False)
bold_red: str = "bold red"
# globals
id_cannot_be_none: str = "id cannot be none"
not_a_git_repo: str = "Not a git repository"
skip_prompt: str = "skip confirmation prompt"


@_pr.command()
def create(
    target: str = typer.Option("", help="target branch name"),
    yes: bool = typer.Option(False, help=skip_prompt),
    diff: bool = typer.Option(False, help="show diff after raising pull request"),
    rebase: bool = typer.Option(
        False, help="rebase source branch with target before creation"
    ),
):
    """Create a pull request"""
    try:
        if not is_git_repo():
            raise ValueError(not_a_git_repo)

        target = validate_input(target, "Target branch", "Target branch cannot be none")

        create_pull_request(target, yes, diff, rebase)
    except Exception:
        error_tip()
        if state["verbose"]:
            traceback_to_console()


@_pr.command()
def delete(
    id: str = typer.Option("", help="pull request number(s) to delete"),
    yes: bool = typer.Option(False, help=skip_prompt),
    diff: bool = typer.Option(False, help="show diff before deleting pull request"),
):
    """Delete pull requests"""
    try:
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
    if not is_git_repo():
        raise ValueError(not_a_git_repo)


class Role(str, Enum):
    """
    enum role choices for pr.show
    defaults to curent
    """

    AUTHOR = "author"
    REVIEWER = "reviewer"
    CURRENT = "current"


@_pr.command()
def list(
    role: Role = Role.CURRENT.value,
    all: bool = typer.Option(
        False, help="show all pull request(s) based on selected role"
    ),
):
    """List pull requests in a repository"""
    try:
        if not is_git_repo():
            raise ValueError(not_a_git_repo)

        list_pull_request(role.value, all)
    except Exception as err:
        console.print(f"ERROR: {err}", style=f"{bold_red}")
        if state["verbose"]:
            traceback_to_console()
        else:
            error_tip()


# `Action` is a subclass of `str` that has a fixed set of values
class Action(str, Enum):
    """review enum choices"""

    APPROVE = "approve"
    UNAPPROVE = "unapprove"
    NEEDS_WORK = "needs_work"
    NONE = "none"


@_pr.command()
def review(
    id: str = typer.Option("", help="pull request number to review"),
    action: Action = Action.NONE.value,
):
    """Add a review to a pull request"""
    try:
        _id = validate_input(id, "Pull request id to review", id_cannot_be_none)
        action = validate_input(
            False if action.value == "none" else action.value,
            "Action [approve|unapprove|needs_work]",
            "action cannot be none",
        )
        review_pull_request(_id, action)
    except Exception as err:
        console.print(f"ERROR: {err}", style=f"{bold_red}")
        if state["verbose"]:
            traceback_to_console()
        else:
            error_tip()


@_pr.command()
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
    """Merge a pull request"""
    try:
        _id = validate_input(id, "Pull request id to merge", id_cannot_be_none)
        merge_pull_request(_id, delete_source_branch, rebase, yes)
    except Exception as err:
        console.print(f"ERROR: {err}", style=f"{bold_red}")
        if state["verbose"]:
            traceback_to_console()
        else:
            error_tip()


@_pr.command()
def diff(
    id: str = typer.Option("", help="pull request number to show diff"),
):
    """View changes in a pull request"""
    try:
        _id = validate_input(id, "Pull request number to show diff", id_cannot_be_none)
        show_diff(_id)
    except Exception as err:
        console.print(f"ERROR: {err}", style=f"{bold_red}")
        if state["verbose"]:
            traceback_to_console()
        else:
            error_tip()


@_pr.command()
def copy(id: str = typer.Option("", help="pull request number to copy")):
    """Copy pull request url to clipboard"""
    try:
        _id = validate_input(id, "Pull request number to copy", id_cannot_be_none)
        copy_pull_request(_id)
    except Exception as err:
        console.print(f"ERROR: {err}", style=f"{bold_red}")
        if state["verbose"]:
            traceback_to_console()
        else:
            error_tip()


@_pr.command()
def view(
    id: str = typer.Option("", help="pull request id to view"),
    web: bool = typer.Option(False, help="view pull request in browser"),
):
    """View a pull requests"""
    try:
        _id = validate_input(id, "Pull request id to view", id_cannot_be_none)
        view_pull_request(_id, web)
    except Exception as err:
        console.print(f"ERROR: {err}", style=f"{bold_red}")
        if state["verbose"]:
            traceback_to_console()
        else:
            error_tip()
