#-*- coding: utf-8 -*-

# Importing the necessary modules for the script to run.
import json
from typer import (
    prompt,
    Exit
)
from bb.utils import (
    cmnd,
    iniparser,
    request,
    api,
    richprint
)

from bb.pr.diff import show_diff

def delete_pull_request(id: list, yes: bool, diff: bool) -> None:
    """
    Delete pull request(s) by ID

    :param id: list
    :type id: list
    :param yes: bool
    :type yes: bool
    :param diff: bool
    :type diff: bool
    """
    username, token, bitbucket_host = iniparser.parse()
    project, repository = cmnd.base_repo()

    for no in id:
        with richprint.live_progress(f"Fetching info on {no} ..."):
            url = api.pull_request_info(bitbucket_host, project, repository, no)
            pull_request_info = request.get_response(url, username, token)

            header = [
                ('SUMMARY', 'bold yellow'),
                ('DESCRIPTION', '#FFFFFF')
            ]

            summary = [
                ("ID", str(pull_request_info[1]['id'])),
                ("State", pull_request_info[1]['state']),
                ("From Branch" , pull_request_info[1]['fromRef']['displayId']),
                ("To Branch" , pull_request_info[1]['toRef']['displayId']),
                ("Title & Description" , pull_request_info[1]['description'])
            ]

        table = richprint.table(header, summary, True)
        richprint.console.print(table)

        if diff:
            show_diff(no)

        if yes or prompt("Proceed [y/n]").lower().strip() == 'y':
            with richprint.live_progress("Deleting Pull Request ..."):
                body = json.dumps({"version": int(pull_request_info[1]['version'])})
                pull_request = request.delete_request(url, username, token, body)

            if pull_request != 204:
                richprint.console.print('Error deleting pull request', style='red')
                raise Exit(code=1)

            richprint.console.print(f"Pull Request Deleted: {pull_request_info[1]['links']['self'][0]['href']}", highlight=True, style='bold green')
