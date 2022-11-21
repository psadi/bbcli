# -*- coding: utf-8 -*-
# pylint: disable=C0301,R0912,R0914

"""
    bb.pr.merge - merges a pull request given a id.
    validates automerge conditions & prompts for optional
    rebase and source branch deletion
"""

from typer import prompt, Exit
from rich import print_json
from bb.utils import cmnd, richprint, iniparser, api, request


def merge_pull_request(
    _id: int, delete_source_branch: bool, rebase: bool, yes: bool
) -> None:
    """
    It merges a pull request, Validates merge conditions and checks for automerge.
    Merges the pull request upon confirmation and prompts for source branch deletion
    """

    username, token, bitbucket_host = iniparser.parse()
    project, repository = cmnd.base_repo()

    with richprint.live_progress(f"Validating Merge for '{_id}' ... ") as live:
        if (
            len(
                request.get(
                    api.pr_source_branch_delete_check(
                        bitbucket_host, project, repository, _id, delete_source_branch
                    ),
                    username,
                    token,
                )[1]
            )
            != 0
        ):
            raise Exit(code=1)
        validation_response = request.get(
            api.validate_merge(bitbucket_host, project, repository, _id),
            username,
            token,
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
            raise Exit(code=1)

    with richprint.live_progress(
        f"Checking for '{repository}' auto-merge conditions ... "
    ) as live:
        pr_info = request.get(
            api.pull_request_info(bitbucket_host, project, repository, _id),
            username,
            token,
        )[1]
        from_branch, target_branch, version = (
            pr_info["fromRef"]["displayId"],
            pr_info["toRef"]["displayId"],
            pr_info["version"],
        )
        pr_merge_response = request.get(
            api.get_merge_info(bitbucket_host, project, repository, target_branch),
            username,
            token,
        )[1]

    if (
        pr_merge_response["status"]["id"] == "AUTO_MERGE_DISABLED"
        or pr_merge_response["status"]["id"] == "NO_PATH"
    ) and pr_merge_response["status"]["available"] is False:
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
        richprint.str_print(pr_merge_response, "bold red")
        raise Exit(code=1)

    rebase_condition = bool(
        rebase
        or prompt(
            f"? Do you want rebase '{from_branch}' branch from '{target_branch}' [y/n]"
        ).lower()
        == "y"
    )

    if (
        yes
        or prompt(
            f"? Proceed with {'rebase and ' if rebase_condition else ''}merge [y/n]"
        ).lower()
        == "y"
    ):
        delete_condition = bool(
            delete_source_branch
            or prompt(
                f"? Do you want to delete source '{from_branch}' branch [y/n]"
            ).lower()
            == "y"
        )

        with richprint.live_progress(
            f"{'Rebasing and ' if rebase_condition else ''}Merging '{pr_info['links']['self'][0]['href']}'... "
        ) as live:
            if rebase_condition:
                request.post(
                    api.pr_rebase(bitbucket_host, project, repository, _id, version)[1],
                    username,
                    token,
                    api.pr_rebase(bitbucket_host, project, repository, _id, version)[0],
                )

            pr_merge_response = request.post(
                f"{api.validate_merge(bitbucket_host, project, repository, _id)}?avatarSize=32&version={version}",
                username,
                token,
                api.pr_merge_body(project, repository, _id, from_branch, target_branch),
            )
            if (
                pr_merge_response[0] == 200
                and pr_merge_response[1]["state"] == "MERGED"
            ):
                live.update(richprint.console.print("MERGED", style="green"))
            elif pr_merge_response[0] == 409:
                live.update(richprint.console.print("FAILED", style="red"))
                richprint.console.print(
                    pr_merge_response[1]["errors"][0]["message"],
                    highlight=True,
                    style="bold red",
                )

        if delete_condition and pr_merge_response[0] in (200, 201):
            with richprint.live_progress(
                f"Deleting Source Ref '{from_branch}'... "
            ) as live:
                request.post(
                    api.pr_cleanup(bitbucket_host, project, repository, _id),
                    username,
                    token,
                    api.pr_cleanup_body(delete_source_branch),
                )
                request.delete(
                    api.delete_branch(bitbucket_host, project, repository, from_branch)[
                        1
                    ],
                    username,
                    token,
                    api.delete_branch(bitbucket_host, project, repository, from_branch)[
                        0
                    ],
                )
                live.update(richprint.console.print("DONE", style="green"))

            cmnd.checkout_and_pull(target_branch)
            cmnd.delete_local_branch(from_branch)
