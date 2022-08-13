#-*- coding: utf-8 -*-

# Importing the modules from the bb.utils package.
from bb.utils import (
    cmnd,
    request,
    iniparser,
    richprint,
    api
)

def show_diff(id: int) -> None:
    """
    > display the diff from remote pull request to the console applicable for create and delete actions

    The function takes a single argument, `url`, which is a string. The function returns `None`

    :param url: the url of the pull request
    :type url: str
    """
    username, token, bitbucket_host = iniparser.parse()
    project, repository = cmnd.base_repo()
    url = api.pull_request_diffrence(bitbucket_host, project, repository, id)
    with richprint.live_progress(f"Fetching Contents from Pull Request ..."):
        response = request.get_response(url, username, token)[1]

    header = [
        ('FROM HASH', 'bold red'),
        ('TO HASH', 'bold green'),
        ('FILE', 'bold white'),
        ('TYPE', 'bold yellow')
    ]

    value_args = []
    for i in response['values']:
        value_args.append((f"{response['fromHash'][0:11]}", f"{response['toHash'][0:11]}", i['path']['toString'], f"{i['type']}"))

    table = richprint.table(header, value_args, True)
    richprint.console.print(table)
