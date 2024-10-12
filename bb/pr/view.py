# -*- coding: utf-8 -*-

############################################################################
# Bitbucket CLI (bb): Work seamlessly with Bitbucket from the command line
#
# Copyright (C) 2022  P S, Adithya (psadi) (ps.adithya@icloud.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################

"""
bb.pr.view open the pull request in browser
"""

import webbrowser

from bb.utils.api import bitbucket_api
from bb.utils.cmnd import base_repo
from bb.utils.request import get
from bb.utils.richprint import console, live_progress, table


def view_pull_request(_id: str, web: bool) -> None:
    """
    Fetches information about a pull request and displays it.

    Args:
        _id (str): The ID of the pull request.
        web (bool): Flag indicating whether to open the pull request in the default browser.

    Returns:
        None
    """
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
