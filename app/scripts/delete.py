# -*- coding: utf-8 -*-
""""
    app.scripts.delete
"""
import json

from typer import prompt
from typer import echo
from typer import Exit

from app.utils import iniparser
from app.utils import command
from app.utils import request
from app.utils import api
from app.utils import richprint


def delete_pull_request(target: list, yes: bool, diff: bool) -> None:
    """Delete pull requests by id"""
    username, token, bitbucket_host = iniparser.parse()
    project, repository = command.base_repo()
    for no in target:
        url = api.pull_request_delete(bitbucket_host, project, repository, no)
        pull_request_info = request.get_response(url, username, token)

        header = {
            'SUMMARY': ['dim'],
            'DESCRIPTION': ['dim']
        }

        summary = {
            "ID": pull_request_info[1]['id'],
            "Description": pull_request_info[1]['description'],
            "From Branch": pull_request_info[1]['fromRef']['displayId'],
            "To Branch": pull_request_info[1]['toRef']['displayId'],
            "Url": pull_request_info[1]['links']['self'][0]['href']
        }

        richprint.to_console(header, summary, True)

        if diff:
            from app.scripts.diff import show_diff
            diff_url = api.pull_request_diffrence(bitbucket_host, project, repository, no)
            show_diff(diff_url)

        if yes or prompt("\nProceed [y/n]").lower().strip() == 'y':
            echo(f"\u1405 Contacting {bitbucket_host} ...")
            body = json.dumps({"version": int(pull_request_info[1]['version'])})
            pull_request = request.delete_request(url, username, token, body)

            if pull_request == 204:
                richprint.to_console(header, {'\u2705 PR Deleted': pull_request_info[1]['links']['self'][0]['href']},
                                     False)
            else:
                echo("\u274C Error deleting pull request")
                raise Exit(code=1)
