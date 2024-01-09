# -*- coding: utf-8 -*-

"""
    bb.repo.delete - deletes a bitbucket repository
"""
import json

from typer import Exit, confirm

from bb.utils.api import delete_repo
from bb.utils.ini import parse
from bb.utils.request import put
from bb.utils.richprint import console, live_progress


def archive_repository(project: str, repo: str, archive: bool) -> None:
    if not confirm(
        f"Proceed to {'archive' if archive else 'unarchive'} '{project}/{repo}'?"
    ):
        raise Exit(code=1)

    username, token, bitbucket_host = parse()
    with live_progress(
        f"{'Archiving' if archive else 'Unarchiving' } Repository '{project}/{repo}' ... "
    ) as live:
        request = put(
            delete_repo(bitbucket_host, project, repo),
            username,
            token,
            json.dumps({"archived": archive}),  # type: ignore
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
