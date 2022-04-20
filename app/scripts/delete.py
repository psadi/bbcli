#-*- coding: utf-8 -*-
""""
    app.scripts.delete
"""
import json

from typer import (
    prompt,
    echo,
    Exit
)

from app.utils import (
    iniparser,
    command,
    request,
    api,
    richprint
)

def delete_pull_request(id: list, yes: bool, diff: bool) -> None:
    """Delete pull request"""
    username, token, bitbucket_host = iniparser.parse()
    project, repository = command.base_repo()
    for no in id:
        with richprint.live_progress(f"Fetching info on {no} ..."):
            url = api.pull_request_info(bitbucket_host, project, repository, no)
            pull_request_info = request.get_response(url, username, token)

            header = {
                'SUMMARY': 'bold yellow',
                'DESCRIPTION': '#FFFFFF'
            }

            summary = {
                "ID": pull_request_info[1]['id'],
                "Description" : pull_request_info[1]['description'],
                "From Branch" : pull_request_info[1]['fromRef']['displayId'],
                "To Branch" : pull_request_info[1]['toRef']['displayId'],
                "Url" : pull_request_info[1]['links']['self'][0]['href']
            }

        richprint.to_console(header, summary, True)

        if diff:
            from app.scripts.diff import show_diff
            diff_url = api.pull_request_diffrence(bitbucket_host, project, repository, no)
            show_diff(diff_url)

        if yes or prompt("\nProceed [y/n]").lower().strip() == 'y':
            with richprint.live_progress("Deleting Pull Request ..."):
                body = json.dumps({"version": int(pull_request_info[1]['version'])})
                pull_request = request.delete_request(url, username, token, body)

            if pull_request == 204:
                richprint.to_console(header, {'\u2705 PR Deleted': pull_request_info[1]['links']['self'][0]['href']}, False)
            else:
                echo("\u274C Error deleting pull request")
                raise Exit(code=1)
