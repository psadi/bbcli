# -*- coding: utf-8 -*-
"""
bb pr: Manage pull requests
"""

from enum import Enum
from typing import Optional

import typer

from bb.pr.copy import copy_pull_request
from bb.pr.create import create_pull_request
from bb.pr.delete import delete_pull_request
from bb.pr.diff import show_diff
from bb.pr.list import list_pull_request
from bb.pr.merge import merge_pull_request
from bb.pr.review import review_pull_request
from bb.pr.view import view_pull_request
from bb.utils.cmnd import is_git_repo
from bb.utils.richprint import console, traceback_to_console
from bb.utils.validate import error_tip, state, validate_input

_pr: typer.Typer = typer.Typer(add_completion=False)
bold_red: str = "bold red"
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
) -> None:
    """Create a pull request"""
    try:
        if not is_git_repo():
            raise ValueError(not_a_git_repo)

        target = validate_input(target, "Target branch", "Target branch cannot be none")

        create_pull_request(target, yes, diff, rebase)
    except Exception as err:
        console.print(f"ERROR: {err}", style=bold_red)
        error_tip()
        if state["verbose"]:
            traceback_to_console()


@_pr.command()
def delete(
    id: str = typer.Option("", help="pull request number(s) to delete"),
    yes: bool = typer.Option(False, help=skip_prompt),
    diff: bool = typer.Option(False, help="show diff before deleting pull request"),
) -> None:
    """Delete pull requests"""
    try:
        if not is_git_repo():
            raise ValueError(not_a_git_repo)

        _id = validate_input(
            id,
            "Pull request id(s) to delete\n? ex: id (or) id1, id2",
            "Id's cannot be empty",
        ).split(",")
        delete_pull_request(_id, yes, diff)
    except Exception as err:
        console.print(f"ERROR: {err}", style=bold_red)
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


@_pr.command()
def list(
    role: str = Role.CURRENT.value,
    all: bool = typer.Option(
        False, help="show all pull request(s) based on selected role"
    ),
) -> None:
    """List pull requests in a repository"""
    try:
        if not is_git_repo():
            raise ValueError(not_a_git_repo)

        list_pull_request(role, all)
    except Exception as err:
        console.print(f"ERROR: {err}", style=f"{bold_red}")
        if state["verbose"]:
            traceback_to_console()
        else:
            error_tip()


class Action(str, Enum):
    """review enum choices"""

    APPROVE = "approve"
    UNAPPROVE = "unapprove"
    NEEDS_WORK = "needs_work"
    NONE = "none"


@_pr.command()
def review(
    id: str = typer.Option("", help="pull request number to review"),
    action: Action = Action.NONE,
) -> None:
    """Add a review to a pull request"""
    try:
        _id: str = validate_input(id, "Pull request id to review", id_cannot_be_none)
        action_value: str = "none" if action == Action.NONE else action.value
        action: str = validate_input(
            action_value,
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
) -> None:
    """Merge a pull request"""
    try:
        _id: str = validate_input(id, "Pull request id to merge", id_cannot_be_none)
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
) -> None:
    """View changes in a pull request"""
    try:
        _id: str = validate_input(
            id, "Pull request number to show diff", id_cannot_be_none
        )
        show_diff(_id)
    except Exception as err:
        console.print(f"ERROR: {err}", style=f"{bold_red}")
        if state["verbose"]:
            traceback_to_console()
        else:
            error_tip()


@_pr.command()
def copy(id: str = typer.Option("", help="pull request number to copy")) -> None:
    """Copy pull request url to clipboard"""
    try:
        _id: str = validate_input(id, "Pull request number to copy", id_cannot_be_none)
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
    web: Optional[bool] = typer.Option(False, help="view pull request in browser"),
) -> None:
    """View a pull request"""
    try:
        _id = validate_input(id, "Pull request id to view", id_cannot_be_none)
        view_pull_request(_id, web)
    except Exception as err:
        console.print(f"ERROR: {err}", style=f"{bold_red}")
        if state["verbose"]:
            traceback_to_console()
        else:
            error_tip()
