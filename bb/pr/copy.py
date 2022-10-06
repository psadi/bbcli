# -*- coding: utf-8 -*-

from bb.utils import api, request, iniparser, cmnd, cp, richprint


def copy_pull_request(id: int) -> None:
    with richprint.live_progress(f"Fetching pull request url ... ") as live:
        username, token, bitbucket_host = iniparser.parse()
        project, repository = cmnd.base_repo()
        url = request.get(
            api.pull_request_info(bitbucket_host, project, repository, id),
            username,
            token,
        )
        cp.copy_to_clipboard(url[1]["links"]["self"][0]["href"])
        live.update(richprint.console.print("DONE", style="bold green"))
    richprint.str_print(
        "Tip: Pull request url is copied to clipboard ('ctrl+v' to paste)",
        "dim white",
    )
