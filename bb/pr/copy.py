# -*- coding: utf-8 -*-

"""
    bb.pr.copy - fetches the pull request from url and copies then to user
    clipboard
"""

from bb.utils import cmnd, ini, request, richprint
from bb.utils.api import bitbucket_api


def copy_pull_request(_id: str) -> None:
    """
    Copy the pull request to user clipboard for convenience
    """
    with richprint.live_progress("Fetching pull request url ... ") as live:
        username: str
        token: str
        bitbucket_host: str
        project: str
        repository: str
        username, token, bitbucket_host = ini.parse()
        project, repository = cmnd.base_repo()
        url: str = request.get(
            bitbucket_api.pull_request_info(bitbucket_host, project, repository, _id),
            username,
            token,
        )[1]["links"]["self"][0]["href"]
        cmnd.cp_to_clipboard(url)
        live.update(richprint.console.print("COPIED", style="bold green"))
    richprint.str_print(
        "Tip: Pull request url is copied to clipboard ('ctrl+v' to paste)",
        "dim white",
    )
