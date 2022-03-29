# -*- coding: utf-8 -*-
"""
BBCLI: An awesome cli utility that can manage pull requests.
"""

# Standard Imports
from enum import Enum
from typing import List, Optional

# Script Imports
import typer
from app.utils import command
from app.utils.docs import wrapper
from app.scripts.test import validate
from app.scripts.create import create_pull_request
from app.scripts.delete import delete_pull_request
from app.scripts.view import view_pull_request
from app.utils.richprint import traceback_to_console

app = typer.Typer()


@app.callback()
def callback():
    """
    BitBucket CLI: A CLI Utility that can manage Pull-Requests. \U0001f600 \n
    """


@app.command()
def create(
        target: str = typer.Option("", help="target branch name"),
        yes: bool = typer.Option(False, help="skip yes/no prompt"),
        diff: bool = typer.Option(False, help="show diff after raising pull request")
):
    """Create a pull request"""
    try:
        if command.is_git_repo() is True:
            if not target:
                target = typer.prompt("Target Branch")
            create_pull_request(target, yes, diff)
        else:
            typer.echo("\u274C Not a git repository")
            raise typer.Exit(code=1)
    except Exception:
        traceback_to_console(Exception)


@app.command()
def delete(
        target: Optional[List[int]] = typer.Option(None, help="pull request number(s) to delete"),
        yes: bool = typer.Option(False, help="skip yes/no prompt"),
        diff: bool = typer.Option(False, help="show diff before deleting pull request")
):
    """Delete a pull request(s) by id"""
    try:
        if command.is_git_repo() is True:
            if not target:
                target = typer.prompt("Pull request number(s)")
            delete_pull_request(target, yes, diff)
        else:
            typer.echo("\u274C Not a git repository")
            raise typer.Exit(code=1)
    except Exception:
        traceback_to_console(Exception)


class Role(str, Enum):
    """roles choice enum"""
    author = "author"
    reviewer = "reviewer"
    # participant = "participant"


@app.command()
def view(
        role: Role = Role.author.value,
        all: bool = typer.Option(False, help="show all pull request(s) based on selected role")
):
    # TO-DO: patterns: str   = typer.Option("repository patterrns, absolute (or) regex")
    """Show pull requests authored & reviewing"""
    try:
        if command.is_git_repo() is True:
            view_pull_request(role.value, all)
        else:
            typer.echo("\u274C Not a git repository")
            typer.Exit(code=1)
    except Exception:
        traceback_to_console(Exception)


@app.command()
def test():
    """Validate bitbucket connection credentials"""
    try:
        validate()
    except Exception:
        traceback_to_console(Exception)


class Arg(str, Enum):
    """docs enum for choices"""
    setup = "setup"
    test = "test"
    create = "create"
    delete = "delete"
    view = "view"
    default = "default"


@app.command()
def docs(option: Arg = Arg.default.value):
    """Show documentation for each available command"""
    try:
        wrapper(option.value)
    except Exception:
        traceback_to_console(Exception)
