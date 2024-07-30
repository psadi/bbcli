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
bb.pr.create - creates a pull request in bitbucket
while doing so it gathers all the facts required for a pr from the
remote and local repository
"""

from typing import Optional

from typer import confirm

from bb.pr.diff import show_diff
from bb.utils import cmnd, request, richprint
from bb.utils.api import bitbucket_api

def gather_facts(
    target: str,
    from_branch: str,
    project: str,
    repository: str,
    title: str,
    description: str,
) -> list:
    """
    It gathers facts for  the pull request from bitbucket and local git
    repository

    Args:
    -   target: str: The target branch
    -   from_branch: str: The source branch
    -   project: str: The project name
    -   repository: str: The repository name
    -   title: str: The title for the pull request
    -   description: str: The description for the pull request
    Returns:
    -   list: The list of reviewers
    Raises:
    -   ValueError: If the source and target branches are the same
    """

    with richprint.live_progress(f"Gathering facts on '{repository}' ..."):
        repo_id = None
        for repo in request.get(bitbucket_api.get_repo_info(project))[1]["values"]:
            if repo["name"] == repository:
                repo_id = repo["id"]

        reviewers = []
        if repo_id is not None:
            for dict_item in request.get(
                bitbucket_api.default_reviewers(project, repo_id, from_branch, target),
            )[1]:
                reviewers.extend(
                    {"user": {"name": dict_item[key]}}
                    for key in dict_item
                    if key == "name"
                )
    table = richprint.table(
        [("SUMMARY", "bold yellow"), ("DESCRIPTION", "#FFFFFF")],
        [
            ("Project", project),
            ("Repository", repository),
            ("Repository ID", str(repo_id)),
            ("From Branch", from_branch),
            ("To Branch", target),
            ("Title", title),
            ("Description", description),
        ],
        True,
    )
    richprint.console.print(table)
    return reviewers


def create_pull_request(target: str, yes: bool, diff: bool, rebase: bool, title: str, description: str) -> None:
    """
    Handles the process of creating a pull request with  options for rebasing,
    confirmation prompts, and displaying the diff.

    Args:
    -   target: str: The target branch
    -   yes: bool: The flag to proceed without confirmation
    -   diff: bool: The flag to display the diff
    -   rebase: bool: The flag to rebase the source branch with the target branch
    -   title: str: Optional title for the pull request. If not provided, it will be taken from the commit message
    -   description: str: Optional description for the pull request. If not provided, it will be taken from the commit message
    Raises:
    -   ValueError: If the source and target branches are the same
    Returns:
    -   None
    """
    _id: Optional[str] = None
    from_branch = cmnd.from_branch()
    if target == from_branch:
        raise ValueError("Source & target cannot be the same")

    if rebase:
        with richprint.live_progress(
            f"Rebasing '{from_branch}' with '{target}' ... "
        ) as live:
            cmnd.git_rebase(target)
            live.update(richprint.console.print("REBASED", style="bold green"))

    title, description = title or cmnd.title_and_description()[0], description or cmnd.title_and_description()[1]

    project, repository = cmnd.base_repo()
    
    reviewers = gather_facts(
        target,
        from_branch,
        project,
        repository,
        title,
        description
    )

    if yes or confirm("Proceed"):
        with richprint.live_progress("Creating Pull Request ..."):
            url = bitbucket_api.pull_request_create(project, repository)
            body = bitbucket_api.pull_request_body(
                title,
                description,
                from_branch,
                repository,
                project,
                target,
                reviewers,
            )
            pull_request = request.post(url, body)

        if pull_request[0] == 201:
            richprint.console.print(
                f"Pull Request Created: {pull_request[1]['links']['self'][0]['href']}",
                highlight=True,
                style="bold green",
            )
            _id = pull_request[1]["links"]["self"][0]["href"].split("/")[-1]
            cmnd.cp_to_clipboard(pull_request[1]["links"]["self"][0]["href"])
        elif pull_request[0] == 409:
            richprint.console.print(
                f"Message: {pull_request[1]['errors'][0]['message']}",
                highlight=True,
                style="bold red",
            )
            richprint.console.print(
                f"Existing Pull Request: {pull_request[1]['errors'][0]['existingPullRequest']['links']['self'][0]['href']}",
                highlight=True,
                style="bold yellow",
            )
            _id = pull_request[1]["errors"][0]["existingPullRequest"]["links"]["self"][
                0
            ]["href"].split("/")[-1]
            cmnd.cp_to_clipboard(
                pull_request[1]["errors"][0]["existingPullRequest"]["links"]["self"][0][
                    "href"
                ]
            )
        else:
            raise ValueError(request.http_response_definitions(pull_request[0]))

        richprint.str_print(
            "Hint: Pull request url is copied to clipboard ('ctrl+v' to paste)",
            "dim white",
        )

    if _id and (
        diff
        or confirm(f"Review diff between '{from_branch}' -> '{target}' in PR #{_id}?")
    ):
        show_diff(_id)
