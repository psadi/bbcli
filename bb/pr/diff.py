# -*- coding: utf-8 -*-

"""
    bb.pr.diff - shows the diffrence in pull requests which is already raised
    TODO: show the diff contents for each file
"""

from bb.utils import cmnd, request, ini, richprint, api


def show_diff(_id: str) -> None:
    """
    Display the diff from remote pull request
    to the console applicable for create and delete actions
    """
    username, token, bitbucket_host = ini.parse()
    project, repository = cmnd.base_repo()
    url = api.pull_request_difference(bitbucket_host, project, repository, _id)
    with richprint.live_progress("Fetching Contents from Pull Request ..."):
        response = request.get(url, username, token)[1]

    header = [
        ("FROM HASH", "bold red"),
        ("TO HASH", "bold green"),
        ("FILE", "bold white"),
        ("TYPE", "bold yellow"),
    ]

    value_args = []
    for i in response["values"]:
        value_args.append(
            (
                f"{response['fromHash'][0:11]}",
                f"{response['toHash'][0:11]}",
                i["path"]["toString"],
                f"{i['type']}",
            )
        )

    table = richprint.table(header, value_args, True)
    richprint.console.print(table)
