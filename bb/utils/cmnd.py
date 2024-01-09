# -*- coding: utf-8 -*-
"""
    bb.utils.cmnd - contains funcs to run native os command
    can capture relavent details from local repository

"""

import platform
import subprocess
from typing import Dict, Optional

from bb.utils.richprint import console, str_print

dim_white: str = "dim white"


def subprocess_run(command: str, text: Optional[str] = None) -> str:
    """
    Runs native os commands and pipes the stdout
    """
    if text is not None:
        text = text.encode("utf-8")  # type: ignore

    try:
        cmnd = subprocess.run(
            command.split(" "),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            input=text,
            check=True,
        )

    except subprocess.CalledProcessError as err:
        console.print("ERROR", style="bold red")
        console.print(err)
        raise RuntimeError(
            f"Command {command} failed with return code {err.returncode}: {err.stderr.decode().strip()}"
        ) from err

    return cmnd.stdout.decode().strip()


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
        raise ValueError("no remote information is found")

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
        raise ValueError(ex) from ex


def checkout_and_pull(branch_name: str) -> None:
    """
    checkouts to a target branch and pulls the changes from remote
    """
    modified_files = len(
        (list(filter(None, (subprocess_run("git ls-files -m")).split("\n"))))
    )
    if modified_files > 0:
        raise ValueError(
            f"Cannot checkout to '{branch_name}' branch.\nCurrent workspace has {modified_files} modified files"
        )

    subprocess.check_call(["git", "checkout", branch_name])

    subprocess.check_call(["git", "pull", "--no-edit"])


def delete_local_branch(branch_name: str):
    """
    given a branch name, deletes its local reference if there are no files in staging area
    """
    if branch_name == from_branch():
        raise ValueError(f"Cannot delete active branch '{branch_name}'")

    subprocess.check_call(["git", "branch", "-D", branch_name])


def clone_repo(repo: str, bitbucket_host: str) -> None:
    "clones a given repostory to the local workspace"
    subprocess.check_call(
        ["git", "clone", f"{bitbucket_host}/scm/{repo}.git", repo.split("/")[1]]
    )


def cp_to_clipboard(url: str) -> None:
    """
    Copy the specified text to the system clipboard.

    Args:
        text: The text to be copied to the clipboard.

    Raises:
        Exit: If the current operating system is not Windows, Linux, or macOS.
    """
    platform_based_cp: Dict[str, str] = {
        "Windows": "clip.exe",
        "Linux": "clip.exe"
        if "microsoft" in platform.release().lower()
        else "xclip -selection clipboard",
        "Darwin": "pbcopy",
    }

    cmd: str = platform_based_cp.get(platform.system(), "n/a")

    if cmd == "n/a":
        raise ValueError("Clipboard copy not supported in platform")

    subprocess_run(cmd, url)


def show_git_diff(from_branch: str, to_branch: str) -> None:
    """
    shows the diff between two branches
    """
    try:
        subprocess.check_call(["git", "diff", to_branch, from_branch])
    except subprocess.CalledProcessError as err:
        raise ValueError("ABORTED") from err
