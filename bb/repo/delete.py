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
bb.repo.delete - deletes a bitbucket repository
"""

from typer import Exit, confirm, prompt

from bb.utils.api import bitbucket_api
from bb.utils.request import delete as delete_request
from bb.utils.richprint import console, live_progress


def delete_repository(project: str, repo: str) -> None:
    """
    Deletes a Bitbucket repository.

    Args:
        project (str): The project key or ID.
        repo (str): The repository slug or ID.

    Raises:
        Exit: If the user cancels the deletion.

    """
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

    with live_progress(f"Deleting Repository '{project}/{repo}' ... ") as live:
        request = delete_request(
            bitbucket_api.delete_repo(project, repo),
            {},
        )

        if request == 202:
            live.update(console.print("DONE", style="bold green"))
