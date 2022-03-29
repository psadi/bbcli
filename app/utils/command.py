# -*- coding: utf-8 -*-
""""
    app.utils.command
"""
import os
import subprocess


def subprocess_run(command: str) -> str:
    """
        a subprocess function that runs native os commands and pipes the stdout
    """
    if os.name == 'nt':
        cmd = subprocess.run(command, stdout=subprocess.PIPE, check=True)
    else:
        cmd = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            shell=True,
            check=True)
    return cmd.stdout.decode().strip()


def is_git_repo() -> bool:
    """Check if the current directory is a git repository"""
    try:
        if os.path.isdir('.git') or subprocess_run('git rev-parse --is-inside-work-tree') == 'true':
            return True
    except subprocess.CalledProcessError:
        return False


def base_repo() -> list:
    """get the local git repository name"""
    cmd = subprocess_run('git remote -v')
    if cmd is not None:
        formatted_cmd = cmd.splitlines()[0].replace('\t', ' ').split(' ')[1].strip()
        project = formatted_cmd.split('/')[-2]
        repository = formatted_cmd.split('/')[-1].split('.')[0]
        return [project, repository]


def title_and_description() -> str:
    """Set the latest commit message as title for pull request"""
    return subprocess_run('git log -1 --pretty=format:%s')


def from_branch() -> str:
    """Get the current working branch"""
    return subprocess_run('git rev-parse --abbrev-ref HEAD')
