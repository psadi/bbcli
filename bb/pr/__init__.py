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
from bb.utils.constants import vars
from bb.utils.helper import error_handler, validate_input

_pr: typer.Typer = typer.Typer(add_completion=False, no_args_is_help=True)


@_pr.command()
def create(
    target: str = typer.Option("", help="target branch name"),
    yes: bool = typer.Option(False, help=vars.skip_prompt),
    diff: bool = typer.Option(False, help="show diff after raising pull request"),
    rebase: bool = typer.Option(
        False, help="rebase source branch with target before creation"
    ),
) -> None:
    """Create a pull request"""

    @error_handler
    def _create(target: str, yes: bool, diff: bool, rebase: bool) -> None:
        if not is_git_repo():
            raise ValueError(vars.not_a_git_repo)

        target = validate_input(target, "Target branch", "Target branch cannot be none")

        create_pull_request(target, yes, diff, rebase)

    _create(target, yes, diff, rebase)


@_pr.command()
def delete(
    id: str = typer.Option("", help="pull request number(s) to delete"),
    yes: bool = typer.Option(False, help=vars.skip_prompt),
    diff: bool = typer.Option(False, help="show diff before deleting pull request"),
) -> None:
    """Delete pull requests"""

    @error_handler
    def _delete(id: str, yes: bool, diff: bool) -> None:
        if not is_git_repo():
            raise ValueError(vars.not_a_git_repo)

        _id = validate_input(
            id,
            "Pull request id(s) to delete\n? ex: id (or) id1, id2",
            "Id's cannot be empty",
        ).split(",")
        delete_pull_request(_id, yes, diff)

    _delete(id, yes, diff)


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

    @error_handler
    def _list(role: str, all: bool) -> None:
        if not is_git_repo():
            raise ValueError(vars.not_a_git_repo)

        list_pull_request(role, all)

    _list(role, all)


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

    @error_handler
    def _review(id: str, action: Action) -> None:
        if not is_git_repo():
            raise ValueError(vars.not_a_git_repo)

        _id: str = validate_input(
            id, "Pull request id to review", vars.id_cannot_be_none
        )
        action_value: str = "none" if action == Action.NONE else action.value
        action: str = validate_input(
            action_value,
            "Action [approve|unapprove|needs_work]",
            "action cannot be none",
        )
        review_pull_request(_id, action)

    _review(id, action)


@_pr.command()
def merge(
    id: str = typer.Option("", help="pull request number to merge"),
    delete_source_branch: bool = typer.Option(
        False, help="deletes source branch after merge"
    ),
    rebase: bool = typer.Option(
        False, help="rebase source branch with target before merge"
    ),
    yes: bool = typer.Option(False, help=vars.skip_prompt),
) -> None:
    """Merge a pull request"""

    @error_handler
    def _merge(id: str, delete_source_branch: bool, rebase: bool, yes: bool) -> None:
        if not is_git_repo():
            raise ValueError(vars.not_a_git_repo)
        _id: str = validate_input(
            id, "Pull request id to merge", vars.id_cannot_be_none
        )
        merge_pull_request(_id, delete_source_branch, rebase, yes)

    _merge(id, delete_source_branch, rebase, yes)


@_pr.command()
def diff(
    id: str = typer.Option("", help="pull request number to show diff"),
) -> None:
    """View changes in a pull request"""

    @error_handler
    def _diff(id: str) -> None:
        if not is_git_repo():
            raise ValueError(vars.not_a_git_repo)
        _id: str = validate_input(
            id, "Pull request number to show diff", vars.id_cannot_be_none
        )
        show_diff(_id)

    _diff(id)


@_pr.command()
def copy(id: str = typer.Option("", help="pull request number to copy")) -> None:
    """Copy pull request url to clipboard"""

    @error_handler
    def _copy(id: str) -> None:
        if not is_git_repo():
            raise ValueError(vars.not_a_git_repo)

        _id: str = validate_input(
            id, "Pull request number to copy", vars.id_cannot_be_none
        )
        copy_pull_request(_id)

    _copy(id)


@_pr.command()
def view(
    id: str = typer.Option("", help="pull request id to view"),
    web: Optional[bool] = typer.Option(False, help="view pull request in browser"),
) -> None:
    """View a pull request"""

    @error_handler
    def _view(id: str, web: Optional[bool]) -> None:
        if not is_git_repo():
            raise ValueError(vars.not_a_git_repo)
        _id = validate_input(id, "Pull request id to view", vars.id_cannot_be_none)
        view_pull_request(_id, web)

    _view(id, web)
