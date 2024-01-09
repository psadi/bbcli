# -*- coding: utf-8 -*-

"""
    bb.repo.delete - deletes a bitbucket repository
"""

from typer import Exit, confirm, prompt

from bb.utils.api import delete_repo
from bb.utils.ini import parse
from bb.utils.request import delete as delete_request
from bb.utils.richprint import console, live_progress


def delete_repository(project: str, repo: str) -> None:
    console.print(
        """
Note: Deleting this repository cannot be undone.
If you don't have a backup, [red]you'll permanently lose its contents and pull requests.[/red]
If you prefer, you can archive this repository instead via [blue]'bb repo archive'[/blue] command
            """,
        style="bold yellow",
    )
    confirm_input = prompt(
        f"To go ahead and delete this repository, type '{project}/{repo}'",
    )

    if not (
        (confirm_input == f"{project}/{repo}")
        and (confirm("This action can't be undone, Proceed ?"))
    ):
        raise Exit(code=1)

    username, token, bitbucket_host = parse()
    with live_progress(f"Deleting Repository '{project}/{repo}' ... ") as live:
        request = delete_request(
            delete_repo(bitbucket_host, project, repo), username, token, {}
        )

        if request == 202:
            live.update(console.print("DONE", style="bold green"))
