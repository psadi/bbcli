# -*- coding: utf-8 -*-

"""
    bb.pr.copy - fetches the pull request from url and copies then to user
    clipboard
"""

from bb.utils import api, request, iniparser, cmnd, cp, richprint


def copy_pull_request(_id: int) -> None:
    """
    Copy the pull request to user clipboard for convenience
    """
    with richprint.live_progress("Fetching pull request url ... ") as live:
        username, token, bitbucket_host = iniparser.parse()
        project, repository = cmnd.base_repo()
        url = request.get(
            api.pull_request_info(bitbucket_host, project, repository, _id),
            username,
            token,
        )
        cp.copy_to_clipboard(url[1]["links"]["self"][0]["href"])
        live.update(richprint.console.print("DONE", style="bold green"))
