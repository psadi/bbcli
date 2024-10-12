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
bb.pr.copy - fetches the pull request from url and copies then to user
clipboard
"""

from bb.utils import cmnd, request, richprint
from bb.utils.api import bitbucket_api


def copy_pull_request(_id: str) -> None:
    """
    Fetches the URL of a pull request from a Bitbucket repository, copies it to the
    clipboard, and provides a hint for pasting it.

    Args:
    -   :param _id: The `_id` parameter in the `copy_pull_request` function is a string that represents the
        unique identifier of a pull request. This identifier is used to fetch the pull request URL from a
        Bitbucket repository
        :type _id: str
    Raises:
    -   :raises: This function does not raise any exceptions
    Returns:
    -   :rtype: None
    """
    with richprint.live_progress("Fetching pull request url ... ") as live:
        project: str
        repository: str
        project, repository = cmnd.base_repo()
        url: str = request.get(
            bitbucket_api.pull_request_info(project, repository, _id),
        )[1]["links"]["self"][0]["href"]
        cmnd.cp_to_clipboard(url)
        live.update(richprint.console.print("COPIED", style="bold green"))
    richprint.str_print(
        "Hint: Pull request url is copied to clipboard ('ctrl+v' to paste)",
        "dim white",
    )
