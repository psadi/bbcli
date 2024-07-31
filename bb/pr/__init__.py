# -*- coding: utf-8 -*-

############################################################################
# Bitbucket CLI (bb): Work seamlessly with Bitbucket from the command line
#
# Copyright (C) 2022  P S, Adithya (psadi) (ps.adithya@icloud.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################

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
from bb.utils.cmnd import is_git_repo, title_and_description
from bb.utils.constants import common_vars
from bb.utils.helper import error_handler, validate_input

_pr: typer.Typer = typer.Typer(add_completion=False, no_args_is_help=True)


@_pr.command(help="Create a pull request")
@error_handler
def create(
    target: str = typer.Option("", help="target branch name"),
    yes: bool = typer.Option(False, help=common_vars.skip_prompt),
    diff: bool = typer.Option(False, help="show diff after raising pull request"),
    rebase: bool = typer.Option(
        False, help="rebase source branch with target before creation"
    ),
    title: str = typer.Option("", help="pull request title"),
    description: str = typer.Option("", help="pull request description"),
) -> None:
    """
    Takes in parameters for target branch name, a confirmation flag, diff
    display flag and rebase flag.
    Args:
    -   :param target: Specifies the branch name where you want to create the pr
        :type target: str
    -   :param yes: A boolean flag that determines whether to skip the prompt during
        the execution of the `create` function. If `yes` is set to `True`, it will skip any prompts that
        would normally require user confirmation or input
        :type yes: bool
    -   :param diff: A boolean option that, when set to `True`, will show the diff after
        raising a pull request. This can be helpful for reviewing the changes that will
        be included in the pull request before finalizing it
        :type diff: bool
    -   :param rebase: A  boolean option that determines  whether the source branch should be
        rebased with the target branch before creating the pull request.
        :type rebase: bool
    Raises:
    -   ValueError: If the repository is not a Git repository
    -   ValueError: If the target branch is not provided
    Returns:
    -   None
    """

    if not is_git_repo():
        raise ValueError(common_vars.not_a_git_repo)

    target = validate_input(target, "Target branch", "Target branch cannot be none")

    title = validate_input(
        title, "Title", "", title if title else title_and_description()[0], True
    )
    description = validate_input(
        description,
        "Description",
        "",
        description if description else title_and_description()[1],
        True,
    )

    create_pull_request(target, yes, diff, rebase, title, description)


@_pr.command(help="Delete pull requests")
@error_handler
def delete(
    id: str = typer.Option("", help="pull request number(s) to delete"),
    yes: bool = typer.Option(False, help=common_vars.skip_prompt),
    diff: bool = typer.Option(False, help="show diff before deleting pull request"),
) -> None:
    """
    Used to delete pull requests with options to specify the pull request number(s)
    to delete, skip confirmation prompts and show a diff before deletion.
     Args:
    -   :param id: Used to specify the pull request number(s) that you want to delete.
            :type id: str
    -   :param yes: A boolean flag that determines whether to skip the confirmation
         prompt before deleting the pull request(s).
            :type yes: bool
    -   :param diff: The `diff` parameter in the `delete` function is a boolean flag that, when set to
        `True`, will show the diff before deleting the pull request. This allows the user to review the
        changes that will be made before confirming the deletion of the pull request
        :type diff: bool
     Raises:
    -   ValueError: If the repository is not a Git repository
    -   ValueError: If the PR ID is not provided
     Returns:
    -   None
    """

    if not is_git_repo():
        raise ValueError(common_vars.not_a_git_repo)

    _id = validate_input(
        id,
        "Pull request id(s) to delete\n? ex: id (or) id1, id2",
        "Id's cannot be empty",
    ).split(",")
    delete_pull_request(_id, yes, diff)


# The class Role defines an enumeration with three roles: AUTHOR, REVIEWER, and CURRENT.
class Role(str, Enum):
    AUTHOR = "author"
    REVIEWER = "reviewer"
    CURRENT = "current"


@_pr.command(help="List pull requests in a repository")
@error_handler
def list(
    role: str = Role.CURRENT.value,
    all: bool = typer.Option(
        False, help="show all pull request(s) based on selected role"
    ),
) -> None:
    """
    Lists pull requests based on a selected role, with an option to show all pull requests.
    Args:
    -   :param role: The `role` parameter is a string that specifies the role for which pull requests should
        be listed. It has a default value of `Role.CURRENT.value`
        :type role: str
    -   :param all: A  boolean flag that determines whether to show all pull requests
        :type all: bool
    Raises:
        ValueError: If the repository is not a Git repository
    Returns:
        None
    """

    if not is_git_repo():
        raise ValueError(common_vars.not_a_git_repo)

    list_pull_request(role, all)


# The class `Action` defines an enumeration of string values representing different actions.
class Action(str, Enum):
    APPROVE = "approve"
    UNAPPROVE = "unapprove"
    NEEDS_WORK = "needs_work"
    NONE = "none"


@_pr.command(help="Add a review to a pull request")
@error_handler
def review(
    id: str = typer.Option("", help="pull request number to review"),
    action: Action = Action.NONE,
) -> None:
    """
    Takes a pull request number and an action to review a pull request in the repository.
    Args:
    -   :param id: A string that represents the pull request number to review.
        :type id: str
    -   :param action: The `action` parameter in the `review` function is an enum type `Action`, which
        represents the action to be taken on a pull request. The possible values for `action` are
        `Action.APPROVE`, `Action.UNAPPROVE`, or `Action.NEEDS_WORK`
        :type action: Action
    Raises:
    -   ValueError: If the repository is not a Git repository
    -   ValueError: If the PR ID is not provided
    -   ValueError: If the action is not provided
    Returns:
    -   None
    """

    if not is_git_repo():
        raise ValueError(common_vars.not_a_git_repo)

    _id: str = validate_input(
        id, "Pull request id to review", common_vars.id_cannot_be_none
    )
    action_value: str = "none" if action == Action.NONE else action.value
    action: str = validate_input(
        action_value,
        "Action [approve|unapprove|needs_work]",
        "'--action' is a mandatory argument, run 'bb pr review --help' for more info",
    )
    review_pull_request(_id, action)


@_pr.command(help="Merge a pull request")
@error_handler
def merge(
    id: str = typer.Option("", help="pull request number to merge"),
    delete_source_branch: bool = typer.Option(
        False, help="deletes source branch after merge"
    ),
    rebase: bool = typer.Option(
        False, help="rebase source branch with target before merge"
    ),
    yes: bool = typer.Option(False, help=common_vars.skip_prompt),
) -> None:
    """
    Merges a pull request with options to delete the source branch, rebase before merging, and skip prompts.
    Args:
    -   :param id: A string representing the pull request number to merge
        :type id: str
    -   :param delete_source_branch: A boolean option that determines whether the source branch should
        be deleted after the merge operation is completed.
        :type delete_source_branch: bool
    -   :param rebase: A  boolean option that determines whether the source branch should be rebased with
        the target branch before merging the pull request.
        :type rebase: bool
    -   :param yes: A  boolean flag that determines whether to skip any prompts or
        confirmations during the merge process.
        :type yes: bool
    Raises:
    -   ValueError: If the repository is not a Git repository
    -   ValueError: If the PR ID is not provided
    Returns:
    -   None
    """

    if not is_git_repo():
        raise ValueError(common_vars.not_a_git_repo)
    _id: str = validate_input(
        id, "Pull request id to merge", common_vars.id_cannot_be_none
    )
    merge_pull_request(_id, delete_source_branch, rebase, yes)


@_pr.command(help="View changes in a pull request")
@error_handler
def diff(
    id: str = typer.Option("", help="pull request number to show diff"),
) -> None:
    """
    Takes a pull request number as input and shows the diff for that pull request.
    Args:
    -   :param id: The `diff` function takes an optional `id` parameter, which is a string representing the
        pull request number to show the diff for
    -   :type id: str
    Raises:
    -   ValueError: If the repository is not a Git repository
    -   ValueError: If the PR ID is not provided
    Returns:
    -   None
    """

    if not is_git_repo():
        raise ValueError(common_vars.not_a_git_repo)
    _id: str = validate_input(
        id, "Pull request number to show diff", common_vars.id_cannot_be_none
    )
    show_diff(_id)


@_pr.command(help="Copy pull request url to clipboard")
@error_handler
def copy(id: str = typer.Option("", help="pull request number to copy")) -> None:
    """
    Copies a specified pull request in a Git repository.
    Args:
    -   :param id: Used to specify the pull request number that needs to be copied
        to clipboard
        :type id: str
    Raises:
    -   ValueError: If the repository is not a Git repository
    -   ValueError: If the PR ID is not provided
    Returns:
    -   None
    """

    if not is_git_repo():
        raise ValueError(common_vars.not_a_git_repo)

    _id: str = validate_input(
        id, "Pull request number to copy", common_vars.id_cannot_be_none
    )
    copy_pull_request(_id)


@_pr.command(help="View a pull request")
@error_handler
def view(
    id: str = typer.Option("", help="pull request id to view"),
    web: Optional[bool] = typer.Option(False, help="view pull request in browser"),
) -> None:
    """
    Takes a pull request ID as input and allows the user to view the pull request either
    in the terminal or in a web browser.
    Args:
    -   :param id: The `id` parameter is a string that represents the pull request ID to view
        :type id: str
    -   :param web: A  boolean flag that determines whether to view the pull request
        in a web browser.
        :type web: Optional[bool]
    Raises:
    -   ValueError: If the repository is not a Git repository
    -   ValueError: If the PR ID is not provided
    -   ValueError: If the PR is not viewable in the terminal or browser
    Returns:
    -   None
    """

    if not is_git_repo():
        raise ValueError(common_vars.not_a_git_repo)
    _id = validate_input(id, "Pull request id to view", common_vars.id_cannot_be_none)
    view_pull_request(_id, web)
