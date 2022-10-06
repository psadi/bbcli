# -*- coding: utf-8 -*-

# Importing the modules from the bb.utils package.
from bb.utils import cmnd, request, iniparser, richprint, api


def show_diff(id: int) -> None:
    """
    Display the diff from remote pull request to the console applicable for create and delete actions
    """
    username, token, bitbucket_host = iniparser.parse()
    project, repository = cmnd.base_repo()
    url = api.pull_request_difference(bitbucket_host, project, repository, id)
    with richprint.live_progress(f"Fetching Contents from Pull Request ..."):
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
