# -*- coding: utf-8 -*-

import json

from bb.utils.api import bitbucket_api
from bb.utils.request import post
from bb.utils.richprint import console, live_progress


def create_repository(
    project: str, repo: str, forkable: bool, default_branch: str
) -> None:
    with live_progress(f"Creating '{project}/{repo}' Repository ... ") as live:
        request = post(
            bitbucket_api.create_repo(project),
            json.dumps(
                {
                    "name": repo,
                    "slug": repo,
                    "scmId": "git",
                    "forkable": forkable,
                    "project": {"key": project},
                    "defaultBranch": f"refs/heads/{default_branch}",
                }
            ),  # type: ignore
        )

        if request[0] == 200:
            live.update(console.print("DONE", style="bold green"))

        if request[0] == 409:
            live.update(console.print("CONFLICT", style="bold yellow"))
            console.print(
                f"Message: {request[1]['errors'][0]['message']}",
                highlight=True,
                style="bold yellow",
            )
