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
bb.pr.diff - shows the diffrence in pull requests which is already raised
TODO: show the diff contents for each file
"""

from bb.utils import cmnd, request, richprint
from bb.utils.api import bitbucket_api


def show_diff(_id: str) -> None:
    """
    Shows the difference in the pull request which is already raised

    Args:
    - _id: str: The pull request id
    Raises:
    - ValueError: If the pull request cannot be fetched
    Returns:
    - None
    """
    project, repository = cmnd.base_repo()
    with richprint.live_progress("Fetching Contents from Pull Request ..."):
        response = request.get(
            bitbucket_api.pull_request_difference(project, repository, _id),
        )[1]

        pr_info = request.get(
            bitbucket_api.pull_request_info(project, repository, _id),
        )[1]

    header = [
        ("HASH", "bold white"),
        ("FILE", "bold white"),
        ("TYPE", "bold yellow"),
    ]
    value_args = [
        (
            f"[bold red]{response['fromHash'][:11]}[/bold red] :arrow_right: [bold green]{response['toHash'][:11]}[/bold green]",
            i["path"]["toString"],
            f"{i['type']}",
        )
        for i in response["values"]
    ]
    table = richprint.table(header, value_args, True)
    richprint.console.print(table)

    cmnd.show_git_diff(
        f"origin/{pr_info['fromRef']['displayId']}",
        f"origin/{pr_info['toRef']['displayId']}",
    )
