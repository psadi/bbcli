#-*- coding: utf-8 -*-

""""
    app.scripts.merge
"""

from time import sleep
from typer import (
    prompt,
    Exit
)
from app.utils import(
    richprint,
    iniparser,
    command,
    api,
    request
)

def merge_pull_request(id: int, delete_source_branch: bool, rebase: bool, yes: bool) -> None:
    delete_condition = False
    rebase_condition = False
    with richprint.live_progress(f"Validating Merge for '{id}' ...") as live:
        username, token, bitbucket_host = iniparser.parse()
        project, repository = command.base_repo()
        if len(request.get_response(
            api.pr_source_branch_delete_check(bitbucket_host, project, repository, id, delete_source_branch),
            username, token
        )[1]) != 0:
            raise
        validation_url = api.validate_merge(bitbucket_host, project, repository, id)
        validation_response = request.get_response(validation_url, username, token)
        if(
            validation_response[1]['canMerge'] == True and
            validation_response[1]['conflicted'] == False and
            validation_response[1]['outcome'] == 'CLEAN'
        ):
            live.update(richprint.console.print("VALIDATED", style="bold white on #00875a"))
            sleep(0.4)
        else:
            live.update(richprint.console.print("FAILED", style="bold white on #de350b"))
            sleep(0.4)
            header = {
                "CONDITION": "bold green",
                "STATUS": "bold white"
            }
            richprint.to_console(header, validation_response[1], True)
            raise Exit(code=1)

    with richprint.live_progress(f"Checking for '{repository}' auto-merge conditions ... ") as live:
        pr_info_url = api.pull_request_info(bitbucket_host, project, repository, id)
        pr_info = request.get_response(pr_info_url, username, token)[1]
        from_branch = pr_info['fromRef']['displayId']
        target_branch = pr_info['toRef']['displayId']
        version = pr_info['version']
        pr_merge_info = api.get_merge_info(bitbucket_host, project, repository, target_branch)
        pr_merge_response = request.get_response(pr_merge_info, username, token)[1]

    if (
        (
            pr_merge_response['status']['id'] == 'AUTO_MERGE_DISABLED' or
            pr_merge_response['status']['id'] == 'NO_PATH'
        ) and
        pr_merge_response['status']['available'] == False
    ):
        richprint.console.print(f"\u1405 '{from_branch}' will merge to '{target_branch}'")
    elif pr_merge_response['status']['id'] == 'PROCEED' and pr_merge_response['status']['available'] == True:
        automerge_branches = []
        for branch in pr_merge_response['path']:
            automerge_branches.append(branch['displayId'])
        richprint.console.print(f"\u1405 '{from_branch}' with merge to '{','.join(automerge_branches).replace(',',' and ')}'")
    else:
        richprint.console.print(pr_merge_response)
        raise Exit(code=1)

    if (
        yes or prompt(f"\u2049\ufe0f Proceed with {'rebase and ' if rebase else ''}merge ? [y/n]").lower() == 'y'
    ):
        if (
            delete_source_branch or
            prompt(f"\u2049\ufe0f Do you want to delete source '{from_branch}' branch ? [y/n]").lower() == 'y'
        ):
            delete_condition = True
        if ( 
            rebase or 
            prompt(f"\u2049\ufe0f Do you want rebase '{from_branch}' branch from '{target_branch}' ? [y/n]").lower() == 'y'
        ):
            rebase_condition = True

        with richprint.live_progress(f"{'Rebasing and' if rebase else ''} Merging '{pr_info['links']['self'][0]['href']}'... ") as live:
            if (rebase_condition):
                pr_rebase_info = api.pr_rebase(bitbucket_host, project, repository, id, version)
                request.post_request(pr_rebase_info[1], username, token, pr_rebase_info[0])

            pr_body = api.pr_merge_body(project, repository, id, from_branch, target_branch)
            pr_merge_url = f"{validation_url}?avatarSize=32&version={version}"
            pr_merge_response = request.post_request(pr_merge_url, username, token, pr_body)
            if pr_merge_response[0] == 200 and pr_merge_response[1]['state'] == 'MERGED':
                live.update(richprint.console.print("MERGED", style="bold white on #00875a"))
            elif pr_merge_response[0] == 409:
                live.update(richprint.console.print("FAILED", style="bold white on #de350b"))
                richprint.console.print(pr_merge_response[1]['errors'][0]['message'])

        if ( delete_condition and pr_merge_response[0] in (200, 201)):
            with richprint.live_progress(f"Deleting Source Ref '{from_branch}'... ") as live:
                pr_cleanup_body = api.pr_cleanup_body(delete_source_branch)
                pr_cleanup_url = api.pr_cleanup(bitbucket_host, project, repository, id)
                request.post_request(pr_cleanup_url, username, token, pr_cleanup_body)
                live.update(richprint.console.print("DONE", style="bold white on #00875a"))