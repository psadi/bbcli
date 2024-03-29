# -*- coding: utf-8 -*-

"""
    bb.pr.diff - shows the diffrence in pull requests which is already raised
    TODO: show the diff contents for each file
"""

from bb.utils import cmnd, request, richprint
from bb.utils.api import bitbucket_api


def show_diff(_id: str) -> None:
    """
    Display the diff from remote pull request
    to the console applicable for create and delete actions
    """
    project, repository = cmnd.base_repo()
    with richprint.live_progress("Fetching Contents from Pull Request ..."):
        response = request.get(
            bitbucket_api.pull_request_difference(project, repository, _id),
        )[1]

        pr_info = request.get(
            bitbucket_api.pull_request_info(project, repository, _id),
        )[1]

    header = [
        ("HASH", "bold white"),
        ("FILE", "bold white"),
        ("TYPE", "bold yellow"),
    ]
    value_args = [
        (
            f"[bold red]{response['fromHash'][:11]}[/bold red] - [bold green]{response['toHash'][:11]}[/bold green]",
            i["path"]["toString"],
            f"{i['type']}",
        )
        for i in response["values"]
    ]
    table = richprint.table(header, value_args, True)
    richprint.console.print(table)

    cmnd.show_git_diff(
        f"origin/{pr_info['fromRef']['displayId']}",
        f"origin/{pr_info['toRef']['displayId']}",
    )
