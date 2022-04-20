#-*- coding: utf-8 -*-
""""
    app.scripts.diff
"""
from app.utils import (
    request,
    iniparser,
    richprint,
    api,
    command
)

def get_diff_url(id: int) -> str:
    username, token, bitbucket_host = iniparser.parse()
    project, repository = command.base_repo()
    url = api.pull_request_diffrence(bitbucket_host, project, repository, id)
    show_diff(url)

def show_diff(url: str) -> None:
    """
        display the diff from remote pull request to the console
        applicable for create and delete actions
    """

    username, token, bitbucket_host = iniparser.parse()
    with richprint.live_progress(f"Fetching Contents from Pull Request ..."):
        response = request.get_response(url, username, token)[1]['values']

    header = {
        'TYPE': 'bold white',
        'CONTENT': 'white'
    }

    value_args = {}

    for i in response:
        value_args.update({i['type'] : i['path']['toString']})

    richprint.to_console(header, value_args, True)
