# -*- coding: utf-8 -*-

"""
    bb.pr.merge - merges a pull request given a id.
    validates automerge conditions & prompts for optional
    rebase and source branch deletion
"""

from rich import print_json
from typer import confirm

from bb.utils import cmnd, request, richprint
from bb.utils.api import bitbucket_api

BOLD_RED = "bold red"


def pr_source_branch_delete_check(
    project: str,
    repository: str,
    _id: str,
    delete_source_branch: bool,
) -> None:
    """
    checks is the source branch is ok to be deleted if requested
    """
    if (
        len(
            request.get(
                bitbucket_api.pr_source_branch_delete_check(
                    project, repository, _id, delete_source_branch
                ),
            )[1]
        )
        != 0
    ):
        raise ValueError("Source branch deletion validation failed")


def validate_pr_source_branch_delete_check(
    project: str, repository: str, _id: str
) -> None:
    """
    validates the pull request source branch and check for conflitcts or vetos
    """
    with richprint.live_progress(f"Validating Merge for '{_id}' ... ") as live:
        validation_response = request.get(
            bitbucket_api.validate_merge(project, repository, _id),
        )
        if (
            validation_response[1]["canMerge"] is True
            and validation_response[1]["conflicted"] is False
            and validation_response[1]["outcome"] == "CLEAN"
        ):
            live.update(richprint.console.print("OK", style="green"))
        else:
            live.update(richprint.console.print("FAILED", style="red"))
            print_json(data=validation_response[1])
            raise ValueError("Merge validation failed")


def validate_automerge_conditions(project: str, repository: str, _id: str) -> tuple:
    """validate all auto merge conitions before pr merge"""
    with richprint.live_progress(
        f"Checking for '{repository}' auto-merge conditions ... "
    ):
        pr_info = request.get(
            bitbucket_api.pull_request_info(project, repository, _id),
        )[1]
        from_branch, target_branch, version = (
            pr_info["fromRef"]["displayId"],
            pr_info["toRef"]["displayId"],
            pr_info["version"],
        )
        return (
            pr_info,
            request.get(
                bitbucket_api.get_merge_info(project, repository, target_branch),
            )[1],
            from_branch,
            target_branch,
            version,
        )


def show_merge_stats(pr_merge_response, from_branch, target_branch) -> None:
    """display all merge related statistics"""
    if (
        pr_merge_response["status"]["id"] in ["AUTO_MERGE_DISABLED", "NO_PATH"]
        and pr_merge_response["status"]["available"] is False
    ):
        richprint.str_print(
            f"> '{from_branch}' will merge to '{target_branch}'", "bold cyan"
        )
    elif (
        pr_merge_response["status"]["id"] == "PROCEED"
        and pr_merge_response["status"]["available"] is True
    ):
        automerge_branches = [
            branch["displayId"] for branch in pr_merge_response["path"]
        ]

        richprint.str_print(
            f"> '{from_branch}' with merge to '{','.join(automerge_branches).replace(',',' and ')}'",
            "bold cyan",
        )
    else:
        raise ValueError(pr_merge_response)


def rebase_pr(project: str, repository: str, _id: str, version: int):
    """perform rebase in source branch on bitbucket"""
    request.post(
        bitbucket_api.pr_rebase(project, repository, _id, version)[1],
        bitbucket_api.pr_rebase(project, repository, _id, version)[0],
    )


def delete_branch(project, repository, _id, from_branch, target_branch):
    """delete source branch in bitbucket and local git repository"""
    with richprint.live_progress(f"Deleting Source Ref '{from_branch}'... ") as live:
        request.post(
            bitbucket_api.pr_cleanup(project, repository, _id),
            bitbucket_api.pr_cleanup_body(True),
        )
        request.delete(
            bitbucket_api.delete_branch(project, repository, from_branch)[1],
            bitbucket_api.delete_branch(project, repository, from_branch)[0],
        )
        live.update(richprint.console.print("DONE", style="green"))

    cmnd.checkout_and_pull(target_branch)
    cmnd.delete_local_branch(from_branch)


def merge_pr(
    live, project: str, repository: str, _id: str, branches_and_version: tuple
) -> None:
    """perform pull request merge"""
    from_branch, target_branch, version = branches_and_version
    pr_merge_response = request.post(
        f"{bitbucket_api.validate_merge(project, repository, _id)}?avatarSize=32&version={version}",
        bitbucket_api.pr_merge_body(
            project, repository, _id, from_branch, target_branch
        ),
    )
    if pr_merge_response[0] == 200 and pr_merge_response[1]["state"] == "MERGED":
        live.update(richprint.console.print("MERGED", style="green"))
    elif pr_merge_response[0] == 409:
        live.update(richprint.console.print("FAILED", style="red"))
        richprint.console.print(
            pr_merge_response[1]["errors"][0]["message"],
            highlight=True,
            style=BOLD_RED,
        )
    return pr_merge_response[0]


def merge_pull_request(
    _id: str, delete_source_branch: bool, rebase: bool, yes: bool
) -> None:
    """
    It merges a pull request, Validates merge conditions and checks for automerge.
    Merges the pull request upon confirmation and prompts for source branch deletion
    """

    project, repository = cmnd.base_repo()
    pr_source_branch_delete_check(project, repository, _id, delete_source_branch)
    validate_pr_source_branch_delete_check(project, repository, _id)
    (
        pr_info,
        pr_merge_response,
        from_branch,
        target_branch,
        version,
    ) = validate_automerge_conditions(project, repository, _id)

    show_merge_stats(pr_merge_response, from_branch, target_branch)

    rebase_condition = rebase or confirm(
        f"? Do you want rebase '{from_branch}' branch from '{target_branch}'"
    )

    if yes or confirm("? Proceed with merge"):
        delete_condition = delete_source_branch or confirm(
            f"? Do you want to delete source '{from_branch}' branch"
        )

        with richprint.live_progress(
            f"{'Rebasing and ' if rebase_condition else ''}Merging '{pr_info['links']['self'][0]['href']}'... "
        ) as live:
            if rebase_condition:
                rebase_pr(project, repository, _id, version)

            pr_merge_response_code = merge_pr(
                live, project, repository, _id, (from_branch, target_branch, version)
            )

        if delete_condition and pr_merge_response_code in (200, 201):
            delete_branch(project, repository, _id, from_branch, target_branch)
