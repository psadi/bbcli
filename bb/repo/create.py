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

import json

from bb.utils.api import bitbucket_api
from bb.utils.request import post
from bb.utils.richprint import console, live_progress


def create_repository(
    project: str, repo: str, forkable: bool, default_branch: str
) -> None:
    """
    Create a repository in Bitbucket.

    Args:
        project (str): The key of the project where the repository will be created.
        repo (str): The name of the repository.
        forkable (bool): Indicates whether the repository can be forked.
        default_branch (str): The name of the default branch for the repository.

    Returns:
        None
    """

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
