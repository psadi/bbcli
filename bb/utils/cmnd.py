# -*- coding: utf-8 -*-
# pylint: disable=C0301
"""
    bb.utils.cmnd - contains funcs to run native os command
    can capture relavent details from local repository

"""

import os
import subprocess
from time import sleep
from typer import Exit
from bb.utils.richprint import console, str_print

dim_white: str = "dim white"


def subprocess_run(command: str) -> str:
    """
    runs native os commands and pipes the stdout
    """
    try:
        cmnd = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=os.name == "posix",
            check=True,
        )

        return cmnd.stdout.decode().strip()

    except subprocess.CalledProcessError as err:
        sleep(0.4)
        console.print("ERROR", style="bold red")
        console.print(err)
        raise ValueError(err) from err


def is_git_repo() -> bool:
    """
    It checks if the current directory is a git repository
    """
    return subprocess_run("git rev-parse --is-inside-work-tree") == "true"


def base_repo() -> list:
    """
    It gets the local git repository name
    """

    cmnd = subprocess_run("git remote -v")

    if cmnd is None:
        str_print("no remote information is found", dim_white)
        raise Exit(code=1)

    formatted_cmnd = cmnd.splitlines()[0].replace("\t", " ").split(" ")[1].strip()

    return [
        formatted_cmnd.split("/")[-2],
        formatted_cmnd.split("/")[-1].split(".")[0],
    ]


def title_and_description() -> list:
    """
    `Set the latest commit message as title for pull request`
    """
    commit_message = subprocess_run("git log --format=%B -n 1")
    tmp = commit_message.split("\n")
    return [tmp[0], "\n".join(tmp[2:])]


def from_branch() -> str:
    """
    `from_branch` returns the current working branch
    """
    return subprocess_run("git rev-parse --abbrev-ref HEAD")


def git_rebase(target_branch: str) -> None:
    """
    rebase source branch with target
    """
    try:
        subprocess_run(f"git pull --rebase origin {target_branch}")
        subprocess_run("git push --force-with-lease")
    except Exception as ex:
        error_code = int(str(ex).rsplit(" ", maxsplit=1)[-1].replace(".", ""))
        error_message = {
            128: "cannot pull with rebase, you have unstaged/uncommitted changes\nplease commit or stash them.",
            1: "Try running `git diff --diff-filter=U --relative` to know more on local conflicts",
        }
        if error_code in error_message:
            str_print(
                error_message[error_code],
                dim_white,
            )
        raise Exit(code=1) from ex


def checkout_and_pull(branch_name: str) -> None:
    """
    checkouts to a target branch and pulls the changes from remote
    """
    modified_files = len(
        (list(filter(None, (subprocess_run("git ls-files -m")).split("\n"))))
    )
    if modified_files > 0:
        str_print(
            f"Cannot checkout to '{branch_name}' branch.\nCurrent workspace has {modified_files} modified files",
            dim_white,
        )
        raise Exit(code=1)
    subprocess_run(f"git checkout {branch_name} && git pull --no-edit")


def delete_local_branch(branch_name: str):
    """
    given a branch name, deletes its local reference if there are no files in staging area
    """
    if branch_name == from_branch():
        str_print(
            f"Cannot delete active branch '{branch_name}'",
            dim_white,
        )
        raise Exit(code=1)

    subprocess_run(f"git branch -D {branch_name}")


def clone_repo(repo: str, bitbucket_host: str) -> None:
    "clones a given repostory to the local workspace"
    os.system(f"git clone {bitbucket_host}/scm/{repo}.git")
