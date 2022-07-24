#-*- coding: utf-8 -*-

# Importing the os and subprocess modules.
import os
import subprocess
from typer import Exit

def subprocess_run(command: str) -> str:
    """
    > This function runs native os commands and pipes the stdout

    :param command: the command to run
    :type command: str
    :return: The stdout of the command is being returned.
    """
    try:
        cmnd = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            shell= os.name == 'posix',
            check=True
        )
        return cmnd.stdout.decode().strip()
    except subprocess.CalledProcessError:
        raise(Exit(code=1))

def is_git_repo() -> bool:
    """
    It checks if the current directory is a git repository
    :return: A boolean value.
    """
    return subprocess_run('git rev-parse --is-inside-work-tree') == 'true'

def base_repo() -> list:
    """
    It gets the local git repository name
    :return: A list of the project and repository names.
    """
    cmnd = subprocess_run('git remote -v')
    if cmnd is not None:
        formatted_cmnd = cmnd.splitlines()[0].replace('\t', ' ').split(' ')[1].strip()
        project = formatted_cmnd.split('/')[-2]
        repository = formatted_cmnd.split('/')[-1].split('.')[0]
        return [project, repository]

def title_and_description() -> str:
    """
    `Set the latest commit message as title for pull request`
    :return: The latest commit message
    """
    return subprocess_run('git log -1 --pretty=format:%s')

def from_branch() -> str:
    """
    `from_branch` returns the current working branch
    :return: The current working branch
    """
    return subprocess_run('git rev-parse --abbrev-ref HEAD')
