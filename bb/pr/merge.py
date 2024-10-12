# -*- coding: utf-8 -*-

############################################################################
# Bitbucket CLI (bb): Work seamlessly with Bitbucket from the command line
#
# Copyright (C) 2022  P S, Adithya (psadi) (ps.adithya@icloud.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################

"""
bb.pr.merge - merges a pull request given a id.
validates automerge conditions & prompts for optional
rebase and source branch deletion
"""

from rich import print_json
from typer import confirm

from bb.utils import cmnd, request, richprint
from bb.utils.api import bitbucket_api
from bb.utils.constants import common_vars


def pr_source_branch_delete_check(
    project: str,
    repository: str,
    _id: str,
    delete_source_branch: bool,
) -> None:
    """
    Check if the source branch of a pull request can be deleted.

    Args:
        project (str): The project name.
        repository (str): The repository name.
        _id (str): The ID of the pull request.
        delete_source_branch (bool): Flag indicating whether to delete the source branch.

    Raises:
        ValueError: If the source branch deletion validation fails.
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
    Validates the merge for a pull request by checking if the source branch can be deleted.

    Args:
        project (str): The project name.
        repository (str): The repository name.
        _id (str): The ID of the pull request.

    Raises:
        ValueError: If the merge validation fails.

    Returns:
        None
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
    """
    Validates the auto-merge conditions for a pull request.

    Args:
        project (str): The project name.
        repository (str): The repository name.
        _id (str): The pull request ID.

    Returns:
        tuple: A tuple containing the pull request information, merge information,
        from branch, target branch, and version.

    """
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
    """
    Display merge statistics based on the given PR merge response, from branch, and target branch.

    Args:
        pr_merge_response (dict): The PR merge response containing merge status information.
        from_branch (str): The name of the branch from which the merge is performed.
        target_branch (str): The name of the target branch to which the merge is performed.

    Raises:
        ValueError: If the merge response status is not recognized.

    Returns:
        None
    """
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
            f"> '{from_branch}' with merge to '{','.join(automerge_branches).replace(',', ' and ')}'",
            "bold cyan",
        )
    else:
        raise ValueError(pr_merge_response)


def rebase_pr(project: str, repository: str, _id: str, version: int):
    """
    Rebase a pull request.

    Args:
        project (str): The project name.
        repository (str): The repository name.
        _id (str): The ID of the pull request.
        version (int): The version of the pull request.

    Returns:
        None
    """
    request.post(
        bitbucket_api.pr_rebase(project, repository, _id, version)[1],
        bitbucket_api.pr_rebase(project, repository, _id, version)[0],
    )


def delete_branch(project, repository, _id, from_branch, target_branch):
    """
    Deletes the source branch and performs cleanup after merging a pull request.

    Args:
        project (str): The project name.
        repository (str): The repository name.
        _id (str): The ID of the pull request.
        from_branch (str): The name of the source branch to be deleted.
        target_branch (str): The name of the target branch.

    Returns:
        None
    """
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
    """
    Merges a pull request with the specified project, repository, and ID.

    Args:
        live: The live object.
        project (str): The project name.
        repository (str): The repository name.
        _id (str): The ID of the pull request.
        branches_and_version (tuple): A tuple containing the from_branch, target_branch, and version.

    Returns:
        int: The status code of the merge operation.
    """
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
            style=common_vars.bold_red,
        )
    return pr_merge_response[0]


def merge_pull_request(
    _id: str, delete_source_branch: bool, rebase: bool, yes: bool
) -> None:
    """
    Merges a pull request with the given ID.

    Args:
        _id (str): The ID of the pull request to merge.
        delete_source_branch (bool): Whether to delete the source branch after merging.
        rebase (bool): Whether to rebase the source branch onto the target branch before merging.
        yes (bool): Whether to proceed with the merge without confirmation.

    Returns:
        None
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
