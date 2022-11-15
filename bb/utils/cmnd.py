# -*- coding: utf-8 -*-

# Importing the os and subprocess modules.
import os
import subprocess
from time import sleep
from typer import Exit
from bb.utils.richprint import console, str_print


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
        raise ValueError(err)


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
    if cmnd is not None:
        formatted_cmnd = cmnd.splitlines()[0].replace("\t", " ").split(" ")[1].strip()
        project = formatted_cmnd.split("/")[-2]
        repository = formatted_cmnd.split("/")[-1].split(".")[0]
        return [project, repository]


def title_and_description() -> str:
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
        subprocess_run(f"git push --force-with-lease")
    except Exception as ex:
        error_code = int(str(ex).split(" ")[-1].replace(".", ""))
        error_message = {
            128: "cannot pull with rebase, you have unstaged/uncommitted changes\nplease commit or stash them.",
            1: "Try running `git diff --diff-filter=U --relative` to know more on local conflicts",
        }
        if error_code in error_message.keys():
            str_print(
                error_message[error_code],
                "dim white",
            )
        raise Exit(code=1)


def checkout_and_pull(branch_name: str) -> None:
    modified_files = len(
        (list(filter(None, (subprocess_run("git ls-files -m")).split("\n"))))
    )
    if modified_files > 0:
        str_print(
            f"Cannot checkout to '{branch_name}' branch.\nCurrent workspace has {modified_files} modified files",
            "dim white",
        )
        raise Exit(code=1)
    subprocess_run(f"git checkout {branch_name} && git pull --no-edit")


def delete_local_branch(branch_name: str):
    if branch_name == from_branch():
        str_print(
            f"Cannot delete active branch '{branch_name}'",
            "dim white",
        )
        raise Exit(code=1)

    subprocess_run(f"git branch -D {branch_name}")
