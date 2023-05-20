# -*- coding: utf-8 -*-

"""
    bb.pr.diff - shows the diffrence in pull requests which is already raised
    TODO: show the diff contents for each file
"""

from bb.utils import api, cmnd, ini, request, richprint


def show_diff(_id: str) -> None:
    """
    Display the diff from remote pull request
    to the console applicable for create and delete actions
    """
    username, token, bitbucket_host = ini.parse()
    project, repository = cmnd.base_repo()
    with richprint.live_progress("Fetching Contents from Pull Request ..."):
        response = request.get(
            api.pull_request_difference(bitbucket_host, project, repository, _id),
            username,
            token,
        )[1]

        pr_info = request.get(
            api.pull_request_info(bitbucket_host, project, repository, _id),
            username,
            token,
        )[1]

    header = [
        ("FROM HASH", "bold red"),
        ("TO HASH", "bold green"),
        ("FILE", "bold white"),
        ("TYPE", "bold yellow"),
    ]

    value_args = [
        (
            f"{response['fromHash'][:11]}",
            f"{response['toHash'][:11]}",
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
