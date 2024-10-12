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

import json

from typer import Exit, confirm

from bb.utils.api import bitbucket_api
from bb.utils.request import put
from bb.utils.richprint import console, live_progress


def archive_repository(project: str, repo: str, archive: bool) -> None:
    """
    Archives or unarchives a repository.

    Args:
        project (str): The name of the project.
        repo (str): The name of the repository.
        archive (bool): If True, the repository will be archived. If False, the repository will be unarchived.

    Raises:
        Exit: If the user does not confirm the action.

    Returns:
        None
    """

    if not confirm(
        f"Proceed to {'archive' if archive else 'unarchive'} '{project}/{repo}'?"
    ):
        raise Exit(code=1)

    with live_progress(
        f"{'Archiving' if archive else 'Unarchiving' } Repository '{project}/{repo}' ... "
    ) as live:
        request = put(
            bitbucket_api.delete_repo(project, repo),
            json.dumps({"archived": archive}),  # type: ignore
        )

        if request[0] == 200:
            live.update(console.print("DONE", style="bold green"))

        if request[0] in (403, 409):
            live.update(console.print("CONFLICT", style="bold yellow"))
            console.print(
                f"Message: {request[1]['errors'][0]['message']}",
                highlight=True,
                style="bold yellow",
            )
