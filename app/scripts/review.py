#-*- coding: utf-8 -*-

""""
    app.scripts.review
"""

import json
from time import sleep
from app.utils.iniparser import parse
from app.utils.request import (
    get_response,
    put_request
)
from app.utils.richprint import (
    live_progress,
    console
)
from app.utils.command import base_repo
from app.utils.api import (
    whoami,
    action_pull_request
)

def review_pull_request(target: int, action: str) -> None:
    username, token, bitbucket_host = parse()

    action_mapper = {
        "approve": ["APPROVED", "Approving", "bold white on #00875a"],
        "unapprove": ["UNAPPROVED", "Unapproving", "bold white on #de350b"],
        "needs_work": ["NEEDS_WORK", "Work Required on", "bold white on #ffab00"],
    }

    with live_progress(f"{action_mapper[action][1]} pull request '{target}' ... ") as live:
        user_id = (get_response(whoami(bitbucket_host), username, token))
        project, repository = base_repo()
        action_data = action_pull_request(bitbucket_host, project, repository, target, user_id[1])
        body = json.dumps({"status": action_mapper[action][0]})
        put_request(action_data, username, token, body)
        sleep(0.4)
        live.update(console.print(f'{action_mapper[action][0]}', style=action_mapper[action][2]))
