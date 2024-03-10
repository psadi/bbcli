# -*- coding: utf-8 -*-

"""
    bb.pr.view open the pull request in browser
"""

import webbrowser

from bb.utils.api import bitbucket_api
from bb.utils.cmnd import base_repo
from bb.utils.request import get
from bb.utils.richprint import console, live_progress, table


def view_pull_request(_id: str, web: bool) -> None:
    """view a pull request in terminal or in a browser"""
    with live_progress(f"Fetching info on pr #{_id} ... ") as live:
        project, repository = base_repo()
        url = get(bitbucket_api.pull_request_info(project, repository, _id))
        live.update(console.print("DONE", style="bold green"))

    if web:
        with live_progress(f"Opening pr #{_id} in default browser ... ") as live:
            try:
                to_broweser = webbrowser.open_new(url[1]["links"]["self"][0]["href"])
                if to_broweser is False:
                    raise ValueError("Unable to open pr in browser")
                live.update(console.print("DONE", style="bold green"))
            except ValueError as err:
                live.update(console.print("ERROR", style="bold red"))
                console.print(f"Message: {err}", style="dim white")

    else:
        console.print(
            f"PR #({url[1]['id']}): {url[1]['fromRef']['displayId']}"
            + " -> "
            + f"{url[1]['toRef']['displayId']}",
            style="bold white",
        )

        console.print(
            table(
                ["_", "_"],
                [
                    ("Title", url[1]["title"]),
                    (
                        "Description",
                        (
                            url[1]["description"]
                            if "description" in url[1].keys()
                            else "-"
                        ),
                    ),
                    ("State", url[1]["state"]),
                ],
                False,
            )
        )
        console.print("Authored by:", style="bold white", new_line_start=True)
        console.print(
            table(
                ["_", "_"],
                [
                    ("ID", url[1]["author"]["user"]["name"]),
                    ("Name", url[1]["author"]["user"]["displayName"]),
                    ("Email", url[1]["author"]["user"]["emailAddress"]),
                ],
                False,
            )
        )
