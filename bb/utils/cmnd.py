# -*- coding: utf-8 -*-

# Importing the os and subprocess modules.
import os
import subprocess


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
    return subprocess_run("git log -1 --pretty=format:%s")


def from_branch() -> str:
    """
    `from_branch` returns the current working branch
    """
    return subprocess_run("git rev-parse --abbrev-ref HEAD")


def git_rebase(target_branch: str) -> None:
    """
    rebase source branch with target
    """
    subprocess_run(f"git pull --rebase origin {target_branch}")
    subprocess_run(f"git push --force-with-lease")
