#-*- coding: utf-8 -*-
""""
    app.scripts.create
"""

import pyperclip as pc
from typer import prompt
from typer import echo
from typer import Exit
from app.utils import iniparser
from app.utils import command
from app.utils import request
from app.utils import api
from app.utils import richprint

def copy_to_clipboard(url: str) -> None:
    """Copy the pull request to user clipboard for convinience"""
    try:
        pc.copy(url)
        pc.paste()
    except: # Dosent work on VM's so we skip the exception if not available
        pass

def create_pull_request(target: str, yes: bool, diff: bool) -> None:
    """Create pull request"""
    username, token, bitbucket_host = iniparser.parse()
    project, repository = command.base_repo()
    title_and_description = command.title_and_description()
    from_branch = command.from_branch()

    if target == from_branch:
        raise Exit()

    repo_id = None
    for repo in request.get_response(api.get_repo_info(bitbucket_host, project), username, token)[1]['values']:
        if repo['name'] == repository:
            repo_id = repo['id']

    reviewers = []
    if repo_id is not None:
        for dict_item in request.get_response(api.default_reviewers(bitbucket_host, project, repo_id, from_branch, target), username, token)[1]:
            for key in dict_item:
                if key == 'name':
                    reviewers.append({"user": {"name": dict_item[key]}})

    header = {
        'SUMMARY': ['dim'],
        'DESCRIPTION': ['dim']
    }

    summary = {
        "Project": project,
        "Repository" : repository,
        "Repository ID" : repo_id,
        "From Branch" : from_branch,
        "To Branch" : target,
        "Title & Description" : title_and_description
    }

    richprint.to_console(header, summary, True)

    if yes or prompt("\nProceed [y/n]").lower().strip() == 'y':
        echo(f"\u1405 Contacting {bitbucket_host} ...")

        url = api.pull_request_create(bitbucket_host, project, repository)
        body = api.pull_request_body(title_and_description, from_branch, repository, project, target, reviewers)
        pull_request = request.post_request(url, username, token, body)

        if pull_request[0] == 201:
            richprint.to_console(header, {'\u2705 PR Created': pull_request[1]['links']['self'][0]['href']}, False)
            pull_request_number = pull_request[1]['links']['self'][0]['href'].split('/')[-1]
            copy_to_clipboard(pull_request[1]['links']['self'][0]['href'])
        elif pull_request[0] == 409:
            richprint.to_console(header, {'\u26A1 existingPullRequest': pull_request[1]['errors'][0]['existingPullRequest']['links']['self'][0]['href']}, False)
            pull_request_number = pull_request[1]['errors'][0]['existingPullRequest']['links']['self'][0]['href'].split('/')[-1]
            copy_to_clipboard(pull_request[1]['errors'][0]['existingPullRequest']['links']['self'][0]['href'])
        else:
            request.http_response_definitions(pull_request[0])
            raise Exit(code=1)

    if diff:
        from app.scripts.diff import show_diff
        url = api.pull_request_diffrence(bitbucket_host, project, repository, pull_request_number)
        show_diff(url)
