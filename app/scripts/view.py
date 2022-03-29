# -*- coding: utf-8 -*-
""""
    app.scripts.view
"""
import typer
from typer import Exit

from app.utils import api
from app.utils import iniparser
from app.utils import command
from app.utils import request
from app.utils import richprint


def to_richprint(repository: str, pr_repo_dict: dict, header: dict) -> None:
    echo(f"\u1405 Repository: {repository}")
    for status, data in pr_repo_dict.items():
        echo(f"\u1405 Status: {status}")
        for elements in data:
            richprint.to_console(header, elements, False)


def view_pull_request(role: str, all: bool) -> None:
    """
        Shows the list of pull requests authored and pull requests reviewing
    """

    username, token, bitbucket_host = iniparser.parse()
    request_url = api.pull_request_viewer(bitbucket_host, role)
    request_repsonse = request.get_response(request_url, username, token)
    repository = command.base_repo()[1]

    repo_dict = {}
    if request_repsonse[0] == 200:
        for pr in request_repsonse[1]['values']:
            repo = f"{pr['fromRef']['repository']['slug']}"
            if repo not in repo_dict.keys():
                repo_dict.update({repo: {}})
                if pr['state'] not in repo_dict[repo].values():
                    repo_dict.update({repo: {pr['state']: []}})
            temp_dict = {'Tittle': pr['title'], 'From Branch': pr['fromRef']['displayId'],
                         'To Branch': pr['toRef']['displayId'], 'URL': pr['links']['self'][0]['href']}
            repo_dict[repo][pr['state']].append(temp_dict)

        header = {
            'SUMMARY': ['dim'],
            'DESCRIPTION': ['dim']
        }

        for key, values in repo_dict.items():
            if key.lower() == repository.lower() and not all:
                to_richprint(key, values, header)
            elif all:
                to_richprint(key, values, header)
            else:
                Exit(code=0)
