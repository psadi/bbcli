# -*- coding: utf-8 -*-

"""
    bb.pr.copy - fetches the pull request from url and copies then to user
    clipboard
"""

from typing import Dict
from bb.utils import api, request, ini, cmnd, cp, richprint


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
            api.pull_request_info(bitbucket_host, project, repository, _id),
            username,
            token,
        )[1]["links"]["self"][0]["href"]
        live.update(richprint.console.print("COPIED", style="bold green"))
        cp.copy_to_clipboard(url)
