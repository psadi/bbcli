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
bb.pr.review marks a pull request as approved/unapproved or needs_work
based on the pr id
"""

import json
from time import sleep

from bb.utils.api import bitbucket_api
from bb.utils.cmnd import base_repo
from bb.utils.request import get, put
from bb.utils.richprint import console, live_progress


def review_pull_request(target: int, action: str) -> None:
    """
    Perform an action on a pull request.

    Args:
        target (int): The pull request number.
        action (str): The action to perform on the pull request.

    Returns:
        None
    """
    action_mapper = {
        "approve": ["APPROVED", "Approving", "green"],
        "unapprove": ["UNAPPROVED", "Unapproving", "red"],
        "needs_work": ["NEEDS_WORK", "Work Required on", "yellow"],
    }

    with live_progress(
        f"{action_mapper[action][1]} pull request '{target}' ... "
    ) as live:
        user_id = get(bitbucket_api.whoami())
        project, repository = base_repo()
        action_data = bitbucket_api.action_pull_request(
            project, repository, target, user_id[1]
        )
        body = json.dumps({"status": action_mapper[action][0]})
        put(action_data, body)
        sleep(0.4)
        live.update(
            console.print(f"{action_mapper[action][0]}", style=action_mapper[action][2])
        )
