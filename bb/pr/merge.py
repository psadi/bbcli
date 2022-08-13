#-*- coding: utf-8 -*-

# Importing the necessary modules for the script to run.
from typer import (
    prompt,
    Exit
)
from bb.utils import(
    cmnd,
    richprint,
    iniparser,
    api,
    request
)
from bb.pr.review import review_pull_request
from rich import print_json

def requires_approval(target: int, action: str):
    """
    `review_pull_request` is called with `target` and `action` as arguments

    :param target: The ID of the pull request you want to review
    :type target: int
    :param action: The action that was performed on the pull request
    :type action: str
    """
    review_pull_request(target, action)

def merge_pull_request(id: int, delete_source_branch: bool, rebase: bool, yes: bool) -> None:
    """
    It merges a pull request, Validates merge conditions and checks for automerge.
    Merges the pull request upon confirmation and prompts for source branch deletion

    :param id: The ID of the pull request you want to merge
    :type id: int
    :param delete_source_branch: If true, the source branch will be deleted after the merge
    :type delete_source_branch: bool
    :param rebase: If True, the source branch will be rebased onto the target branch before merging
    :type rebase: bool
    :param yes: If you want to skip the confirmation prompt, you can pass this parameter
    :type yes: bool
    """
def merge_pull_request(id: int, delete_source_branch: bool, rebase: bool, yes: bool) -> None:
    delete_condition = False
    rebase_condition = False
    with richprint.live_progress(f"Validating Merge for '{id}' ... ") as live:
        username, token, bitbucket_host = iniparser.parse()
        project, repository = cmnd.base_repo()
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
            live.update(richprint.console.print("OK", style="green"))
        else:
            live.update(richprint.console.print("FAILED", style="red"))
            print_json(data=validation_response[1])
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
        richprint.str_print(f"> '{from_branch}' will merge to '{target_branch}'", "bold cyan")
    elif pr_merge_response['status']['id'] == 'PROCEED' and pr_merge_response['status']['available'] == True:
        automerge_branches = []
        for branch in pr_merge_response['path']:
            automerge_branches.append(branch['displayId'])
        richprint.str_print(f"> '{from_branch}' with merge to '{','.join(automerge_branches).replace(',',' and ')}'", "bold cyan")
    else:
        richprint.str_print(pr_merge_response, "bold red")
        raise Exit(code=1)

    if (rebase or
        prompt(f"? Do you want rebase '{from_branch}' branch from '{target_branch}' [y/n]").lower() == 'y'
    ):
        rebase_condition = True

    if (yes or
        prompt(f"? Proceed with {'rebase and ' if rebase_condition else ''}merge [y/n]").lower() == 'y'
    ):
        if (delete_source_branch or
            prompt(f"? Do you want to delete source '{from_branch}' branch [y/n]").lower() == 'y'
        ):
            delete_condition = True

        with richprint.live_progress(f"{'Rebasing and' if rebase_condition else ''} Merging '{pr_info['links']['self'][0]['href']}'... ") as live:
            if (rebase_condition):
                pr_rebase_info = api.pr_rebase(bitbucket_host, project, repository, id, version)
                request.post_request(pr_rebase_info[1], username, token, pr_rebase_info[0])

            pr_body = api.pr_merge_body(project, repository, id, from_branch, target_branch)
            pr_merge_url = f"{validation_url}?avatarSize=32&version={version}"
            pr_merge_response = request.post_request(pr_merge_url, username, token, pr_body)
            if pr_merge_response[0] == 200 and pr_merge_response[1]['state'] == 'MERGED':
                live.update(richprint.console.print("MERGED", style="green"))
            elif pr_merge_response[0] == 409:
                live.update(richprint.console.print("FAILED", style="red"))
                richprint.console.print(pr_merge_response[1]['errors'][0]['message'], highlight=True, style='bold red')

        if ( delete_condition and pr_merge_response[0] in (200, 201)):
            with richprint.live_progress(f"Deleting Source Ref '{from_branch}'... ") as live:
                pr_cleanup_body = api.pr_cleanup_body(delete_source_branch)
                pr_cleanup_url = api.pr_cleanup(bitbucket_host, project, repository, id)
                request.post_request(pr_cleanup_url, username, token, pr_cleanup_body)
                live.update(richprint.console.print("DONE", style="green"))