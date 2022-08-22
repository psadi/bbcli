# -*- coding: utf-8 -*-

# Importing the necessary modules for the script to run.
from pygments import highlight
import pyperclip as pc
from typer import prompt, Exit
from bb.pr.diff import show_diff
from bb.utils import cmnd, iniparser, request, api, richprint


def copy_to_clipboard(url: str) -> None:
    """
    Copy the pull request to user clipboard for convinience

    """
    try:
        pc.copy(url)
        pc.paste()
    except Exception:  # Dosent work on VM's so we skip the exception if not available
        pass


def gather_facts(
    target: str,
    from_branch: str,
    project: str,
    repository: str,
    username: str,
    token: str,
    bitbucket_host: str,
    title_and_description: str,
) -> list:
    """
    It gathers facts for  the pull request from bitbucket and local git
    repository
    """

    with richprint.live_progress(f"Gathering facts on '{repository}' ..."):
        repo_id = None
        for repo in request.get(
            api.get_repo_info(bitbucket_host, project), username, token
        )[1]["values"]:
            if repo["name"] == repository:
                repo_id = repo["id"]

        reviewers = []
        if repo_id is not None:
            for dict_item in request.get(
                api.default_reviewers(
                    bitbucket_host, project, repo_id, from_branch, target
                ),
                username,
                token,
            )[1]:
                for key in dict_item:
                    if key == "name":
                        reviewers.append({"user": {"name": dict_item[key]}})

        header = [("SUMMARY", "bold yellow"), ("DESCRIPTION", "#FFFFFF")]

        summary = [
            ("Project", project),
            ("Repository", repository),
            ("Repository ID", str(repo_id)),
            ("From Branch", from_branch),
            ("To Branch", target),
            ("Title & Description", title_and_description),
        ]

    table = richprint.table(header, summary, True)
    richprint.console.print(table)
    return [header, reviewers]


def create_pull_request(target: str, yes: bool, diff: bool) -> None:
    """
    It creates a pull request.
    """
    from_branch = cmnd.from_branch()
    if target == from_branch:
        raise Exit(code=1)

    username, token, bitbucket_host = iniparser.parse()
    project, repository = cmnd.base_repo()
    title_and_description = cmnd.title_and_description()
    header, reviewers = gather_facts(
        target,
        from_branch,
        project,
        repository,
        username,
        token,
        bitbucket_host,
        title_and_description,
    )

    if yes or prompt("Proceed [y/n]").lower().strip() == "y":
        with richprint.live_progress(f"Creating Pull Request ..."):
            url = api.pull_request_create(bitbucket_host, project, repository)
            body = api.pull_request_body(
                title_and_description,
                from_branch,
                repository,
                project,
                target,
                reviewers,
            )
            pull_request = request.post(url, username, token, body)

        if pull_request[0] == 201:
            richprint.console.print(
                f"Pull Request Created: {pull_request[1]['links']['self'][0]['href']}",
                highlight=True,
                style="bold green",
            )
            id = pull_request[1]["links"]["self"][0]["href"].split("/")[-1]
            copy_to_clipboard(pull_request[1]["links"]["self"][0]["href"])
            richprint.str_print(
                "Tip: Pull request url is copied to clipboard ('ctrl+v' to paste)",
                "dim white",
            )
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
            id = pull_request[1]["errors"][0]["existingPullRequest"]["links"]["self"][
                0
            ]["href"].split("/")[-1]
            copy_to_clipboard(
                pull_request[1]["errors"][0]["existingPullRequest"]["links"]["self"][0][
                    "href"
                ]
            )
            richprint.str_print(
                "Tip: Pull request url is copied to clipboard ('ctrl+v' to paste)",
                "dim white",
            )
        else:
            request.http_response_definitions(pull_request[0])
            raise Exit(code=1)

    if diff:
        show_diff(id)
