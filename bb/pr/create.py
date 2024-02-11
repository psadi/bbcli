# -*- coding: utf-8 -*-

"""
    bb.pr.create - creates a pull request in bitbucket
    while doing so it gathers all the facts required for a pr from the
    remote and local repository
"""

from typing import Optional

from typer import confirm

from bb.pr.diff import show_diff
from bb.utils import cmnd, ini, request, richprint
from bb.utils.api import bitbucket_api


def gather_facts(
    target: str,
    from_branch: str,
    project: str,
    repository: str,
    title_and_description: str,
) -> list:
    """
    It gathers facts for  the pull request from bitbucket and local git
    repository
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
            ("Title", title_and_description[0]),
            ("Description", title_and_description[1]),
        ],
        True,
    )
    richprint.console.print(table)
    return reviewers


def create_pull_request(target: str, yes: bool, diff: bool, rebase: bool) -> None:
    """
    It creates a pull request.
    """

    _id: Optional[str] = None
    username, token, bitbucket_host = ini.parse()
    from_branch = cmnd.from_branch()
    if target == from_branch:
        raise ValueError("Source & target cannot be the same")

    if rebase:
        with richprint.live_progress(
            f"Rebasing {from_branch} with {target} ... "
        ) as live:
            cmnd.git_rebase(target)
            live.update(richprint.console.print("REBASED", style="bold green"))

    project, repository = cmnd.base_repo()
    title_and_description = cmnd.title_and_description()
    reviewers = gather_facts(
        target,
        from_branch,
        project,
        repository,
        title_and_description,
    )

    if yes or confirm("Proceed"):
        with richprint.live_progress("Creating Pull Request ..."):
            url = bitbucket_api.pull_request_create(project, repository)
            body = bitbucket_api.pull_request_body(
                title_and_description,
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
            "Tip: Pull request url is copied to clipboard ('ctrl+v' to paste)",
            "dim white",
        )

    if _id and (
        diff
        or confirm(f"Review diff from '{from_branch}' -> to '{target}' in PR #{_id}?")
    ):
        show_diff(_id)
