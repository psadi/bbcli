# -*- coding: utf-8 -*-

"""
bb: repo - repository management
"""

from typer import Argument, Option, Typer

from bb.repo.archive import archive_repository
from bb.repo.create import create_repository
from bb.repo.delete import delete_repository
from bb.utils.cmnd import clone_repo
from bb.utils.ini import parse
from bb.utils.richprint import console, traceback_to_console
from bb.utils.validate import error_tip, state, validate_input

_repo = Typer(add_completion=True, no_args_is_help=True)


@_repo.command()
def clone(
    name: str = Argument(..., help="repository name, Format: project/repository"),
) -> None:
    """Clone a BitBucket repository locally"""
    try:
        name = validate_input(
            name, "project/repository to clone", "repository can't be none"
        )
        console.print(f"Cloning '{name}' into '{name.split('/')[1]}'...")
        clone_repo(name, parse()[2])
    except Exception as err:
        console.print(f"ERROR: {err}", style="bold red")
        if state["verbose"]:
            traceback_to_console()
        else:
            error_tip()


@_repo.command()
def delete(
    project: str = Option("", help="project name of the repository"),
    repo: str = Option("", help="repository name to delete"),
) -> None:
    "Delete a Bitbucket repository"
    try:
        project = validate_input(project, "Project name", "project can't be none")
        repo = validate_input(repo, "Repository Name", "repository can't be none")

        delete_repository(project, repo)

    except Exception as err:
        console.print(f"ERROR: {err}", style="bold red")
        if state["verbose"]:
            traceback_to_console()
        else:
            error_tip()


@_repo.command()
def archive(
    project: str = Option("", help="project name of the repository"),
    repo: str = Option("", help="repository name to archive"),
) -> None:
    "Archive a Bitbucket repository"
    try:
        project = validate_input(project, "Project name", "project can't be none")
        repo = validate_input(repo, "Repository Name", "repository can't be none")

        archive_repository(project, repo, True)

    except Exception as err:
        console.print(f"ERROR: {err}", style="bold red")
        if state["verbose"]:
            traceback_to_console()
        else:
            error_tip()


@_repo.command()
def unarchive(
    project: str = Option("", help="project name of the repository"),
    repo: str = Option("", help="repository name to unarchive"),
) -> None:
    "Unarchive a Bitbucket repository"
    try:
        project = validate_input(project, "Project name", "project can't be none")
        repo = validate_input(repo, "Repository Name", "repository can't be none")

        archive_repository(project, repo, False)

    except Exception as err:
        console.print(f"ERROR: {err}", style="bold red")
        if state["verbose"]:
            traceback_to_console()
        else:
            error_tip()


@_repo.command()
def create(
    project: str = Option("", help="project name for the repository"),
    repo: str = Option("", help="repository name to create"),
    forkable: bool = Option(False, help="Make repository forkable"),
    default_branch: str = Option("master", help="Set default branch "),
) -> None:
    """Create a Bitbucket repository"""
    try:
        project = validate_input(project, "Project name", "project can't be none")
        repo = validate_input(repo, "Repository Name", "repository can't be none")

        create_repository(project, repo, forkable, default_branch)

    except Exception as err:
        console.print(f"ERROR: {err}", style="bold red")
        if state["verbose"]:
            traceback_to_console()
        else:
            error_tip()
