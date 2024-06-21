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
bb: repo - repository management
"""

from typer import Argument, Option, Typer

from bb.repo.archive import archive_repository
from bb.repo.create import create_repository
from bb.repo.delete import delete_repository
from bb.utils.cmnd import clone_repo
from bb.utils.constants import common_vars
from bb.utils.helper import error_handler, validate_input
from bb.utils.ini import parse
from bb.utils.richprint import console

_repo = Typer(add_completion=True, no_args_is_help=True)


@_repo.command()
def clone(
    name: str = Argument(..., help="repository name, Format: project/repository"),
) -> None:
    """
    Clone a repository from Bitbucket.

    Args:
        name (str): The name of the repository to clone. Format: project/repository.

    Returns:
        None
    """

    @error_handler
    def _clone(name):
        name = validate_input(
            name, "project/repository to clone", common_vars.repo_cant_be_none
        )

        console.print(f"Cloning '{name}' into '{name.split('/')[1]}'...")
        clone_repo(name, parse()[2])

    _clone(name)


@_repo.command()
def delete(
    project: str = Option("", help=common_vars.project_name_of_repo),
    repo: str = Option("", help="repository name to delete"),
) -> None:
    """
    Delete a repository.

    Args:
        project (str): The name of the project.
        repo (str): The name of the repository to delete.

    Returns:
        None
    """

    @error_handler
    def _delete(project, repo):
        project = validate_input(
            project, common_vars.project_name, common_vars.project_cant_be_none
        )
        repo = validate_input(
            repo, common_vars.repository_name, common_vars.repo_cant_be_none
        )

        delete_repository(project, repo)

    _delete(project, repo)


@_repo.command()
def archive(
    project: str = Option("", help=common_vars.project_name_of_repo),
    repo: str = Option("", help="repository name to archive"),
) -> None:
    """
    Archives a repository in the specified project.

    Args:
        project (str): The name of the project where the repository is located.
        repo (str): The name of the repository to archive.

    Returns:
        None
    """

    @error_handler
    def _archive(project, repo):
        project = validate_input(
            project, common_vars.project_name, common_vars.project_cant_be_none
        )
        repo = validate_input(
            repo, common_vars.repository_name, common_vars.repo_cant_be_none
        )

        archive_repository(project, repo, True)

    _archive(project, repo)


@_repo.command()
def unarchive(
    project: str = Option("", help=common_vars.project_name_of_repo),
    repo: str = Option("", help="repository name to unarchive"),
) -> None:
    """
    Unarchives a repository in the specified project.

    Args:
        project (str): The name of the project where the repository is located.
        repo (str): The name of the repository to unarchive.

    Returns:
        None
    """

    @error_handler
    def _unarchive(project, repo):
        project = validate_input(
            project, common_vars.project_name, common_vars.project_cant_be_none
        )
        repo = validate_input(
            repo, common_vars.repository_name, common_vars.repo_cant_be_none
        )

        archive_repository(project, repo, False)

    _unarchive(project, repo)


@_repo.command()
def create(
    project: str = Option("", help="project name for the repository"),
    repo: str = Option("", help="repository name to create"),
    forkable: bool = Option(False, help="Make repository forkable"),
    default_branch: str = Option("master", help="Set default branch "),
) -> None:
    """
    Create a new repository.

    Args:
        project (str): Project name for the repository.
        repo (str): Repository name to create.
        forkable (bool): Flag to make the repository forkable.
        default_branch (str): Default branch for the repository.

    Returns:
        None
    """

    @error_handler
    def _create(project, repo, forkable, default_branch):
        project = validate_input(
            project, common_vars.project_name, common_vars.project_cant_be_none
        )
        repo = validate_input(
            repo, common_vars.repository_name, common_vars.repo_cant_be_none
        )

        create_repository(project, repo, forkable, default_branch)

    _create(project, repo, forkable, default_branch)
