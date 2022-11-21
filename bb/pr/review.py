# -*- coding: utf-8 -*-

"""
    bb.pr.review marks a pull request as approved/unapproved or needs_work
    based on the pr id
"""

import json
from time import sleep
from bb.utils.iniparser import parse
from bb.utils.request import get, put
from bb.utils.richprint import live_progress, console
from bb.utils.cmnd import base_repo
from bb.utils.api import whoami, action_pull_request


def review_pull_request(target: int, action: str) -> None:
    """
    It takes a target (pull request number) and an action (approve, unapprove, needs_work) and then
    performs the action on the pull request
    """
    username, token, bitbucket_host = parse()

    action_mapper = {
        "approve": ["APPROVED", "Approving", "green"],
        "unapprove": ["UNAPPROVED", "Unapproving", "red"],
        "needs_work": ["NEEDS_WORK", "Work Required on", "yellow"],
    }

    with live_progress(
        f"{action_mapper[action][1]} pull request '{target}' ... "
    ) as live:
        user_id = get(whoami(bitbucket_host), username, token)
        project, repository = base_repo()
        action_data = action_pull_request(
            bitbucket_host, project, repository, target, user_id[1]
        )
        body = json.dumps({"status": action_mapper[action][0]})
        put(action_data, username, token, body)
        sleep(0.4)
        live.update(
            console.print(f"{action_mapper[action][0]}", style=action_mapper[action][2])
        )
