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
bb.utils.cmnd - contains funcs to run native os command
can capture relavent details from local repository

"""

import platform
import subprocess
from typing import Dict, Optional

from bb.utils.richprint import console


def subprocess_run(command: str, text: Optional[str] = None) -> str:
    """
    Executes a command using the subprocess module and returns the output as a string.

    Args:
        command (str): The command to be executed.
        text (Optional[str]): The input text to be passed to the command (default: None).

    Returns:
        str: The output of the command as a string.

    Raises:
        RuntimeError: If the command fails with a non-zero return code.

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
        raise RuntimeError(
            f"\nCommand '{command}' failed with return code {err.returncode}\n\n{err.stderr.decode().strip()}"
        ) from err

    return cmnd.stdout.decode().strip()


def is_git_repo() -> bool:
    """
    Check if the current directory is a Git repository.

    Returns:
        bool: True if the current directory is a Git repository, False otherwise.
    """
    return subprocess_run("git rev-parse --is-inside-work-tree") == "true"


def base_repo() -> list:
    """
    Retrieves the base repository information.

    Returns:
        list: A list containing the base repository owner and name.

    Raises:
        ValueError: If no remote information is found.
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
    Extracts the title and description from the latest git commit message.

    Returns:
        list: A list containing the title and description of the commit message.
    """
    commit_message = subprocess_run("git log --format=%B -n 1")
    tmp = commit_message.split("\n")
    return [tmp[0], "\n".join(tmp[2:])]


def from_branch() -> str:
    """
    Get the current branch name.

    Returns:
        str: The name of the current branch.
    """
    return subprocess_run("git rev-parse --abbrev-ref HEAD")


def git_rebase(target_branch: str) -> None:
    """
    Rebase the current branch onto the specified target branch.

    Args:
        target_branch (str): The name of the target branch to rebase onto.

    Raises:
        ValueError: If an error occurs during the rebase process.

    Returns:
        None
    """
    try:
        subprocess_run(f"git pull --rebase origin {target_branch}")
        subprocess_run("git push --force-with-lease")
    except Exception as ex:
        raise ValueError(ex) from ex


def checkout_and_pull(branch_name: str) -> None:
    """
    Checkout the specified branch and pull the latest changes from the remote repository.

    Args:
        branch_name (str): The name of the branch to checkout.

    Raises:
        ValueError: If there are modified files in the current workspace.

    Returns:
        None
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
    Deletes a local branch.

    Args:
        branch_name (str): The name of the branch to be deleted.

    Raises:
        ValueError: If the branch to be deleted is the currently active branch.

    """
    if branch_name == from_branch():
        raise ValueError(f"Cannot delete active branch '{branch_name}'")

    subprocess.check_call(["git", "branch", "-D", branch_name])


def clone_repo(repo: str, bitbucket_host: str) -> None:
    """
    Clone a repository from Bitbucket.

    Args:
        repo (str): The name of the repository to clone.
        bitbucket_host (str): The Bitbucket host URL.

    Returns:
        None
    """
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
        "Linux": (
            "clip.exe"
            if "microsoft" in platform.release().lower()
            else "xclip -selection clipboard"
        ),
        "Darwin": "pbcopy",
    }

    cmd: str = platform_based_cp.get(platform.system(), "n/a")

    if cmd == "n/a":
        raise ValueError("Clipboard copy not supported in platform")

    subprocess_run(cmd, url)


def show_git_diff(from_branch: str, to_branch: str) -> None:
    """
    Show the git diff between two branches.

    Args:
        from_branch (str): The name of the source branch.
        to_branch (str): The name of the target branch.

    Raises:
        ValueError: If the git diff command fails.

    Returns:
        None
    """
    try:
        subprocess.check_call(["git", "diff", to_branch, from_branch])
    except subprocess.CalledProcessError as err:
        raise ValueError("ABORTED") from err
