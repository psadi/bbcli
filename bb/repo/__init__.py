# -*- coding: utf-8 -*-

"""
bb: repo - repository management
"""

from typer import Argument, Option, Typer

from bb.repo.archive import archive_repository
from bb.repo.create import create_repository
from bb.repo.delete import delete_repository
from bb.utils.cmnd import clone_repo
from bb.utils.constants import vars
from bb.utils.helper import error_handler, validate_input
from bb.utils.ini import parse
from bb.utils.richprint import console

_repo = Typer(add_completion=True, no_args_is_help=True)


@_repo.command()
def clone(
    name: str = Argument(..., help="repository name, Format: project/repository"),
) -> None:
    """Clone a BitBucket repository locally"""

    @error_handler
    def _clone(name):
        name = validate_input(
            name, "project/repository to clone", vars.repo_cant_be_none
        )

        console.print(f"Cloning '{name}' into '{name.split('/')[1]}'...")
        clone_repo(name, parse()[2])

    _clone(name)


@_repo.command()
def delete(
    project: str = Option("", help=vars.project_name_of_repo),
    repo: str = Option("", help="repository name to delete"),
) -> None:
    "Delete a Bitbucket repository"

    @error_handler
    def _delete(project, repo):
        project = validate_input(project, vars.project_name, vars.project_cant_be_none)
        repo = validate_input(repo, vars.repoitory_name, vars.repo_cant_be_none)

        delete_repository(project, repo)

    _delete(project, repo)


@_repo.command()
def archive(
    project: str = Option("", help=vars.project_name_of_repo),
    repo: str = Option("", help="repository name to archive"),
) -> None:
    "Archive a Bitbucket repository"

    @error_handler
    def _archive(project, repo):
        project = validate_input(project, vars.project_name, vars.project_cant_be_none)
        repo = validate_input(repo, vars.repoitory_name, vars.repo_cant_be_none)

        archive_repository(project, repo, True)

    _archive(project, repo)


@_repo.command()
def unarchive(
    project: str = Option("", help=vars.project_name_of_repo),
    repo: str = Option("", help="repository name to unarchive"),
) -> None:
    "Unarchive a Bitbucket repository"

    @error_handler
    def _unarchive(project, repo):
        project = validate_input(project, vars.project_name, vars.project_cant_be_none)
        repo = validate_input(repo, vars.repoitory_name, vars.repo_cant_be_none)

        archive_repository(project, repo, False)

    _unarchive(project, repo)


@_repo.command()
def create(
    project: str = Option("", help="project name for the repository"),
    repo: str = Option("", help="repository name to create"),
    forkable: bool = Option(False, help="Make repository forkable"),
    default_branch: str = Option("master", help="Set default branch "),
) -> None:
    """Create a Bitbucket repository"""

    @error_handler
    def _create(project, repo, forkable, default_branch):
        project = validate_input(project, vars.project_name, vars.project_cant_be_none)
        repo = validate_input(repo, vars.repoitory_name, vars.repo_cant_be_none)

        create_repository(project, repo, forkable, default_branch)

    _create(project, repo, forkable, default_branch)
